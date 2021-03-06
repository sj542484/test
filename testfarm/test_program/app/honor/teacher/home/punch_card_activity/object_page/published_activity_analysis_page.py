#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.wait_element_vue import WaitElement


class PublishedActivityAnalysisSummaryPage(BasePage):
    """ 已发布活动 分析汇总页面"""
    analysis_tips = '★★★ Error- 分析汇总 详情页面 未加载成功'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var=15):
        """以“Day 1”为依据"""
        locator = (By.XPATH, '//span[@class="activity-day-cell-title"]/b[text()="Day 1"]')
        ele = self.wait.wait_check_element(locator, var)
        self.my_assert.assertTrue(ele, self.analysis_tips)
        return ele

    @teststep
    def down_button(self):
        """ 下拉 按钮"""
        locator = (By.XPATH, '//span[@class="van-dropdown-menu__title"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def day_name(self):
        """Day X"""
        locator = (By.XPATH, '//span[@class="activity-day-cell-title"]/b')
        return self.wait.wait_find_elements(locator)

    @teststep
    def date_name(self):
        """日期"""
        locator = (By.XPATH, '//div[@class="van-cell__label"]')
        return self.wait.wait_find_elements(locator)


class PublishedActivityAnalysisSummaryDetailPage(BasePage):
    """ 已发布活动 分析汇总详情页面"""
    st_item_value = "//div[@id='student-cell']"  # 完成情况 学生条目
    hw_item_value = "//div[@id='question-cell']"  # 答题分析 作业条目
    game_type_value = '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]'  # 小游戏类型

    analysis_vue_tips = '★★★ Error- 未进入分析汇总详情vue界面'
    st_list_tips = '★★★ Error- 完成情况tab 学生列表未加载成功'
    hw_list_tips = '★★★ Error- 答题分析 页面作业列表'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var):
        """以“完成统计”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(var))
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.analysis_vue_tips)
        return ele

    @teststeps
    def wait_check_empty_tips_page(self, var=10):
        """以 提示text 作为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error" and text()="暂无数据"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def finish_tab(self):
        """完成统计"""
        locator = (By.XPATH, "//span[text()='完成统计']")
        return self.wait.wait_find_element(locator)

    @teststep
    def answer_analysis_tab(self):
        """答题分析"""
        locator = (By.XPATH, "//span[text()='答题分析']")
        return self.wait.wait_find_element(locator)

    # 完成统计tab 学生列表
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生完成情况 元素”为依据"""
        locator = (By.XPATH, self.st_item_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def finish_tab_st_items(self):
        """学生 条目"""
        locator = (By.XPATH, self.st_item_value)
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_type(self):
        """基础班/提分版/试用期学生"""
        locator = (By.XPATH, '//div[@class="van-image van-icon__image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_finish_status(self):
        """学生 完成与否"""
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
        locator = (By.XPATH, '//div[@class="van-image van-image--round"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    # 答题分析tab 页面
    @teststeps
    def wait_check_hw_list_page(self):
        """以“cup 元素”为依据"""
        locator = (By.XPATH, self.hw_item_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def analysis_tab_hw_items(self):
        """作业包 条目"""
        locator = (By.XPATH, self.hw_item_value)
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_type(self):
        """游戏类型"""
        locator = (By.XPATH, self.game_type_value)
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_level(self):
        """提分"""
        locator = (By.XPATH, '//span[@class="question-cell-tag van-tag van-tag--large van-tag--primary"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_name(self):
        """游戏 名称"""
        locator = (By.XPATH, '//div[@class="question-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def average_achievement(self):
        """全班首轮平均成绩x%"""
        locator = (By.XPATH, '//span[@class="question-cell-label-left"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def ranking_list(self):
        """排行榜"""
        locator = (By.XPATH, '//span[@class="question-cell-label-right"]')
        return self.wait.wait_find_elements(locator)

