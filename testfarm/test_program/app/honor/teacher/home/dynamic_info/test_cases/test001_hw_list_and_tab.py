#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class Homework(unittest.TestCase):
    """作业列表 & 答题分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.info = DynamicPage()
        cls.get = GetAttribute()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切回apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Homework, self).run(result)

    @testcase
    def test_homework_list_and_tab(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.info.current_activity()
        self.home.hw_icon()  # 进入习题 最近动态页面
        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点

        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        if self.info.wait_check_no_hw_page():
            print('最近习题动态页面为空')
            self.info.back_up_button()
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        else:
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            self.info.hw_list_operation()  # 列表
            self.info.into_hw()  # 进入 作业包
            self.vue.app_web_switch()  # 切到apk 再切回web

            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
            if self.detail.wait_check_page():
                self.finish_situation_operation()  # 完成情况 tab
                self.answer_analysis_operation()  # 答题分析 tab

            self.info.back_up_button()  # 返回 作业list 页面
            self.vue.app_web_switch()  # 切到apk 再切回web
            if self.info.wait_check_page():  # 页面检查点
                self.info.back_up_button()  # 返回 主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        print('-------------------完成情况tab-------------------')
        if self.detail.wait_check_empty_tips_page():
            self.assertTrue(self.detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.detail.wait_check_st_list_page(), self.detail.st_list_tips)
            self.st_list_statistics()  # 完成情况 学生列表

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
        analysis = self.detail.analysis_tab()  # 答题分析 tab
        analysis.click()  # 进入 答题分析 tab页
        print('-------------------答题分析tab-------------------')
        if self.detail.wait_check_empty_tips_page():
            self.assertTrue(self.detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.detail.wait_check_hw_list_page(), self.detail.hw_list_tips)
            self.answer_analysis_detail()  # 答题分析 列表

    @teststeps
    def answer_analysis_detail(self):
        """答题分析 详情页"""
        item = self.detail.analysis_tab_hw_list_info()[1]  # 游戏 条目
        for i in range(len(item) - 1):
            print(item[i])
            print('---------------------------')

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        students = self.detail.finish_tab_st_items()[1]  # 学生条目
        for i in range(len(students)-1):
            print('--------------------------------------')
            print(students[i])  # 打印所有学生信息
