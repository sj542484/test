# coding=utf-8
import random
import time
import unittest
import HTMLTestRunner

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.vocabulary_choice_page import VocabularyChoice
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type_yb import GetVariable as gv
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.yb_dict import yb_operate_word, yb_operate_yb
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """词汇选择- yb字体"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.vocab_select = VocabularyChoice()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vocabulary_selection_yb(self):
        self.login_page.app_status()   # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 主界面检查点
            print("已进入主界面：")
            self.home_page.click_hk_tab(2)  # 进入 做作业

            if self.homework.wait_check_hw_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.VOC_CHO_YB in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.VOC_CHO_YB:
                            var[1][i].click()
                            count = self.homework.games_count(0, '词汇选择', gv.VOC_CHO)
                            self.game_exist(count[0])

                            if count[1] == 10:  # 判断小游戏list是否需滑屏
                                game_count = self.homework.swipe_screen('词汇选择')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.VOC_CHO_YB, '词汇选择')  # 作业list翻页
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
                if self.homework.wait_check_game_list_page(gv.VOC_CHO_YB):
                    print('####################################################')
                    homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式
                    self.homework.games_type()[index].click()  # 进入小游戏
                    self.diff_type(homework_type)  # 不同模式小游戏的 游戏过程

                    # self.vocab_select.result_page()  # 结果页
                    # self.vocab_select.result_detail_page()  # 结果页 查看答案 按钮
                    # self.vocab_select.study_again(homework_type)  # 结果页 错题再练 按钮

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have词汇选择小游戏')
        self.homework.back_up_button()  # 返回主界面

    @teststeps
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        print(tpe)
        if tpe == '选单词':
            self.vocab_select_choice_word()
        elif tpe == '选解释':
            self.vocab_select_choice_explain()
        elif tpe == '听音选词':  # 听音选词模式
            # print('听音选词模式')
            self.vocab_select_listen_choice()

    @teststeps
    def vocab_select_choice_explain(self):
        """《词汇选择》 - 选解释模式 游戏过程--普通单词一般做法，符合yb字体规范的特殊处理"""
        if self.vocab_select.wait_check_page():  # 页面检查点
            rate = self.vocab_select.rate()
            for i in range(int(rate)):
                self.vocab_select.click_voice()
                word = self.vocab_select.question_content()  # 中文解释
                options = self.vocab_select.option_button()
                if len(word) > 2:
                    options[random.randint(0, len(options)-1)].click()  # 随机点击选项
                else:
                    value = yb_operate_yb(word)
                    for j in range(4):
                        if options[j].text == value:
                            options[j].click()
                            break
                self.homework.next_button()
                time.sleep(1)
            time.sleep(2)

    @teststeps
    def vocab_select_choice_word(self):
        """《词汇选择》 - 选单词模式 游戏过程"""
        if self.vocab_select.wait_check_page():  # 页面检查点
            rate = self.vocab_select.rate()
            for i in range(int(rate)):
                word = self.vocab_select.question_content()  # 中文解释
                options = self.vocab_select.option_button()
                if len(word) != 3:
                    options[random.randint(0, len(options)-1)].click()  # 随机点击选项
                else:
                    value = yb_operate_word(word)
                    for j in range(4):
                        if options[j].text.lower() == value:
                            options[j].click()
                            break
                self.homework.next_button()
            time.sleep(2)

    @teststeps
    def vocab_select_listen_choice(self):
        """《词汇选择》 - 听音选词模式 游戏过程"""
        if self.vocab_select.wait_check_page():  # 页面检查点
            rate = self.vocab_select.rate()
            for i in range(int(rate)):
                self.vocab_select.voice()
                self.vocab_select.click_voice()

                options = self.vocab_select.option_button()
                options[random.randint(0, len(options)-1)].click()  # 随机点击选项

                self.vocab_select.explain()  # 中文解释
                self.homework.next_button()
            time.sleep(2)


if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(Games('test_vocabulary_selection_yb'))

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
