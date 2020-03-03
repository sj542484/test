#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.wait_element_vue import WaitElement


class VanclassApplyPage(BasePage):
    """ 班级 入班申请详情页 元素信息"""
    apply_vue_tips = '★★★ Error- 未进入班级 入班申请详情vue页'
    apply_list_tips = '★★★ Error- 入班申请详情页未加载成功'
    more_tips = '★★★ Error- 未进入更多按钮详情'

    empty_tips = '暂无入班申请学生'

    def __init__(self):
        self.wait = WaitElement()
        self.screen = self.get_window_size()

    @teststeps
    def wait_check_page(self):
        """以“title: 入班申请”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="入班申请"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_st_list_page(self):
        """以“学生头像”为依据"""
        locator = (By.XPATH, '//div[@id="class-apply-list-cell"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_empty_tips_page(self, var=10):
        """以 提示text 作为依据"""
        locator = (By.XPATH, "//div[text()='暂无数据']")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def icon(self):
        """头像"""
        locator = (By.XPATH, '//div[@class="van-image van-image--round"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_nick(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="class-apply-content-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_remark(self):
        """学生 备注名"""
        locator = (By.XPATH, '//div[@class="class-apply-content-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def more_button(self):
        """更多 按钮"""
        locator = (By.XPATH, '//i[@class="class-apply-content-icon van-icon van-icon-ellipsis"]')
        return self.wait.wait_find_elements(locator)

    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.XPATH, '//div[@class="van-popup van-popup--round van-popup--bottom van-action-sheet"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def more_agree_button(self):
        """同意 按钮"""
        locator = (By.XPATH, '//span[text()="同意"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def more_reject_button(self):
        """拒绝 按钮"""
        locator = (By.XPATH, '//span[text()="拒绝"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def more_cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//div[@class="van-action-sheet__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def swipe_vertical_web(self, ratio_x, start_y, end_y, steps=1000):
        """
        上/下滑动 x值不变
        :param ratio_x: x坐标系数
        :param start_y: 滑动起点y坐标系数
        :param end_y: 滑动终点y坐标系数
        :param steps: 持续时间ms
        :return: None
        """
        x = int(self.screen[0] * ratio_x)
        y1 = int(self.screen[1] * start_y)
        y2 = int(self.screen[1] * end_y)

        self.driver.swipe(x, y1, x, y2, steps)
