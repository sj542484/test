#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.utils.wait_element import WaitElement


class SpokenPage(BasePage):
    """题单详情 页面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:题详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'详情')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self, var=10):
        """以“题单详情页面  列表是否已加载出来”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "title")
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
