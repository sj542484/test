# coding=utf-8
import unittest

from app.student.login.object_page.home_page import HomePage
from app.student.homework.object_page.homework_page import Homework
from app.student.login.object_page.login_page import LoginPage
from app.student.word_book.object_page.clear_user_data import CleanDataPage
from app.student.word_book.object_page.word_book import WordBook
from app.student.word_book.object_page.word_result_page import ResultPage
from conf.decorator import setup, teardown, testcase, teststeps


class Word(unittest.TestCase):
    """单词本"""

    @classmethod
    @setup
    def setUp(cls):
        cls.home = HomePage()
        cls.word = WordBook()
        cls.result = ResultPage()
        cls.login = LoginPage()
        cls.homework = Homework()
        cls.login.app_status()  # 判断APP当前状态

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_recite_word_again(self):
        """下一年级单词"""
        if self.home.wait_check_home_page ():  # 页面检查点
            print ('进入主界面')
            self.home.click_hk_tab (1)  # 点击 背单词
            """
            进入单词本有两种状况:
            1、脚本test002运行未完成，出现继续图标
            2、脚本test002运行完成，
            """
            if self.word.wait_check_start_page ():  # 页面检查点

                if self.word.wait_check_start_page ():  # 页面检查点
                    self.word.word_start_button()  # 点击 Go按钮
                    print ("开始单词本练习")
                    if self.result.wait_check_next_grade ():
                        self.result.confirm_button()
                        if self.word.wait_check_game_page():
                            self.word.play_word_book()
                            self.result.result_page_handle()

                elif self.word.wait_check_continue_page ():  # 页面检查点
                    print ("脚本test002 运行失败 ，此脚本无法继续执行！")



