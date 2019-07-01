# coding=utf-8
import time
import unittest
import HTMLTestRunner

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.restore_word_page import RestoreWord
from testfarm.test_program.app.honor.student.homework.object_page.result_page import ResultPage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type_yb import GetVariable as gv
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.yb_dict import yb_operate_word, yb_operate_yb


class Games(unittest.TestCase):
    """还原单词-yb字体"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.res_word = RestoreWord()
        cls.base_page = BasePage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_restore_word_yb(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            print("已进入主界面：")
            self.home_page.click_hk_tab(2)  # 进入 做作业

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.RES_WORD_YB in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.RES_WORD_YB:
                            var[1][i].click()
                            # count = self.homework.games_count(0, '还原单词')
                            self.game_exist([1])
                else:
                    print('当前页no have该作业')
                    BasePage().screen_swipe_up(0.5, 0.75, 0.25, 1000)
                    # self.home_page.swipe(var[0], gv.RES_WOR_YB, '还原单词')  # 作业list翻页
                    self.game_exist([1])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """词汇选择游戏具体操作 及 操作后的滑屏"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.RES_WORD_YB):
                    print('####################################################')
                    self.homework.games_type()[index].click()  # 进入小游戏
                    answer = self.restore_word_yb()  # 小游戏的 游戏过程
                    # self.word_spelling.result()  # 结果页
                    self.check_answer_page(answer[0], answer[1])  # 结果页 查看答案 按钮
                    # self.word_spelling.study_again(homework_type)  # 结果页 错题再练 按钮

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回 作业列表
        else:
            print('no have词汇选择小游戏')
        self.homework.back_up_button()  # 返回主界面

    @teststeps
    def restore_word_yb(self):
        """《还原单词》 游戏过程"""
        rate = self.res_word.rate()
        answer = []
        if self.res_word.wait_check_page():  # 页面检查点
            for i in range(int(rate)):
                explain = self.res_word.prompt()  # 展示的提示词
                word = self.res_word.word()
                value = yb_operate_word(explain)
                if len(value) == 1:
                    for k in range(len(word)):
                        if word[k].text.lower() == value:
                            loc = self.base_page.get_element_location(word[k])
                            y2 = self.base_page.get_element_location(word[0])[1] - 40
                            self.res_word.button_swipe(loc[0], loc[1], loc[0], y2)
                            break
                else:
                    for z in range(len(value) - 1, -1, -1):  # 倒序
                        print(z, value[z])
                        for k in range(len(word)):
                            word2 = self.res_word.word()
                            if value[z] == word2[k].text and k != 0:
                                loc = self.base_page.get_element_location(word2[k])
                                y2 = self.base_page.get_element_location(word2[0])[1] - 40
                                self.res_word.button_swipe(loc[0], loc[1], loc[0], y2)
                                break

                answer.append(explain)
                self.res_word.click_voice()
                print('------------------')
                self.homework.next_button()

        return rate, answer

    @teststeps
    def check_answer_page(self, i, answer):
        """查看答案页面"""
        if ResultPage().wait_check_result_page() == '排行榜':
            print('点击查看答案按钮')
            ResultPage().check_result_button()
            print('判断是否滑动：', i)
            if int(i) <= 16:
                self.yb_operate()
            else:
                item = self.res_word.hint()
                if int(i) % len(item) == 0:
                    page = int(int(i) / len(item))
                else:
                    page = int(int(i) / len(item)) + 1
                print('页数:', page)
                for j in range(page):
                    last_one = self.yb_operate()  # 滑动前页面内最后一个小游戏title
                    self.res_word.screen_swipe_up(0.5, 0.75, 0.35, 1000)
                    item_2 = self.res_word.hint()  # 滑动后页面内的解释 的数量
                    if item_2[len(item_2) - 1].text == last_one:
                        print('到底啦', last_one)
                        self.res_word.back_up_button()
                        break
                    elif item_2[len(item_2) - 1].text == answer[len(answer) - 1]:
                        # 滑动后到底，因为普通情况下最多只有两页，滑动一次即可到底
                        print('滑动后到底', last_one)
                        k = []
                        for i in range(len(item_2) - 1, -1, -1):  # 倒序
                            if item_2[i].text == last_one:
                                k.append(i + 1)
                                break
                        self.yb_operate(k[0])
                        break
                    else:
                        continue
                self.res_word.screen_swipe_down(0.5, 0.35, 0.75, 1000)
                self.homework.back_up_button()
            time.sleep(2)

    @teststeps
    def yb_operate(self, index=0):
        """查看答案页面 -- 展示的解释内容验证"""
        explain = self.res_word.hint()
        word = self.res_word.answer()
        for i in range(index, len(explain)):
            key = word[i].text
            if key != 'ew':   # 'ew'为特例
                value = yb_operate_yb(key[0].lower())
            else:
                value = yb_operate_yb(key.lower())

            if explain[i].text == value:    # 如果无误，则点击听力按钮
                self.res_word.voice_button(i)  # 结果页 - 听力按钮
                print('听力按钮:', i)
            else:
                print('error', key, explain[i].text, value)
        return explain[len(explain) - 1].text


if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(Games('test_restore_word'))

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
