#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import teststep
from utils.wait_element import WaitElement


class MessagePage(BasePage):
    """消息中心页面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:消息中心”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'消息')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def iv_read_count(self):
        """以“未读消息数”的id为依据"""
        count = self.driver.find_elements_by_id(gv.PACKAGE_ID + "iv_read")
        return len(count)

    @teststep
    def message_count(self):
        """以“消息总数”的class_name为依据"""
        message = self.driver.find_elements_by_class_name("android.widget.RelativeLayout")
        return message

    @teststep
    def click_message(self):
        """以“消息”的class_name为依据"""
        self.driver.\
            elements_by_class_name("android.widget.RelativeLayout")\
            .click()

    @teststep
    def del_message(self):
        """以“删除消息”的class_name为依据"""
        # # 设定系数
        # a = 554.0 / 1080
        # b = 1625.0 / 1794
        elements = self.message_count()
        print('len(elements):', len(elements))
        # for i in range(len(elements))

    @teststep
    def click_negative_button(self):
        """以“取消按钮”的id为依据"""
        self.driver.\
            element_by_id(gv.PACKAGE_ID + 'md_buttonDefaultNegative')\
            .click()

    @teststep
    def click_positive_button(self):
        """以“确认按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + 'md_buttonDefaultPositive')\
            .click()

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class_name为依据"""
        self.driver\
            .find_element_by_class_name("android.widget.ImageButton")\
            .click()
