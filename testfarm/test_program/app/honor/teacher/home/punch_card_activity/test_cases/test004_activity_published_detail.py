#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

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
        cls.detail = PublishedActivityDetailPage()
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
    def test_published_activity_detail(self):
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

            self.published_activity_operation()  # 已发布活动 详情页

            self.assertTrue(self.detail.wait_check_page(), self.detail.detail_vue_tips)
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
    def published_activity_operation(self):
        """已发布活动 详情页"""
        self.assertTrue(self.detail.wait_check_page(), self.detail.detail_vue_tips)
        self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)
        print('-------------------已发布活动 详情页-------------------')
        title = '全部班级'
        count = 0
        length = 1
        while count < length:
            print('------------------------')
            self.detail.down_button()  # 下拉按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue
            if self.detail.wait_check_menu_page():
                menu_item = self.detail.menu_item()
                length = len(menu_item)
                title = self.detail.menu_item_text()[count].text
                menu_item[count].click()
                self.vue.app_web_switch()  # 切到apk 再切到vue

            print(title)
            if self.detail.wait_check_choose_result_page(title):
                tea = self.detail.teacher_name()
                van = self.detail.van_name()
                info = self.activity_vanclass_info()  # 已发布活动 列表
                for i in range(len(tea)):
                    print(tea[i].text, van[i].text)

                    print(info[i])

            count += 1

    @teststeps
    def activity_vanclass_info(self):
        """已发布活动 列表"""
        num = self.detail.published_activity_num()
        unit = self.detail.published_activity_unit()
        title = self.detail.published_activity_title()

        content = []
        for i in range(0, len(num), 4):
            item = []
            for j in range(4):
                var = num[j].text, unit[j].text, title[j].text
                item.append(var)
            content.append(item)
        return content
