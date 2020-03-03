#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator_vue import teststep, teststeps
from utils.wait_element_vue import WaitElement


class InviteStPage(BasePage):
    """ 邀请学生 详情页面"""
    wechat_friend_value = gv.PACKAGE_ID + "weixin"  # 微信好友
    invite_vue_tips = '★★★ Error- 未进入班级 邀请学生详情vue页'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title: 邀请学生”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="邀请学生"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def vanclass_name(self):
        """班级名"""
        locator = (By.XPATH, '//span[@class="invitation-background-content-title"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def vanclass_num(self):
        """班号"""
        locator = (By.XPATH, '//span[@class="invitation-background-content-title"]')
        ele = self.wait.wait_find_elements(locator)[1].text
        print(ele)
        return ele

    @teststep
    def hint_content(self):
        """提示 具体内容"""
        locator = (By.XPATH, '//span[@class="invitation-background-content-desc"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def share_button(self):
        """分享按钮"""
        locator = (By.XPATH, '//span[@class="invitation-background-content-bottom-desc"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def copy_link_button(self):
        """复制链接 按钮"""
        locator = (By.XPATH, '//span[@class="invitation-background-content-bottom-desc"]')
        self.wait.wait_find_elements(locator)[1].click()

    @teststep
    def copy_no_button(self):
        """复制班号 按钮"""
        locator = (By.XPATH, '//span[@class="invitation-background-content-bottom-desc"]')
        self.wait.wait_find_elements(locator)[2].click()

    # 分享控件
    @teststeps
    def wait_check_share_page(self):
        """以“微信好友”为依据"""
        locator = (By.ID, self.wechat_friend_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def wechat_friend(self):
        """微信好友"""
        locator = (By.XPATH, '//div[@class="class-score-star-cell-title"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def wechat_friends(self):
        """朋友圈 """
        locator = (By.XPATH, '//div[@class="class-score-star-cell-title"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def wait_check_share_wechat_page(self, var=5):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'微信号/QQ/邮箱登录')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def wechat_back_button(self):
        """微信好友 返回"""
        locator = (By.CLASS_NAME, "android.widget.ImageView")
        self.wait.wait_find_element(locator).click()

    @teststeps
    def wait_check_share_not_login_page(self, var=5):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'由于登录过期，请重新登录。无法分享到微信')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def back_up_button(self):
        """微信好友 返回"""
        locator = (By.CLASS_NAME, "android.widget.Button")
        self.wait.wait_find_element(locator).click()
