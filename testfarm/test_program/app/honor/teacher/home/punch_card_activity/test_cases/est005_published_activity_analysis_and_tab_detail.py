#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.home.punch_card_activity.object_page.published_activity_analysis_page import \
    PublishedActivityAnalysisPage, PublishedActivityAnalysisDetailPage
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
    """已发布活动 详情页"""

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
        cls.analysis = PublishedActivityAnalysisPage()
        cls.analysis_detail = PublishedActivityAnalysisDetailPage()
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
    def test_published_activity_analysis(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.login.app_status()  # 判断APP当前状态

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.punch_activity_icon()  # 进入打卡活动页面
        self.assertTrue(self.activity.wait_check_app_page(), self.activity.activity_tips)
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.published_activities_tab().click()
        self.vue.app_web_switch()  # 切到app 再切回vue
        if self.activity.wait_check_no_activity_page():
            self.assertTrue(self.activity.wait_check_no_activity_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
            self.into_activity()  # 进入 已发布活动详情页

            self.assertTrue(self.published.wait_check_page(), self.published.detail_vue_tips)
            self.published.analysis_button()  # 分析汇总 按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue

            self.activity_analysis_operation()  # 分析汇总 详情页

            self.assertTrue(self.published.wait_check_page(), self.published.detail_vue_tips)
            self.activity.back_up_button()  # 返回 打卡活动list 页面
            self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.back_up_button()  # 返回 主界面
        self.vue.switch_app()  # 切到app

    @teststeps
    def into_activity(self):
        """进入活动列表中的该活动
        """
        self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
        name = self.activity.published_activity_name()  # 活动名
        index = random.randint(0, len(name) - 1)
        print("进入已发布活动:", name[index].text)
        activity = [name[index].text]
        name[index].click()  # 进入活动
        self.vue.app_web_switch()  # 切到apk 再切到vue

        return activity

    @teststeps
    def activity_analysis_operation(self):
        """分析汇总 页"""
        self.assertTrue(self.analysis.wait_check_page(), self.analysis.analysis_tips)
        days = self.analysis.day_name()
        dates = self.analysis.date_name()

        day_content = []
        date_content = []
        for i in range(len(days)):
            day = days[i].text
            date = dates[i].text
            print(day, '\n', date)

            day_var = day.split()[1]
            date_var = date.replace('-', '')
            if i == 0:
                self.assertEqual(day.split()[1], '1', '★★★ Error -第一个不是Day 1')
            else:
                self.assertEqual(int(day_var) - int(day_content[-1]), 1, '★★★ Error -Day不是递增{}'.format(day_content))

                var = False
                if int(date_var) - int(date_content[-1]) > 0:
                    var = True
                self.assertTrue(var, '★★★ Error -Date不是递增{}'.format(day_content))

            day_content.append(day_var)
            date_content.append(date_var)

        index = random.randint(0, len(dates) - 1)
        print("进入已发布活动:", days[index].text)
        activity = days[index].text
        days[index].click()  # 进入活动
        self.vue.app_web_switch()

        self.finish_situation_operation(activity)  # 完成情况 tab
        self.answer_analysis_operation(activity)  # 答题分析 tab
        
    @teststeps
    def finish_situation_operation(self, title):
        """完成情况tab 具体操作"""
        self.assertTrue(self.analysis_detail.wait_check_page(), self.analysis_detail.analysis_vue_tips)
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
        self.assertTrue(self.analysis_detail.wait_check_page(), self.analysis_detail.hw_list_tips)
        analysis = self.analysis_detail.answer_analysis_tab()  # 答题分析 tab
        analysis.click()  # 进入 答题分析 tab页

        print('-------------------答题分析tab-------------------')
        if self.analysis_detail.wait_check_empty_tips_page():
            self.assertTrue(self.analysis_detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.analysis_detail.wait_check_hw_list_page(), self.analysis_detail.hw_list_tips)
            self.answer_analysis_detail()  # 答题分析 列表

    @teststeps
    def answer_analysis_detail(self):
        """答题分析 详情页"""
        item = self.analysis_detail.analysis_tab_hw_list_info()[1]  # 游戏 条目
        for i in range(len(item) - 1):
            print(item[i])
            print('---------------------------')

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        students = self.analysis_detail.finish_tab_st_items()[1]  # 学生条目
        for i in range(len(students)-1):
            print('--------------------------------------')
            print(students[i])  # 打印所有学生信息
