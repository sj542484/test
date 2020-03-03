#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.wait_element import WaitElement


class PaperReportPage(BasePage):
    """ 试卷 报告详情 页面"""
    analysis_tab_value = "//span[text()='答卷分析']"  # 答卷分析tab

    paper_detail_tips = '★★★ Error- 未进入试卷答卷情况详情页'
    edit_tips = '★★★ Error- 未进入试卷编辑详情页'

    hw_list_tips = '★★★ Error- 答卷分析 页面作业列表'
    st_list_tips = '★★★ Error- 完成情况tab 学生列表未加载成功'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title: 答卷分析”为依据"""
        locator = (By.XPATH, self.analysis_tab_value)
        return self.wait.wait_check_element(locator)

    # 单个试卷
    @teststep
    def analysis_tab(self):
        """答卷分析 tab"""
        locator = (By.XPATH, self.analysis_tab_value)
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def finished_tab(self):
        """完成情况 tab"""
        locator = (By.XPATH, "//span[text()='完成情况']")
        return self.wait \
            .wait_find_element(locator)

    @teststeps
    def wait_check_empty_tips_page(self, var=10):
        """以 提示text 作为依据"""
        locator = (By.XPATH, "//div[text()='暂无数据']")
        return self.wait.wait_check_element(locator, var)

    # 答卷分析 tab
    @teststeps
    def wait_check_paper_list_page(self):
        """以“游戏条目 元素”为依据"""
        locator = (By.XPATH, '//div[@id="question-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def game_type(self):
        """游戏类型"""
        locator = (By.XPATH, '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]')
        ele = self.wait.wait_find_elements(locator)
        return ele

    @teststep
    def game_level(self):
        """提分"""
        locator = (By.XPATH, '//span[@class="question-cell-tag van-tag van-tag--large van-tag--primary"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_num(self):
        """共x题"""
        locator = (By.XPATH, '//span[@class="question-cell-count"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_name(self):
        """游戏 名称"""
        locator = (By.XPATH, '//div[@class="question-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def van_average_achievement(self):
        """全班平均得分x分; 总分x分"""
        locator = (By.XPATH, '//span[@class="question-cell-label-left"]')
        return self.wait.wait_find_elements(locator)

    # 完成情况tab
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生完成情况 元素”为依据"""
        locator = (By.XPATH, '//div[@id="student-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def st_score(self):
        """学生 完成与否"""
        locator = (By.XPATH, '//span[@class="student-cell-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="van-cell__title student-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="van-image van-image--round"]/img')
        return self.wait.wait_find_elements(locator)

    # 完成情况tab -- 个人答题结果页
    @teststeps
    def wait_check_per_detail_page(self, var):
        """以“title”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()={}]'.format(var))
        return self.wait.wait_check_element(locator)

    @teststep
    def paper_type(self):
        """ 类型"""
        locator = (By.XPATH, '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def paper_name(self):
        """ 名称"""
        locator = (By.XPATH, '//span[@class="paper-topic-details-content-title"]')
        return self.wait.wait_find_elements(locator)

    # 测评模式 - 百分制/AB制
    @teststeps
    def score_type(self):
        """测评模式 - 百分制/AB制"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[1].text

    @teststeps
    def score(self):
        """百分制"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_element(locator).text

    # 考试时间
    @teststep
    def time_title(self):
        """考试时间"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[3].text

    @teststep
    def time_str(self):
        """时间"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[2].text

    # 小题数
    @teststep
    def num_title(self):
        """小题数"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[5].text

    @teststep
    def game_num(self):
        """小题数"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[4].text

    # 限制交卷
    @teststep
    def limit_type(self):
        """限制交卷"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[7].text

    @teststep
    def limit_hand(self):
        """限制/不限制交卷"""
        locator = (By.XPATH, '//div[@class="van-grid-item__content van-grid-item__content--center"]/span')
        return self.wait \
            .wait_find_elements(locator)[6].text

    # 个人答题结果页 -- 题型list
    @teststep
    def game_list_title(self):
        """ 题型"""
        locator = (By.XPATH, '//span[@class="paper-analysis-details-title"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)

    @teststep
    def game_title(self):
        """ 名称"""
        locator = (By.XPATH, '//div[@class="van-cell__title paper-report-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_desc(self):
        """ 共x题 xx分"""
        locator = (By.XPATH, '//div[@class="van-cell__label paper-report-cell-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_score(self):
        """ 得分"""
        locator = (By.XPATH, '//div[@class="van-cell__value paper-report-cell-value"]/span')
        return self.wait.wait_find_elements(locator)

    # 答题结果页 -详情页面
    @teststeps
    def wait_check_per_answer_list_page(self):
        """以“游戏title”为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__content"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def first_report(self):
        """首次正答"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__right"]/span')
        ele = self.wait.wait_find_element(locator).text
        print(ele)

    # 编辑试卷 页面
    @teststeps
    def wait_check_edit_page(self):
        """以“title:编辑试卷”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'编辑试卷')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def assign_button(self):
        """布置试卷 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_assign")
        self.wait.wait_find_element(locator).click()

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "action_first")
        self.wait.wait_find_element(locator).click()

    @teststep
    def confirm_button(self):
        """确定 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "action_second")
        self.wait.wait_find_element(locator).click()
