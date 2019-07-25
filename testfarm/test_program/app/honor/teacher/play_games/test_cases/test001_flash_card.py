# coding=utf-8
import unittest

from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.object_page.home_page import  ThomePage
from app.honor.teacher.play_games.object_page import Homework
from app.honor.teacher.play_games.object_page import FlashCard
from app.honor.teacher.play_games import GetVariable as gv
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page import QuestionDetailPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.game = GamesPage()
        cls.flash_card = FlashCard()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_flash_card(self):
        """对不同小游戏类型，选择不同函数进行相应的操作"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.FLA_CARD)  # 进入首页后 进入题库tab，并搜索题单

            if self.question.wait_check_page('题单'):  # 页面检查点
                name = self.question.question_name()
                for i in range(len(name[0])):
                    if name[1][i] == gv.FLA_CARD:
                        name[0][i].click()  # 点击进入该作业

                        count = []  # 小游戏数目
                        self.homework.games_count('闪卡练习',count)  # 小游戏个数统计
                        self.game_exist(count)  # 具体操作
                        break

                if self.question.wait_check_page('题单'):  # 检查点
                    self.home.click_tab_hw()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """闪卡练习游戏具体操作 """
        if len(count) != 0:
            for index in count:
                if self.detail.wait_check_page():
                    if self.detail.wait_check_list_page():
                        print('############################################################')
                        homework_type = self.homework.game_mode(index)  # 获取小游戏模式

                        if "学习" in homework_type:
                            self.flash_card_study(index)
                        elif "抄写" in homework_type:
                            self.flash_card_copy(index)

                        print('############################################################')
                        if self.flash_card.wait_check_result_page():
                            self.home.back_up_button()  # 返回小游戏界面
                            if self.game.wait_check_page():
                                self.home.back_up_button()  # 返回 题单详情页
        else:
            print('no have闪卡练习小游戏')
        if self.detail.wait_check_page():  # 检查点
            self.home.back_up_button()  # 返回 题库页面

    @teststeps
    def flash_card_study(self, index):
        """闪卡练习--学习模式"""
        self.homework.num(index).click()  # 进入小游戏
        if self.game.wait_check_page():
            if self.game.wait_check_list_page():
                self.game.start_button()  # 开始答题 按钮
                result = self.flash_card.study_pattern()  # 闪卡练习 学习游戏过程

                # 结果页 标星内容再练一遍
                if self.flash_card.wait_check_result_page():  # 结果页检查点
                    print('标星内容再练一遍:')
                    self.flash_card.selected_sum()  # 标星内容统计
                    self.flash_card.star_again_button()  # 点击 标星内容再练一遍 按钮
                    self.flash_card.study_pattern()  # 闪卡练习 学习模式游戏过程

                # 结果页 再练一遍
                if self.flash_card.wait_check_result_page():  # 结果页检查点
                    print('再练一遍:')
                    self.flash_card.study_again_button()  # 点击 再练一遍 按钮
                    self.flash_card.study_pattern()  # 闪卡练习 学习模式游戏过程

                if self.flash_card.wait_check_result_page():  # 结果页检查点
                    self.flash_card.result_page(result[0], result[1])  # 点击结果页听力按钮 和 star按钮

    @teststeps
    def flash_card_copy(self, index):
        """闪卡练习--抄写模式"""
        self.homework.num(index).click()  # 进入小游戏
        if self.game.wait_check_page():
            if self.game.wait_check_list_page():
                self.game.start_button()  # 开始答题 按钮
                result = self.flash_card.copy_pattern()  # 闪卡练习 抄写模式 游戏过程

                # 结果页 标星内容再练一遍
                if self.flash_card.wait_check_result_page():  # 结果页检查点
                    print('标星内容再练一遍:')
                    self.flash_card.selected_sum()  # 标星内容统计
                    self.flash_card.star_again_button()  # 点击 标星内容再练一遍 按钮
                    self.flash_card.copy_pattern()  # 闪卡练习 抄写模式游戏过程

                # 结果页 再练一遍
                if self.flash_card.wait_check_result_page():  # 结果页检查点
                    print('再练一遍:')
                    self.flash_card.study_again_button()  # 点击 再练一遍 按钮
                    self.flash_card.copy_pattern()  # 闪卡练习 游戏过程

                if self.flash_card.wait_check_result_page():  # 结果页检查点
                    self.flash_card.result_page(result[0], result[1])  # 点击结果页听力按钮 和 star按钮
