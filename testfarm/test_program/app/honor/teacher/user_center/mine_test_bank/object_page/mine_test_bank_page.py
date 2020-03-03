#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time

from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststeps, teststep
from utils.wait_element import WaitElement


class MineTestBankPage(BasePage):
    """我的题库 页面"""
    question_value = gv.PACKAGE_ID + "test_bank_name"  # 题单名
    question_type_value = gv.PACKAGE_ID + "type"  # 题单类型
    num_value = gv.PACKAGE_ID + "exercise_num"  # 共X题

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“我的题库”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的题库')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“存在 我的题库列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator)

    @teststep
    def question_name(self):
        """以“题目名称”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(self.question_value)
        content = [x.text for x in ele]
        return ele, content

    @teststep
    def question_type(self, index):
        """以“类型”的id为依据"""
        item = self.driver \
            .find_elements_by_id(self.question_type_value)[index]. \
            text
        return item

    @teststep
    def question_perfect(self, index):
        """以 加“精”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "perfect")[index]
        return ele

    @teststep
    def question_num(self, index):
        """以“数量”的id为依据"""
        item = self.driver \
            .find_elements_by_id(self.num_value)[index].text
        return item

    @teststep
    def question_author(self):
        """以“作者”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "author")
        return ele

    @teststep
    def question_basket(self):
        """以 右下角“题筐 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_pool") \
            .click()

    @teststep
    def menu_button(self, index):
        """以 条目右侧“菜单按钮”的id为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_eg")[index] \
            .click()
        time.sleep(1)

    @teststep
    def recommend_to_school(self):
        """推荐到学校 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "recommend") \
            .click()
        time.sleep(2)
