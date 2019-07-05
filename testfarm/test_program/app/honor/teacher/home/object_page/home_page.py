#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import re
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.utils.click_bounds import ClickBounds
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class ThomePage(BasePage):
    """app主页面元素信息"""
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
        locator = (By.ID, gv.PACKAGE_ID + "class_info")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_image_page(self):
        """班级列表数据过多时，滑屏后是否在第一页，以轮播图为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "notice_img")
        return self.wait.wait_check_element(locator, 3)

    @teststep
    def wait_check_empty_tips_page(self, var=3):
        """暂时没有数据"""
        locator = (By.ID, gv.PACKAGE_ID + "load_empty")
        return self.wait.wait_check_element(locator, var)

    # 菜单栏
    @teststep
    def spoken_icon(self):
        """口语icon"""
        self.driver\
            .find_elements_by_id(gv.PACKAGE_ID + "notice")[0]\
            .click()

    @teststep
    def spoken_text(self):
        """口语"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type_text")[0].text
        print(ele)

    @teststep
    def hw_icon(self):
        """习题icon"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "notice")[1]\
            .click()

    @teststep
    def hw_text(self):
        """习题"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type_text")[1].text
        print(ele)

    @teststep
    def paper_icon(self):
        """试卷icon"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "notice")[2] \
            .click()

    @teststep
    def paper_text(self):
        """试卷"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type_text")[2].text
        print(ele)

    @teststep
    def word_icon(self):
        """单词本icon"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "notice")[3] \
            .click()

    @teststep
    def word_text(self):
        """单词本"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type_text")[3].text
        print(ele)

    @teststep
    def listen_icon(self):
        """每日一听icon"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "notice")[4] \
            .click()

    @teststep
    def listen_text(self):
        """每日一听"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type_text")[4].text
        print(ele)

    @teststep
    def add_class_button(self):
        """以“创建班级 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "add_class") \
            .click()

    @teststep
    def class_sort_button(self):
        """以“排序 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "class_sort") \
            .click()

    # 班级列表
    @teststeps
    def wait_check_van_page(self):
        """以“有无班级”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "class_info")
        return self.wait.wait_check_element(locator)

    @teststep
    def item_detail(self):
        """首页 条目名称  班号+班级名"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "class_info")
        return item

    @teststep
    def vanclass_name(self, var):
        """班级名"""
        value = re.sub(r'\[.*?\]', '', var)
        return value

    @teststep
    def vanclass_no(self, var):
        """班号"""
        m = re.match(".*\[(.*)\].*", var)  # title中有一个括号
        value = re.findall(r'\d+(?#\D)', m.group(1))
        return value[0]

    @teststep
    def st_count(self):
        """学生人数"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "student_num")
        return item

    @teststep
    def timing_button(self):
        """以“定时作业 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "draft") \
            .click()

    @teststep
    def assign_hw_button(self):
        """右下角“布置作业 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "add_hw") \
            .click()

    @teststep
    def unread_point(self):
        """未读 小红点"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "unread")
        return ele

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.CLASS_NAME, "android.widget.ImageButton")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            self.driver \
                .find_element_by_class_name("android.widget.ImageButton").click()
        except:
            raise

    @teststeps
    def all_element(self):
        """页面内所有class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        #
        # print('===========')
        # for i in range(len(ele)):
        #     print(ele[i].text)
        # print('==========')
        return ele

    # 公共元素- 底部三个tab元素：首页、题库、个人中心
    @teststep
    def click_tab_hw(self):
        """以“首页tab”的id为依 据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + 'tab_hw')\
            .click()

    @teststep
    def click_tab_test_bank(self):
        """以“题库tab”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'tab_bank') \
            .click()

    @teststep
    def click_tab_profile(self):
        """以“个人中心tab”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'tab_profile')\
            .click()

    # 温馨提示 页面
    @teststeps
    def wait_check_tips_page(self, var=3):
        """以“icon”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "md_title")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_title").text
        print(item)
        return item

    @teststep
    def tips_content(self):
        """温馨提示 具体内容"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_content").text
        print(item)
        return item

    @teststep
    def never_notify(self):
        """不再提醒"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_promptCheckbox") \
            .click()

    @teststeps
    def wait_check_input_page(self, var=5):
        """以“icon”为依据"""
        locator = (By.ID, "android:id/input")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def input(self):
        """输入框"""
        ele = self.driver \
            .find_element_by_id("android:id/input")
        return ele

    @teststep
    def character_num(self):
        """字符数"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_minMax").text
        print(ele)
        return ele

    @teststeps
    def click_block(self):
        """点击空白处 取消修改"""
        ClickBounds().click_bounds(360, 100)

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_buttonDefaultNegative") \
            .click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_buttonDefaultPositive") \
            .click()

    @teststep
    def commit(self):
        """确定 按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_buttonDefaultPositive")
        return ele

    @teststep
    def open_menu(self, ele):
        """条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(1000).release().perform()

    @teststep
    def menu_item(self, index):
        """条目 左键长按菜单"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "md_title")[index] \
            .click()

    @teststeps
    def tips_content_commit(self):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.commit_button()  # 确定按钮
            print('--------------------------')

    @teststeps
    def tips_content_cancel(self):
        """温馨提示 页面信息  -- 取消"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.cancel_button()  # 取消按钮
            print('--------------------------')

    @teststeps
    def tips_commit(self):
        """温馨提示 -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.commit_button()  # 确定按钮

    @teststeps
    def tips_cancel(self):
        """温馨提示 -- 取消"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.cancel_button()  # 取消按钮

    @teststeps
    def into_vanclass_operation(self, var):
        """进入班级"""
        if self.wait_check_list_page():
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            name = self.item_detail()  # 班号+班级名
            for i in range(len(name)):
                van = self.vanclass_name(name[i].text)  # 班级名
                if van == var:
                    print('进入班级:', var)
                    name[i].click()  # 进入班级
                    break

