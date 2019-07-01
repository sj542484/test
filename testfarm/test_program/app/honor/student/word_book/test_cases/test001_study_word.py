# coding=utf-8
import unittest
from app.student.login.object_page.home_page import HomePage
from app.student.homework.object_page.homework_page import Homework
from app.student.login.object_page.login_page import LoginPage
from app.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.student.word_book.object_page.clear_user_data import CleanDataPage
from app.student.word_book.object_page.sql_data.data_action import DataActionPage
from app.student.word_book.object_page.word_book import WordBook
from app.student.word_book.object_page.word_result_page import ResultPage
from conf.decorator import setup, teardown, testcase
from utils.toast_find import Toast


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
        cls.common = DataActionPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_study_word(self):
        """新词练习"""
        # self.common.get_id_back_home()   # 不清空数据，直接继续练习
        CleanDataPage().clear_user_all_data()  # 清空用户单词数据 重新练习

        if self.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            self.home.click_hk_tab(1)  # 点击 背单词
            self.word.word_book_operate()  # 单词本 游戏过程
            self.result.result_page_handle()
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")
