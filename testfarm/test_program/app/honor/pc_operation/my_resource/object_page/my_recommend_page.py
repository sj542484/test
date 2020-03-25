#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By
from conf.decorator_pc import teststeps, teststep
from app.honor.pc_operation.tools.wait_element import WaitElement


class ManageRecommendPage():
    """管理推荐题界面"""

    def __init__(self, driver):
        self.wait = WaitElement(driver)
        self.driver = driver

    @teststeps
    def wait_check_page(self, index=10):
        """以  批量取消 元素 的xpath为依据"""
        locator = (By.XPATH, "//span[text()='批量取消']")
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def wait_check_no_page(self, index=5):
        """以  暂无数据 元素 的xpath为依据"""
        locator = (By.XPATH, '//div[@id="empty-block"]')
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def wait_check_list_page(self, index=10):
        """以  批量取消 元素 的xpath为依据"""
        locator = (By.XPATH, '//div[@class="testbank-name"]')
        return self.wait.wait_check_element(locator, index)

    @teststep
    def menu(self):
        """ 题单"""
        locator = (By.XPATH, '//a[text()="题单"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def games(self):
        """ 大题"""
        locator = (By.XPATH, '//a[text()="大题"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def paper(self):
        """ 大题"""
        locator = (By.XPATH, '//a[text()="试卷"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def create_date(self):
        """推荐日期"""
        locator = (By.XPATH, '//span[@class="account-name"]/parent::td/following-sibling::td')
        ele = self.wait.wait_find_elements(locator)
        return ele

    @teststeps
    def cancel_btn(self):
        """批量取消 按钮"""
        locator = (By.XPATH, "//span[text()='批量取消']/parent::button")
        self.wait\
            .wait_find_element(locator).click()

    @teststep
    def all_choose_button(self):
        """ 单选框"""
        locator = (By.XPATH, '//label[@class="el-checkbox"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def choose_button(self):
        """ 单选框"""
        locator = (By.XPATH, '//label[@class="el-checkbox"]')
        return self.wait.wait_find_elements(locator)
