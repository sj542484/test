#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element_vue import WaitElement


class VanclassStarPage(BasePage):
    """ 班级 星星详情页"""

    def __init__(self):
        self.get = GetAttribute()
        self.wait = WaitElement()
        self.home = ThomePage()

    @teststeps
    def wait_check_star_page(self):
        """以“title:星星排行榜”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="星星排行榜"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_tab_list_page(self):
        """以“星星排行榜”为依据"""
        locator = (By.XPATH, '//div[@id="class-score-star-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_empty_tips_page(self):
        """暂无数据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error" and text()="暂无数据"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def this_week_tab(self):
        """本周 tab"""
        locator = (By.XPATH, '//span[@class="van-ellipsis" and text()="本周"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def last_week_tab(self):
        """上周"""
        locator = (By.XPATH, '//span[@class="van-ellipsis" and text()="上周"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def this_month_tab(self):
        """本月 tab"""
        locator = (By.XPATH, '//span[@class="van-ellipsis" and text()="本月"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def all_tab(self):
        """全部"""
        locator = (By.XPATH, '//span[@class="van-ellipsis" and text()="全部"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def st_order(self):
        """排序"""
        locator = (By.XPATH, '//div[@class="class-score-star-cell-icon"]/div')
        ele = self.wait.wait_find_elements(locator)
        content = [k for k in ele if k.get_attribute('class') != 'van-image van-image--round']
        return content

    @teststep
    def st_icon(self):
        """头像"""
        locator = (By.XPATH, '//img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="class-score-star-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def num(self):
        """积分/星星数目"""
        locator = (By.XPATH, '//div[@class="class-score-star-cell-right"]')
        return self.wait.wait_find_elements(locator)
