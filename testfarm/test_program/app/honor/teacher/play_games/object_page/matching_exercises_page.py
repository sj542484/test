#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.play_games.object_page.homework_page import Homework
from testfarm.test_program.app.honor.teacher.play_games.object_page.result_page import ResultPage
from testfarm.test_program.app.honor.teacher.play_games.test_data.matching_exercise_data import match_operation
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.judge_character_type import JudgeType
from testfarm.test_program.utils.wait_element import WaitElement


class MatchingExercises(BasePage):
    """连连看"""
    def __init__(self):
        self.result = ResultPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:连连看”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'连连看')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def word(self):
        """展示的Word"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele

    # 以下为答案详情页面元素
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_answer")
        return self.wait.wait_check_element(locator)

    @teststep
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "iv_speak")[index] \
            .click()

    @teststep
    def result_answer(self, index):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "tv_answer")[index].text
        return ele

    @teststep
    def result_explain(self, index):
        """解释"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "tv_hint")[index].text
        return ele

    @teststep
    def result_mine(self, index):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "iv_mine")[index]
        value = GetAttribute().selected(ele)
        return value

    @teststeps
    def match_exercise(self):
        """《连连看》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = {} # 答题结果
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()

                if int(rate) % 5 == 0:
                    page = int(int(rate)/5)
                else:
                    page = int(int(rate) / 5) + 1
                print('页数:', page)

                for j in range(page):  # 然后在不同页面做对应的题目
                    print('第%s页：' % (j+1))
                    word = []  # 单词list
                    word_index = []  # 单词在所有button中的索引
                    explain = []  # 解释list
                    explain_index = []   # 解释在所有button中的索引

                    ele = self.word()  # 所有button
                    for i in range(3, len(ele)):
                        if JudgeType().is_alphabet(ele[i].text[0]):  # 如果是字母
                            word.append(ele[i].text)
                            word_index.append(i)
                        else:  # 如果是汉字
                            explain.append(ele[i].text)
                            explain_index.append(i)

                    for k in range(len(word)):  # 具体操作
                        Homework().rate_judge(rate, k+j*4)  # 测试当前rate值显示是否正确

                        value = match_operation(word[k])  # 数据字典
                        ele[word_index[k]].click()  # 点击解释
                        for z in range(len(explain)):
                            if explain[z] == value:
                                timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                                answer[word[k]] = explain[z]
                                ele[explain_index[z]].click()  # 点击对应word

                                if j ==0 and k == 0:  # 测试 配对成功后，不可再次点击
                                    ele[word_index[k]].click()
                                print('--------------------------')
                                break
                    time.sleep(1)
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('=================================')
                return rate, answer

    @teststeps
    def result_detail_page(self, rate):
        """《连连看》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('==============================================')
                    print('查看答案:')
                    self.error_sum(rate)
            else:
                print('★★★ Error - 未进入查看答案页面')

    @teststeps
    def error_sum(self, rate):
        """查看答案 - 点击答错的题 对应的 听力按钮"""
        print('题数:', int(rate))
        print('-----------------------------------')
        for i in range(0, int(rate)):
            print('解释:', self.result_explain(i))  # 解释
            print('单词:', self.result_answer(i))  # 正确word
            mine = self.result_mine(i)  # 对错标识
            if mine != 'true':
                print('★★★ Error - 对错标识')
            else:
                print('对错标识:', mine)
            print('-----------------------------------')

            self.result_voice(i)  # 点击发音按钮

        if self.wait_check_detail_page():
            self.result.back_up_button()  # 返回结果页

    @teststeps
    def study_again(self):
        """再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            print('==============================================')
            self.result.again_button()[0].click()  # 结果页 错题再练/再练一遍 按钮
            result = self.match_exercise()  # 游戏过程
            return result
