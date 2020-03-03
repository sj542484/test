#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.dynamic_info.object_page.spoken_finish_tab_detail_page import SpokenFinishDetailPage
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
        cls.van = VanclassPage()
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

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)

        self.van.vanclass_hw()  # 点击 本班作业 tab
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
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
        self.van.back_up_button()  # 返回主界面
        self.vue.switch_app()  # 切到apk

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        if self.hw_detail.wait_check_empty_tips_page():
            self.assertTrue(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            print('====================完成情况tab====================')
            self.st_list_statistics()  # 完成情况tab 列表信息

    @teststeps
    def st_list_statistics(self, content=None):
        """完成情况 tab页信息"""
        self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
        if content is None:
            content = []

        name = self.hw_detail.st_name()  # 学生name
        status = self.hw_detail.st_finish_status()  # 学生完成与否

        if len(name) > 7 and not content:
            for i in range(len(name)-1):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

            content = [name[-2].text, status[len(name)-2].text]  # 最后一个game的name type
            self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            self.st_list_statistics(content)
        else:
            var = 0
            if content:
                for k in range(len(name)):
                    if content[0] == name[k].text and content[1] == status[k].text:
                        var += k
                        break

            for j in range(var, len(name)):
                print('学生:', name[j].text, ' ', status[j].text)  # 打印所有学生信息

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        analysis = self.hw_detail.analysis_tab()  # 答题分析 tab
        analysis.click()  # 进入 答题分析 tab页
        if self.get.selected(analysis) is False:
            print('★★★ Error- 进入 答题分析 tab页')
        else:
            print('-------------------答题分析tab-------------------')
            if self.hw_detail.wait_check_empty_tips_page():
                self.assertTrue(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
                print('暂无数据')
            else:
                self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
                self.answer_analysis_detail()  # 答题分析tab 列表信息

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答题分析 tab页信息"""
        if content is None:
            content = []

        mode = self.hw_detail.game_type()  # 游戏类型
        name = self.hw_detail.game_name()  # 游戏name
        average = self.hw_detail.average_achievement()  # 本班完成率

        if len(mode) > 5 and not content[0]:
            content = []
            for j in range(len(mode) - 1):
                print(mode[j].text, name[j].text, average[j].text)

            content.append(name[len(mode)-2].text)  # 最后一个game的name
            content.append(mode[-2].text)  # 最后一个game的type
            self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content)
        else:
            var = 0
            if content:
                for k in range(len(mode)):
                    if content[0] == name[k].text and content[1] == mode[k].text:
                        var += k
                        break

            for j in range(var, len(mode)):
                print(mode[j].text, name[j].text, average[j].text)
