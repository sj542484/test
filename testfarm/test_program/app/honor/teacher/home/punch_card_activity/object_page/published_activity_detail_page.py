#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re

from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.wait_element_vue import WaitElement


class PublishedActivityDetailPage(BasePage):
    """ 已发布活动 详情页面"""
    detail_tips = '★★★ Error- 未进入 已发布活动 详情页面'
    detail_vue_tips = '★★★ Error- 未进入 已发布活动 详情vue页面'
    detail_list_tips = '★★★ Error- 已发布活动 详情页面 未加载成功'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var=15):
        """以“title: 分析汇总”为依据"""
        locator = (By.XPATH, '//div[@class="activity-publishing-nav-right" and text()="分析汇总"]')
        ele = self.wait.wait_check_element(locator, var)
        self.my_assert.assertTrue(ele, self.detail_tips)
        return ele

    @teststeps
    def wait_check_list_page(self, var=15):
        """以“id="activity-publishing-detail-cell"”为依据"""
        locator = (By.XPATH, '//div[@id="activity-publishing-detail-cell"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_empty_tips_page(self, var=5):
        """以 暂无数据提示 作为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error" and text()="暂无数据"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def down_button(self):
        """ 下拉 按钮"""
        locator = (By.XPATH, '//span[@class="van-dropdown-menu__title"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def student_name(self):
        """学生 title"""
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


class PublishedActivityDailyAnalysisPage(BasePage):
    """ 已发布活动 每日详情页面"""
    analysis_tips = '★★★ Error- 未进入每日详情 页面'
    analysis_list_tips = '★★★ Error- 每日详情 页面 未加载成功'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self):
        """以“title:每日详情”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="每日详情"]')
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.analysis_tips)
        return ele

    @teststeps
    def wait_check_list_page(self, var=15):
        """以“id="activity-day-cell"”为依据"""
        locator = (By.XPATH, '//div[@id="activity-day-cell"]')
        ele = self.wait.wait_check_element(locator, var)
        self.my_assert.assertTrue(ele, self.analysis_list_tips)
        return ele

    @teststep
    def st_tab(self):
        """学生"""
        locator = (By.XPATH, '//div[@class="van-tab-active"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def hint_tab(self):
        """提示信息"""
        locator = (By.XPATH, "//span[text()='点击可查看答题分析 ']")
        return self.wait.wait_find_element(locator)

    @teststeps
    def icon(self):
        """每天的状态"""
        locator = (By.XPATH, '//div[@id="activity-day-cell"]/span')
        eles = self.wait.wait_find_elements(locator)

        unfinish = {}  # 待打卡
        unpublish = {}  # 等待发布
        miss = {}  # 缺卡
        for i in range(len(eles)):
            if 'daidaka-icon' in eles[i].get_attribute("class"):
                unfinish[i] = eles[i]
            elif 'queka-icon' in  eles[i].get_attribute("class"):
                miss[i] = eles[i]
            elif 'weifabu-icon' in  eles[i].get_attribute("class"):
                unpublish[i] = eles[i]
        return unfinish, miss, unpublish


    @teststep
    def day_name(self):
        """Day X"""
        locator = (By.XPATH, '//span[contains(@class,"activity-day-cell-title")]/b')
        return self.wait.wait_find_elements(locator)

    @teststep
    def date_name(self):
        """日期"""
        locator = (By.XPATH, '//span[@class="activity-day-cell-title activity-day-cell-title-time"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def status(self):
        """每天的状态"""
        locator = (By.XPATH, '//div[@id="activity-day-cell"]/span/b')
        return self.wait.wait_find_elements(locator)


class PublishedActivityDailyAnalysisDetailPage(BasePage):
    """ 已发布活动 每日详情 的详情页面"""
    game_type_value = '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]'  # 小游戏类型

    analysis_vue_tips = '★★★ Error- 未进入 每日详情的详情界面'
    st_detail_tips = '★★★ Error- 每日详情 的详情页面未加载成功'
    empty_tips = '★★★ Error- 每日详情 的详情页面暂无数据'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var):
        """以“title”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(var))
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.analysis_vue_tips)
        return ele

    @teststeps
    def wait_check_empty_page(self, var=20):
        """以“暂无数据 元素”为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self, var=20):
        """以“最优成绩 元素”为依据"""
        locator = (By.XPATH, '//div[@id="question-cell"]')
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
            print(item)
            print('------------------------------------')
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
