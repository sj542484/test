#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.flash_card_page import FlashCard
from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.test_data.homework_title_type import GetVariable as gv
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.decorator import setup, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)

        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.game = GamesPage()
        cls.flash_card = FlashCard()

        BasePage().set_assert(cls.ass)

    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Games, self).run(result)

    @testcase
    def test_flash_card(self):
        """对不同小游戏类型，选择不同函数进行相应的操作"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.FLA_CARD)  # 进入首页后 进入题库tab，并搜索题单
            self.homework.games_operation(gv.FLA_CARD, self.game_exist, '闪卡练习')  # 查找题单内 该类型的小游戏
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, game, name):
        """闪卡练习游戏具体操作 """
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                print('############################################################')
                print(name)
                homework_type = self.homework.game_mode(name)  # 获取小游戏模式
                game.click()  # 进入小游戏

                if "单词学习" in homework_type:
                    self.flash_card_study(self.flash_card.word_study_pattern)
                elif "句子学习" in homework_type:
                    self.flash_card_study(self.flash_card.sentence_study_pattern)
                elif "抄写" in homework_type:
                    self.flash_card_copy()

                if self.flash_card.wait_check_result_page():  # 从结果页返回 题单详情页
                    self.home.back_up_button()  # 返回 详情界面
                    if self.game.wait_check_page():
                        self.home.back_up_button()  # 返回 题单详情页
        else:
            print('未进入题单详情页')

    @teststeps
    def flash_card_study(self, fun):
        """闪卡练习--学习模式"""
        if self.game.wait_check_page():
            if self.game.wait_check_list_page():
                self.game.start_button()  # 开始答题 按钮
                result = fun()  # 闪卡练习 学习游戏过程

                # self.star_again(self.flash_card.study_pattern)  # 结果页 标星内容再练一遍
                self.study_again(fun)  # 结果页 再练一遍
                self.click_operation(result)  # 点击结果页听力按钮 和 star按钮

    @teststeps
    def flash_card_copy(self):
        """闪卡练习--抄写模式"""
        if self.game.wait_check_page():
            if self.game.wait_check_list_page():
                self.game.start_button()  # 开始答题 按钮
                result = self.flash_card.word_copy_pattern()  # 闪卡练习 抄写模式 游戏过程

                self.star_again(self.flash_card.word_copy_pattern)  # 结果页 标星内容再练一遍

                # self.study_again(self.flash_card.copy_pattern)  # 结果页 再练一遍
                # self.click_operation(result) # 点击结果页听力按钮 和 star按钮

    @teststeps
    def star_again(self, func):
        """标星内容再练一遍"""
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            print('标星内容再练一遍:')
            self.flash_card.selected_sum()  # 标星内容统计
            self.flash_card.star_again_button()  # 点击 标星内容再练一遍 按钮
            func()  # 闪卡练习 游戏过程

    @teststeps
    def study_again(self, func):
        """结果页 再练一遍"""
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            print('再练一遍:')
            self.flash_card.study_again_button()  # 点击 再练一遍 按钮
            func()  # 闪卡练习 游戏过程

    @teststeps
    def click_operation(self, result):
        """结果页 点击操作"""
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            self.flash_card.finish_study()  # 完成学习
            self.flash_card.study_sum()  # 学习结果

            self.flash_card.result_page_operation(result[1])  # 点击结果页听力按钮 和 star按钮
