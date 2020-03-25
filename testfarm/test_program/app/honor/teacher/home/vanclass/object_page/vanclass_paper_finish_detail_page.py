#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class PaperDetailPage(BasePage):
    """试卷 详情页面"""
    assign_van_locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选择班级')]")

    paper_tips = '★★★ Error- 未进入试卷 报告详情页面'
    paper_list_tips = '★★★ Error- 试卷 报告详情页面未加载成功'
    back_paper_tips = '★★★ Error- 未返回试卷 详情页面'

    paper_assign_tips = '★★★ Error- 未进入试卷布置页面'

    def __init__(self):
        self.wait = WaitElement()
        self.change_image = ChangeImage()

    @teststeps
    def wait_check_page(self, var):
        """以“title: ”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(var))
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以 顶部信息 为依据"""
        locator = (By.XPATH, '//div[@class="paper-topic-details"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def paper_type(self):
        """试卷"""
        locator = (By.XPATH, '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]')
        return self.wait \
            .wait_check_element(locator)

    @teststeps
    def paper_title(self):
        """title"""
        locator = (By.XPATH, '//span[@class="paper-topic-details-content-title"]')
        item = self.wait \
            .wait_find_element(locator).text
        print('试卷名称:', item)
        return item

    # 测评模式 - 百分制/AB制
    @teststeps
    def score_type(self):
        """测评模式 - 百分制/AB制"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]')
        item = self.wait.wait_find_element(locator)
        var = item.find_elements_by_xpath('.//span')
        content = [k.text for k in var]
        print(content)
        return content

    # 考试时间
    @teststep
    def test_time(self):
        """考试时间"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]')
        item = self.wait.wait_find_elements(locator)[1]
        var = item.find_elements_by_xpath('.//span')
        content = [k.text for k in var]
        return content

    # 小题数
    @teststep
    def games_num(self):
        """小题数"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]')
        item = self.wait.wait_find_elements(locator)[2]
        var = item.find_elements_by_xpath('.//span')
        content = [k.text for k in var]
        return content

    # 限制交卷
    @teststep
    def limit_type(self):
        """限制交卷"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]')
        item = self.wait.wait_find_elements(locator)[3]
        var = item.find_elements_by_xpath('.//span')
        content = [k.text for k in var]
        return content

    # 题型
    @teststep
    def game_list_title(self):
        """题型"""
        locator = (By.XPATH, '//span[@class="paper-analysis-details-title"]')
        return self.wait \
            .wait_find_element(locator).text

    @teststep
    def question_name(self):
        """小游戏名"""
        locator = (By.XPATH, '//div[@class="van-cell__title paper-report-cell-title"]/span')
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def num(self, index):
        """每个小游戏 题数"""
        locator = (By.XPATH, '//span[@class="van-cell__label paper-report-cell-label"]')
        return self.wait \
            .wait_find_elements(locator)[index]

    @teststep
    def arrow(self, index):
        """箭头"""
        locator = (By.XPATH, '//i[@class="van-icon van-icon-arrow van-cell__right-icon"]')
        return self.wait \
            .wait_find_elements(locator)[index]

