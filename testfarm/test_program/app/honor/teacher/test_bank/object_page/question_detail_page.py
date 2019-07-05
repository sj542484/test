#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.utils.wait_element import WaitElement


class QuestionDetailPage(BasePage):
    """题单详情 页面"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:题单详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题单详情')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“题单详情页面  列表是否已加载出来”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "test_bank_name")
        return self.wait.wait_check_element(locator)

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
    def all_check_button(self):
        """全选/全不选 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "all_check") \
            .click()

    @teststep
    def check_button(self):
        """单选 按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "cb_add")
        return ele
