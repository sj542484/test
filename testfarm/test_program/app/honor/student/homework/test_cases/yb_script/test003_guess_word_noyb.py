# coding=utf-8
import time
import unittest
import HTMLTestRunner

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.guess_word_page import GuessWord
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type_yb import GetVariable as gv
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.yb_dict import no_yb_operate_word
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """猜词游戏 -yb字体"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.guess_word = GuessWord()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_guess_word_noyb(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():
            print("已进入主界面：")
            self.home_page.click_hk_tab(2)  # 进入 做作业

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.GUE_WOR in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.GUE_WOR:
                            var[1][i].click()
                            count = self.homework.games_count(0, '猜词游戏', gv.GUE_WOR)
                            self.game_exist(count[0])
                            if count[1] == 10:
                                game_count = self.homework.swipe_screen('猜词游戏')
                                self.game_exist(game_count)
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.GUE_WOR, '猜词游戏')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """猜词游戏游戏具体操作 及 操作后的滑屏"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.GUE_WOR):
                    print('####################################################')
                    homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式
                    self.homework.games_type()[index].click()  # 进入小游戏
                    self.diff_type_no(homework_type)  # 不同模式小游戏的 游戏过程

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have猜词游戏小游戏')
        self.homework.back_up_button()  # 返回主界面

    @teststeps
    def diff_type_no(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        print(tpe)
        if tpe == '有发音':
            self.voice_pattern_no()
        elif tpe == '无发音':
            self.no_voice_pattern_no()

    @teststeps
    def voice_pattern_no(self):
        """《猜词游戏 有发音模式》 游戏过程"""
        if self.guess_word.wait_check_page():  # 页面检查点
            rate = self.guess_word.rate()
            for i in range(int(rate)):
                content = self.guess_word.chinese()  # 展示的题目内容
                letters = self.guess_word.keyboard()  # 小键盘 字母
                if len(content) == 3:
                    value = no_yb_operate_word(content)
                    if len(value) == 1:
                        for k in range(len(letters)):
                            if letters[k].text == value:
                                letters[k].click()  # 点击键盘对应字母
                                break
                    else:
                        for k in range(len(value)):
                            for z in range(len(letters)):
                                if letters[z].text == value[k]:
                                    letters[z].click()  # 点击键盘对应字母
                                    break
                else:
                    for j in range(len(content)):
                        for k in range(len(letters)):
                            if letters[k].text == content[j]:
                                letters[k].click()  # 点击键盘对应字母
                                break
                time.sleep(2)

    @teststeps
    def no_voice_pattern_no(self):
        """《猜词游戏 无发音模式》 游戏过程"""
        if self.guess_word.wait_check_page():  # 页面检查点
            rate = self.guess_word.rate()
            for i in range(int(rate)):
                content = self.guess_word.chinese()  # 展示的题目内容
                letters = self.guess_word.keyboard()  # 小键盘 字母
                if len(content) == 3:
                    value = no_yb_operate_word(content)
                    if len(value) == 1:
                        for k in range(len(letters)):
                            if letters[k].text == value:
                                letters[k].click()  # 点击键盘对应字母
                                break
                    else:
                        for k in range(len(value)):
                            for z in range(len(letters)):
                                if letters[z].text == value[k]:
                                    letters[z].click()  # 点击键盘对应字母
                                    break
                else:
                    for j in range(len(content)):
                        for k in range(len(letters)):
                            if letters[k].text == content[j]:
                                letters[k].click()  # 点击键盘对应字母
                                break
                time.sleep(2)


if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(Games('test_guess_word'))

        report_title = u'自动化测试执行报告'
        desc = '用于展示修改样式后的HTMLTestRunner'
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filename = r'C:/Users/V/Desktop/Testreport/Result_' + timestr + '.html'

        fp = open(filename, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=report_title,
            description=desc)
        runner.run(suite)
        fp.close()
