# coding=utf-8
import unittest
from builtins import classmethod
from functools import reduce
from math import ceil

from app.student.login.object_page.home_page import HomePage
from app.student.homework.object_page.homework_page import Homework
from app.student.login.object_page.login_page import LoginPage
from app.student.word_book_rebuild.object_page.clear_user_data import CleanDataPage
from app.student.word_book_rebuild.object_page.data_action import DataActionPage
from app.student.word_book_rebuild.object_page.new_word_game import NewWordGame
from app.student.word_book_rebuild.object_page.word_book import WordBook
from app.student.word_book_rebuild.object_page.word_result_page import ResultPage
from conf.decorator import setup, teardown, testcase


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
        cls.clear = CleanDataPage()
        cls.newgame = NewWordGame()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_study_word(self):
        """新词练习"""
        if self.home.wait_check_home_page():  # 页面检查点
            self.clear.get_id_back(action=0)

            student_all_words = self.common.get_student_word()
            print("分组单词：", student_all_words)

            if self.home.wait_check_home_page():  # 页面检查点
                print('进入主界面')
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.word.wait_check_start_page():   # 开始页面检查点
                    self.word.word_start_button()      # 点击 Go按钮

                elif self.word. wait_check_continue_page():    # 继续学习页面
                    self.word.word_continue_button()           # 继续学习按钮

                all_word = self.common.get_all_word_count(student_all_words)
                group_count = int(ceil(all_word/10))
                print(group_count)

                for i in range(group_count):
                    change_words = self.common.change_teacher_word_group(student_all_words)
                    study_word = student_all_words['系统'] if \
                        len(student_all_words['老师']) == 0 else student_all_words['老师']
                    print("学习单词：", study_word)
                    if self.word.wait_check_game_page():
                        self.newgame.play_new_word_game_operate(study_word, str(i + 1), change_words)

                        if ResultPage().wait_check_result_page():
                            print("进入结果页面\n")
                            after_game_new_words = self.newgame.read_data_from_json()['新词']
                            after_review_words = self.newgame.read_data_from_json()['复习单词']
                            ResultPage().check_result_word_data(after_game_new_words, after_review_words)
                            self.common.remove_studied_word(after_game_new_words, student_all_words)
                            self.result.clock_button()    # 打卡
                            self.result.show_page_ele()  # 炫耀一下页面
                            self.home.click_back_up_button()  # 返回
                            if self.result.wait_check_result_page():
                                self.result.more_again_button()  # 再练一次
                    else:
                        if self.word.wait_check_count_limit_page():
                            if i != 6:
                                print('★★★ 未到第七组显示次数已用完！')

                            print('今日练习次数已用完，休息一下，明天再练！')
                            self.word.limit_confirm_button()  # 确定
                            if self.word.wait_check_start_page():
                                self.home.click_back_up_button()
                                break
