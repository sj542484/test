# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 10:57
# -------------------------------------------
import re
import unittest

from ddt import ddt, data

from app.honor.student.library.object_pages.library_page import LibraryGamePage
from app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from app.honor.student.listen_everyday.object_page.level_page import LevelPage
from app.honor.student.listen_everyday.object_page.listen_data_handle import ListenDataHandle
from app.honor.student.listen_everyday.object_page.listen_game_page import ListenGamePage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.decorator import setup, teardown, teststeps


@ddt
class SelectLevel(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.listen = ListenHomePage()
        cls.game = ListenGamePage()
        cls.login = LoginPage()
        cls.level = LevelPage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass


    @data('2A')
    @teststeps
    def test_listen_game(self, level_name):
        if self.game.home.wait_check_home_page():  # 页面检查点
            user_data = UserCenterPage().get_user_info()
            stu_id = user_data[0]
            ListenDataHandle().delete_student_all_listening_records(stu_id)
        if self.game.home.wait_check_home_page():  # 页面检查点
            print('进入主界面', '\n')
            self.game.home.click_hk_tab(4)   # 点击每日一听
            if self.listen.wait_check_listen_everyday_home_page():
                self.listen.level_button().click()

                if self.level.wait_check_listening_level_page():
                    while not self.level.wait_check_level_page(level_name):
                        HomePage().screen_swipe_up(0.5, 0.8, 0.4, 1000)

                    if self.level.start_button(level_name).text == '开始':
                        self.level.start_button(level_name).click()
                    self.game.home.click_back_up_button()
                    level_num = int(re.findall(r'\d+', level_name)[0])
                    exercise_count = 3 if level_num > 4 else 5
                    for i in range(exercise_count + 1):
                        if self.listen.wait_check_listen_everyday_home_page():
                            self.listen.start_button().click()

                        if self.game.wait_check_gaming_page():
                            self.game.play_listen_game_process()

                        elif self.listen.wait_check_degrade_page():
                            print('是否感觉题太难了，需要切换到稍简单级别的练习吗？', '\n')
                            self.game.home.commit()

                        elif self.listen.wait_check_certificate_page():
                            print('该等级已学习完毕（没有题目）')
                            LibraryGamePage().share_page_operate()
                            if self.listen.wait_check_certificate_page():
                                self.listen.start_excise_button().click()


                        if i == exercise_count:
                            if self.listen.wait_today_limit_img_page():
                                print('今天你已练完{}道听力，保持适度才能事半公倍哦！'.format(exercise_count), '\n')
                                self.listen.commit_button().click()

                            else:
                                print('★★★ Error-- 未发现题数限制提示页面！')



