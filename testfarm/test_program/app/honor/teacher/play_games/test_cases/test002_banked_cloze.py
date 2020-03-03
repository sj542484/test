#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.banked_cloze_page import BankedCloze
from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.play_games.test_data.homework_title_type import GetVariable as gv
from conf.decorator import setup, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class Games(unittest.TestCase):
    """选词填空"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)

        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.choice = BankedCloze()
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
    def test_banked_cloze(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.CHO_WOR_CL)  # 进入首页后 点击 题库tab
            self.homework.games_operation(gv.CHO_WOR_CL, self.game_exist, '选词填空')  # 查找题单内 该类型的小游戏
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, game, name):
        """选词填空游戏具体操作 及 结果页操作"""
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                print('##########################################################')
                print(name)
                game.click()  # 进入小游戏

                if self.game.wait_check_page():
                    if self.game.wait_check_list_page():
                        word = self.get_prompt_operation()  # 获取提示词

                        if self.game.wait_check_list_page():
                            self.game.start_button()  # 开始答题 按钮
                            result = self.choice.banked_cloze_operation(word)  # 选词填空 游戏过程
                            self.result.result_page_time(result[2])  # 结果页 -- 所用时间

                            # result2 = self.choice.study_again(word)  # 结果页 错题再练/再练一遍 按钮
                            # self.result.result_page_time(result2[1][2], result2[0])  # 结果页 -- 所用时间

                            correct = self.choice.check_detail_page(result[1], result[0])  # 查看答案 操作
                            self.result.result_page_correct_rate(correct, result[0])  # 结果页 准确率
                            print('##########################################################')
                            self.homework.back_operation()   # 从结果页返回 题单详情页
                else:
                    print('未进入小游戏界面')
        else:
            print('未进入题单详情页')

    @teststeps
    def get_prompt_operation(self):
        """获取提示词"""
        word_list = []
        if WaitElement().judge_is_exists(self.choice.prompt_locator):
            self.choice.prompt()  # 右上角 提示词
            if self.home.wait_check_tips_page():
                content = self.choice.prompt_content()  # 取出提示内容
                self.choice.click_blank()  # 点击空白处 弹框消失
                word_list = content.split('   ')  # 取出单词列表

            print('待输入的单词:', word_list)
        else:
            print("无提示词")
        return word_list
