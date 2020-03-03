#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.wait_element_vue import WaitElement


class SpokenAnalysisDetailStudentPage(BasePage):
    """ 口语 答题分析 按学生看页面 及二级详情页面"""
    st_check_value = "//span[text()='按学生看']"
    st_item_value = "//div[@id='student-cell']"  # 按学生看 学生条目
    tab_class_value = 'van-tab van-tab--active'  # 按学生看tab 被选中时 class值

    @teststeps
    def __init__(self):
        self.home = ThomePage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“按学生看”为依据"""
        locator = (By.XPATH, self.st_check_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def check_tab_status(self, var):
        """按学生看/按题查看 tab 父元素  状态判断"""
        value = var.find_element_by_xpath('.//parent::div').get_attribute('class')
        return value

    @teststep
    def student_tab(self):
        """按学生看 tab"""
        locator = (By.XPATH, self.st_check_value)
        return self.wait.wait_find_elements(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“学生条目”为依据"""
        locator = (By.XPATH, self.st_item_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="van-image van-image--round"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_finish_status(self):
        """学生 完成与否"""
        locator = (By.XPATH, '//span[@class="student-cell-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="class="van-cell__title student-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def st_items(self):
        """学生 条目"""
        locator = (By.XPATH, self.st_item_value)
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_type(self):
        """基础班/提分版学生"""
        locator = (By.XPATH, '//div[@class="van-image van-icon__image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def finish_tab_st_items(self):
        """学生 条目"""
        ele = self.st_items()

        content = []  # 页面内所有条目 元素text
        elements = []  # 页面内所有条目元素
        for i in range(len(ele)):
            item = []  # 每一个条目的所有元素text
            element = []  # 每一个条目的所有元素
            descendant = ele[i].find_elements_by_xpath('.//descendant::*')[3:5]

            for j in range(len(descendant)):
                item.append(descendant[j].text)
                element.append(descendant[j])

            content.append(item)
            elements.append(element)

        return elements, content

    # 二级页面 答题分析详情页
    @teststeps
    def wait_check_detail_page(self):
        """以“title: 详情”为依据"""
        locator = (By.XPATH, "//div[text()='详情']")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_detail_list_page(self):
        """以“ star”为依据"""
        locator = (By.XPATH, '//div[@class="van-cell"]/div[@class="van-cell__title completion-detail-title-text"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def detail_st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-icon van-image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def detail_st_finish_status(self):
        """学生 完成与否"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-label van-rate"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def detail_st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//span[@class="completion-detail-header-title"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def detail_st_type(self):
        """学生 提分版/基础版/试用期"""
        locator = (By.XPATH, '//div[@class="van-image van-icon__image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def hint(self):
        """句子"""
        locator = (By.XPATH, '//div[@class="completion-detail-header"]/div[@class="completion-detail-header-tip"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def total_report(self):
        """报告"""
        locator = (By.XPATH, '//div[@class="spoken-detail-header-number"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def question(self):
        """题目"""
        locator = (By.XPATH, '//div[@class="van-cell__title completion-detail-title-text"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def star(self):
        """完成率"""
        locator = (By.XPATH, '//div[@class="completion-detail-label-text van-rate"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def speak_button(self):
        """发音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-swipe-size completion-detail-label-icon"]')
        return self.wait.wait_find_elements(locator)

    # 修改成绩
    @teststeps
    def wait_check_modify_achieve_page(self):
        """以“修改成绩”为依据"""
        locator = (By.XPATH, "//div[text()='修改成绩']")
        return self.wait.wait_check_element(locator)

    @teststep
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__confirm van-hairline--left"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def per_student_answer_detail(self):
        """student 答题情况详情页"""
        if self.wait_check_detail_list_page():
            self.detail_st_icon()  # 学生头像
            name = self.detail_st_name()  # 学生name
            self.detail_st_type()
            status = self.detail_st_finish_status()  # 学生完成与否
            print('-----------------------------')
            self.hint()  # 提示信息

            self.detail_operation()  # 详情页 具体操作

    @teststeps
    def detail_operation(self):
        """详情页 具体操作"""
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        games = self.question()  # 游戏题目
        speak = self.speak_button()  # 发音按钮
        for j in range(len(games)):
            if self.wait_check_detail_page():  # 页面检查点
                if self.wait_check_detail_list_page():
                    # speak[j].click()
                    print(j + 1, '.', games[j].text)  # 游戏题目

        index = random.randint(0, len(games)-1)
        self.star()[index].click()  # 过关 按钮
        if self.wait_check_modify_achieve_page():
            # todo 修改成绩
            self.commit_button()
            MyToast().toast_assert(self.name, Toast().toast_vue_operation('修改成功'))  # 获取toast
