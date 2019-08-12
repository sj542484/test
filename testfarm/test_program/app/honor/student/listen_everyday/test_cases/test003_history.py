# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 15:57
# -------------------------------------------
import unittest

from app.honor.student.listen_everyday.object_page.history_page import HistoryPage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.decorator import setup, teardown, teststeps


class SelectLevel(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.listen = ListenHomePage()
        cls.history = HistoryPage()
        cls.login = LoginPage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @teststeps
    def test_history_log(self):
        if self.history.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            self.history.home.click_hk_tab(4)   # 点击 每日一听
            if self.listen.wait_check_listen_everyday_home_page():
                excise_time = self.listen.excise_time()
                print('已练听力：', excise_time.text)
                self.listen.history_button().click()
                if self.history.wait_check_history_page():
                    print('进入历史记录')
                    self.history.history_page_operate()
            if self.listen.wait_check_listen_everyday_home_page():
                self.listen.click_back_up_button()

