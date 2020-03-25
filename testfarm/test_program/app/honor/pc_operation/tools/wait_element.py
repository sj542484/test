#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from conf.decorator_pc import teststeps

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WaitElement():
    """页面检查点 及 等待元素加载"""
    def __init__(self, driver):
        self.driver = driver

    @teststeps
    def wait_check_element(self, locator, timeout=15):
        """判断元素是否存在 存在就返回True,不存在就返回False"""
        self.wait_load_display()

        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
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
        self.wait_load_display()

        return WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of_element_located(locator))

    @teststeps
    def wait_find_element_visibility(self, locator, timeout=20, poll=1):
        """查找元素并返回元素
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 元素
        """
        WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of_element_located(locator))
        self.wait_load_display()
        return WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of_element_located(locator))

    @teststeps
    def wait_find_elements(self, locator, timeout=15, poll=0.5):
        """查找元素集合并返回元素
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 元素
        """
        self.wait_load_display()

        return WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of_all_elements_located(locator))

    @teststeps
    def wait_until_not_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否已经不存在,不存在了返回True,还存在就返回False
        :param locator: 元素属性
        """
        self.wait_load_display()

        try:
            WebDriverWait(self.driver, timeout, poll).until_not(
                EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststeps
    def wait_click_element(self, locator, timeout=15, poll=0.5):
        """ 判断某个元素中是否可见并且可点击
        :param locator: 元素属性
        """
        self.wait_load_display()

        return WebDriverWait(self.driver, timeout, poll).until(
            EC.element_to_be_clickable(locator))

    @teststeps
    def judge_is_selected(self, element, timeout=15, poll=0.5):
        """ 判断某个元素是否被选中"""
        self.wait_load_display()

        return WebDriverWait(self.driver, timeout, poll).until(
            EC.element_to_be_selected(element))

    @teststeps
    def judge_is_visibility(self, element, timeout=15, poll=0.5):
        """判断元素是否可见"""
        self.wait_load_display()

        try:
            WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of(element))
            return True
        except:
            return False

    @teststeps
    def wait_load_display(self):
        """等待 加载蒙层&加载图画 消失"""
        # 先等待加载蒙层消失
        WebDriverWait(self.driver, 20, 0.5).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'el-loading-mask')]")))

        # 等待加载图画消失
        WebDriverWait(self.driver, 20, 0.5).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'el-loading-spinner')]")))

    def wait_clickable(self):
        # 先等待加载蒙层消失
        WebDriverWait(self.driver, 20, 0.5).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'el-loading-mask')]")))

        # 等待加载图画消失
        WebDriverWait(self.driver, 20, 0.5).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'el-loading-spinner')]")))

        # 掩盖的div元素
        ObscureDiv = (By.XPATH,
                      "//div[@class='el-loading-mask is-fullscreen el-loading-fade-leave-active el-loading-fade-leave-to']")
        # 使用显示等待，等待掩盖的div消失
        return WebDriverWait(self.driver, 20, 0.5).until(EC.invisibility_of_element_located(ObscureDiv))
