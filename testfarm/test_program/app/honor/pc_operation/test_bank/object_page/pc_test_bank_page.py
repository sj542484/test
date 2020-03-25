#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By
from pynput.mouse import Controller

from conf.base_page import BasePage
from conf.decorator_pc import teststeps
from app.honor.pc_operation.tools.wait_element import WaitElement


class TestBankPage(BasePage):
    """题库界面"""

    def __init__(self, driver):
        self.wait = WaitElement(driver)
        self.mouse = Controller()

    @teststeps
    def wait_check_page(self, var=15):
        """以 进入我的题库 按钮 元素 的xpath为依据"""
        locator = (By.XPATH, '//a[@class="right-link"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_no_page(self, index=5):
        """以  暂无数据 元素 的xpath为依据"""
        locator = (By.XPATH, '//div[@id="empty-block"]')
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def our_school_button(self):
        """本校 按钮"""
        locator = (By.XPATH, '//a[text()="本校"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def recommend_author(self):
        """推荐人"""
        locator = (By.XPATH, '//td[text()="推荐人"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def choose_button(self):
        """单选框"""
        locator = (By.XPATH, '//span[@class="el-checkbox__inner"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def out_bank_button(self):
        """移出本校题库 按钮"""
        locator = (By.XPATH, '//a[text()="移出本校题库"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def wait_check_menu_list_page(self, var=15):
        """以 推荐人  元素 的xpath为依据"""
        locator = (By.XPATH, '//a[@class="tab active" and text()="题单"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_games_list_page(self, var=15):
        """以 推荐人  元素 的xpath为依据"""
        locator = (By.XPATH, '//a[@class="tab active" and text()="大题"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_paper_list_page(self, var=15):
        """以 推荐人  元素 的xpath为依据"""
        locator = (By.XPATH, '//a[@class="tab active" and text()="试卷"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def menu(self):
        """ 题单"""
        locator = (By.XPATH, '//div[@class="tab-group"]/a[text()="题单"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def games(self):
        """ 大题"""
        locator = (By.XPATH, '//div[@class="tab-group"]/a[text()="大题"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def paper(self):
        """ 大题"""
        locator = (By.XPATH, '//div[@class="tab-group"]/a[text()="试卷"]')
        self.wait.wait_find_element(locator).click()

    # 题单 温馨提示 页面
    @teststeps
    def wait_check_menu_tips_page(self, var=5):
        """以 el-message-box 元素 的xpath为依据"""
        locator = (By.XPATH, '//div[@class="el-message-box__title"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def tips_title_menu(self):
        """温馨提示title"""
        locator = (By.XPATH, '//div[@class="el-message-box__title"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def tips_content_menu(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="el-message-box__message"]/p[text()="确认移出则本校题库不再显示该资源，对已经布置的作业、卷子等不会影响使用。"]')
        return self.wait.wait_find_element(locator).text

    # 大题 温馨提示 页面
    @teststeps
    def wait_check_games_tips_page(self, var=5):
        """以 el-message-box 元素 的xpath为依据"""
        locator = (By.XPATH, '//span[@class="el-dialog__title"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def tips_title_games(self):
        """温馨提示title"""
        locator = (By.XPATH, '//span[@class="el-dialog__title"]')
        return self.wait.wait_find_elements(locator)[-1].text

    @teststeps
    def tips_content_games(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="notice" and text()="确认移出则本校题库不再显示该资源，对已经布置的作业、卷子等不会影响使用。"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//span[text()="取消"]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//span[contains(text(), "确定")]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def games_commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//span[text()="确定"]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def menu_tips_content(self):
        """温馨提示"""
        print('--------------------------')
        if self.wait_check_menu_tips_page():
            print(self.tips_title_menu())
            self.tips_content_menu()
            self.commit_button()  # 确定按钮
        print('--------------------------')

    @teststeps
    def games_tips_content(self):
        """温馨提示"""
        print('--------------------------')
        if self.wait_check_games_list_page():
            # print(self.tips_title_games())
            self.tips_content_games()
            self.games_commit_button()  # 确定按钮
        print('--------------------------')
