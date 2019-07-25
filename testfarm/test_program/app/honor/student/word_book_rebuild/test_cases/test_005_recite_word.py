#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/8 8:48
# -----------------------------------------
import unittest

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.wordbook_rebuild import WordBookRebuildPage
from testfarm.test_program.app.honor.student.word_book_rebuild.test_data.account import *
from testfarm.test_program.conf.decorator import setup, teardown, testcase


class ReciteWord(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.login.app_status(stu_account=STU_ACCOUNT, stu_password=STU_PASSWORD)  # 判断APP当前状态
        cls.word_info = cls.word_rebuild.read_words_info_from_file()

    @teardown
    def tearDown(self):
        pass


    @testcase
    def test_recite_words(self):
        """测试复习单词"""

