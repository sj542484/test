#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.reading_comprehension_page import ReadComprehension
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.test_data.homework_title_type import GetVariable as gv
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.decorator import setup, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """阅读理解"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.read = ReadComprehension()
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
    def test_reading_comprehension(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.REA_COMPRE)  # 进入首页后 进入题库tab，并搜索题单
            self.homework.games_operation(gv.REA_COMPRE, self.game_exist, '阅读理解')  # 查找题单内 该类型的小游戏

            if self.question.wait_check_page():  # 检查点
                self.home.click_tab_hw()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
            
    @teststeps
    def game_exist(self, game, name):
        """阅读理解 游戏具体操作"""
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                print('####################################################')
                print(name)
                game.click()  # 进入小游戏

                if self.game.wait_check_page():
                    if self.game.wait_check_list_page():
                        self.game.start_button()  # 开始答题 按钮

                        result = self.read.reading_operation()  # 阅读理解 游戏过程
                        self.result.result_page_time(result[2])  # 结果页 -- 所用时间

                        # result2 = self.read.study_again()  # 结果页 再练一遍 按钮
                        # self.result.result_page_time(result2[2], '再练一遍')  # 结果页 -- 所用时间
                        #
                        self.read.check_detail_page(result[1], result[0])  # 结果页 查看答案
                        print('####################################################')
                        self.homework.back_operation()  # 从结果页返回 题单详情页
