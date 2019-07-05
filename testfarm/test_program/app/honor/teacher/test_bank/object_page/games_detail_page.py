#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
import re
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.judge_character_type import JudgeType
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class GamesPage(BasePage):
    """游戏 详情页面"""
    game_title_value = gv.PACKAGE_ID + "title"  # 游戏名
    question_index_value = gv.PACKAGE_ID + "index"  # 题号
    speak_button_value = gv.PACKAGE_ID + "iv_speak"  # 听力按钮
    question_value = gv.PACKAGE_ID + "question"  # 题目
    hint_word_value = gv.PACKAGE_ID + "hint"  # 选词填空的提示词
    voice_button_value = gv.PACKAGE_ID + "iv_play"  # 听音选择 播音按钮

    def __init__(self):
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=20):
        """以“title:详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'详情')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self, var=20):
        """以“游戏title”为依据"""
        locator = (By.ID, self.game_title_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def recommend_button(self):
        """推荐到学校 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "recommend") \
            .click()
        time.sleep(2)

    @teststep
    def collect_button(self):
        """收藏/取消收藏 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "collect") \
            .click()
        time.sleep(1)

    @teststep
    def put_to_basket_button(self):
        """加入题筐 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "add_pool") \
            .click()

    @teststep
    def start_button(self):
        """开始答题"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "demo").click()

    @teststep
    def game_title(self):
        """游戏title"""
        item = self.driver \
            .find_element_by_id(self.game_title_value)
        print(item.text)
        return item.text

    @teststep
    def game_info(self):
        """游戏 具体信息"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "info") \
            .text
        return item

    @teststeps
    def game_num(self):
        """获取游戏数量"""
        ele = self.game_info().split()

        if len(ele) == 2:
            num = re.sub("\D", "", ele[0])  # 共5题    2018-02-28
        else:
            num = re.sub("\D", "", ele[1])  # 自定义模式    共8题    2018-02-28
        return int(num)

    @teststeps
    def teacher_nickname(self):
        """老师昵称"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "name") \
            .text
        print(item)
        print('--------------------')
        return item

    #
    @teststep
    def question_index(self):
        """题号"""
        item = self.driver \
            .find_elements_by_id(self.question_index_value)
        return item

    @teststeps
    def verify_question_index(self):
        """验证  题号是否存在"""
        return self.wait.judge_is_exists(self.question_index_value)

    @teststep
    def word(self):
        """单词"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "word")
        return item

    @teststep
    def remove(self):
        """去除"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "remove")
        return item

    @teststep
    def explain(self):
        """解释"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "explain")
        return item

    @teststep
    def sentence(self):
        """句子"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_answer")
        return item

    @teststep
    def hint(self):
        """句子- 解释"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_hint")
        return item

    @teststep
    def speak_button(self, index):
        """听力按钮"""
        self.driver \
            .find_elements_by_id(self.speak_button_value)[index] \
            .click()

    @teststep
    def verify_speak_button(self):
        """验证 听力按钮 是否存在"""
        try:
            self.driver.find_element_by_id(self.speak_button_value)
            return True
        except Exception:
            return False

    # 单选
    @teststeps
    def verify_voice_button(self):
        """验证 听音选择的 播音按钮 是否存在"""
        try:
            self.driver.find_element_by_id(self.voice_button_value)
            return True
        except Exception:
            return False

    @teststep
    def play_button(self):
        """听音选择的 播音按钮"""
        self.driver \
            .find_element_by_id(self.voice_button_value)\
            .click()

    # 文章类题 补全文章/阅读理解
    @teststeps
    def verify_content_text(self):
        """验证 阅读理解/完形填空的文章 是否存在"""
        try:
            self.driver.find_element_by_id(gv.PACKAGE_ID + "content")
            return True
        except Exception:
            return False

    @teststep
    def article_content(self):
        """阅读理解/完形填空的文章"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "content").text
        print(item)
        print('-----------------------------------')

    @teststep
    def single_question(self):
        """题目"""
        item = self.driver \
            .find_elements_by_id(self.question_value)
        return item

    @teststep
    def option_char(self):
        """选项 ABCD"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_char")
        return item

    @teststep
    def option_item(self):
        """选项 内容"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_item")
        return item

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1]

    @teststeps
    def option_button(self):
        """选项"""
        ele = self.driver \
            .find_elements_by_xpath(
                "//android.widget.TextView[contains(@resource-id,'%s')]"
                "/following-sibling::*/android.widget.LinearLayout"
                "/android.widget.LinearLayout/android.widget.TextView" % self.question_value)

        item = []  # 当前页面中所有题目的选项
        var = []  # 所有题目的正确选项
        rate = []  # 百分数值
        count = []  # text为A的元素index

        for i in range(0, len(ele), 2):
            if ele[i].text == 'A':
                count.append(i)
        count.append(len(ele))  # 多余 只为最后一题

        for i in range(len(count)-1):
            options = []  # 每个题目的选项
            for j in range(count[i], count[i+1], 2):
                if j+1 == count[-1] and (j+1) % 2 != 0:  # len(ele)为奇数 去掉
                    break

                options.append(ele[j+1].text)
                if GetAttribute().selected(ele[j]) == 'true':
                    rate.append(ele[j+1].text)
                    var.append(ele[j+1])
            item.append(options)

        return item, var, rate

    @teststep
    def verify_options(self):
        """验证 选项 ABCD 是否存在"""
        try:
            self.driver.find_element_by_id(gv.PACKAGE_ID + "tv_char")
            return True
        except Exception:
            return False

    @teststeps
    def verify_hint_word(self):
        """验证 选词填空的wording: 提示词 补全文章 是否存在"""
        try:
            self.driver.find_element_by_id(self.hint_word_value)
            return True
        except Exception:
            return False

    @teststep
    def hint_word(self):
        """wording: 提示词"""
        item = self.driver \
            .find_element_by_id(self.hint_word_value).text
        print(item)

    @teststep
    def prompt_word(self):
        """提示的单词"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "prompt").text
        print(item)
        print('-----------------------------------')

    @teststep
    def question_judge(self, var):
        """元素 resource-id属性值是否为题目"""
        value = GetAttribute().resource_id(var)
        if value == self.question_value:
            return True
        else:
            return False

    # 听音选图
    @teststep
    def verify_img(self):
        """验证 img 是否存在"""
        locator = (By.ID, gv.PACKAGE_ID + "img")
        return self.wait.judge_is_exists(locator)

    @teststeps
    def img_option(self):
        """选项"""
        ele = self.driver.find_elements_by_xpath(
                            "//android.widget.TextView[contains(@resource-id,'%s')]"
                            "/following-sibling::*/android.widget.LinearLayout"
                            "/android.widget.LinearLayout/android.widget.TextView" % self.question_value)

        item = []  # 当前页面中所有题目的选项
        var = []  # 所有题目的正确选项
        rate = []  # 百分数值
        count = []  # text为A的元素index

        for i in range(0, len(ele), 2):
            if ele[i].text == 'A':
                count.append(i)
        count.append(len(ele))  # 多余 只为最后一题

        for i in range(len(count) - 1):
            options = []  # 每个题目的选项
            for j in range(count[i], count[i + 1], 2):
                if j + 1 == count[-1] and (j + 1) % 2 != 0:  # len(ele)为奇数 去掉
                    break

                options.append(ele[j + 1].text)
                if GetAttribute().selected(ele[j]) == 'true':
                    rate.append(ele[j + 1].text)
                    var.append(ele[j + 1])
            item.append(options)

        return item, var, rate

    @teststeps
    def get_num(self, var=0):
        """获取 当前页面中第一题 题号"""
        item = self.single_question()[var].text.split(".")
        if JudgeType().is_number(item[0]):  # 判断是否是数字 -- 题号
            return int(item[0])
        else:
            # print('★★★ Error -该题目没有题号:', item)
            return 0

    @teststeps
    def swipe_operation(self, swipe_num):
        """滑屏 获取所有题目内容"""
        """滑屏 获取所有题目内容"""
        ques_last_index = 0

        for i in range(swipe_num):
            if ques_last_index < swipe_num:
                ques_first_index = self.get_num()  # 当前页面中第一题 题号

                if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                    for step in range(0, 10):
                        self.swipe.swipe_vertical(0.5, 0.5, 0.62)
                        if self.get_num() == ques_last_index + 1:  # 正好
                            break
                        elif self.get_num() < ques_last_index + 1:  # 下拉拉过了
                            self.swipe.swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                            if self.get_num() == ques_last_index + 1:  # 正好
                                break

                last_one = self.get_last_element()  # 页面最后一个元素
                ques_num = self.single_question()  # 题目

                if self.question_judge(last_one):  # 判断最后一项是否为题目
                    for j in range(len(ques_num) - 1):
                        current_index = self.get_num(j)  # 当前页面中题号

                        if current_index > ques_last_index:
                            print('-----------------------------')
                            print(ques_num[j].text)
                            options = self.option_button()  # 选项
                            print('选项:', options[0][j])
                            ques_last_index = self.get_num(j)  # 当前页面中 做过的最后一题 题号
                else:  # 判断最后一题是否为选项
                    for k in range(len(ques_num)):
                        if k < len(ques_num) - 1:  # 前面的题目照常点击
                            current_index = self.get_num(k)  # 当前页面中题号

                            if current_index > ques_last_index:
                                print('-----------------------------')
                                print(ques_num[k].text)
                                options = self.option_button()  # 选项
                                print('选项:', options[0][k])
                                ques_last_index = self.get_num(k)  # 当前页面中 做过的最后一题 题号
                        elif k == len(ques_num) - 1:  # 最后一个题目上滑一部分再进行选择
                            self.swipe.swipe_vertical(0.5, 0.8, 0.55)
                            ques_num = self.single_question()  # 题目
                            for z in range(len(ques_num)):
                                current_index = self.get_num(z)  # 当前页面中题号

                                if current_index > ques_last_index:
                                    print('-----------------------------')
                                    print(ques_num[z].text)
                                    options = self.option_button()  # 选项
                                    print('选项:', options[0][z])
                                    ques_last_index = self.get_num(z)  # 当前页面中 做过的最后一题 题号
                                    break

                if i != swipe_num - 1:
                    self.swipe.swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
            else:
                break