#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.click_bounds import ClickBounds
from utils.wait_element_vue import WaitElement


class ActivityTemplateDetailPage(BasePage):
    """ 活动模板 详情页面"""
    detail_tips = '★★★ Error- 未进入 活动模板 详情页面'
    detail_vue_tips = '★★★ Error- 未进入 活动模板详情vue页面'
    detail_list_tips = '★★★ Error- 活动模板详情页面 未加载成功'

    def __init__(self):
        self.wait = WaitElement()
        self.screen = self.get_window_size()

    @teststeps
    def wait_check_app_page(self):
        """以“title:布置活动”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="布置活动"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self, var=15):
        """以“title: 布置活动”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="布置活动"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self, var=15):
        """以“class="activity-template-content"”为依据"""
        locator = (By.XPATH, '//div[@class="activity-template-content"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def activity_title(self):
        """打卡活动名称 title"""
        locator = (By.XPATH, '//div[@class="activity-template-cell-title"]/span/b')
        return self.wait.wait_find_element(locator).text

    @teststep
    def activity_name(self):
        """打卡活动名称"""
        locator = (By.XPATH, '//span[@class="activity-template-cell-desc"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def activity_slogan_title(self):
        """活动宣传 title"""
        locator = (By.XPATH, '//b[@class="activity-template-slogan-title"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def activity_slogan(self):
        """活动宣传内容"""
        locator = (By.XPATH, '//span[@class="activity-template-cell-desc activity-template-slogan-contant"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def activity_source_title(self):
        """活动资源 title"""
        locator = (By.XPATH, '//div[@class="activity-template-cell-imglist"]/span/b')
        return self.wait.wait_find_element(locator).text

    @teststep
    def activity_source_img(self):
        """活动资源 图片"""
        locator = (By.XPATH, '//img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def activity_source_name(self):
        """活动资源 名"""
        locator = (By.XPATH, '//span[@class="activity-template-cell-book-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def play_title(self):
        """玩法 title"""
        locator = (By.XPATH, '//div[@id="activity-template-cell"]/div/span/b')
        return self.wait.wait_find_element(locator).text

    @teststep
    def play_content(self):
        """玩法 内容"""
        locator = (By.XPATH, '//div[@id="activity-template-cell"]/div/span/span[@class="activity-template-cell-desc"]')
        return self.wait.wait_find_element(locator).text

    # 班级列表
    @teststep
    def publish_activity(self):
        """发布打卡活动 title"""
        locator = (By.XPATH, '//div[@id="activity-template-class-cell"]/span/b')
        ele = self.wait.wait_find_elements(locator)[-1].text
        print(ele)

    @teststep
    def choose_button(self):
        """班级 单选框"""
        locator = (By.XPATH, '//i[@class="van-icon van-icon-success"]/parent::div')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def van_name(self):
        """班级 名称"""
        locator = (By.XPATH, '//div[@id="activity-template-class-cell"]/div[@class="van-cell__title"]/div')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def van_info(self):
        """班级 人数"""
        locator = (By.XPATH, '//div[@id="activity-template-class-cell"]')
        return self.wait.wait_find_elements(locator)[1:]

    @teststeps
    def share_preview_button(self):
        """分享预览 按钮"""
        locator = (By.XPATH, '//div[text()="分享预览"]')
        self.wait.wait_find_element(locator).click()
        print('点击 分享预览 按钮')

    @teststep
    def assign_button(self):
        """发布 按钮"""
        locator = (By.XPATH, '//div[text()="发布"]')
        self.wait.wait_find_element(locator).click()

    # 分享预览 页面
    @teststeps
    def wait_check_preview_page(self, var=15):
        """以“van-image van-image-preview__image”为依据"""
        locator = (By.XPATH, '//div[@class="van-image van-image-preview__image"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def preview_img(self):
        """打卡活动名称 title"""
        locator = (By.XPATH, '//img[@class="van-image__img"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def click_block(self):
        """点击 空白处"""
        ClickBounds().click_bounds(540, 200)

    @teststeps
    def choose_class_operation(self):
        """选择班级 学生"""
        MyAssert().assertTrue_new(self.wait_check_list_page(), self.detail_list_tips)
        print('----------------------------')
        button = self.choose_button()  # 单选框
        van = self.van_name()  # 班级 元素

        choose = 0
        count = 0
        for k in range(len(button)):
            name = van[k].text.split('\n')[0]
            if all([button[k].get_attribute("class") == 'van-checkbox__icon van-checkbox__icon--round',
                name != GetVariable().VANCLASS]):
                count += 1
                print('所选择的班级:', name)
                choose = name
                button[k].click()
                print('-----------------------------')
                break

        if self.wait_check_list_page():
            self.swipe_vertical_web(0.5, 0.2, 0.9)

        if count == 0:
            print('暂无可选择班级')
            return None
        else:
            return choose

    @teststeps
    def wait_check_tips_page(self, var=15):
        """以“温馨提示”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def publish_tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[text()="点击“确认”后，学生即可收到活动并参与，确认布置？"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//span[text()="取消"]/parent::button')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def confirm_button(self):
        """确认 按钮"""
        locator = (By.XPATH, '//span[text()="确认"]/parent::button')
        self.wait\
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
