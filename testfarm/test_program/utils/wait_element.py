#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
from conf.base_page import BasePage
from conf.decorator import teststeps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WaitElement(BasePage):
    """页面检查点 及 等待元素加载"""

    @teststeps
    def wait_check_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否存在 存在就返回True,不存在就返回False"""
        try:
            WebDriverWait(self.driver, timeout, poll).until(
                EC.presence_of_element_located(locator))
            return True
        except:
            return False

    @teststeps
    def wait_find_element(self, locator, timeout=15, poll=0.5):
        """查找元素并返回元素
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 元素
        """
        try:
            element = WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_elements(*locator))
            return element
        except:
            return None

    @teststeps
    def wait_until_not_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否已经不存在,不存在了返回True,还存在就返回False
        :param locator: 元素属性
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until_not(
                EC.presence_of_element_located(locator))
            return True
        except:
            return False

    @teststeps
    def wait_click_element(self, locator, timeout=15, poll=0.5):
        """ 判断某个元素中是否可见并且可点击
        :param locator: 元素属性
        """
        return WebDriverWait(self.driver, timeout, poll).until(
            EC.element_to_be_clickable(locator))

    @teststeps
    def judge_is_selected(self, element, timeout=15, poll=0.5):
        """ 判断某个元素是否被选中"""
        return WebDriverWait(self.driver, timeout, poll).until(
            EC.element_to_be_selected(element))

    @teststeps
    def judge_is_visibility(self, element, timeout=15, poll=0.5):
        """判断元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of(element))
            return True
        except:
            return False

    @teststeps
    def judge_is_exists(self, locator):
        """判断元素是否存在"""
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def send_keys(self, locator, text):
        """"""
        self.wait_find_element(locator).send_keys(text)
