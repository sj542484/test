#!/usr/bin/env python3
# code:UTF-8
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
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
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "play_voice")
        return ele

    @teststeps
    def question(self):
        """题目内容"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "rich_text")
        return ele

    @teststeps
    def input_num(self):
        """获取 输入框 个数"""
        content = self.get.description(self.question())

        count_sp = 0
        for k in content[6:]:  # 去掉 ‘86 ## ’
            if k.isspace():
                count_sp += 1

        count = count_sp // 6
        return count

    @teststeps
    def option_button(self):
        """选项 单词
        :returns 元素、元素text
        """
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "text")

        content = {}  # 索引值: 单词元素,单词text
        for i in range(len(ele)):
            if ele[i].text != '':
                content.setdefault(i, []).append(ele[i])
                content.setdefault(i, []).append(ele[i].text)

        return content

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
        var = self.get.description(self.question())
        content = ' '.join(var.split())  # 删除字符串中的连续空格只保留一个
        value = content[6:].split(' ')  # answer

        answer = []
        for i in range(len(value)):
            if value[i] != '':
                answer.append(value[i])  # 所有输入框值的列表
        print('我的答题结果:', answer)
        return answer

    @teststeps
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_elements_by_id(self.correct_value)
        return word

    @teststeps
    def explain(self):
        """展示的翻译"""
        word = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_explain")
        return word

    # 查看答案页面
    @teststeps
    def result_answer(self):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + 'tv_mine')
        return ele

    @teststeps
    def result_mine(self):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_mine")
        return ele

    @teststeps
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_speak")[index] \
            .click()

    @teststeps
    def listen_form_sentence(self):
        """听音连句 具体操作过程"""
        if self.wait_check_page():
            if Homework().wait_check_play_page():
                answer = []  # 我的答题结果
                timestr = []  # 获取每小题的时间

                self.voice_button().click()  # 发音按钮

                rate = Homework().rate()  # 获取待完成小题数
                for i in range(int(rate)):
                    print('========================================')
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

                    num = self.input_num()  # 待输入单词个数
                    print('待输入单词个数：', num)
                    for j in range(num):
                        options = self.option_button()
                        keys = self.clear_repeat(options.keys())
                        index = random.choice(keys)
                        print('选择：', options[index][1], index)

                        if j == num - 1:
                            Homework().commit_button_operation('false')  # 提交 按钮 状态判断 加点击

                        options[index][0].click()
                        print('-----------------------')
                        time.sleep(1)
                    mine = self.mine_answer()
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击

                    self.correct_page_operation(mine, i, timestr, answer)  # 答案页面

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                final_time = self.result.get_time(timestr[len(timestr) - 1])  # 最后一个小题的时间
                print('=========================================================')
                return rate, answer, final_time

    @teststeps
    def correct_page_operation(self, result, i, timestr, answer):
        """点击提交按钮后的答案页面
        :param result: 我选择的答案
        :param i: 第X小题
        :param timestr:统计每小题的计时控件time信息
        :param answer: 作对的题
        """
        if self.wait_check_correct_page():
            print('----------------------')
            mine = self.mine_answer()  # 为答案页面展示的 我的答题结果

            item = self.correct()[0].text
            correct = list(item[5:].split())  # 正确答案
            print('解释:', self.explain()[0].text)  # 解释
            if len(mine) < len(correct):  # 输入少于单词字母数的字符
                print('★★★ Error - 字符数少:', len(mine), len(correct), mine, correct)
            else:
                var = 0
                for k in range(len(correct)):  # 测试 答案判断是否正确
                    if result[k] != correct[k]:
                        var += 1
                        break

                if var != 0:
                    answer.append(mine[0])

            self.click_voice_operation(i)  # 点击发音按钮 操作

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
                self.voice_button().click()  # 多次点击发音按钮
                j += 1
            time.sleep(1)
        else:
            self.voice_button().click()  # 点击 发音按钮
        print('--------')

    @teststeps
    def clear_repeat(self, repeat_list):
        """dict_keys转化为list"""
        new_dict = {}
        after_deal = new_dict.fromkeys(repeat_list).keys()
        return list(after_deal)

    @teststeps
    def check_detail_page(self, result):
        """查看答案 操作过程
        :param result: 答题结果
        """
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('======================================')
                print('查看答案:')
                self.answer_explain_type(result)

                self.result.back_up_button()  # 返回结果页
            print('==============================================')

    @teststeps
    def answer_explain_type(self, result, content=None):
        """答案/解释类型
        :param result: 答题结果
        :param content: 翻页
        """
        if content is None:
            content = []

        if self.result.wait_check_detail_page():
            hint = self.explain()  # 解释
            if len(hint) > 4 and not content:
                self.listen_ergodic_list(result, len(hint) - 1)
                content = [hint[-2].text]

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.answer_explain_type(result, content)
            else:
                var = 0
                if content:
                    for k in range(len(hint)):
                        if content[0] == hint[k].text:
                            var += k + 1
                            break

                self.listen_ergodic_list(result, len(hint), var)

    @teststeps
    def listen_ergodic_list(self, result, length, var=0):
        """听音连句 遍历列表
        :param result :答题结果
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        answer = self.correct()  # 答案
        mine = self.result_answer()  # 我的
        explain = self.explain()  # 解释
        status = self.result_mine()    # 对错标识

        for i in range(var, length):
            print(explain[i].text, '\n', mine[i].text, '\n', answer[i].text)
            if mine[i].text != result[i]:
                print('★★★ Error- 我的答题结果与游戏过程中不一致', mine[i].text, result[i])
            else:
                mode = GetAttribute().selected(status[i])
                if answer[i].text[3:] != mine[i].text[3:]:  # 答错
                    if mode != 'false':
                        print('★★★ Error- 对错标识 与 答题结果不一致', mode)
                else:
                    if mode != 'true':
                        print('★★★ Error- 对错标识 与 答题结果不一致', mode)

                print('-----------------------------------------')
                self.result_voice(i)  # 点击发音按钮

    @teststeps
    def study_again(self):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()

            result = self.listen_form_sentence()  # 不同模式 对应不同的游戏过程
            return item[1], result
