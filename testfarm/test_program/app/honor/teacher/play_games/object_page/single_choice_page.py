#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page import Homework
from app.honor.teacher.play_games.object_page import ResultPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class SingleChoice(BasePage):
    """单项选择"""
    def __init__(self):
        self.result = ResultPage()
        self.game = GamesPage()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:单项选择”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单项选择')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def question_content(self):
        """获取题目内容"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "question").text
        return ele

    @teststep
    def option_button(self):
        """获取所有选项 - 四个选项"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_char")
        return ele

    @teststeps
    def option_selected(self):
        """获取所有选项 - 选项selected属性"""
        time.sleep(1)
        ele = self.option_button()

        value = []  # 四个选项selected属性值为true的个数
        for j in range(len(ele)):  # 统计答案正确与否
            if  GetAttribute().selected(ele[j]) == 'true':
                value.append(j)
                value.append(GetAttribute().description(ele[j]))
        return value

    @teststep
    def option_content(self, index):
        """获取所有选项 - 四个选项内容"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_item")[index].text
        return ele

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_answer")
        return self.wait.wait_check_element(locator)

    @teststeps
    def single_choice_operation(self):
        """《单项选择》 游戏过程   返回当前大题的题数，正确题目内容， 最终完成时间"""
        if self.wait_check_page():
            if Homework().wait_check_play_page():
                timestr = []  # 获取每小题的时间
                questions = []  # 答对的题
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operation('false')  # 下一题 按钮 判断加 点击操作

                    item = self.question_content()  # 题目
                    print('题目:', item)
                    options = self.option_button()  # 四个选项
                    options[random.randint(0, len(options)-1)].click()  # 随机点击选项

                    var = self.option_selected()  # 统计答案正确与否
                    if len(var) == 2:  # 如果选项的selected属性为true的作业数为1,说明答对了，则+1
                        print('回答正确:', self.option_content(var[0]))
                        questions.append(self.question_content())
                    else:
                        if var[1] == 'error':
                            print('回答错误:%s;   正确答案:%s'%(self.option_content(var[0]),self.option_content(var[2])))
                        else:
                            print('回答错误:%s;   正确答案:%s'%(self.option_content(var[2]),self.option_content(var[0])))

                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    Homework().next_button_operation('true')  # 下一题 按钮 状态判断 加点击
                    print('--------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                final_time = self.result.get_time(timestr[-1])  # 最后一个小题的时间
                print('===============================================')
                return rate, questions, final_time

    @teststeps
    def check_detail_page(self, count):
        """《单项选择》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('查看答案页面:')
                self.swipe_operation(int(count))  # 单选题 滑屏及具体操作
                self.result.back_up_button()  # 返回结果页

    @teststeps
    def study_again(self):
        """《单项选择》 错题再练/再练一遍 操作过程"""
        print('===============================================')
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()
            result = self.single_choice_operation()  # 单项选择 - 游戏过程
            return item[1], result

    @teststeps
    def swipe_operation(self, swipe_num):
        """滑屏 获取所有题目内容"""
        ques_last_index = 0

        for i in range(swipe_num):
            if ques_last_index < swipe_num:
                ques_first_index = self.game.get_num()  # 当前页面中第一题 题号

                if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                    for step in range(0, 10):
                        self.swipe.swipe_vertical(0.5, 0.5, 0.62)
                        if self.game.get_num() == ques_last_index + 1:  # 正好
                            break
                        elif self.game.get_num() < ques_last_index + 1:  # 下拉拉过了
                            self.swipe.swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                            if self.game.get_num() == ques_last_index + 1:  # 正好
                                break

                last_one = self.game.get_last_element()  # 页面最后一个元素
                ques_num = self.game.single_question()  # 题目

                if self.game.question_judge(last_one):  # 判断最后一项是否为题目
                    for j in range(len(ques_num) - 1):
                        current_index = self.game.get_num(j)  # 当前页面中题号

                        if current_index > ques_last_index or (current_index == 0 and ques_last_index != 0):  # 判断当前题号是否是已完成的；以及题目无题号时
                            print('-----------------------------')
                            print(ques_num[j].text)
                            options = self.option_button()  # 选项
                            print('选项:', options[j].text)
                            ques_last_index = self.game.get_num(j)  # 当前页面中 做过的最后一题 题号
                else:  # 判断最后一题是否为选项
                    for k in range(len(ques_num)):
                        if k < len(ques_num) - 1:  # 前面的题目照常点击
                            current_index = self.game.get_num(k)  # 当前页面中题号

                            if current_index > ques_last_index or (current_index == 0 and ques_last_index != 0):
                                print('-----------------------------')
                                print(ques_num[k].text)
                                options = self.option_button()  # 选项
                                print('选项:', options[k].text)
                                ques_last_index = self.game.get_num(k)  # 当前页面中 做过的最后一题 题号
                        elif k == len(ques_num) - 1:  # 最后一个题目上滑一部分再进行选择
                            self.swipe.swipe_vertical(0.5, 0.8, 0.55)
                            ques_num = self.game.single_question()  # 题目
                            for z in range(len(ques_num)):
                                current_index = self.game.get_num(z)  # 当前页面中题号

                                if current_index > ques_last_index or (current_index == 0 and ques_last_index != 0):
                                    print('-----------------------------')
                                    print(ques_num[z].text)
                                    options = self.option_button()  # 选项
                                    print('选项:', options[z].text)
                                    ques_last_index = self.game.get_num(z)  # 当前页面中 做过的最后一题 题号
                                    break

                if i != swipe_num - 1:
                    self.swipe.swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
            else:
                break
