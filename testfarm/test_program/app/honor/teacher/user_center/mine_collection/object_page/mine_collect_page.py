#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.wait_element import WaitElement


class CollectionPage(BasePage):
    """我的收藏 页面"""
    label_manage_value = "//android.widget.TextView[contains(@text,'标签管理')]"

    def __init__(self):
        self.filter = FilterPage()
        self.wait = WaitElement()
        self.question = TestBankPage()
        self.home = ThomePage()

    @teststeps
    def wait_check_page(self):
        """以“title:我的收藏”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的收藏')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“存在 我的收藏列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator)

    @teststep
    def more_button(self):
        """以“更多 按钮”的class name为依据"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView") \
            .click()

    @teststeps
    def wait_check_label_manage_page(self):
        """以“存在 我的收藏列表”的text为依据"""
        locator = (By.XPATH, self.label_manage_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def label_manage_button(self):
        """以“标签管理 按钮”的class name为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'标签管理')]") \
            .click()

    @teststep
    def the_end(self):
        """以“没有更多了”的text为依据"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'没有更多了')]") \
            .text
        return item

    @teststep
    def question_basket(self):
        """以 右下角“题筐 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_pool") \
            .click()

    @teststep
    def menu_button(self, index):
        """以 条目右侧“菜单按钮”的id为依据"""
        self.driver\
            .find_elements_by_id(gv.PACKAGE_ID + "iv_eg")[index] \
            .click()
        time.sleep(1)

    # 标签管理
    @teststeps
    def wait_check_manage_page(self):
        """以“title:标签管理”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'标签管理')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_manage_list_page(self):
        """以“”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_label_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def label_title(self):
        """label title"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")
        return item

    @teststep
    def open_menu(self, ele):
        """标签条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(500).release().perform()

    @teststep
    def menu_item(self, index):
        """标签条目 左键长按菜单"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "md_title")[index] \
            .click()

    # 菜单 内容  # 检查点：home_page.py的 wait_check_tips_page()
    @teststep
    def put_to_basket(self):
        """以 菜单- 加入题筐 的text为依据"""
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'加入题筐')]") \
            .click()

    @teststep
    def stick_label(self):
        """以 菜单- 贴标签 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'贴标签')]") \
            .click()

    @teststep
    def recommend_to_school(self):
        """以 菜单- 推荐到学校 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'推荐到学校')]") \
            .click()

    @teststep
    def cancel_collection(self):
        """以 菜单- 取消收藏 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消收藏')]") \
            .click()

    # 贴标签
    @teststeps
    def wait_check_label_page(self):
        """以“title:贴标签”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'贴标签')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def save_button(self):
        """以 贴标签 - 保存按钮 的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "certain") \
            .click()

    @teststep
    def check_box(self, index):
        """以 贴标签 - 单选框 的id为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "cb_checked")[index] \
            .click()

    @teststep
    def add_label(self):
        """以 贴标签 - 创建标签 的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fb_add_label") \
            .click()

    @teststeps
    def verify_collect_result(self, menu, var='题单'):
        """验证 添加收藏 结果"""
        if self.wait_check_page():
            print('------------------验证 -收藏结果------------------')
            if var == '大题':
                TuserCenterPage().filter_button()  # 筛选按钮
                if FilterPage().wait_check_page():
                    TuserCenterPage().click_game_list()  # 点击大题
                    FilterPage().commit_button()  # 确定按钮
            elif var == '试卷':
                TuserCenterPage().filter_button()  # 筛选按钮
                if FilterPage().wait_check_page():
                    TuserCenterPage().click_test_paper()  # 点击试卷
                    FilterPage().commit_button()  # 确定按钮

            if self.wait_check_page():
                if self.wait_check_list_page():
                    item = TestBankPage().question_name()  # 获取
                    menu1 = item[1][0]
                    if '提分' in menu:
                        menu = menu[:-2]
                    if menu != menu1:
                        print('★★★ Error- 加入收藏失败', menu, menu1)
                    else:
                        print('加入收藏成功')
                        print('----------------')
                        for z in range(len(item[0])):
                            print(item[1][z])
                            if self.wait_check_page():
                                self.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入收藏的题单取消收藏

                                if self.home.wait_check_tips_page():
                                    self.cancel_collection()  # 取消收藏
                                    print('确定取消收藏')
                                    print('------------------')

            if self.wait_check_page():
                self.home.back_up_button()  # 返回个人中心页面
    
    @teststeps
    def cancel_collection_operation(self):
        """恢复测试数据 - 取消收藏"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_list_page():
                print('---------------------')
                print('恢复测试数据:')
                item = self.question.question_name()  # 获取
                for z in range(len(item[0])):
                    if self.wait_check_list_page():
                        name = self.question.question_name()  # 获取
                        print(name[1][0])
                        self.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入收藏的题单取消收藏

                        if self.home.wait_check_tips_page():
                            self.cancel_collection()  # 取消收藏
                            print('确定取消收藏')
                            print('------------------')
