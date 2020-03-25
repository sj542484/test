#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from conf.base_page import BasePage
from conf.decorator import teststeps
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WaitElement(BasePage):
    """页面检查点 及 等待元素加载"""

    @teststeps
    def wait_check_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否存在
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 存在就返回True,不存在就返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(
                EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    @teststeps
    def wait_check_list_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否加载成功
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 存在就返回True,不存在就返回False
        """
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
            return WebDriverWait(self.driver, timeout, poll).until(
                EC.visibility_of_element_located(locator))
        except Exception:
            raise Exception('页面未找到{}元素' .format(locator))

    @teststeps
    def wait_find_elements(self, locator, timeout=15, poll=0.5):
        """查找元素并返回元素
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 元素
        """
        try:
            return WebDriverWait(self.driver, timeout, poll).until(
                EC.presence_of_all_elements_located(locator))
        except Exception:
            raise Exception('页面未找到{}元素'.format(locator))

    @teststeps
    def wait_until_not_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否已经不存在
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 不存在返回True,存在返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until_not(
                EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    @teststeps
    def wait_click_element(self, locator, timeout=15, poll=0.5):
        """
        封装点击元素操作
        :param timeout:
        :param poll:
        :param locator: 自定义元素
        :return:
        """
        try:
            return WebDriverWait(self.driver, timeout, poll).until(
                EC.element_to_be_clickable(locator))
        except Exception:
            raise Exception('元素{}不可点击' .format(locator))

    @teststeps
    def judge_is_clickable(self, locator, timeout=15, poll=0.5):
        """ 判断某个元素中是否可见并且可点击
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 通过判断enabled属性值，返回元素或false
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(
                EC.element_to_be_clickable(locator))
            return True
        except Exception:
            return False

    @teststeps
    def judge_is_selected(self, element, timeout=15, poll=0.5):
        """ 判断某个元素是否被选中
        :param element: 元素
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 元素
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(
                EC.element_to_be_selected(element))
            return True
        except Exception:
            return False

    @teststeps
    def judge_is_visibility(self, element, timeout=15, poll=0.5):
        """判断元素是否可见
        :param element: 元素
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 可见就返回True,不可见就返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of(element))
            return True
        except:
            return False

    @teststeps
    def judge_is_exists(self, locator):
        """判断元素是否存在
        :param locator: 元素属性
        :returns: 存在就返回True,不存在就返回False
        """
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except Exception:
            return False

    @teststeps
    def send_keys_operation(self, locator, text):
        """输入文本
        :param locator: 元素属性
        :param text: 文本信息
        """
        self.wait_find_element(locator).send_keys(text)
