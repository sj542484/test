# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/21 10:38
# -------------------------------------------
# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 15:57
# -------------------------------------------
import unittest

from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.listen_everyday.object_page.history_page import HistoryPage
from testfarm.test_program.app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from testfarm.test_program.app.honor.student.listen_everyday.object_page.rank_page import RankPage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.conf.decorator import setup, teardown, teststeps
import time

class SelectLevel(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.listen = ListenHomePage()
        cls.rank = RankPage()
        cls.login = LoginPage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @teststeps
    def test_rank(self):
        if self.rank.home.wait_check_home_page():  # 页面检查点
            time.sleep(3)
            name = UserCenterPage().get_user_info()[3]
            if self.rank.home.wait_check_home_page():
                print('进入主界面')
                self.rank.home.click_hk_tab(4)   # 点击 每日一听
                if self.listen.wait_check_listen_everyday_home_page():
                    excise_time = self.listen.excise_time()
                    print('已练听力：', excise_time.text, '\n')
                    self.listen.rank_button().click()
                    if self.rank.wait_check_rank_page():
                        self.rank.rank_ele_operate(name)

