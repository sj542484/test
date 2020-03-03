#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.wait_element_vue import WaitElement


class SpokenAnalysisDetailQuestionPage(BasePage):
    """ 口语 答题分析 按题查看页面 及二级详情页面"""
    question_check_value = "//span[text()='按题查看']"
    tab_class_value = 'van-tab van-tab--active'  # 按题查 tab被选中时 class值

    @teststeps
    def __init__(self):
        self.home = ThomePage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”为依据"""
        locator = (By.XPATH, self.question_check_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def check_tab_status(self, var):
        """按题查看 tab 父元素  状态判断"""
        value = var.find_element_by_xpath('.//parent::div')\
            .get_attribute('class')
        return value

    @teststep
    def question_tab(self):
        """按题查看 tab"""
        locator = (By.XPATH, "//span[text()='按题查看']")
        return self.wait.wait_find_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“题目 条目”为依据"""
        locator = (By.XPATH, '//div[@class="spoken-cell van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def question(self):
        """题目"""
        locator = (By.XPATH, '//div[@class="van-cell__title completion-detail-title-text"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def finish_ratio(self):
        """完成率"""
        locator = (By.XPATH, '//span[@class="spoken-label-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def speak_button(self):
        """发音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def detail_st_type(self):
        """学生 提分版/基础版/试用期"""
        locator = (By.XPATH, '//div[@class="van-image van-icon__image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def game_items(self):
        """游戏条目"""
        locator = (By.XPATH, '//div[@class="spoken-cell van-cell"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def games_item_list(self):
        """按题查看页面 -游戏 条目
        :returns:  游戏类型 & 页面内所有game
        """
        ele = self.game_items()

        content = []  #
        for i in range(len(ele)):
            descendant = ele[i].find_elements_by_xpath('.//child::*')
            item = [k.text for k in descendant if k.text != '']  # 每一个game
            content.append(item[1:3])

        return ele, content

    # 按题查看 二级详情页
    @teststeps
    def wait_check_detail_page(self):
        """以“title: 详情”为依据"""
        locator = (By.XPATH, "//div[text()='详情']")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_detail_list_page(self):
        """以“ star”为依据"""
        locator = (By.XPATH, '//div[@class="spoken-detail-cell van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def game_name(self):
        """游戏名"""
        locator = (By.XPATH, '//div[@class="van-cell__title spoken-detail-header-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def hint(self):
        """句子"""
        locator = (By.XPATH, '//div[@class="spoken-detail-header-tip"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)

    @teststep
    def total_report(self):
        """报告"""
        locator = (By.XPATH, '//div[@class="spoken-detail-header-number"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="van-cell__title spoken-detail-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def detail_speak_button(self):
        """发音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def star(self):
        """完成率"""
        locator = (By.XPATH, '//div[@class="spoken-detail-cell-rate van-rate"]')
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
    def per_question_answer_detail(self):
        """game 答题情况详情页"""

        if self.wait_check_detail_list_page():
            self.game_name()  # 游戏名称
            self.hint()  # 提示信息
            self.total_report()  # 总报告
            print('-----------------------------')

        self.detail_operation()  # 详情页 具体操作

    @teststeps
    def detail_operation(self):
        """详情页 具体操作"""
        st = self.st_name()  # 游戏题目
        speak = self.detail_speak_button()  # 发音按钮
        for j in range(len(st)):
            if self.wait_check_detail_page():  # 页面检查点
                if self.wait_check_detail_list_page():
                    # speak[j].click()
                    print(j + 1, '.', st[j].text)  # 学生姓名

        star = self.star()
        index = random.randint(0, len(star)-1)
        star[index].click()  # 过关 按钮
        if self.wait_check_modify_achieve_page():
            # todo 修改成绩
            self.commit_button()
            Toast().toast_vue_operation('修改成功')
