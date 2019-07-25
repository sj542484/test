# coding=utf-8
import unittest

from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.word_book.object_page.clear_user_data import CleanDataPage
from testfarm.test_program.app.honor.student.word_book.object_page.data_action import WordBookDataHandle
from testfarm.test_program.app.honor.student.word_book.object_page.word_book import WordBook
from testfarm.test_program.app.honor.student.word_book.object_page.word_result_page import ResultPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.toast_find import Toast


class Word (unittest.TestCase):
    """单词本"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.word = WordBook()
        cls.login = LoginPage()
        cls.result = ResultPage()
        cls.homework = Homework()
        cls.login.app_status()  # 判断APP当前状态
        cls.common = WordBookDataHandle()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_study_word(self):
        """新词练习"""
        # self.common.get_id_back_home()   # 不清空数据，直接继续练习
        if self.home.wait_check_home_page():
            user_info = UserCenterPage().get_user_info()
            stu_id = user_info[0]
            CleanDataPage().clear_user_all_data(stu_id)  # 清空用户单词数据 重新练习

            if self.home.wait_check_home_page():  # 页面检查点
                print('进入主界面')
                self.home.click_hk_tab(1)  # 点击 背单词
                self.word.word_book_operate(stu_id)  # 单词本 游戏过程
                self.result.result_page_handle()
            else:
                Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
                print("未进入主界面")
