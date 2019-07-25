# coding=utf-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page import Homework
from app.honor.teacher.play_games.object_page import MatchingExercises
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.play_games.object_page import ResultPage
from app.honor.teacher.play_games import GetVariable as gv
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page import QuestionDetailPage
from utils.toast_find import Toast
from conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """连连看"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.question = TestBankPage()
        cls.match = MatchingExercises()
        cls.game = GamesPage()
        cls.detail = QuestionDetailPage()
        cls.result = ResultPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_match_exercise(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation(gv.MAT_EXE)  # 进入首页后 进入题库tab，并搜索题单

            if self.question.wait_check_page('题单'):  # 页面检查点
                name = self.question.question_name()
                for i in range(len(name[0])):
                    if name[1][i] == gv.MAT_EXE:
                        name[0][i].click()  # 点击进入该作业

                        count = []  # 小游戏数目
                        self.homework.games_count('连连看', count)  # 小游戏个数统计
                        self.game_exist(count)  # 具体操作
                        break

                if self.question.wait_check_page('题单'):  # 检查点
                    self.home.click_tab_hw()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """连连看 游戏具体操作 及 结果页操作"""
        if len(count) != 0:
            for index in count:
                if self.detail.wait_check_page():
                    if self.detail.wait_check_list_page():
                        print('####################################################')
                        self.homework.num(index).click()  # 进入小游戏
                        if self.game.wait_check_page():
                            if self.game.wait_check_list_page():
                                self.game.start_button()  # 开始答题 按钮

                                result = self.match.match_exercise()  # 游戏过程
                                self.result.result_page_correct_rate(result[1], result[0])  # 结果页 -- 准确率
                                self.match.result_detail_page(result[0])  # 结果页 查看答案 按钮
                                self.match.study_again()  # 结果页 再练一遍 按钮
                                self.result.result_page_correct_rate(result[1], result[0])  # 结果页 -- 准确率

                                print('####################################################')
                                self.homework.back_operation()  # 从结果页返回 题单详情页
        else:
            print('no have连连看 小游戏')
        if self.detail.wait_check_page():  # 检查点
            self.home.back_up_button()  # 返回 题库页面
