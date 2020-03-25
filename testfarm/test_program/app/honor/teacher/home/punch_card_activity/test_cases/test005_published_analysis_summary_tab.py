#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.home.punch_card_activity.object_page.published_activity_analysis_page import \
    PublishedActivityAnalysisSummaryPage, PublishedActivityAnalysisSummaryDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.published_activity_detail_page import PublishedActivityDetailPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.punch_card_activity.object_page.punch_card_page import PunchCardPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.vue_context import VueContext


class Activity(unittest.TestCase):
    """已发布活动 分析汇总tab页"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.activity = PunchCardPage()
        cls.published = PublishedActivityDetailPage()
        cls.analysis = PublishedActivityAnalysisSummaryPage()
        cls.analysis_detail = PublishedActivityAnalysisSummaryDetailPage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切回apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Activity, self).run(result)

    @testcase
    def test_published_activity_analysis_summary(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():
            self.home.punch_activity_icon()  # 进入打卡活动页面
            if self.activity.wait_check_app_page():
                self.vue.switch_h5()  # 切到web

                if self.activity.wait_check_page():
                    self.activity.published_activities_tab().click()
                    self.vue.app_web_switch()  # 切到app 再切回vue
                    if self.activity.wait_check_no_activity_page():
                        print('暂无数据')
                        self.assertFalse(self.activity.wait_check_no_activity_page(), '暂无数据')
                    else:
                        self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
                        self.activity.into_activity()  # 进入 已发布活动详情页

                        if self.published.wait_check_page():
                            self.published.analysis_button()  # 分析汇总 按钮
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                            self.activity_analysis_operation()  # 分析汇总 详情页

                            if self.published.wait_check_page():
                                self.activity.back_up_button()  # 返回 打卡活动list 页面
                                self.vue.app_web_switch()  # 切到apk 再切到vue

                    if self.activity.wait_check_page():
                        self.activity.back_up_button()  # 返回 主界面
                        self.vue.switch_app()  # 切到app

    @teststeps
    def activity_analysis_operation(self):
        """分析汇总 页"""
        if self.analysis.wait_check_page():
            days = self.analysis.day_name()
            dates = self.analysis.date_name()

            day_content = []
            publish_date = []  # 日期
            now_time = 0
            for i in range(len(days)):
                print('--------------------------')
                day = days[i].text
                date = dates[i].text
                print(day, '\n', date)

                day_var = day.split()[1]
                if i == 0:
                    now_time = date
                    self.assertEqual(day.split()[1], '1', '★★★ Error -第一个不是Day 1')
                else:
                    self.assertEqual(int(day_var) - int(day_content[-1]), 1, '★★★ Error -Day不是递增')
                    publish_date.append(self.activity.offline_publish_date_operation(date, now_time))

                day_content.append(day_var)
            self.assertTrue(self.activity.is_arithmetic(publish_date), '★★★ Error -分析汇总页面 日期未按递增顺序排序')
            print('分析汇总页面 状态 排序无误')
            print('分析汇总页面 日期按递增顺序排序')
            print('--------------------------')

            index = random.randint(0, len(dates) - 1)
            print("进入:", days[index].text)
            day = days[index].text
            days[index].click()  # 进入 分析汇总详情页
            self.vue.app_web_switch()  # 切到apk 再切到vue

            self.finish_situation_operation(day.lower())  # 完成情况 tab
            self.answer_analysis_operation(day.lower())  # 答题分析 tab

            if self.analysis.wait_check_page():
                self.activity.back_up_button()  # 返回 分析汇总页
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def finish_situation_operation(self, title):
        """完成情况tab 具体操作"""
        if self.analysis_detail.wait_check_page(title):
            print('-------------------完成情况tab-------------------')
            if self.analysis_detail.wait_check_empty_tips_page():
                self.assertTrue(self.analysis_detail.wait_check_empty_tips_page(), '暂无数据')
                print('暂无数据')
            else:
                self.assertTrue(self.analysis_detail.wait_check_st_list_page(), self.analysis_detail.st_list_tips)
                self.st_list_statistics()  # 完成情况 学生列表

    @teststeps
    def answer_analysis_operation(self, title):
        """答题分析tab 具体操作"""
        if self.analysis_detail.wait_check_page(title):
            analysis = self.analysis_detail.answer_analysis_tab()  # 答题分析 tab
            analysis.click()  # 进入 答题分析 tab页

            print('-------------------答题分析tab-------------------')
            if self.analysis_detail.wait_check_empty_tips_page():
                self.assertFalse(self.analysis_detail.wait_check_empty_tips_page(), '暂无数据')
                print('暂无数据')
            else:
                self.assertTrue(self.analysis_detail.wait_check_hw_list_page(), self.analysis_detail.hw_list_tips)
                self.answer_analysis_detail()  # 答题分析 列表

            if self.analysis_detail.wait_check_page(title):
                self.activity.back_up_button()  # 返回 分析汇总页
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def answer_analysis_detail(self):
        """答题分析 详情页"""
        content = []  # 页面内所有条目 元素text
        elements = []  # 页面内所有条目元素

        ele = self.analysis_detail.analysis_tab_hw_items()  # 作业包 条目
        for i in range(len(ele)):
            print('--------------------------------------')
            descendant = ele[i].find_elements_by_xpath('.//descendant::*')[0]
            elements.append(descendant)

            item = descendant.text.split('\n')
            if '提分' in item[0]:
                item.insert(1, '提分')
                item[0] = item[0][:4]
            print(item)
            content.append(item)

        return elements, content

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        ele = self.analysis_detail.finish_tab_st_items()

        content = []  # 页面内所有条目 元素text
        elements = []  # 页面内所有条目元素
        for i in range(len(ele)):
            print('--------------------------------------')
            item = []  # 每一个条目的所有元素text
            element = []  # 每一个条目的所有元素
            descendant = ele[i].find_elements_by_xpath('.//descendant::*')[3:5]

            for j in range(len(descendant)):
                item.append(descendant[j].text)
                element.append(descendant[j])
            print(item)
            content.append(item)
            elements.append(element)

        return elements, content
