#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.object_page.single_choice_page import SingleChoice
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.test_data.homework_title_type import GetVariable as gv
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from conf.decorator import setup, teardown, teststeps, testcase
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """单项选择"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.single = SingleChoice()
        cls.question = TestBankPage()
        cls.game = GamesPage()
        cls.detail = QuestionDetailPage()
        cls.result = ResultPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_single_choice(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.SIN_CHO)  # 进入首页后 进入题库tab，并搜索题单

            if self.question.wait_check_page('题单'):  # 页面检查点
                name = self.question.question_name()
                for i in range(len(name[0])):
                    if name[1][i] == gv.SIN_CHO:
                        name[0][i].click()  # 点击进入该作业

                        count = []  # 小游戏数目
                        self.homework.games_count('单项选择', count)  # 统计小游戏个数
                        self.game_exist(count)  # 具体操作
                        break

                if self.question.wait_check_page('题单'):  # 检查点
                    self.home.click_tab_hw()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """单项选择游戏具体操作 及 结果页操作"""
        if len(count) != 0:
            for index in count:
                if self.detail.wait_check_page():
                    if self.detail.wait_check_list_page():
                        print('#################################################################')
                        self.homework.num(index).click()  # 进入小游戏
                        if self.game.wait_check_page():
                            if self.game.wait_check_list_page():
                                self.game.start_button()  # 开始答题 按钮

                                result = self.single.single_choice_operation()  # 单项选择 - 游戏过程
                                self.result.result_page_time(result[2])  # 结果页 -- 所用时间
                                # self.result.result_page_correct_rate(result[1], result[0])  # 结果页 准确率
                                #
                                # result2 = self.single.study_again()  # 结果页 错题再练/再练一遍 按钮
                                # self.result.result_page_correct_rate(result[1] + result2[1][1], result[0])  # 结果页 -- 准确率
                                # self.result.result_page_time(result2[1][2], result2[0])  # 结果页 -- 所用时间

                                self.single.check_detail_page(result[0])  # 结果页 查看答案
                                print('#################################################################')
                                self.homework.back_operation()  # 从结果页返回 题单详情页
        else:
            print('no have单项选择小游戏')
        if self.detail.wait_check_page():  # 检查点
            self.home.back_up_button()  # 返回 题库页面
