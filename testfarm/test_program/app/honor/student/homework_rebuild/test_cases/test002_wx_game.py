#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/8 11:42
# -----------------------------------------
import unittest

from testfarm.test_program.app.honor.student.homework.object_page.wk_game_page import WKGamePage
from testfarm.test_program.app.honor.student.library.object_pages.game_page import LibraryGamePage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase


class FlashCard(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.wk = WKGamePage()
        cls.login_page = LoginPage()
        cls.library = LibraryGamePage()
        cls.login_page.app_status()  # 判断APP当前状态

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_wk_game(self):
        """测试微课"""
        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_hk_tab(2)  # 进入习题
            bank_info = self.library.enter_into_game('微课测试1', '微课')
            bank_name = bank_info[1][0].text
            bank_info[0][0] .click()
            self.wk.wk_game_operate()
            if self.library.wait_check_game_list_page('微课测试1'):
                self.library.click_back_up_button()
                if self.library.wait_check_bank_list_page():
                    if self.library.bank_progress_by_name(bank_name) != '100%':
                        print('★★★ 微课退出后，题目进度不为100%')

                    self.library.click_back_up_button()
                    if self.library.wait_check_homework_list_page():
                        self.library.click_back_up_button()
