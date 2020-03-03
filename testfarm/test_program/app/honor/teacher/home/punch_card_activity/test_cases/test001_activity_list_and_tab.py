#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.punch_card_activity.object_page.punch_card_page import PunchCardPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class Activity(unittest.TestCase):
    """活动列表 & 活动模板/已发布活动tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.activity = PunchCardPage()
        cls.get = GetAttribute()
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
    def test_activity_list_and_tab(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.login.app_status()  # 判断APP当前状态

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.punch_activity_icon()  # 进入打卡活动页面
        self.assertTrue(self.activity.wait_check_app_page(), self.activity.activity_tips)
        self.vue.switch_h5()  # 切到web

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity_template_operation()  # 活动模板 tab
        self.published_activities_operation()  # 已发布活动 tab

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.back_up_button()  # 返回 主界面
        self.vue.switch_app()  # 切到app

    @teststeps
    def activity_template_operation(self):
        """活动模板tab 具体操作"""
        self.activity.activity_template_tab()  # 活动模板 tab
        print('-------------------活动模板tab-------------------')
        if self.activity.wait_check_no_activity_page():
            self.activity.back_up_button()
            self.assertFalse(self.activity.wait_check_no_activity_page(), '暂无数据')
        else:
            self.assertTrue(self.activity.wait_check_template_list_page(), self.activity.activity_list_tips)
            self.activity_template_item()  # 已发布活动 列表

    @teststeps
    def published_activities_operation(self):
        """已发布活动tab 具体操作"""
        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)

        analysis = self.activity.published_activities_tab()  # 已发布活动 tab
        analysis.click()  # 进入 已发布活动 tab页
        self.vue.app_web_switch()  # 切到apk 再切到vue

        print('-------------------已发布活动tab-------------------')
        if self.activity.wait_check_no_activity_page():
            self.activity.back_up_button()
            self.assertTrue(self.activity.wait_check_no_activity_page(), '暂无数据')
        else:
            self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
            self.published_activity_list()  # 已发布活动 列表

    @teststeps
    def activity_template_item(self):
        """活动 条目信息"""
        name = self.activity.template_activity_name()  # 名称
        info = self.activity.template_activity_info()  # 模板信息
        status = self.activity.template_activity_type()  # 模板类型

        for i in range(len(name)):
            print('-------------------------------')
            print(name[i].text, '\n',
                  info[i].text, '\n',
                  status[i].text)

    @teststeps
    def published_activity_list(self):
        """已发布活动 条目信息"""
        name = self.activity.published_activity_name()  # 名称
        dates = self.activity.published_activity_date()  # 日期
        status = self.activity.published_activity_status()  # 状态

        item = self.activity.published_info()
        total_person = self.activity.published_activity_total_person_info()  # 总人数
        invite_person = self.activity.published_activity_invite_person_info()  # 活动 邀请总人数
        current_day = self.activity.published_activity_current_day_info()  # 当前天数
        total_day = self.activity.published_activity_total_day_info()  # 总天数

        print(len(total_person), len(invite_person), len(current_day), len(total_day))

        for i in range(len(name)):
            print(name[i].text, '    ', status[i].text, '\n',
                  dates[i].text)
            print('-----------------')
            print(total_person[i], '\n',
                  invite_person[i], '\n',
                  current_day[i], '\n',
                  total_day[i])
            print('-----------------------------------')
