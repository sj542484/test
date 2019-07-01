# coding=utf-8
import time
import unittest

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.result_page import ResultPage
from testfarm.test_program.app.honor.student.homework.object_page.form_sentence_page import FormSentence
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type import GetVariable as gv
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class Games(unittest.TestCase):
    """连词成句"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.sentence = FormSentence()
        cls.result = ResultPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_form_sentence(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():
            self.home_page.click_hk_tab(2)

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()

                if gv.FORM_SENT in var[0]:
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.FORM_SENT:
                            var[1][i].click()  # 点击进入该作业
                            count = self.homework.games_count(0, '连词成句', gv.FORM_SENT)  # 小游戏个数统计
                            self.game_exist(count[0])  # 具体操作

                            if count[1] == 10:  # 判断小游戏list是否需滑屏
                                game_count = self.homework.swipe_screen('连词成句')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                            break
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.FORM_SENT, '连词成句')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """连词成句游戏具体操作 及 结果页操作"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.FORM_SENT):
                    print('############################################')
                    self.homework.games_type()[index].click()  # 进入小游戏
                    answer = self.sentence.form_sentence_operate()  # 游戏过程

                    self.sentence.check_detail_page(answer[0], answer[1], answer[2])  # 查看答案
                    self.sentence.study_again()  # 再练一遍

                    print('#############################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have连词成句小游戏')
        self.homework.back_up_button()  # 返回主界面
