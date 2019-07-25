#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
import re
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.judge_character_type import JudgeType
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class GamesPage(BasePage):
    """游戏 详情页面"""
    game_title_value = gv.PACKAGE_ID + "title"  # 游戏名
    question_index_value = gv.PACKAGE_ID + "index"  # 题号
    speak_button_value = gv.PACKAGE_ID + "iv_speak"  # 听力按钮
    question_value = gv.PACKAGE_ID + "question"  # 题目
    hint_word_value = gv.PACKAGE_ID + "hint"  # 选词填空的提示词
    voice_button_value = gv.PACKAGE_ID + "iv_play"  # 听音选择 播音按钮
    article_content_value = gv.PACKAGE_ID + "rich"  # 补全文章 文章元素
    content_value = gv.PACKAGE_ID + "cl_content"  # 阅读理解 文章元素
    char_value = gv.PACKAGE_ID + "tv_char"  # 选项 ABCD

    def __init__(self):
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=10):
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

    # #
    # @teststep
    # def question_index(self):
    #     """题号"""
    #     item = self.driver \
    #         .find_elements_by_id(self.question_index_value)
    #     return item
    #
    # @teststeps
    # def verify_question_index(self):
    #     """验证  题号是否存在"""
    #     locator = (By.ID, self.question_index_value)
    #     return self.wait.judge_is_exists(locator)

    @teststep
    def word(self):
        """单词"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "word")
        return item

    @teststep
    def remove_type(self):
        """去除 类型"""
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

    @teststeps
    def verify_speak_button(self):
        """验证 听力按钮 是否存在"""
        locator = (By.ID, self.speak_button_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def speak_button(self, index):
        """听力按钮"""
        self.driver \
            .find_elements_by_id(self.speak_button_value)[index] \
            .click()

    # 听音连句
    @teststep
    def obstruct(self):
        """干扰内容"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_obstruct")
        return item

    # 单选
    @teststeps
    def verify_voice_button(self):
        """验证 听音选择的 播音按钮 是否存在"""
        locator = (By.ID, self.voice_button_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def play_button(self):
        """听音选择的 播音按钮"""
        self.driver \
            .find_element_by_id(self.voice_button_value)\
            .click()

    # 文章类题 补全文章/阅读理解
    @teststeps
    def verify_article_content_text(self):
        """验证 补全文章的文章 是否存在"""
        locator = (By.ID, self.article_content_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def article_content(self):
        """补全文章的文章"""
        item = self.driver \
            .find_element_by_id(self.article_content_value).text
        print(item)
        print('-----------------------------------')

    @teststeps
    def verify_content_text(self):
        """验证 阅读理解的文章 是否存在"""
        locator = (By.ID, self.content_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def content(self):
        """阅读理解的文章"""
        item = self.driver \
            .find_element_by_id(self.content_value).text
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
            .find_elements_by_id(self.char_value)
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
        locator = (By.ID, self.char_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def verify_hint_word(self):
        """验证 选词填空的wording: 提示词 是否存在"""
        locator = (By.ID, self.hint_word_value)
        return self.wait.judge_is_exists(locator)

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

    # 磨耳朵
    @teststep
    def verify_sentence(self):
        """验证 句子 是否存在"""
        locator = (By.ID, gv.PACKAGE_ID + "sentence")
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
