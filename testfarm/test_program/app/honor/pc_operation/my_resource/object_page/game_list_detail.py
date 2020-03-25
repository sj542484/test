#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_pc import teststeps
from app.honor.pc_operation.tools.wait_element import WaitElement


class GameDetailPage(BasePage):
    """我的题库 - 大题详情页"""

    def __init__(self, driver):
        self.wait = WaitElement(driver)
        self.driver = driver

    @teststeps
    def wait_check_switch_page(self, index=20):
        """以  //div[class="page detail-page"] 元素 的xpath为依据"""
        locator = (By.XPATH, '//div[@class="el-dialog__wrapper iframe-dialog-wrapper"]')
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def switch_iframe(self):
        """切换iframe"""
        locator = (By.XPATH, "//iframe[contains(@src,'https://game.vanthink.cn/WK/#/detail')]")
        iframe = self.wait \
            .wait_find_element(locator)
        self.driver.switch_to.frame(iframe)

    @teststeps
    def switch_back(self):
        self.driver.switch_to.default_content()

    @teststeps
    def wait_check_page(self, index=20):
        """以  //div[@class="testbank-info"] 元素 的xpath为依据"""
        locator = (By.XPATH, '//div[@class="detail-content"]')
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def delete_question_btn(self):
        """删除题目 按钮"""
        locator = (By.XPATH, '//button[text()="删除题目"]')
        self.wait \
            .wait_find_element(locator).click()
        
    # 删除提示 页面
    @teststeps
    def wait_check_tips_title(self):
        """提示title"""
        locator = (By.XPATH, '//div[@class="el-dialog el-dialog--tiny"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def tips_content(self):
        """提示 具体内容"""
        locator = (By.XPATH, '//div[@class="notice"]')
        return self.wait \
            .wait_check_element(locator)

    @teststeps
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//span[text()="确定"]/parent::button')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def tips_content_commit(self):
        """提示  -- 确定"""
        if self.wait.wait_clickable():
            if self.wait_check_tips_title():
                self.commit_button()  # 确定按钮

    @teststeps
    def close_operation(self):
        """关闭操作"""
        if self.wait.wait_clickable():
            self.close_button()

    @teststeps
    def close_button(self):
        """x按钮"""
        locator = (By.XPATH, '//button/i[@class="el-dialog__close el-icon el-icon-close"]')
        self.wait \
            .wait_find_element(locator).click()
