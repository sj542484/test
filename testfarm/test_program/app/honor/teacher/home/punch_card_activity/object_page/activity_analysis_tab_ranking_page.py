#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.wait_element_vue import WaitElement


class HwAnalysisRankPage(BasePage):
    """ 答题分析 排行榜 详情页面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“列表中 序号”为依据"""
        locator = (By.XPATH, '//div[@id="student-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def st_index(self):
        """序号"""
        locator = (By.XPATH, '//span[@class="ranking-index"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_icon(self):
        """icon"""
        locator = (By.XPATH, '//img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_finish_status(self):
        """学生 完成"""
        locator = (By.XPATH, '//span[@class="student-cell-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="van-cell__title student-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="van-image van-image--round"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def best_tab(self):
        """最优成绩 tab"""
        locator = (By.XPATH, '//span[@class="van-ellipsis" and text()="最优成绩"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def first_tab(self):
        """首次成绩 tab"""
        locator = (By.XPATH, '//span[@class="van-ellipsis" and text()="首次成绩"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def spend_time(self):
        """用时"""
        locator = (By.XPATH, '//span[@class="student-cell-label"]')
        return self.wait.wait_find_elements(locator)
