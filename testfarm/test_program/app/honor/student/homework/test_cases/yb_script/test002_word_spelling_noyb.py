# coding=utf-8
import unittest

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.word_spelling_page import WordSpelling
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type_yb import GetVariable as gv
from testfarm.test_program.utils.games_keyboard import games_keyboard
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.yb_dict import no_yb_operate_word
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """单词拼写 -yb字体"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.word_spelling = WordSpelling()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_word_spelling_noyb(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            print("已进入主界面：")
            self.home_page.click_hk_tab(2)  # 进入 做作业

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.WOR_SPE in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.WOR_SPE:
                            var[1][i].click()
                            count = self.homework.games_count(0, '单词拼写', gv.WOR_SPE)
                            self.game_exist(count[0])
                            if count[1] == 10:
                                game_count = self.homework.swipe_screen('单词拼写')
                                self.game_exist(game_count)
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.WOR_SPE, '单词拼写')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """词汇选择游戏具体操作 及 操作后的滑屏"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.WOR_SPE):
                    print('####################################################')
                    homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式
                    self.homework.games_type()[index].click()  # 进入小游戏
                    self.diff_type_no(homework_type)  # 不同模式小游戏的 游戏过程

                    # self.word_spelling.result_page()  # 结果页
                    # self.word_spelling.result_detail_page()  # 结果页 查看答案 按钮
                    # self.word_spelling.study_again(homework_type)  # 结果页 错题再练 按钮

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have词汇选择小游戏')
        self.homework.back_up_button()  # 返回主界面

    @teststeps
    def diff_type_no(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        print(tpe)
        if tpe == '默写模式':
            self.dictation_pattern_no()
        elif tpe == '自定义':
            self.custom_pattern_no()
        else:  # 随机模式
            self.random_pattern_no()

    @teststeps
    def random_pattern_no(self):
        """《单词拼写 随机模式》 游戏过程"""
        if self.word_spelling.wait_check_page():  # 页面检查点
            rate = self.word_spelling.rate()
            for i in range(int(rate)):
                explain = self.word_spelling.explain()  # 展示的解释
                if len(explain) == 3:
                    value = no_yb_operate_word(explain)
                    if len(value) == 1:
                        games_keyboard(value)  # 点击键盘对应字母
                    else:  # 'ew'
                        word = self.word_spelling.word()
                        for k in range(len(value)):
                            if value[k] not in word:
                                games_keyboard(value[k])  # 点击键盘对应字母
                                break

                self.homework.next_button()
                self.word_spelling.click_voice()
                self.homework.next_button()

    @teststeps
    def custom_pattern_no(self):
        """《单词拼写 自定义模式》 游戏过程"""
        if self.word_spelling.wait_check_page():  # 页面检查点
            rate = self.word_spelling.rate()
            for i in range(int(rate)):
                explain = self.word_spelling.explain()  # 展示的解释
                if len(explain) == 3:
                    value = no_yb_operate_word(explain)
                    if len(value) == 1:
                        games_keyboard(value)  # 点击键盘对应字母
                    else:  # 'ew'
                        for k in range(len(value)):
                            games_keyboard(value[k])  # 点击键盘对应字母

                self.homework.next_button()
                self.word_spelling.click_voice()
                self.homework.next_button()

    @teststeps
    def dictation_pattern_no(self):
        """《单词拼写 默写模式》 游戏过程"""
        if self.word_spelling.wait_check_page():  # 页面检查点
            rate = self.word_spelling.rate()
            for i in range(int(rate)):
                explain = self.word_spelling.explain()  # 展示的解释
                if len(explain) == 3:
                    value = no_yb_operate_word(explain)
                    if len(value) == 1:
                        games_keyboard(value)  # 点击键盘对应字母
                    else:  # 'ew'
                        for k in range(len(value)):
                            games_keyboard(value[k])  # 点击键盘对应字母

                self.homework.next_button()
                self.word_spelling.click_voice()
                self.homework.next_button()
