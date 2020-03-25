#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.wait_element import WaitElement


class SpokenPage(BasePage):
    """题单详情 页面"""
    menu_detail_tips = '★★★ Error- 未进入题单详情页面'
    menu_detail_list_tips = '★★★ Error- 题单详情页面未加载成功'

    def __init__(self):
        self.wait = WaitElement()
        self.question = TestBankPage()
        self.basket = TestBasketPage()
        self.home = ThomePage()

    @teststeps
    def wait_check_page(self):
        """以“title:题详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'详情')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self, var=10):
        """以“题单详情页面  列表是否已加载出来”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "title")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def recommend_button(self):
        """推荐到学校 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "recommend") \
            .click()
        time.sleep(2)

    @teststep
    def collect_button(self):
        """收藏/取消收藏 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "collect") \
            .click()
        time.sleep(1)

    @teststep
    def put_to_basket_button(self):
        """加入题筐 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "add_pool") \
            .click()
    
    @teststeps
    def add_to_basket(self, ques_index=2):
        """加题单 进 题筐"""
        if self.question.wait_check_game_type_page():  # 页面检查点
            item = self.question.question_name()  # 获取
            item[0][ques_index].click()  # 点击第3道题

            if self.wait_check_page():  # 页面检查点
                if self.wait_check_list_page():
                    print('加题进题筐')
                    self.put_to_basket_button()  # 点击加入题筐按钮

                    if self.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回按钮

                        if self.question.wait_check_page('搜索'):  # 页面检查点
                            self.question.question_basket_button()  # 题筐按钮

                            if self.basket.wait_check_page():  # 页面检查点
                                if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                    print('★★★ Error- 加入题筐失败')

                                    self.home.back_up_button()
                                    if self.question.wait_check_page('搜索'):  # 页面检查点
                                        self.home.click_tab_hw()  # 返回 主界面
                                elif self.basket.wait_check_list_page():
                                    return True
                            else:
                                print('未进入 题筐页面')
                        else:
                            print('未返回 题库页面')
            else:
                print('未进入 题单详情页')

            return False
