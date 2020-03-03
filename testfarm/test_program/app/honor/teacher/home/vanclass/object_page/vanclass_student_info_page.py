#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class StDetailPage(BasePage):
    """ 班级成员- 学生信息 详情页面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title: 学生详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学生详情')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“title: 学生详情”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "nick_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def st_name(self):
        """name"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "name")
        return ele.text

    @teststep
    def st_nickname(self):
        """nickname"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "nick_name")
        return ele.text

    @teststep
    def st_tags(self):
        """提分/试用/基础"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tags")
        return ele.text

    @teststep
    def phone_title(self):
        """手机号"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'手机号')]").text
        print(item)

    @teststep
    def st_phone(self):
        """手机号"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "phone")
        return ele

    @teststep
    def data_title(self):
        """数据统计"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'数据统计')]").text
        print(item)

    @teststep
    def card_title(self):
        """拼图卡片"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'拼图卡片')]").text
        print(item)

    @teststep
    def hw_title(self):
        """习题作业"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'作业')]").text
        print(item)

    @teststep
    def paper_title(self):
        """本班卷子"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'本班卷子')]").text
        print(item)

    @teststep
    def spoken_title(self):
        """口语作业"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'口语作业')]").text
        print(item)

    @teststep
    def judge_st_tags(self):
        """判断元素 '提分/试用/基础' 存在与否"""
        locator = (By.ID, gv.PACKAGE_ID + "tags")
        return self.wait.judge_is_exists(locator)

    @teststep
    def data_statistic(self):
        """数据统计"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "count")\
            .click()

    @teststep
    def picture_count(self):
        """拼图 个数"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "puzzle_count")\
            .click()

    @teststep
    def hw_count(self):
        """作业个数"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "hw_count")\
            .click()

    # 数据统计/拼图
    @teststeps
    def wait_check_per_detail_page(self, var):
        """以“title: ”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    # 数据统计
    @teststep
    def st_commit_button(self):
        """数据统计 - 该学生不存在"""
        self.driver \
            .find_element_by_id("android:id/button1") \
            .click()

    # 拼图
    @teststeps
    def wait_check_picture_page(self):
        """以“title: ”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_report")
        return self.wait.wait_check_element(locator)

    @teststep
    def picture_report(self):
        """拼图 报告"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_report")
        print(ele.text)

    @teststep
    def judge_picture(self):
        """判断拼图页面 - 图片存在"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_puzzle")
        return self.wait.judge_is_exists(locator)

    @teststep
    def picture_num(self):
        """拼图 数量 """
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_puzzle_num")
        return ele
