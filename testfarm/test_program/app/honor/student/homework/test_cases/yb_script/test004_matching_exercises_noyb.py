# coding=utf-8
import time
import unittest
import HTMLTestRunner

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.matching_exercises_page import MatchingExercises
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type_yb import GetVariable as gv
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.yb_dict import no_yb_operate_yb
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """连连看 - yb字体"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.match_up = MatchingExercises()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_match_exercise_noyb(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            print("已进入主界面：")
            self.home_page.click_hk_tab(2)  # 进入 做作业

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.MAT_EXE in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.MAT_EXE:
                            var[1][i].click()
                            count = self.homework.games_count(0, '连连看', gv.MAT_EXE)
                            self.game_exist(count[0])
                            if count[1] == 10:
                                game_count = self.homework.swipe_screen('连连看')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.MAT_EXE, '连连看')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """游戏具体操作 及 操作后的滑屏"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.MAT_EXE):
                    print('####################################################')
                    self.homework.games_type()[index].click()  # 进入小游戏
                    self.match_exercise_no()  # 游戏过程

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
    def match_exercise_no(self):
        """《连连看》 游戏过程"""
        if self.match_up.wait_check_page():  # 页面检查点
            rate = self.match_up.rate()

            if int(rate) % 5 == 0:  # 根据题目数判断分几页展示
                page = int(int(rate) / 5)
            else:
                page = int(int(rate) / 5) + 1
            print('页数:', page)

            for j in range(page):  # 然后在不同页面做对应的题目
                print(j)
                word = []  # 单词list
                word_index = []  # 单词在所有button中的索引
                explain = []  # 解释list
                explain_index = []   # 解释在所有button中的索引
                ele = self.match_up.word()  # 所有button
                for i in range(3, len(ele)):
                    if ele[i].text[0] != "/":
                        word.append(ele[i].text)
                        word_index.append(i)
                    else:
                        explain.append(ele[i].text)
                        explain_index.append(i)
                print(word_index, word, explain, explain_index)

                for k in range(len(word)):  # 具体操作
                    print('word:', word[k], len(word[k]))
                    if len(word[k]) <= 2:
                        value = no_yb_operate_yb(word[k])
                        ele[word_index[k]].click()
                        for z in range(len(explain)):
                            if explain[z] == value:
                                print('explain:', explain[z])
                                ele[explain_index[z]].click()
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
