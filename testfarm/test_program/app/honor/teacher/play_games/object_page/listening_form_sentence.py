#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page import Homework
from app.honor.teacher.play_games.object_page import ResultPage
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class ListenFormSentence(BasePage):
    """听音连句"""
    correct_value = gv.PACKAGE_ID + "tv_right"  # 提交 按钮之后 答案页展示的答案

    def __init__(self):
        self.get = GetAttribute()
        self.result = ResultPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:听音连句”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'听音连句')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def voice_button(self):
        """发音按钮"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "play_voice").click()

    @teststeps
    def question(self):
        """题目内容"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "rich")
        return ele

    @teststeps
    def input_num(self):
        """获取 输入框 个数"""
        content = self.get.description(self.question())
        value = content.split('## ')

        count = len(value[1]) // 2
        return count

    @teststeps
    def option_button(self):
        """选项 单词
        :returns 元素、元素text
        """
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "text")

        item = [] # 单词元素
        content = []
        for i in range(len(ele)):
            if ele[i].text != '':
                item.append(ele[i])
                content.append(ele[i].text)
        print('选项：', content)
        return item, content

    @teststeps
    def clear_button(self):
        """页面内清除按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "clear")
        return ele

    # 点击 提交按钮之后 答案页展示的答案
    @teststeps
    def wait_check_correct_page(self):
        """以“正确答案”的ID为依据"""
        locator = (By.ID, self.correct_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def mine_answer(self):
        """获取 输入框 的结果"""
        content = self.get.description(self.question())
        value = content.split(' ')

        answer = []
        for i in range(2, len(value), 2):
            if value[1][i] != '':
                answer.append(value[i])  # 所有输入框值的列表
        print('answer:', answer)
        return answer

    @teststeps
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(self.correct_value).text
        return word

    @teststeps
    def explain(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_explain").text
        print('解释:', word)

    # 查看答案页面
    @teststeps
    def result_answer(self, index):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + 'tv_mine')[index].text
        return ele

    @teststeps
    def result_mine(self, index):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_mine")[index]
        value = self.get.selected(ele)
        return value

    @teststeps
    def listen_form_sentence(self):
        if self.wait_check_page():
            if Homework().wait_check_play_page():
                answer = []  # 我的答题结果
                timestr = []  # 获取每小题的时间

                self.voice_button()  # 发音按钮

                rate = Homework().rate()  # 获取待完成小题数
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

                    mine = []  # 我的答案
                    num = self.input_num()  # 待输入单词个数
                    for j in range(num):
                        Homework().commit_button_operation('false')  # 提交 按钮 状态判断 加点击

                        options = self.option_button()
                        index = random.randint(0, len(options[0])-1)
                        print(options[1][index])
                        options[0][index].click()
                        print('-----------------------')

                    mine.append(self.mine_answer())  # 输入的单词
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击

                    self.correct_page_operation(mine, i, rate, timestr, answer)  # 答案页面

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                final_time = ResultPage().get_time(timestr[len(timestr) - 1])  # 最后一个小题的时间
                print('===============================================')
                return rate, answer, final_time

    @teststeps
    def correct_page_operation(self, content, i, rate, timestr, answer):
        """点击提交按钮后的答案页面
        :param content: 我选择的答案
        :param i: 第X小题
        :param answer: 作对的题
        """
        if self.wait_check_correct_page():
            print('----------------------')
            result = content[- 1]
            print('我的答案:', result)
            mine = self.mine_answer()  # 为答案页面展示的 我的答题结果
            print('我的答题结果:', mine)

            correct = self.correct()  # 正确答案
            self.explain()  # 解释
            if len(mine) <= len(correct):  # 输入少于或等于单词字母数的字符
                if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('★★★ Error - 字符数少于或等于时:', mine.lower(), result.lower())
            else:  # 输入过多的字符
                if correct + mine[len(correct):].lower() != correct + result[
                                                                      len(correct):].lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('★★★ Error - 字符输入过多时:', correct + mine[len(correct):].lower(),
                          correct + result[len(correct):].lower())

            var = 0
            for k in range(len(correct)):  # 测试 答案判断是否正确
                if result[k] not in correct:
                    var += 1
                    break

            if var != 0:
                answer.append(mine[0])
            self.click_voice_operation(i)  # 点击发音按钮 操作

            Homework().rate_judge(rate, i - 1)  # 测试当前rate值显示是否正确
            timestr.append(Homework().time())  # 统计每小题的计时控件time信息
            print('---------------------------')
            Homework().next_button_operation('true')  # 下一题 按钮 状态判断 加点击

    @teststeps
    def click_voice_operation(self, i):
        """点击发音按钮 操作
        :param i: 第X小题
        """
        if i == 1:  # 第2题
            j = 0
            print('多次点击发音按钮:')
            while j < 4:
                print(j)
                self.voice_button()  # 多次点击发音按钮
                j += 1
            time.sleep(1)
        else:
            self.voice_button()  # 点击 发音按钮
        print('--------')

    @teststeps
    def check_detail_page(self, rate):
        """查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('======================================')
                print('查看答案:')
                print('题数:', int(rate))
                for i in range(0, int(rate)):
                    print(self.correct()[i].text)  # 答案
                    print(self.result_answer(i))  # 我的
                    print(self.explain(i))  # 解释
                    print('对错标识:', self.result_mine(i))  # 对错标识
                    print('-----------------------------------')
                    self.voice_button(i)  # 点击发音按钮

                self.result.back_up_button()  # 返回结果页
            print('==============================================')

    @teststeps
    def study_again(self, tpe):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()

            result = self.listen_form_sentence(tpe)  # 不同模式 对应不同的游戏过程
            return item[1], result
