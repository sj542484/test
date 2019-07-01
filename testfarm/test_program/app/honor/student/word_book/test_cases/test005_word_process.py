import unittest

from app.student.login.object_page.home_page import HomePage
from app.student.login.object_page.login_page import LoginPage
from app.student.word_book.object_page.sql_data.data_action import DataActionPage
from app.student.word_book.object_page.sql_data.mysql_data import MysqlData
from app.student.word_book.object_page.word_book import WordBook
from app.student.word_book.object_page.word_progress import ProgressPage
from conf.decorator import setup, teardown


class WordProcess(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.home = HomePage()
        cls.mysql = MysqlData()
        cls.word = WordBook()
        cls.progress = ProgressPage()
        cls.login = LoginPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.common = DataActionPage()

    @teardown
    def tearDown(self):
        pass

    def test_word_process(self):
        """词书进度"""
        self.common.get_id_nick_back_home()   # 获取student_id
        if self.home.wait_check_home_page():
            print('进入主界面')
            self.home.click_hk_tab(1)  # 点击 背单词
            if self.word.wait_check_start_page() or self.word.wait_check_continue_page():
                self.progress.word_progress_icon()
                if self.progress.wait_check_progress_page():
                    self.progress.progress_ele_check()
                    self.word.back_to_home()


