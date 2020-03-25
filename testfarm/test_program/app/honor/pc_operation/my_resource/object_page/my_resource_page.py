#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By
from conf.decorator import teststeps, teststep
from app.honor.pc_operation.tools.wait_element import WaitElement


class MyResourcePage():
    """我的题库界面"""
    establish_locator = (By.LINK_TEXT, "创建新题")
    page_button_value = '//ul[@class="el-pager"]/li'

    def __init__(self, driver):
        self.wait = WaitElement(driver)
        self.driver = driver

    @teststeps
    def wait_check_page(self, index=10):
        """以  创建新题 元素 的xpath为依据"""
        locator = (By.LINK_TEXT, "创建新题")
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def establish_question_btn(self):
        """创建新题 按钮"""
        time.sleep(1)
        self.wait \
            .wait_find_element(self.establish_locator).click()

    @teststeps
    def manage_recommend_btn(self):
        """创建新题 按钮"""
        time.sleep(1)
        locator = (By.LINK_TEXT, "管理推荐题")
        self.wait\
            .wait_find_element(locator).click()

    @teststeps
    def menu_tab(self):
        """题单 tab"""
        locator = (By.XPATH, '//a[text()="题单"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def game_list_tab(self):
        """大题 tab"""
        locator = (By.XPATH, '//a[text()="大题"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def test_paper_tab(self):
        """试卷 tab"""
        locator = (By.XPATH, '//a[text()="试卷"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_menu_name_not(self):
        """切换到大题tab, 等待 元素 题单名称 消失"""
        locator = (By.XPATH, '//td[contains(text(),"题单名称")]')
        return self.wait.wait_until_not_element(locator, 5)

    @teststeps
    def collect_tab(self):
        """收藏"""
        locator = (By.XPATH, '//a[text()="收藏"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def mine_tab(self):
        """我的"""
        locator = (By.XPATH, '//a[text()="我的"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_upload_not(self):
        """切换到我的tab, 等待 元素 上传者 消失"""
        locator = (By.XPATH, '//td[text()="上传者"]')
        return self.wait.wait_until_not_element(locator, 5)

    # 我的tab
    @teststeps
    def wait_check_mine_game_page(self, index=10):
        """以  创建新题 元素 的xpath为依据"""
        locator = (By.XPATH, "//span[contains(text(),'全部分类')]")
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def add_public_test_bank_tab(self):
        """ 加入公共题库  按钮"""
        time.sleep(2)
        locator = (By.XPATH, '//span[text()=" 加入公共题库"]')
        self.wait \
            .wait_find_element(locator).click()

    # 我的题单列表
    @teststep
    def choose_button(self):
        """ 单选框"""
        locator = (By.XPATH, '//label[@class="el-checkbox"]')
        return self.wait.wait_find_elements(locator)[1:]

    @teststep
    def hw_type(self):
        """游戏/作业 类型"""
        locator = (By.XPATH, '//div[@class="testbank-name small large"]/span[@class="type"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def hw_name(self):
        """游戏/作业 名称"""
        locator = (By.XPATH, '//div[@class="testbank-name small large"]/span[@class="title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def hw_num(self, index):
        """游戏/作业 名称"""
        locator = (By.XPATH, '//*[@id="page-content"]/div/div[2]/table/tbody/tr[{}]/td[3]'.format(index))
        return self.wait.wait_find_element(locator).text

    @teststep
    def choose_count(self):
        """班级 描述"""
        locator = (By.XPATH, '//label[@class="el-checkbox"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def assign_button(self):
        """发布作业 按钮"""
        self.driver \
            .find_element_by_id('gv.PACKAGE_ID + "action_first"') \
            .click()

    # game列表
    @teststep
    def game_name(self):
        """游戏/作业 名称"""
        locator = (By.XPATH, '//div[@class="testbank-name"]/span[@class="title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def judge_page_button(self, var=5):
        """判断是否有 页面跳转按钮"""
        locator = (By.XPATH, self.page_button_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def next_page_button(self):
        """下一页 按钮"""
        self.driver \
            .find_element_by_xpath('//button[@class="btn-next"]') \
            .click()

    @teststep
    def page_button(self):
        """页面跳转 按钮"""
        time.sleep(1)
        locator = (By.XPATH, self.page_button_value)
        ele = self.wait.wait_find_elements(locator)
        return ele

    # 题单详情页
    @teststep
    def hw_title(self):
        """游戏/作业 类型"""
        locator = (By.XPATH, '//div[@class="title"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def chrome_back_button(self):
        """chrome 后退按钮"""
        self.driver.back()  # back
        self.driver.back()  # back
