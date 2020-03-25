#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import time

from selenium.webdriver.common.by import By

from conf.decorator_vue import teststep, teststeps
from conf.base_page import BasePage
from utils.assert_package import MyAssert
from utils.vue_context import VueContext
from utils.wait_element_vue import WaitElement


class PunchCardPage(BasePage):
    """打卡活动 页面元素信息"""
    activity_name_value = 'activity-list-cell-title'  # 条目名称

    activity_tips = '★★★ Error- 未进入 打卡活动页面'
    activity_vue_tips = '★★★ Error- 未进入打卡活动vue界面'
    activity_list_tips = '★★★ Error- 未进入活动模板列表'

    def __init__(self):
        self.wait = WaitElement()
        self.screen = self.get_window_size()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_app_page(self):
        """以“title:打卡活动”为依据"""
        locator = (By.XPATH, "//android.view.View[@text='打卡活动']")
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.activity_tips)
        return ele

    @teststeps
    def wait_check_page(self):
        """以“title:打卡活动”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="打卡活动"]')
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.activity_vue_tips)
        return ele

    @teststeps
    def wait_check_no_activity_page(self, var=10):
        """暂无数据 作为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error" and text()="暂无数据"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def help_button(self):
        """ 提示 按钮"""
        locator = (By.XPATH, '//i[@class="nav-right-icon van-icon van-icon-question-o"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def activity_template_tab(self):
        """活动模版"""
        locator = (By.XPATH, "//span[text()='活动模版']")
        return self.wait.wait_find_element(locator)

    @teststep
    def published_activities_tab(self):
        """已发布活动"""
        locator = (By.XPATH, "//span[text()='已发布活动']")
        return self.wait.wait_find_element(locator)

    # 活动模板列表 元素
    @teststeps
    def wait_check_template_list_page(self):
        """以 条目 为依据"""
        locator = (By.XPATH, '//div[@id="activity-list-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def template_activity_name(self):
        """活动模板条目名称"""
        locator = (By.XPATH, '//div[@class="activity-list-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def template_activity_info(self):
        """活动模板信息：5本书  每日1本  请于2020-04-26前布置"""
        locator = (By.XPATH, '//div[@class="activity-list-cell-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def template_activity_type(self):
        """活动模板类型：自创/学校"""
        locator = (By.XPATH, '//span[@class="activity-list-cell-self"]')
        return self.wait.wait_find_elements(locator)

    # 已发布活动列表 元素
    @teststeps
    def wait_check_published_list_page(self):
        """以 条目 为依据"""
        locator = (By.XPATH, '//div[@id="activity-list-right-detail-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def published_activity_name(self):
        """活动条目名称"""
        locator = (By.XPATH, '//div[@class="activity-list-right-detail-title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def published_activity_date(self):
        """活动时间信息：2020-02-12 / 2020-02-16"""
        locator = (By.XPATH, '//div[@class="activity-list-right-detail-row"]')
        ele = self.wait.wait_find_elements(locator)[1::2]
        return [k.find_element_by_xpath('.//span') for k in ele]

    @teststeps
    def published_activity_status(self):
        """活动状态：进行中/已结束"""
        locator = (By.XPATH, '//div[@class="activity-list-right-detail-row"]')
        ele = self.wait.wait_find_elements(locator)[1::2]
        content = []
        for k in ele:
            var = k.find_elements_by_xpath('.//span')
            content.append(var[1])
        return content

    @teststeps
    def is_arithmetic(self, l):
        """发布日期相等or递增"""
        delta = l[1] - l[0]
        for index in range(len(l) - 1):
            if not (l[index + 1] - l[index] >= delta):
                return False
        return True

    @teststep
    def published_info(self):
        """活动信息"""
        locator = (By.XPATH, '//div[@class="van-grid"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def published_activity_total_num(self):
        """活动 总人数统计信息"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-number")]/b')
        return self.wait.wait_find_elements(locator)[::4]

    @teststep
    def published_activity_total_unit(self):
        """活动 总人数统计信息 单位"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-word")]')
        return self.wait.wait_find_elements(locator)[::3]

    @teststep
    def published_activity_total_title(self):
        """活动 总人数统计信息"""
        locator = (By.XPATH, '//div[contains(@class,"activity-list-right-detail-item-label")]')
        return self.wait.wait_find_elements(locator)[::4]

    @teststep
    def published_activity_invite_num(self):
        """活动 邀请总人数统计信息"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-number")]/b')
        return self.wait.wait_find_elements(locator)[1::4]

    @teststep
    def published_activity_invite_unit(self):
        """活动 邀请总人数统计信息 单位"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-word")]')
        return self.wait.wait_find_elements(locator)[1::3]

    @teststep
    def published_activity_invite_title(self):
        """活动 邀请总人数统计信息"""
        locator = (By.XPATH, '//div[contains(@class,"activity-list-right-detail-item-label")]')
        return self.wait.wait_find_elements(locator)[1::4]

    @teststep
    def published_activity_current_day_num(self):
        """活动 总天数统计信息"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-number")]/b')
        return self.wait.wait_find_elements(locator)[2::4]

    @teststep
    def published_activity_current_day_title(self):
        """活动 总天数统计信息"""
        locator = (By.XPATH, '//div[contains(@class,"activity-list-right-detail-item-label")]')
        return self.wait.wait_find_elements(locator)[2::4]

    @teststep
    def published_activity_total_day_num(self):
        """活动 总天数统计信息"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-number")]/b')
        return self.wait.wait_find_elements(locator)[3::4]

    @teststep
    def published_activity_total_day_unit(self):
        """活动 总天数统计信息 单位"""
        locator = (By.XPATH, '//span[contains(@class,"activity-list-right-detail-word")]')
        return self.wait.wait_find_elements(locator)[2::3]

    @teststep
    def published_activity_total_day_title(self):
        """活动 总天数统计信息"""
        locator = (By.XPATH, '//div[contains(@class,"activity-list-right-detail-item-label")]')
        return self.wait.wait_find_elements(locator)[3::4]

    @teststeps
    def published_activity_total_person_info(self):
        """活动 总人数统计信息"""
        num = self.published_activity_total_num()
        unit = self.published_activity_total_unit()
        title = self.published_activity_total_title()

        content = []
        for i in range(len(num)):
            content.append([title[i].text, num[i].text, unit[i].text])
        return content

    @teststeps
    def published_activity_invite_person_info(self):
        """活动 邀请总人数统计信息"""
        num = self.published_activity_invite_num()
        title = self.published_activity_invite_title()
        unit = self.published_activity_invite_unit()

        content = []
        for i in range(len(num)):
            content.append([title[i].text, num[i].text, unit[i].text])
        return content

    @teststeps
    def published_activity_current_day_info(self):
        """活动 当前天数统计信息"""
        num = self.published_activity_current_day_num()
        title = self.published_activity_current_day_title()

        content = []
        for i in range(len(num)):
            content.append([title[i].text, num[i].text])
        return content

    @teststeps
    def published_activity_total_day_info(self):
        """活动 总天数统计信息"""
        num = self.published_activity_total_day_num()
        unit = self.published_activity_total_day_unit()
        title = self.published_activity_total_day_title()

        content = []
        for i in range(len(num)):
            content.append([title[i].text, num[i].text, unit[i].text])
        return content

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//img[@class="vt-page-left-img-Android"]')
        self.wait.wait_find_element(locator).click()

    # 温馨提示 页面
    @teststeps
    def wait_check_tips_page(self, var=3):
        """以“温馨提示”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__header" and text()="温馨提示"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.XPATH, '//div[text()="温馨提示"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def help_tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title van-dialog__message--center"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def no_vanclass_tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title van-dialog__message--left"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def known_button(self):
        """知道了 按钮"""
        locator = (By.XPATH, '//span[@text()="知道了"]/parent::button')
        self.wait.wait_find_element(locator).click()

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

    @teststeps
    def into_activity(self):
        """进入活动列表中的该活动"""
        MyAssert().assertTrue(self.wait_check_published_list_page(), self.activity_list_tips)
        name = self.published_activity_name()  # 活动名
        status = self.published_activity_status()  # 状态
        total_person = self.published_activity_total_person_info()  # 总人数

        content = [k for k in range(len(status)) if status[k].text != '已结束' and total_person[k][1] != '0']
        index = random.randint(0, len(content) - 1)
        print(content[index])
        print("进入已发布活动:", name[content[index]].text)
        activity = [name[content[index]].text]
        name[content[index]].click()  # 进入活动
        VueContext().app_web_switch()  # 切到apk 再切到vue

        return activity

    @teststeps
    def publish_date_operation(self, dates):
        """日期处理
        :param dates:待处理日期
        """
        now_time = time.strftime("%Y-%m-%d", time.localtime())   # 生成当前时间
        now = now_time.split('-')
        date = dates.split('-')

        year = int(date[0])
        var = 30
        if int(date[1]) in (1, 3, 5, 7, 8, 10, 12):
            var = 31
        elif int(date[1]) == 2:
            if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
                var = 29
            else:
                var = 28

        days = 365 * (int(now[0]) - year) + var * (int(now[1]) - int(date[1])) + int(now[2]) - int(date[2])
        print('-----------------')

        return days

    @teststeps
    def offline_publish_date_operation(self, dates, now_time):
        """日期处理
        :param dates:待处理日期
        :param now_time: 比对日期
        """
        now = now_time.split('-')
        date = dates.split('-')

        year = int(now[0])
        var = 30
        if int(now[1]) in (1, 3, 5, 7, 8, 10, 12):
            var = 31
        elif int(now[1]) == 2:
            if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
                var = 29
            else:
                var = 28
        days = 365 * (int(date[0]) - year) + var * (int(date[1]) - int(now[1])) + int(date[2]) - int(now[2])
        return days
