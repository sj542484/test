#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class SettingPage(BasePage):
    """设置页面"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:设置”的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def help_center(self):
        """以“帮助中心”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "help") \
            .click()

    @teststep
    def help_center(self):
        """以“帮助中心”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "help")\
            .click()

    @teststep
    def copyright_complaints(self):
        """以“版权申诉”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "right") \
            .click()

    @teststep
    def regist_protocol(self):
        """以“注册协议”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "protocol") \
            .click()

    @teststep
    def version_check(self):
        """以“版本号”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "version_check") \
            .click()

    @teststep
    def version(self):
        """以“版本号”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "version") \
            .click()

    @teststep
    def logout_button(self):
        """以“退出登录按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "logout") \
            .click()

    @teststep
    def back_up_button(self):
        """以“返回按钮”的id为依据"""
        self.driver\
            .find_element_by_class_name("android.widget.ImageButton") \
            .click()

    @teststeps
    def logout_operation(self):
        """退出登录"""
        ThomePage().click_tab_profile()    # 进入首页后点击‘个人中心’按钮
        if TuserCenterPage().wait_check_page():  # 页面检查点
            TuserCenterPage().click_setting()  # 进入设置页面

            if self.wait_check_page():  # 页面检查点
                self.logout_button()  # 退出登录按钮
                ThomePage().tips_content_commit()  # 退出登录提示框
                # if not TloginPage().wait_check_page():
                #     print(' 退出登录失败 ')

    @teststep
    def logout(self):
        """退出登录"""
        ThomePage().back_up_button()  # 进入‘个人中心’页面
        if TuserCenterPage().wait_check_page():  # 页面检查点
            TuserCenterPage().click_setting()  # 进入设置页面

            if self.wait_check_page():  # 页面检查点
                self.logout_button()  # 退出登录按钮
                ThomePage().tips_content_commit()  # 退出登录提示框


class HelpCenter(BasePage):
    """二级页面：帮助中心页面"""

    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:帮助中心”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'帮助中心')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“VIEW”的CLASS NAME为依据"""
        locator = (By.XPATH, "//android.view.View[contains(@text,'我的助教')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def title(self):
        """以“title”的class name为依据"""
        ele = self.driver \
            .find_element_by_xpath('//android.view.ViewGroup/android.widget.TextView')
        print(ele.text)

    @teststeps
    def img(self):
        """以“二维码图片”的class name为依据"""
        ele = self.driver \
            .find_element_by_xpath('//android.webkit.WebView/android.widget.Image')
        return ele

    @teststeps
    def view(self):
        """以“view”的class name为依据"""
        ele = self.driver\
            .find_element_by_xpath('//android.webkit.WebView/android.view.View')
        print(ele.text)


class CopyRight(BasePage):
    """版权申诉"""
    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:版权申诉”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'版权申诉')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“VIEW”的CLASS NAME为依据"""
        locator = (By.XPATH, "//android.webkit.WebView/android.view.View")
        return self.wait.wait_check_element(locator)

    @teststeps
    def content_view(self, value):
        """以“条款内容”的class name为依据"""
        ele = self.driver \
            .find_elements_by_xpath("//android.webkit.WebView/android.view.View")

        for i in range(len(ele)):
            item = ele[i].text
            if (item is not None) and (item not in value):
                value.append(item)
                print(item)


class ProtocolPage(BasePage):
    """注册协议"""
    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:注册协议”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'注册协议')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“view”的CLASS NAME为依据"""
        locator = (By.XPATH, "//android.webkit.WebView/android.view.View")
        return self.wait.wait_check_element(locator)

    @teststeps
    def content_view(self, value):
        """以“条款内容”的class name为依据"""
        ele = self.driver \
            .find_elements_by_xpath("//android.webkit.WebView/android.webkit.WebView"
                                         "/descendant::android.view.View")

        for i in range(len(ele)):
            item = ele[i].text
            if (item is not None) and (item not in value):
                value.append(item)
                print(item)
