#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import time
import re
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page import Homework
from app.honor.teacher.play_games.object_page import ResultPage
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class PictureDictation(BasePage):
    """听音选图"""
    def __init__(self):
        self.result = ResultPage()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:听音选图”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'听音选图')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def img_options(self):
        """展示的图片"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "img")
        return ele

    @teststeps
    def sentence(self):
        """展示的句子 点击喇叭听写单词"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "sentence").text
        return ele

    # 以下为答案详情页面元素
    @teststeps
    def wait_check_detail_page(self):
        """以“progress”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID+ "tv_progress")
        return self.wait.wait_check_element(locator)

    @teststep
    def result_voice(self):
        """语音按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "iv_play") \
            .click()

    @teststep
    def result_progress(self):
        """进度"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_progress").text
        return ele

    @teststep
    def result_sentence(self):
        """句子"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "text")
        return ele

    @teststep
    def result_img(self):
        """图片 选项"""
        ele = self.driver \
            .find_elements_by_xpath("//android.support.v7.widget.RecyclerView/*")  # 包括 句子+选项

        count = []  # 
        option = []  # 
        for i in range(len(ele)):
            if GetAttribute().class_name(ele[i]) == 'android.widget.LinearLayout':
                count.append(i)

        count.append(len(ele))
        for j in range(len(count)-1):
            option.append(count[j+1]-count[j]-1)
        return option

    @teststeps
    def get_first_num(self):
        """获取 当前页面第一个题号"""
        item = self.result_sentence()[0].text.split(".")[0]
        return item

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1].text

    @teststep
    def question_judge(self, var):
        """页面中最后一个题目是否有选项"""
        ele = self.driver.find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]/"
                                                 "parent::android.widget.LinearLayout/"
                                                 "following-sibling::android.widget.RelativeLayout" % var)

        if len(ele) == 0:
            return True
        else:
            return False

    @teststeps
    def picture_dictation(self):
        """《听音选图》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

                    question = self.sentence()  # 句子
                    print(i+1, '.', question)

                    options = self.img_options()  # 图片选项
                    print('选项:', len(options))
                    if i == int(rate)-1:
                        self.swipe.swipe_vertical(0.1, 0.5, 0.9)  # 向右滑屏进入上一题
                        self.swipe.swipe_vertical(0.9, 0.5, 0.1)  # 返回最后一题

                    index = random.randint(0, len(options)) - 1
                    answer.append(options[index])
                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    options[index].click()
                    print('---------------------------------------')
                    time.sleep(3)

                while True:
                    if Homework().commit_button_judge('true'):
                        Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                        Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击
                        if Toast().find_toast('请听完音频，再提交答案', 3):
                            print('请听完音频，再提交答案')
                        break
                    else:
                        time.sleep(3)
                print('==============================================')
                return rate, answer

    @teststeps
    def result_detail_page(self, rate):
        """《听音选图》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('查看答案:')
                    print('题数:', int(rate))
                    self.result_voice()  # 点击发音按钮

                    self.swipe_operation(int(rate))  # 具体操作

                    progress = re.sub("\D", "", self.result_progress())  # 时间进度
                    if int(progress) == 00000000:
                        print('★★★ Error- 听力时间进度', int(progress))
                    self.result.back_up_button()  # 返回结果页
            print('==============================================')

    @teststeps
    def swipe_operation(self, rate):
        """查看答案 滑屏 获取所有题目内容"""
        ques_last_index = 0  # 每个页面最后操作过的题号

        for i in range(rate):
            question = self.result_sentence()  # 句子
            ques_first_index = int(question[0].text.split(".")[0])

            if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                for step in range(0, 10):
                    self.swipe.swipe_vertical(0.5, 0.5, 0.62)
                    if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                        question = self.result_sentence()
                        break
                    elif int(self.get_first_num()) < ques_last_index + 1:  # 下拉拉过了
                        self.swipe.swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                        if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                            question = self.result_sentence()
                            break

            last_one = self.get_last_element()  # 最后一个题目

            if int(rate) == ques_last_index:  # 最后一题
                break
            else:
                if self.question_judge(last_one):  # 判断最后一项为题目
                    options = self.result_img()  # 选项
                    for j in range(len(question) - 1):
                        print('-----------------------------')
                        current_index = int(question[j].text.split(".")[0])
                        if current_index > ques_last_index:
                            print(question[j].text)
                            print('选项:', options[j])
                    ques_last_index = int(question[- 2].text.split(".")[0])
                else:  # 判断最后一题为选项
                    options = self.result_img()  # 选项
                    for k in range(len(question)):
                        print('-----------------------------')
                        if k < len(question) - 1:  # 前面的题目照常点击
                            current_index = int(question[k].text.split(".")[0])
                            if current_index > ques_last_index:
                                print(question[k].text)
                                print('选项:', options[k])
                                if k == len(question) - 2:
                                    ques_last_index = int(question[-2].text.split(".")[0])
                        elif k == len(question) - 1:  # 最后一个题目上滑一部分再进行选择
                            self.swipe.swipe_vertical(0.5, 0.7, 0.4)
                            question = self.result_sentence()
                            options = self.result_img()  # 选项
                            for z in range(len(question)):
                                current_index = int(question[z].text.split(".")[0])
                                if current_index > ques_last_index:
                                    print(question[z].text)
                                    print('选项:', options[z])
                                    ques_last_index = int(question[z].text.split(".")[0])
                                    break

                if i != rate - 1:
                    self.swipe.swipe_vertical(0.5, 0.9, 0.27)  # 滑屏

    @teststeps
    def study_again(self):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()[0].click()  # 结果页 错题再练/再练一遍 按钮
            self.picture_dictation()  # 游戏过程
