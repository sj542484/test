#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.wait_element_vue import WaitElement


class PublishedActivityDetailPage(BasePage):
    """ 已发布活动 详情页面"""
    detail_tips = '★★★ Error- 未进入 已发布活动 详情页面'
    detail_vue_tips = '★★★ Error- 未进入 已发布活动 详情vue页面'
    detail_list_tips = '★★★ Error- 已发布活动 详情页面 未加载成功'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_app_page(self):
        """以“title:全部班级”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="全部班级"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self, var=15):
        """以“title: 分析汇总”为依据"""
        locator = (By.XPATH, '//div[@class="activity-publishing-nav-right" and text()="分析汇总"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self, var=15):
        """以“id="activity-publishing-detail-cell"”为依据"""
        locator = (By.XPATH, '//div[@id="activity-publishing-detail-cell"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def down_button(self):
        """ 下拉 按钮"""
        locator = (By.XPATH, '//span[@class="van-dropdown-menu__title"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def teacher_name(self):
        """老师 title"""
        locator = (By.XPATH, '//span[@class="activity-publishing-detail-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def van_name(self):
        """活动班级名"""
        locator = (By.XPATH, '//span[@class="activity-publishing-detail-class-name"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def published_activity_num(self):
        """活动 人数统计信息 - 人数"""
        locator = (By.XPATH, '//span[@class="activity-publishing-detail-number"]/b')
        return self.wait.wait_find_elements(locator)

    @teststep
    def published_activity_unit(self):
        """活动 人数统计信息 - 单位"""
        locator = (By.XPATH, '//span[@class="activity-publishing-detail-word"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def published_activity_title(self):
        """活动 人数统计信息 title"""
        locator = (By.XPATH, '//div[@class="activity-publishing-detail-item-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def analysis_button(self):
        """ 分析汇总 按钮"""
        locator = (By.XPATH, '//div[@class="activity-publishing-nav-right" and text()="分析汇总"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def published_activity_all_person_info(self):
        """活动 人数统计信息"""
        num = self.published_activity_num()
        unit = self.published_activity_unit()
        title = self.published_activity_title()

        content = []
        for i in range(0, len(num), 4):  # 实打卡/缺卡/邀请人数/分享次数 元素均相同
            content.extend([num[i].text, unit[i].text, title[i].text])
        return content

    @teststep
    def published_activity_invite_person_info(self):
        """活动 人数统计信息"""
        num = self.published_activity_num()
        unit = self.published_activity_unit()
        title = self.published_activity_title()

        content = []
        for i in range(0, len(num), 4):
            content.extend([num[i + 1].text, unit[i + 1].text, title[i + 1].text])
        return content

    @teststep
    def published_activity_current_day_info(self):
        """活动 人数统计信息"""
        num = self.published_activity_num()
        unit = self.published_activity_unit()
        title = self.published_activity_title()

        content = []
        for i in range(0, len(num), 4):
            content.extend([num[i + 2].text, unit[i + 2].text, title[i + 2].text])
        return content

    @teststep
    def published_activity_all_day_info(self):
        """活动 人数统计信息"""
        num = self.published_activity_num()
        unit = self.published_activity_unit()
        title = self.published_activity_title()

        content = []
        for i in range(0, len(num), 4):
            content.extend([num[i + 3].text, unit[i + 3].text, title[i + 3].text])
        return content

    @teststeps
    def wait_check_menu_page(self, var=15):
        """以content”为依据"""
        locator = (By.XPATH, '//div[@class="van-popup van-popup--top van-dropdown-item__content"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def menu_item_text(self):
        """ 下拉 菜单条目text"""
        locator = (By.XPATH, '//div[@class="activity-dropitem-title"]/div')
        return self.wait.wait_find_elements(locator)[::2]

    @teststep
    def menu_item(self):
        """ 下拉 菜单条目"""
        locator = (By.XPATH, '//div[@class="activity-dropitem-title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def wait_check_choose_result_page(self, var):
        """以content”为依据"""
        locator = (By.XPATH, '//div[@class="van-ellipsis" and text()="{}"]'.format(var))
        return self.wait.wait_check_element(locator)
