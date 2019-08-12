# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 10:57
# -------------------------------------------
import unittest

from app.honor.student.library.object_pages.library_page import LibraryGamePage
from app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from app.honor.student.listen_everyday.object_page.level_page import LevelPage
from app.honor.student.listen_everyday.object_page.listen_data_handle import ListenDataHandle
from app.honor.student.listen_everyday.object_page.listen_game_page import ListenGamePage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.decorator import setup, teardown, teststeps


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

    @teststeps
    def test_select_level(self):
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
                    if self.level.start_button('2A').text == '开始':
                        self.level.start_button('2A').click()
                    self.game.home.click_back_up_button()
                    for i in range(4):
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


                        if i == 3:
                            if self.listen.wait_today_limit_img_page():
                                print('今天你已练完3道听力，保持适度才能事半公倍哦！', '\n')
                                self.listen.commit_button().click()

                            else:
                                print('★★★ Error-- 未发现题数限制提示页面！')



