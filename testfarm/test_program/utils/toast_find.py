#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf.decorator import teststeps
from conf.base_page import BasePage


class Toast(BasePage):
    """获取toast 弹框"""

    @teststeps
    def find_toast(self, text, timeout=5, poll_frequency=0.5):
        """is toast exist, return True or False"""
        # noinspection PyBroadException
        try:
            toast = ("xpath", "//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast), text)
            return True
        except Exception:
            return False

    @teststeps
    def get_toast(self, var=5):
        """is toast exist, return True or False """
        # noinspection PyBroadException
        try:
            toast = (By.CLASS_NAME, "android.widget.Toast")
            WebDriverWait(self.driver, var, 0.5).until(EC.presence_of_element_located(toast))
            return True
        except Exception:
            return False

    @teststeps
    def toast_text(self):
        """ toast弹框 信息"""
        item = self.driver \
            .find_element_by_class_name("android.widget.Toast").text
        print(item)

