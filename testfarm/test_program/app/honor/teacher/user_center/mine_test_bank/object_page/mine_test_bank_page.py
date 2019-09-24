#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time

from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststeps, teststep
from utils.wait_element import WaitElement


class MineTestBankPage(BasePage):
    """我的题库 页面"""
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
