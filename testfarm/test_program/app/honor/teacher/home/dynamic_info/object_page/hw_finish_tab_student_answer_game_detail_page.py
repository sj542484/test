#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re

from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.wait_element_vue import WaitElement


class StAnswerDetailPage(BasePage):
    """ 完成情况 学生答题情况 详情页面"""
    menu_value = '//div[@class="van-popup van-popup--bottom van-action-sheet"]'  # 更多按钮 -条目元素
    game_type_value = '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]'  # 小游戏类型

    st_detail_tips = '★★★ Error- 未进入学生答题情况 详情页面'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var):
        """以“最优成绩 元素”为依据"""
        locator = (By.XPATH, "//div[text()='%s']" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self, var=20):
        """以“最优成绩 元素”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def game_mode(self, item):
        """小游戏模式--匹配小括号内游戏模式"""
        if "引用" in item:
            item = item[:-5]

        m = re.match(".*（(.*)）.*", item)  # title中有一个括号
        if m:
            return m.group(1)
        else:
            return None

    @teststeps
    def per_game_item(self):
        """个人答题情况页面 -游戏 条目
        :returns:  游戏类型 & 页面内所有game
        """
        locator = (By.XPATH, '//div[@class="question-cell van-cell"]')
        ele = self.wait.wait_find_elements(locator)

        content = []  #
        for i in range(len(ele)):
            descendant = ele[i].find_elements_by_xpath('.//child::span')
            item = [k.text for k in descendant if k.text != '']  # 每一个game
            content.append(item)

        return ele, content

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
    def optimal_first_achievement(self):
        """最优成绩-首轮成绩"""
        locator = (By.XPATH, '//span[@class="question-cell-label-left"]')
        return self.wait.wait_find_elements(locator)
