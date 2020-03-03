#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.decorator import teststeps
from conf.base_page import BasePage
from utils.wait_element import WaitElement


class MIAlbumPage(BasePage):
    """小米5C 微课 -选择本地视频"""
    path_item_value = 'com.android.fileexplorer:id/path_item'

    @teststeps
    def __init__(self):
        self.wait = WaitElement()

    # 本地视频 有视频/无视频
    @teststeps
    def wait_check_page(self, var=10):
        """title:选择文件 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选择文件')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def judge_path_item(self):
        """判断是否有path_item元素"""
        locator = (By.ID, self.path_item_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def path_item(self):
        """路径"""
        ele = self.driver \
            .find_elements_by_id(self.path_item_value)
        return ele

    @teststeps
    def files_name(self):
        """文件夹"""
        ele = self.driver \
            .find_elements_by_id("com.android.fileexplorer:id/file_name")
        return ele

    @teststeps
    def wait_check_list_page(self, item, var=10):
        """title: 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % item)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def more_button(self):
        """更多 按钮"""
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'更多')]") \
            .click()

    @teststeps
    def cancel_button(self):
        """取消 按钮"""
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'取消')]") \
            .click()

    @teststeps
    def wait_check_more_page(self, var=10):
        """title: 为依据"""
        locator = (By.ID, "miui:id/title")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def order_button(self):
        """排序 按钮"""
        self.driver \
            .find_elements_by_id("miui:id/title")[0] \
            .click()

    @teststeps
    def wait_check_order_page(self, var=10):
        """排序方式 title: 排序 为依据"""
        locator = (By.ID, "miui:id/alertTitle")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def order_item_button(self, index=0):
        """排序方式:名称"""
        self.driver \
            .find_elements_by_id("miui:id/title")[index] \
            .click()

    @teststeps
    def wait_check_video_list_page(self, var=10):
        """title:下载 为依据"""
        locator = (By.ID, "com.android.fileexplorer:id/file_separator")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def video_item(self):
        """视频"""
        ele = self.driver\
            .find_elements_by_id("com.android.fileexplorer:id/file_name")

        return ele

    @teststeps
    def confirm_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'确定')]") \
            .click()

    # 本地视频 有视频 进入视频列表
    @teststeps
    def choose_video_operation(self, name):
        """选择视频"""
        ele = self.video_item()  # 视频

        content = []
        index = 0
        for i in range(len(ele)):
           if name == ele[i].text:
               content.append(ele[i])
               ele[i].click()
               index += 1
               break
        return content, index
