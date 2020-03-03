#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element_vue import WaitElement


class SpokenFinishDetailPage(BasePage):
    """ 口语详情 页面"""
    game_type_value = '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]'  # 小游戏类型

    @teststeps
    def __init__(self):
        self.home = ThomePage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    # 完成情况tab 二级页面
    @teststeps
    def wait_check_game_list_page(self, var=15):
        """以“过关状态：已完成/未完成”为依据"""
        locator = (By.XPATH, '//div[@class="question-cell van-cell"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def game_finish_status(self):
        """小游戏 -未完成/星星数"""
        locator = (By.XPATH, '//div[@class="van-hairline--bottom"]')
        ele = self.wait.wait_find_elements(locator)
        content = [var for var in ele]
        return content

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

    # 三级页面 答题分析详情页
    @teststeps
    def wait_check_detail_page(self, var=15):
        """以“title: 详情”为依据"""
        locator = (By.XPATH, "//div[text()='详情']")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_detail_list_page(self):
        """以“ star”为依据"""
        locator = (By.XPATH, '//div[@class="van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def detail_st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-icon van-image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def detail_st_finish_status(self):
        """学生 完成与否"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-label van-rate"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def detail_st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//span[@class="completion-detail-header-title"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def detail_st_type(self):
        """学生 提分版/基础版/试用期"""
        locator = (By.XPATH, '//div[@class="van-image van-icon__image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def hint(self):
        """句子"""
        locator = (By.XPATH, '//div[@class="completion-detail-header"]/div[@class="completion-detail-header-tip"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)

    # 列表
    @teststep
    def game_items(self):
        """题目元素 """
        locator = (By.XPATH, '//div[@class="van-cell"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def per_game_item(self):
        """个人答题情况页面 -游戏 条目
        :returns:  游戏类型 & 页面内所有game元素
        """
        ele = self.game_items()

        content = []  #
        for i in range(len(ele)):
            descendant = ele[i].find_elements_by_xpath('.//child::span')
            item = [k.text for k in descendant if k.text != '']  # 每一个game
            content.append(item)

        return ele, content

    @teststep
    def question(self):
        """题目"""
        locator = (By.XPATH, '//div[@class="van-cell"]/div[@class="van-cell__title completion-detail-title-text"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def star_ratio(self):
        """完成率"""
        locator = (By.XPATH, '//div[@class="completion-detail-label-text van-rate"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def speak_button(self):
        """发音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)

    # 修改成绩
    @teststeps
    def wait_check_modify_achieve_page(self):
        """以“修改成绩”为依据"""
        locator = (By.XPATH, "//div[text()='修改成绩']")
        return self.wait.wait_check_element(locator)
