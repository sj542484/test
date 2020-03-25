#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class StHwDetailPage(BasePage):
    """ 班级成员- 学生作业 详情页面"""

    def __init__(self):
        self.wait = WaitElement()
        self.screen = self.get_window_size()

    @teststeps
    def wait_check_app_page(self, var):
        """以“title: ”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self, var):
        """以“tab”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(var))
        return self.wait.wait_check_element(locator)

    @teststep
    def unfinished_tab(self):
        """未完成"""
        locator = (By.XPATH, "//span[text()='未完成']")
        return self.wait.wait_find_element(locator)

    @teststep
    def finished_tab(self):
        """已完成"""
        locator = (By.XPATH, "//span[text()='已完成']")
        return self.wait.wait_find_element(locator)

    @teststeps
    def wait_check_empty_tips_page(self, var=10):
        """ 以提示text作为依据"""
        locator = (By.XPATH, "//div[text()='暂无数据']")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_hw_list_page(self):
        """以“作业 名称”为依据"""
        locator = (By.XPATH, '//div[@class="van-cell__title student-list-title"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def hw_title(self):
        """作业title"""
        locator = (By.XPATH, '//div[@class="van-cell__title student-list-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def hw_finish(self):
        """作业 完成情况"""
        locator = (By.XPATH, '//div[@class="van-cell__value student-list-value"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait.wait_find_element(locator).click()

    # 游戏
    @teststeps
    def wait_check_game_page(self, var):
        """以“title: ”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(var))
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_game_list_page(self, var):
        """以“title: ”为依据"""
        locator = (By.XPATH, '//div[@class="question-cell-title"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def game_type(self):
        """游戏类型"""
        locator = (By.XPATH, '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_name(self):
        """游戏 名称"""
        locator = (By.XPATH, '//div[@class="question-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def optimal_achievement(self):
        """最优成绩-"""
        locator = (By.XPATH, '//span[@class="question-cell-label-left"]')
        return self.wait.wait_find_elements(locator)

    # 游戏详情页
    @teststeps
    def wait_check_detail_page(self, name, var=15):
        """以“首次正答”的xpath-index为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(name))
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def toast_operation(self, var):
        """is toast exist, return True or False """
        if self.find_toast(var):
            print(var)
        else:
            print('★★★ Error- 未弹toast:', var)

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
