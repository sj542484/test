#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re

from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class TestBasketPage(BasePage):
    """题筐 页面"""
    basket_tips = '★★★ Error- 未进入题筐页面'
    back_basket_tips = '★★★ Error- 未返回题筐页面'
    basket_list_tips = '★★★ Error- 题筐内暂无数据'

    def __init__(self):
        self.wait = WaitElement()
        self.question = TestBankPage()
        self.filter = FilterPage()
        self.home = ThomePage()
        self.detail = QuestionDetailPage()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self):
        """以“title:题筐”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题筐')]")
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.basket_tips)
        return ele

    @teststeps
    def wait_check_list_page(self, var=20):
        """以“题筐是否有题”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def empty_text(self):
        """以“空白页”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + 'load_empty')
        ele = self.wait.wait_find_element(locator).text
        print(ele)

    @teststep
    def question_name(self):
        """以“题目名称”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "test_bank_name")
        ele = self.wait \
            .wait_find_elements(locator)

        content = [x.text for x in ele]
        return ele, content

    @teststep
    def all_check_button(self):
        """以“全选按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + 'select_all')
        self.wait.wait_find_element(locator) \
            .click()

    @teststep
    def check_button(self):
        """以“单选按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "cb_add")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def question_type(self):
        """以“类型”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "type")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def question_num(self):
        """以“共x题”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "exercise_num")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def question_author(self):
        """以“作者”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def out_basket_button(self):
        """以“移出题筐 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "action_first")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def assign_button(self):
        """以“布置作业 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "action_second")
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def last_judge(self, var):
        """最后一个元素 resource-id属性值是否为作者"""
        value = GetAttribute().resource_id(var)
        if value == gv.PACKAGE_ID + "author":
            return True
        else:
            return False

    @teststeps
    def add_to_basket(self, ques_index=2):
        """加题单 进 题筐"""
        if self.question.wait_check_page():  # 页面检查点
            self.question_name()[0][ques_index].click()  # 点击第ques_index道题

            if self.detail.wait_check_page():  # 页面检查点
                if self.detail.wait_check_list_page():  # 页面检查点
                    print('加题单进题筐')
                    self.detail.all_check_button()  # 全选按钮
                    if self.detail.wait_check_list_page():  # 页面检查点
                        self.detail.put_to_basket_button()  # 点击加入题筐按钮

                        if self.detail.wait_check_list_page():  # 页面检查点
                            self.home.back_up_button()  # 返回按钮

                            if self.detail.wait_check_list_page():  # 页面检查点
                                self.question.question_basket_button()  # 题筐按钮

                                if self.wait_check_page():  # 页面检查点
                                    if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                        print('★★★ Error- 加入题筐失败')

                                        self.home.back_up_button()
                                        if self.question.wait_check_page():  # 页面检查点
                                            self.home.click_tab_hw()  # 返回 主界面
                                        return False
                                    elif self.wait_check_list_page():
                                        return True

    @teststeps
    def basket_ready_operation(self):
        """ 查看目前题筐还差多少题"""
        num = 0
        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.question.question_basket_button()  # 题筐 按钮
            if self.wait_check_page():  # 页面检查点
                if self.wait_check_list_page():  # 题筐有题
                    self.all_check_button()  # 全选按钮
                    ele = self.assign_button()  # 布置作业 按钮
                    num = 50 - int(re.sub("\D", "", ele.text))  # 提取 题数
                elif self.home.wait_check_empty_tips_page():  # 暂无数据
                    self.empty_text()
                    num = 50
                    print('-------------------------------------------')

            return num

    @teststeps
    def back_basket_operation(self):
        """ 返回题筐底部"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_list_page():  # 页面检查点
                self.all_check_button()  # 全选按钮
                ele = self.assign_button()  # 布置作业 按钮
                num = 50 - int(re.sub("\D", "", ele.text))  # 提取 题数

                if self.wait_check_list_page():  # 页面检查点
                    self.all_check_button()  # 全选按钮
                    if num > 6:
                        var = num // 6 + 1
                        while var > 0:
                            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
                            var -= 1

    @teststeps
    def judge_add_basket_operation(self, names):
        """滑屏到题筐底部 进行加入题筐验证"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_list_page():  # 页面检查点
                self.all_check_button()  # 全选按钮
                ele = self.assign_button()  # 布置作业 按钮
                num = 50 - int(re.sub("\D", "", ele.text))  # 提取 题数

                count = []
                var = num // 6 + 1
                while var > 0:
                    self.my_assert.assertTrue(self.wait_check_list_page(), self.basket_list_tips)  # 页面检查点
                    item = self.question_name()[1]  # 获取题目

                    index = -1
                    length = len(item)-1
                    if len(item) > 5:
                        length = len(item) - 2
                        index = 0
                    for i in range(length, index, -1):
                        for j in range(len(names)):
                            if item[i] == names[j]:
                                print(item[i])
                                count.append(i)
                                break

                    if not count:
                        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
                    var -= 1

                print('----------------------------')
                if self.wait_check_page():
                    self.home.back_up_button()  # 返回 题库页面
                    self.my_assert.assertFalse(len(count) == 0, '★★★ Error -加入题筐失败, {}'.format(names))
                    print('加入题筐成功')
