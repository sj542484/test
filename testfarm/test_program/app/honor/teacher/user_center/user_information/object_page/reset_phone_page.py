#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from utils.wait_element import WaitElement


class PhoneReset(BasePage):
    """修改手机号页面所有控件信息"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:修改手机号”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'修改手机号')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def et_phone(self):
        """以“手机号”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "et_phone")
        return ele

    @teststep
    def verify(self):
        """以“验证码”的id为依据"""

        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "verify_input")
        return ele

    @teststep
    def count_time(self):
        """以“获取验证码按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "count_time")\
            .click()

    @teststep
    def btn_certain(self):
        """以“确定按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "btn_certain")\
            .click()
