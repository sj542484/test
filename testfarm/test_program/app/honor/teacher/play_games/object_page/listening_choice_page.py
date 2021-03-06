#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import time
import random
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststeps, teststep
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class Listening(BasePage):
    """听后选择"""
    question_value = gv.PACKAGE_ID + "question"  # 题目

    def __init__(self):
        self.get = GetAttribute()
        self.swipe = SwipeFun()
        self.wait = WaitElement()
        self.result = ResultPage()


    @teststeps
    def wait_check_page(self):
        """以“title:听后选择”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'听后选择')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def exo_play(self):
        """播放按钮"""
        horn = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "exo_play")
        return horn

    @teststep
    def exo_pause(self):
        """暂停按钮"""
        horn = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "exo_pause")
        return horn

    @teststep
    def exo_progress(self):
        """播放 进度"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "exo_progress")
        return ele

    @teststep
    def exo_position(self):
        """播放 位置"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "exo_position")
        return ele

    @teststep
    def exo_duration(self):
        """音频长短"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "exo_duration")
        return ele

    @teststeps
    def red_tips(self):
        """上方红色提示"""
        try:
            self.driver.find_element_by_id(gv.PACKAGE_ID + "tv_hint")
            return True
        except:
            return False

    @teststeps
    def option_button(self, var):
        """选项"""
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]"
                                    "/following-sibling::android.view.ViewGroup/android.widget.LinearLayout"
                                    "/android.widget.LinearLayout/android.widget.TextView" % var)
        item = []
        content = []
        for i in range(0, len(ele), 2):
            item.append(ele[i])
            content.append(ele[i+1].text)
        return item, content

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "time").text
        return ele

    @teststep
    def options(self):
        """选项"""
        answer = self.driver\
            .find_elements_by_id(gv.PACKAGE_ID + "tv_char")
        return answer

    @teststep
    def option_item(self):
        """选项 内容"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID +"tv_item")
        return item

    @teststep
    def questions(self):
        """题目"""
        num = self.driver\
            .find_elements_by_id(self.question_value)
        return num

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1]

    @teststeps
    def get_first_num(self):
        """获取 当前页面第一个题号"""
        return self.questions()[0].text.split(".")[0]
    
    @teststep
    def question_judge(self, var):
        """元素 resource-id属性值是否为题目"""
        value = GetAttribute().resource_id(var)
        return True if value == self.question_value else False

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“rate”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_play")
        return self.wait.wait_check_element(locator)

    @teststeps
    def listen_choice_operation(self):
        """《听后选择》 游戏过程"""
        if self.wait_check_page():  # 页面检查
            if Homework().wait_check_play_page():
                hint = self.red_tips()  # 顶部红色提示信息
                if not hint:   # 检查是否有红色提示
                    print("----没有红色标识------")

                print('音频长度：', self.exo_duration().text)
                horn = self.exo_play()
                if not GetAttribute().enabled(horn):  # 播放按钮检查
                    print("★★★ Error- 播放按钮不可点击")
                else:
                    print("播放按钮可点击")
                    horn.click()
                    print('当前播放位置：', self.exo_position().text)
                    #
                    # horn = self.exo_pause()
                    # if GetAttribute().enabled(horn):  # 暂停按钮钮检查
                    #     print("★★★ Error- 喇暂停按钮可点击")
                    # else:
                    #     print("暂停按钮不可点击")

                    if self.red_tips() is False:  # 检查红色提示 是否消失
                        answer = []  # return值 与结果页内容比对
                        timestr = []  # 获取每小题的时间
                        rate = int(Homework().rate())  # 获取待完成数
                        print("作业个数：", rate)
                        self.swipe_operation(int(rate), timestr, answer)

                        while True:  # 由于下一步 按钮会在音频播放完成后可点击
                            if Homework().commit_button_judge('true'):
                                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                                Homework().commit_button_operation('true')  # 下一题 按钮 状态判断 加点击

                                if self.result.wait_check_result_page(5):  # 结果页检查点
                                    break
                                else:
                                    time.sleep(3)
                        print('==============================================')
                        return rate

    @teststeps
    def exo_pause_operation(self):
        """暂停按钮"""
        print('音频长度：', self.exo_duration().text)
        horn = self.exo_pause()  # 自动播放
        if not GetAttribute().enabled(horn):  # 暂停按钮钮检查
            print("★★★ Error- 出现错误：喇暂停按钮可点击")
        else:
            print("暂停按钮不可点击")

    @teststeps
    def exo_play_operation(self):
        """播音"""
        button = self.exo_play()  # 发音按钮
        if not GetAttribute().enabled(button):  # 播放按钮检查
            print("★★★ Error- 出现错误：播放按钮可点击")
        else:
            print("播放按钮不可点击")
        progress = self.exo_position().text
        print('当前播放位置：', progress)
        if int(progress) == 00000000:
            print('★★★ Error- 听力时间进度', int(progress))

    @teststeps
    def swipe_operation(self, swipe_num, timestr, answer):
        """滑屏 获取所有题目内容"""
        ques_last_index = 0  # 每个页面最后操作过的题号
        index = 0  # 每做一题加一

        if Homework().wait_check_play_page():
            rate = Homework().rate()  # 小题数
            for i in range(swipe_num):
                if ques_last_index < swipe_num:
                    ques = self.questions()  # 题目
                    ques_first_index = int(ques[0].text.split(".")[0])  # 页面中第一道题 题号

                    if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                        for step in range(0, 10):
                            self.swipe.swipe_vertical(0.5, 0.5, 0.62)
                            if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                                ques = self.questions()
                                break
                            elif int(self.get_first_num()) < ques_last_index + 1:  # 下拉拉过了
                                self.swipe.swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                                if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                                    ques = self.questions()
                                    break

                    last_one = self.get_last_element()  # 页面中最后一个元素

                    if self.question_judge(last_one):  # 判断最后一个元素为题目
                        for j in range(len(ques) - 1):
                            current_index = int(ques[j].text.split(".")[0])
                            if current_index > ques_last_index:
                                self.click_options(rate, index, ques[j].text, timestr, answer)
                                index += 1
                        ques_last_index = int(ques[- 2].text.split(".")[0])
                    else:  # 最后一个元素为选项
                        for k in range(len(ques)):
                            if k < len(ques) - 1:  # 前面的题目照常点击
                                current_index = int(ques[k].text.split(".")[0])
                                if current_index > ques_last_index:
                                    self.click_options(rate, index, ques[k].text, timestr, answer)
                                    index += 1
                                    if k == len(ques) - 2:
                                        ques_last_index = int(ques[-2].text.split(".")[0])
                            elif k == len(ques) - 1:  # 最后一个题目上滑一部分再进行选择
                                self.swipe.swipe_vertical(0.5, 0.76, 0.60)
                                ques = self.questions()
                                for z in range(len(ques)):
                                    current_index = int(ques[z].text.split(".")[0])
                                    if current_index > ques_last_index:
                                        self.click_options(rate, index, ques[z].text, timestr, answer)
                                        index += 1
                                        ques_last_index = int(ques[z].text.split(".")[0])
                                        break

                    if i != swipe_num - 1:
                        self.swipe.swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
                else:
                    break

    @teststeps
    def click_options(self, rate, i, questions, timestr, answer):
        """点击选项/判断rate及计时功能"""
        Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

        options = self.option_button(questions)  # 选项
        print(questions, '\n',
              '选项:', options[1])

        index = random.randint(0, len(options[0]) - 1)
        answer.append(options[1][index])
        options[0][index].click()

        timestr.append(self.time())  # 统计每小题的计时控件time信息
        print('-----------------------------------------')

    @teststeps
    def result_detail_page(self, rate):
        """《听后选择》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('查看答案:')
                    print('题数:', int(rate))
                    print('音频长度：', self.exo_duration().text)
                    horn = self.exo_play()
                    if not GetAttribute().enabled(horn):  # 播放按钮检查
                        print("出现错误：喇叭不可点-------")
                    else:
                        horn.click()  # 点击暂停按钮
                        # time.sleep(2)
                        # button = self.exo_pause()
                        # if not GetAttribute().enabled(button):  # 暂停按钮钮检查
                        #     print("出现错误：喇暂停按钮不可点击-------")
                        # else:
                        #     print("暂停按钮不可点击")

                        progress = self.exo_position().text
                        print('当前播放位置：', progress)
                        var = re.sub("\D", "", progress)
                        if int(var) == 0000:
                            print('★★★ Error- 听力时间进度', var)
                        elif var > re.sub("\D", "", self.exo_duration().text):
                            print('★★★ Error- 听力时间进度有误', var)

                    self.swipe_operation(int(rate))  # 具体操作

                    self.result.back_up_button()  # 返回结果页
            print('==============================================')

    @teststeps
    def study_again(self):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()[0].click()  # 结果页 错题再练/再练一遍 按钮

            self.listen_choice_operation()  # 游戏过程
