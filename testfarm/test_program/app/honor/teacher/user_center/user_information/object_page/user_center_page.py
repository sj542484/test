#!/usr/bin/env python
# encoding:UTF-8
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.wait_element import WaitElement


class TuserCenterPage(BasePage):
    """个人中心 页面"""
    nickname_value = gv.PACKAGE_ID + 'name'  # 个人中心页面昵称

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=10):
        """以“消息”为依据"""
        locator = (By.ID, self.nickname_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def click_avatar_profile(self):
        """以“头像”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'avatar_profile') \
            .click()

    @teststep
    def nickname(self):
        """以“昵称”的id为依据"""
        ele = self.driver \
            .find_element_by_id(self.nickname_value) \
            .text
        return ele

    @teststep
    def click_mine_collection(self):
        """以“我的收藏”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'star') \
            .click()

    @teststep
    def click_mine_recommend(self):
        """以“我的推荐”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'recommend') \
            .click()

    @teststep
    def click_mine_bank(self):
        """以“我的题库”的id为依据"""
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'我的题库')]")\
            .click()

    @teststep
    def click_tiny_course(self):
        """以“微课”的class_name为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'微课')]") \
            .click()

    @teststep
    def click_message(self):
        """以“消息”的class_name为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'消息')]") \
            .click()

    @teststep
    def click_setting(self):
        """以“设置”的class_name为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'设置')]") \
            .click()


class HelpCenter(BasePage):
    """二级页面：帮助中心页面"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:帮助中心”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'帮助中心')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“VIEW”的CLASS NAME为依据"""
        locator = (By.CLASS_NAME, "android.view.View")
        return self.wait.wait_check_element(locator)

    @teststeps
    def view(self):
        """以“view”的class name为依据"""
        time.sleep(3)
        ele = self.driver\
            .find_elements_by_class_name("android.view.View")

        value = []
        for i in range(len(ele)):
            item = GetAttribute().description(ele[i])
            if (item is not None) and (item not in value):
                value.append(item)
                print(value[i])


class Copyright(BasePage):
    """版权申诉"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:版权申诉”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'版权申诉')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“VIEW”的CLASS NAME为依据"""
        locator = (By.CLASS_NAME, "android.view.View")
        return self.wait.wait_check_element(locator)

    @teststeps
    def content_view(self, value):
        """以“条款内容”的class name为依据"""
        ele = self.driver \
            .find_elements_by_class_name("android.view.View")

        for i in range(len(ele)):
            item = GetAttribute().description(ele[i])
            print(item)
            if (item is not None) and (item not in value):
                value.append(item)
                print(item)
        print('------------------------------------')


class ProtocolPage(BasePage):
    """注册协议"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:注册协议”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'注册协议')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“view”的CLASS NAME为依据"""
        locator = (By.CLASS_NAME, "android.webkit.WebView")
        return self.wait.wait_check_element(locator)

    @teststeps
    def content_view(self, value):
        """以“条款内容”的class name为依据"""
        ele = self.driver \
            .find_elements_by_class_name("android.view.View")

        for i in range(len(ele)):
            item = GetAttribute().description(ele[i])
            if (item is not None) and (item not in value):
                value.append(item)
                print(item)
