# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/14 14:24
# -------------------------------------------
import unittest
import time
from testfarm.test_program.app.honor.student.listen_everyday.object_page.level_page import LevelPage
from testfarm.test_program.app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.conf.decorator import setup, teardown, teststeps


class SelectLevel(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.listen = ListenHomePage()
        cls.level = LevelPage()
        cls.login = LoginPage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @teststeps
    def test_select_level(self):
        if self.level.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            time.sleep(5)
            self.level.home.click_hk_tab(4)   # 点击 背单词
            if self.listen.wait_check_listen_everyday_home_page():
                self.listen.level_button().click()
                if self.level.wait_check_listening_level_page():
                    self.level.level_page_ele_operate()

            if self.listen.wait_check_listen_everyday_home_page():
                self.level.click_back_up_button()




