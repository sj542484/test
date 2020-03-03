#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from utils.assert_package import MyAssert
from utils.click_bounds import ClickBounds
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class ThomePage(BasePage):
    """app主页面元素信息"""
    img_locator = (By.ID, gv.PACKAGE_ID + "notice_img")  # 轮播图
    tab_icon_locator = (By.ID, gv.PACKAGE_ID + "notice")  # 各tab icon
    tab_locator = (By.ID, gv.PACKAGE_ID + "type_text")  # 各tab
    vanclass_locator = (By.ID, gv.PACKAGE_ID + "class_info")  # 班级条目

    home_tips = '★★★ Error- 未进入主界面'
    van_list_tips = '★★★ Error- 无班级'
    back_home_tips = '★★★ Error- 未返回主界面'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=20):
        """以“title:最新动态”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'最新动态')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self):
        """以“有无班级”为依据"""
        return self.wait.wait_check_element(self.vanclass_locator)

    @teststeps
    def wait_check_image_page(self):
        """班级列表数据过多时，滑屏后是否在第一页，以轮播图为依据"""
        return self.wait.wait_check_element(self.img_locator, 3)

    @teststep
    def wait_check_empty_tips_page(self, var=3):
        """暂时没有数据"""
        locator = (By.ID, gv.PACKAGE_ID + "load_empty")
        return self.wait.wait_check_element(locator, var)

    # 轮播图
    @teststeps
    def wait_check_poll_img_page(self, var=20):
        """以“title:班级年报”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'班级年报')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def poll_img(self):
        """轮播图"""
        self.wait\
            .wait_find_element(self.img_locator).click()

    @teststep
    def poll_button(self):
        """轮播按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "indicator")
        return self.wait\
            .wait_find_elements(locator)[1:]

    # 菜单栏
    @teststep
    def hw_icon(self):
        """作业icon"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[0]\
            .click()

    @teststep
    def hw_text(self):
        """作业"""
        ele = self.wait \
            .wait_find_elements(self.tab_locator)[0].text
        print(ele)

    @teststep
    def paper_icon(self):
        """试卷icon"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[1] \
            .click()

    @teststep
    def paper_text(self):
        """试卷"""
        ele = self.wait \
            .wait_find_elements(self.tab_locator)[1].text
        print(ele)

    @teststep
    def word_icon(self):
        """单词本icon"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[2] \
            .click()

    @teststep
    def word_text(self):
        """单词本"""
        ele = self.wait \
            .wait_find_elements(self.tab_locator)[2].text
        print(ele)

    @teststep
    def listen_icon(self):
        """每日一听icon"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[3] \
            .click()

    @teststep
    def listen_text(self):
        """每日一听"""
        ele = self.wait \
            .wait_find_elements(self.tab_locator)[3].text
        print(ele)

    @teststep
    def punch_activity_icon(self):
        """打卡活动icon"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[4] \
            .click()

    @teststep
    def punch_activity_text(self):
        """打卡活动"""
        ele = self.wait \
            .wait_find_elements(self.tab_locator)[4].text
        print(ele)

    @teststep
    def add_class_button(self):
        """以“创建班级 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "add_class")
        self.wait \
            .wait_find_element(locator) \
            .click()

    @teststep
    def class_sort_button(self):
        """以“排序 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "class_sort")
        self.wait \
            .wait_find_element(locator) \
            .click()

    # 班级列表
    @teststep
    def item_detail(self):
        """首页 条目名称  班号+班级名"""
        return self.wait\
            .wait_find_elements(self.vanclass_locator)

    @teststep
    def vanclass_name(self, var):
        """班级名"""
        value = re.sub(r'\[.*?\]', '', var)
        return value

    @teststeps
    def vanclass_no(self, var):
        """班号"""
        m = re.match(r".*\[(.*)\].*", var)  # title中有一个中括号
        value = re.findall(r'\d+(?#\D)', m.group(1))
        return value[0]

    @teststep
    def st_count(self):
        """学生人数"""
        locator = (By.ID, gv.PACKAGE_ID + "student_num")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def timing_button(self):
        """以“定时作业 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "draft")
        self.wait.wait_find_element(locator).click()

    @teststep
    def assign_hw_button(self):
        """右下角“布置作业 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "add_hw")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def unread_point(self):
        """未读 小红点"""
        locator = (By.ID, gv.PACKAGE_ID + "unread")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.CLASS_NAME, "android.widget.ImageButton")
        self.wait\
            .wait_find_element(locator).click()

    # 公共元素- 底部三个tab元素：首页、题库、个人中心
    @teststep
    def click_tab_hw(self):
        """以“首页tab”的id为依 据"""
        locator = (By.ID, gv.PACKAGE_ID + "tab_hw")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def click_tab_test_bank(self):
        """以“题库tab”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tab_bank")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def click_tab_profile(self):
        """以“个人中心tab”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tab_profile")
        self.wait \
            .wait_find_element(locator).click()

    # 温馨提示 页面
    @teststeps
    def wait_check_tips_page(self, var=3):
        """以“icon”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "md_title")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.ID, gv.PACKAGE_ID + "md_title")
        ele = self.wait.wait_find_element(locator)
        print(ele.text)
        return ele

    @teststep
    def tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.ID, gv.PACKAGE_ID + "md_content")
        ele = self.wait \
            .wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def never_notify(self):
        """不再提醒"""
        locator = (By.ID, gv.PACKAGE_ID + "md_promptCheckbox")
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_check_input_page(self, var=5):
        """以“icon”为依据"""
        locator = (By.ID, "android:id/input")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def input(self):
        """输入框"""
        locator = (By.ID, "android:id/input")
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def character_num(self):
        """字符数"""
        locator = (By.ID, gv.PACKAGE_ID + "md_minMax")
        return self.wait \
            .wait_find_element(locator).text

    @teststeps
    def click_block(self):
        """点击空白处 取消修改"""
        ele = self.tips_title()  # 修改窗口 提示信息
        x = ele.location['x']
        y = ele.location['y']
        print(x+200, y-400)
        ClickBounds().click_bounds(x+200, y-400)

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "md_buttonDefaultNegative")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "md_buttonDefaultPositive")
        return self.wait.wait_find_element(locator)

    @teststep
    def open_menu(self, ele):
        """条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(1000).release().perform()

    @teststep
    def menu_item(self, index):
        """条目 左键长按菜单"""
        locator = (By.ID, gv.PACKAGE_ID + "md_title")
        self.wait \
            .wait_find_elements(locator)[index].click()

    @teststeps
    def tips_content_commit(self, var=5):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page(var):  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.commit_button().click()  # 确定按钮
            print('--------------------------')

    @teststeps
    def tips_content_cancel(self, var=5):
        """温馨提示 页面信息  -- 取消"""
        if self.wait_check_tips_page(var):  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.cancel_button()  # 取消按钮
            print('--------------------------')

    @teststeps
    def tips_commit(self):
        """温馨提示 -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.commit_button().click()  # 确定按钮

    @teststeps
    def tips_cancel(self):
        """温馨提示 -- 取消"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.cancel_button()  # 取消按钮

    @teststeps
    def tips_never_cancel(self):
        """温馨提示 页面信息  -- 有 不再提醒 元素"""
        if self.wait_check_tips_page():
            print('------------------------------------------', '\n',
                  '温馨提示 页面:')
            self.tips_title()
            self.tips_content()
            self.never_notify()  # 不再提醒
            self.cancel_button()  # 取消按钮

    @teststep
    def brackets_text_out(self, var):
        """去掉作业title的 括号及text """
        value = re.sub(r"\(.*?\)$|\\（.*?\\）$", "", var)
        return value

    @teststep
    def brackets_text_in(self, var):
        """取出 作业title的 括号中的text"""
        if '(' in var:
            m = re.compile(r'[(](.*?)[)]', re.S)
            var = re.findall(m, var)[0]  # title中有一个括号

        return var

    @teststeps
    def into_vanclass_operation(self, var):
        """进入 班级"""
        MyAssert().assertTrue_new(self.wait_check_list_page(), self.van_list_tips)
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
        MyAssert().assertTrue_new(self.wait_check_list_page(), self.van_list_tips)
        name = self.item_detail()  # 班号+班级名
        for i in range(len(name)):
            van = self.vanclass_name(name[i].text)  # 班级名
            if van == var:
                print('进入班级:', var)
                name[i].click()  # 进入班级
                break

    @teststeps
    def wait_check_permission(self):
        """录音权限申请"""
        locator = (By.ID, "com.lbe.security.miui:id/permission_message")
        return self.wait.wait_check_element(locator, 5)

    @teststep
    def allow_button(self):
        """允许 按钮"""
        locator = (By.XPATH, '//android.widget.Button[contains(@text, "允许")]')
        self.wait.wait_find_element(locator, 5).click()
