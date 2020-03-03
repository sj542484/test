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
from utils.get_attribute import GetAttribute
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

    @teststeps
    def wait_check_page(self):
        """以“title:题筐”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题筐')]")
        return self.wait.wait_check_element(locator)

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
    def all_question(self):
        """页面内所有 题目条目"""
        name = self.question_name()[1]  # 题目名称
        mode = self.question_type()  # 题目类型
        nums = self.question_num()  # 题目 小题数
        author = self.question_author()  # 题目作者

        for i in range(len(author)):
            print(name[i], '\n',
                  mode[i].text, '\n',
                  nums[i].text, '\n',
                  author[i].text)
            print('---------------')
        return len(name)

    @teststeps
    def add_to_basket(self, func, ques_index=2):
        """加题单 进 题筐"""
        if self.question.wait_check_game_type_page():  # 页面检查点
            self.question_name()[0][ques_index].click()  # 点击第ques_index道题

            if self.detail.wait_check_page():  # 页面检查点
                if func():
                    print('加题进题筐')
                    self.detail.all_check_button()  # 全选按钮
                    if self.wait_check_list_page():
                        self.detail.put_to_basket_button()  # 点击加入题筐按钮

                        if self.detail.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回按钮

                            if self.question.wait_check_page('搜索'):  # 页面检查点
                                self.question.question_basket()  # 题筐按钮

                                if self.wait_check_page():  # 页面检查点
                                    if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                        print('★★★ Error- 加入题筐失败')

                                        self.home.back_up_button()
                                        if self.question.wait_check_page('搜索'):  # 页面检查点
                                            self.home.click_tab_hw()  # 返回 主界面
                                    elif self.wait_check_list_page():
                                        return True
                                else:
                                    print('未进入 题筐页面')
                            else:
                                print('未返回 题库页面')
            else:
                print('未进入 题单详情页')
        else:
            print('未进入 题库页')
            return False

    @teststeps
    def basket_ready_operation(self):
        """ 查看目前题筐有多少题"""
        num = 0
        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.question.question_basket()  # 题筐 按钮

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
