#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/21 15:38
# -----------------------------------------
import unittest

from testfarm.test_program.app.honor.student.homework_rebuild.object_pages.homework_public_page import HomeWorkPublicElePage
from testfarm.test_program.app.honor.student.library.object_pages.game_page import LibraryGamePage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.web.object_pages.assign_homework import AssignHomeworkPage
from testfarm.test_program.app.honor.student.web.object_pages.driver import Driver
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststep


class FlashCard(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login_page = LoginPage()
        cls.library = LibraryGamePage()
        cls.hw_public = HomeWorkPublicElePage()
        cls.login_page.app_status()  # 判断APP当前状态


    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_check_speak_game_is_unit(self):
        if self.home.wait_check_home_page():
            web_driver = Driver()
            web_driver.set_driver()
            AssignHomeworkPage().assign_homework_operate()
            web_driver.quit_web()
            self.home.screen_swipe_up(0.5, 0.3, 0.8, 1000)
            for index in [1, 3]:
                if self.home.wait_check_home_page():
                    self.home.click_hk_tab(index)
                    if index == 1:
                        print('检验口语练习作业\n')
                    else:
                        print('检验普通练习作业\n')
                    if self.library.wait_check_homework_list_page():
                        self.find_test_homework()
                        self.home.click_back_up_button()
                        if self.library.wait_check_bank_list_page():
                            self.home.click_back_up_button()
                            if self.library.wait_check_homework_list_page():
                                self.home.click_back_up_button()

    @teststep
    def find_test_homework(self):
        hw_name_list = []
        flag = False
        while True:
            homework_name = self.library.homework_list()
            for hw in homework_name:
                if hw.text in hw_name_list:
                    continue
                else:
                    hw_name_list.append(hw.text)
                    if hw.text == 'test':
                        hw.click()
                        if self.library.wait_check_bank_list_page():
                            self.library.bank_name_list()[0].click()
                        flag = True
                        break
            if flag:
                break

            if self.hw_public.wait_check_end_tip_page():
                break
            self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)

        if 'test' not in hw_name_list:
            print('★★★ 在作业列表中未发现已布置的作业')
        else:
            print('习题布置成功')



