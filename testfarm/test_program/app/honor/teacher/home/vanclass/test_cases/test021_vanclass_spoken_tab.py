#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.object_page.spoken_finish_tab_detail_page import SpokenFinishDetailPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class VanclassSpoken(unittest.TestCase):
    """口语 完成情况&答题分析 tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.v_hw = VanclassHwPage()
        cls.hw_detail = HwDetailPage()
        cls.speak = SpokenFinishDetailPage()
        cls.get = GetAttribute()
        cls.vue = VueContext()

        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassSpoken, self).run(result)

    @testcase
    def test_spoken_tab(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)

        self.van_detail.vanclass_hw()  # 点击 本班作业 tab
        name = self.v_hw.into_operation(gv.HW_TITLE, gv.VANCLASS, '口语')

        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
        print("题单:", name[0])
        self.finish_situation_operation()  # 完成情况 tab
        self.answer_analysis_operation()  # 答题分析 tab
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 本班口语作业

        self.vue.app_web_switch()  # 切到apk 再切回vue
        self.assertTrue(self.v_hw.wait_check_page(name[1]), self.v_hw.van_hw_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切回vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
        self.van_detail.back_up_button()  # 返回主界面
        self.vue.switch_app()  # 切到apk

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        if self.hw_detail.wait_check_empty_tips_page():
            self.assertTrue(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
            print('====================完成情况tab====================')
            self.st_list_statistics()  # 完成情况tab 列表信息

    @teststeps
    def st_list_statistics(self):
        """完成情况 tab页信息"""
        name = self.hw_detail.st_name()  # 学生name
        status = self.hw_detail.st_finish_status()  # 学生完成与否

        for i in range(len(name)):
            print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.hw_detail.analysis_tab()  # 进入 答题分析 tab页
        print('-------------------答题分析tab-------------------')
        if self.hw_detail.wait_check_empty_tips_page():
            print('暂无数据')
            self.assertFalse(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
        else:
            self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
            self.answer_analysis_detail()  # 答题分析tab 列表信息

    @teststeps
    def answer_analysis_detail(self):
        """答题分析 tab页信息"""
        mode = self.hw_detail.game_type()  # 游戏类型
        name = self.hw_detail.game_name()  # 游戏name
        average = self.hw_detail.average_achievement()  # 本班完成率

        for j in range(len(mode)):
            print(mode[j].text, name[j].text, average[j].text)
