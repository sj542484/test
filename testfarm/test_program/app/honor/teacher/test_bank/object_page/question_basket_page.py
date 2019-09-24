#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from conf.base_config import GetVariable as gv
from utils.wait_element import WaitElement


class QuestionBasketPage(BasePage):
    """题筐 页面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:题筐”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题筐')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self, var=20):
        """以“题筐是否有题”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def empty_text(self):
        """以“空白页”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + 'load_empty').text
        print(ele)

    @teststep
    def all_check_button(self):
        """以“全选按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "select_all") \
            .click()

    @teststep
    def check_button(self):
        """以“单选按钮”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "cb_add")
        return ele

    @teststep
    def question_name(self):
        """以“题目名称”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        return ele

    @teststep
    def question_type(self):
        """以“类型”的id为依据"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type")
        return item

    @teststep
    def question_num(self):
        """以“共x题”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "exercise_num")
        return ele

    @teststep
    def question_author(self):
        """以“作者”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "author")
        return ele

    @teststep
    def out_basket_button(self):
        """以“移出题筐 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_first") \
            .click()

    @teststep
    def assign_button(self):
        """以“布置作业 按钮”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_second")
        return ele

    @teststep
    def last_judge(self, var):
        """最后一个元素 resource-id属性值是否为作者"""
        value = GetAttribute().resource_id(var)
        if value == gv.PACKAGE_ID + "author":
            return True
        else:
            return False

    @teststeps
    def all_question(self):
        """页面内所有 题目条目"""
        name = self.question_name()  # 题目名称
        mode = self.question_type()  # 题目类型
        num = self.question_num()  # 题目 小题数
        author = self.question_author()  # 题目作者

        for i in range(len(author)):
            print(name[i].text, '\n',
                  mode[i].text, '\n',
                  num[i].text, '\n',
                  author[i].text)
            print('---------------')
        return len(name)
