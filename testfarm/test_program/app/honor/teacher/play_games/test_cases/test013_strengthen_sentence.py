# coding=utf-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.play_games.object_page.homework_page import Homework
from testfarm.test_program.app.honor.teacher.play_games.object_page.strengthen_sentence_page import StrengthenSentencePage
from testfarm.test_program.app.honor.teacher.play_games.test_data.homework_title_type import GetVariable as gv
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class Games(unittest.TestCase):
    """强化炼句"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = Homework()
        cls.question = TestBankPage()
        cls.sentence = StrengthenSentencePage()
        cls.game = GamesPage()
        cls.detail = QuestionDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_strengthen_sentence(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():
            self.question.search_operation()  # 进入首页后 进入题库tab，并搜索题单

            if self.question.wait_check_page('题单'):  # 页面检查点
                name = self.question.question_name()
                for i in range(len(name[0])):
                    if name[1][i] == gv.STREN_SENT:
                        name[0][i].click()  # 点击进入该作业

                        count = []  # 小游戏数目
                        self.homework.games_count('强化炼句', count)  # 小游戏个数统计
                        self.game_exist(count)  # 具体操作
                        break

                if self.question.wait_check_page('题单'):  # 检查点
                    self.home.click_tab_hw()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """强化炼句游戏具体操作"""
        if len(count) != 0:
            for index in count:
                if self.detail.wait_check_page():
                    if self.detail.wait_check_list_page():
                        print('#############################################')
                        homework_type = self.homework.game_mode(index)  # 获取小游戏模式
                        self.homework.num(index).click()  # 进入小游戏
                        if self.game.wait_check_page():
                            if self.game.wait_check_list_page():
                                self.game.start_button()  # 开始答题 按钮
                                self.sentence.diff_type(homework_type)  # 不同模式小游戏的 游戏过程

                                print('#############################################')
                                self.homework.back_operation()  # 从结果页返回 题单详情页
        else:
            print('no have强化炼句小游戏')
        if self.detail.wait_check_page():  # 检查点
            self.home.back_up_button()  # 返回 题库页面
