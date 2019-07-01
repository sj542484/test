# coding=utf-8
import time
import unittest
import HTMLTestRunner

from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.flash_card_page import FlashCard
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type_yb import GetVariable as gv
from testfarm.test_program.utils.games_keyboard import games_keyboard
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.yb_dict import no_yb_operate_word
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """闪卡练习 - yb字体"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.flash_card = FlashCard()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_flash_card_noyb(self):
        """对不同小游戏类型，选择不同函数进行相应的操作"""
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            print("已进入主界面：")
            self.home_page.click_hk_tab(2)  # 进入 做作业

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.FLA_CARD in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])-1):
                        if var[0][i] == gv.FLA_CARD:
                            var[1][i].click()
                            count = self.homework.games_count(0, '闪卡练习', gv.FLA_CARD)
                            self.game_exist(count[0])
                            if count[1] == 10:
                                game_count = self.homework.swipe_screen('闪卡练习')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.FLA_CARD, '闪卡练习')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """闪卡练习游戏具体操作 及 操作后的滑屏"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.FLA_CARD):
                    print('####################################################')
                    homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式
                    print(homework_type)
                    if homework_type == "学习模式":
                        self.flash_card_study(index)
                        print('闪卡练习 学习模式over')
                    elif homework_type == "抄写模式":
                        self.flash_card_copy(index)
                        print('闪卡练习 抄写模式over')

                    print('####################################################')
                    if self.flash_card.wait_check_result_page():  # 结果页检查点
                        self.homework.back_up_button()
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have闪卡练习小游戏')
        self.homework.back_up_button()  # 返回主界面

    @teststeps
    def flash_card_study(self, index):
        """闪卡练习--学习模式"""
        self.homework.games_type()[index].click()
        time.sleep(3)
        self.study_pattern_no()  # 闪卡练习 学习游戏过程
        # if self.flash_card.study_sum():  # 结果页检查点
        #     self.flash_card.result_page(answer[0], answer[1])  # 点击结果页听力按钮 和 star按钮

        # # 结果页 标星内容再练一遍
        # if self.flash_card.study_sum():  # 结果页检查点
        #     self.flash_card.selected_sum()
        #     self.flash_card.study_pattern()  # 闪卡练习 学习模式游戏过程
        #
        # # 结果页 再练一遍
        # if self.flash_card.study_sum():  # 结果页检查点
        #     self.flash_card.study_again()
        #     self.flash_card.study_pattern()  # 闪卡练习 游戏过程

        self.homework.back_up_button()  # 结果页 返回按钮
        time.sleep(2)

    @teststeps
    def flash_card_copy(self, index):
        """闪卡练习--抄写模式"""
        self.homework.games_type()[index].click()
        time.sleep(3)
        self.copy_pattern_no()  # 闪卡练习 抄写模式 游戏过程
        # if self.flash_card.study_sum():  # 结果页检查点
        #     self.flash_card.result_page(answer[0], answer[1])  # 点击结果页听力按钮 和 star按钮
        #
        # # 结果页 标星内容再练一遍
        # if self.flash_card.study_sum():  # 结果页检查点
        #     self.flash_card.selected_sum()
        #     self.flash_card.copy_pattern()  # 闪卡练习 抄写模式游戏过程
        #
        # # 结果页 再练一遍
        # if self.flash_card.study_sum():  # 结果页检查点
        #     self.flash_card.study_again()
        #     self.flash_card.copy_pattern()  # 闪卡练习 游戏过程

        self.flash_card.back_up_button()  # 结果页 返回按钮
        time.sleep(2)

    @teststeps
    def study_pattern_no(self):
        """《闪卡练习 学习模式》 游戏过程"""
        answer = []
        rate = self.flash_card.rate()
        if self.flash_card.wait_check_page():   # 页面检查点
            for i in range(int(rate)):
                word = self.flash_card.english_study()  # 单词
                explain = self.flash_card.explain_study()  # 解释

                if len(word) <= 2:
                    value = no_yb_operate_word(word)
                    if value == explain:
                        answer.append(word)
                else:
                    print('error:', word)

                self.flash_card.click_rotate()  # 点击翻转页面按钮切换页面
                self.flash_card.click_voice()  # 点击听力按钮
                for j in range(2):
                    self.flash_card.click_rotate()  # 切换页面
                self.flash_card.click_rotate()  # 点击翻转页面按钮切换页面

                if i in range(1, int(rate), 2):  # 点击star按钮
                    self.flash_card.click_star()
                self.homework.next_button()  # 下一题按钮
        return rate, answer

    @teststeps
    def copy_pattern_no(self):
        """《闪卡练习 抄写模式》 游戏过程"""
        answer = []
        rate = self.flash_card.rate()
        if self.flash_card.wait_check_page():  # 页面检查点
            for i in range(int(rate)):
                self.flash_card.click_voice()  # 听力按钮
                explain = self.flash_card.explain_copy()  # 展示的音标
                word = self.flash_card.word_copy()   # 展示的单词
                if len(explain) == 3:
                    value = no_yb_operate_word(explain)
                    answer.append(explain)
                    if len(value) == 1 and value == word.lower():
                        games_keyboard(value)  # 点击键盘对应字母
                    elif len(value) == 2 and value == word.lower():
                        for k in range(len(value)):
                            games_keyboard(value[k])  # 点击键盘对应字母
                else:
                    print("第几题：%s" % (i + 1), "单词是:%s" % self.flash_card.word_copy().text)
                    for j in range(len(word)):
                        games_keyboard(word[j])  # 点击键盘对应字母

                if i in range(1, int(rate), 2):  # 点击star按钮
                    self.flash_card.click_star()
                time.sleep(1)
        return rate, answer


if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(Games('test_flash_card'))

        report_title = u'Example用例执行报告'
        desc = '用于展示修改样式后的HTMLTestRunner'
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filename = r'C:/Users/V/Desktop/Testreport/Result_' + timestr + '.html'
        print(filename)
        fp = open(filename, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=report_title,
            description=desc)
        runner.run(suite)
        fp.close()
