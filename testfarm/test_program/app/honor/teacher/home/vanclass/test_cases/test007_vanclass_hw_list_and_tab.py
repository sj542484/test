#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class Homework(unittest.TestCase):
    """习题列表 & 答题分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.v_hw = VanclassHwPage()
        cls.hw_detail = HwDetailPage()
        cls.van = VanclassPage()
        cls.get = GetAttribute()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Homework, self).run(result)

    @testcase
    def test_homework_list_and_tab(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)

        self.van.vanclass_hw()  # 点击 本班作业 tab
        title = gv.HW_TITLE.format(gv.VANCLASS)
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        if self.v_hw.wait_check_empty_tips_page():
            self.v_hw.no_data()  # 暂无数据
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
        else:
            print('本班作业:')
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
            name = self.v_hw.hw_name()  # 作业name
            progress = self.v_hw.hw_create_time()  # 进度
            count = 0
            for i in range(len(name)):
                text = name[i].text
                pro = progress[i].text.split()
                finish = re.sub("\D", "", pro[-1])
                if finish[0] != '0' and self.home.brackets_text_in(text) == '习题':
                    print('###########################################################')
                    print('作业:', text)
                    name[i].click()  # 进入 作业
                    count += 1
                    break

            if count == 0:
                print('暂无该作业')
            else:
                self.vue.app_web_switch()  # 切到apk 再切到vue
                self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
                self.finish_situation_operation()  # 完成情况 tab
                self.answer_analysis_operation()  # 答题分析 tab

                if self.hw_detail.wait_check_page():  # 页面检查点
                    self.v_hw.back_up_button()  # 返回 本班作业

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
        self.van.back_up_button()  # 返回主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        print('-------------------完成情况tab-------------------')
        if self.hw_detail.wait_check_empty_tips_page():
            self.assertTrue(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
            self.st_list_statistics()  # 完成情况 学生列表

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        analysis = self.hw_detail.analysis_tab()  # 答题分析 tab
        analysis.click()  # 进入 答题分析 tab页
        print('-------------------答题分析tab-------------------')
        if self.hw_detail.wait_check_empty_tips_page():
            self.assertTrue(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
            self.answer_analysis_detail()  # 答题分析 列表

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答题分析 详情页"""
        if content is None:
            content = []

        item = self.hw_detail.analysis_tab_hw_list_info()[1]  # 游戏 条目
        if len(item) > 4 and not content:
            for i in range(len(item) - 1):
                print(item[i])
                print('---------------------------')

            var = [item[-2][1] if len(item[-2]) == 3 else item[-2][2]]  # if 无提分标志 else 有
            content = [var[0], item[-2][0]]  # 最后一个game的name & type
            self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content)
        else:
            var = 0
            length = len(item)
            if content:
                for k in range(len(item)):
                    title = [item[k][1] if len(item[k]) == 4 else item[k][2]]
                    if content[0] == title[0] and content[1] == item[k][0]:
                        var = k + 1
                        break
                if var == 0:
                    var = 1
                if length > 4:
                    length = 4

            for i in range(var, length):
                print(item[i])
                print('---------------------------')
            self.v_hw.swipe_vertical_web(0.5, 0.2, 0.9)

    @teststeps
    def st_list_statistics(self, content=None):
        """已完成/未完成 学生列表信息统计"""
        if content is None:
            content = []

        students = self.hw_detail.finish_tab_st_items()[1]  # 学生条目
        if len(students) > 8 and not content:
            for i in range(len(students)-1):
                print('--------------------------------------')
                print(students[i])  # 打印所有学生信息

            content = [students[-2]]  # 最后一个学生 name&完成情况
            self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            if self.hw_detail.wait_check_hw_list_page():
                self.st_list_statistics(content)
        else:
            var = 0
            length = len(students)
            if content:
                for k in range(len(students)):
                    if content == students[k]:
                        var = k + 1
                        break
                if var == 0:
                    var = 1
                if length > 8:
                    length = 8

            for i in range(var, length):
                print('--------------------------------------')
                print(students[i])  # 打印所有学生信息
