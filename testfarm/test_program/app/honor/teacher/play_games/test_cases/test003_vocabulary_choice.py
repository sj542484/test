#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.object_page.vocabulary_choice_page import VocabularyChoice
from app.honor.teacher.play_games.test_data.homework_title_type import GetVariable as gv
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.decorator import setup, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """词汇选择"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)

        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.vocab_select = VocabularyChoice()
        cls.question = TestBankPage()
        cls.game = GamesPage()
        cls.detail = QuestionDetailPage()
        cls.result = ResultPage()

        BasePage().set_assert(cls.ass)

    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Games, self).run(result)

    @testcase
    def test_vocabulary_choice(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.VOC_CHO)  # 进入首页后 进入题库tab，并搜索题单
            self.homework.games_operation(gv.VOC_CHO, self.game_exist, '词汇选择')  # 查找题单内 该类型的小游戏
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, game, name):
        """词汇选择游戏具体操作 及 结果页操作"""
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                print('######################################################')
                print(name)
                game_type = self.homework.game_mode(name)  # 获取小游戏模式
                game.click()  # 进入小游戏

                if self.game.wait_check_page():
                    if self.game.wait_check_list_page():
                        self.game.start_button()  # 开始答题 按钮
                        result = self.vocab_select.diff_type(game_type)  # 不同模式小游戏的 游戏过程
                        # self.result.result_page_correct_rate(result[1], result[0])  # 结果页 准确率

                        if game_type == '选单词':
                            self.vocab_select.result_detail_page()  # 结果页 查看答案 按钮
                        elif game_type == '听音选义':
                            result2 = self.vocab_select.study_again(game_type)  # 结果页 错题再练/再练一遍 按钮
                            self.result.result_page_correct_rate(result[1] + result2[1][1], result[0])  # 结果页 -- 准确率

                        self.homework.back_operation()   # 从结果页返回 题单详情页
