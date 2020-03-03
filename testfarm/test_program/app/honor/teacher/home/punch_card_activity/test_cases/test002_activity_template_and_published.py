#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import time
import unittest

from app.honor.teacher.home.punch_card_activity.object_page.activity_template_detail_page import ActivityTemplateDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.published_activity_detail_page import \
    PublishedActivityDetailPage
from app.honor.teacher.home.punch_card_activity.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.punch_card_activity.object_page.punch_card_page import PunchCardPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.toast_find import Toast
from utils.vue_context import VueContext


class Activity(unittest.TestCase):
    """活动模板tab 发布"""

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
        cls.detail = ActivityTemplateDetailPage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切回apk
        errors = self.ass.get_error() + self.my_toast.get_error()
        if errors:
            print(errors)
            self.ass_result.addFailure(self, errors[0])

    def run(self, result=None):
        self.ass_result = result
        super(Activity, self).run(result)

    @testcase
    def test_activity_detail_publish(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.login.app_status()  # 判断APP当前状态

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.punch_activity_icon()  # 进入打卡活动页面
        self.assertTrue(self.activity.wait_check_app_page(), self.activity.activity_tips)
        self.vue.switch_h5()  # 切到web

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        if self.activity.wait_check_no_activity_page():
            self.assertTrue(self.activity.wait_check_no_activity_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.activity.wait_check_template_list_page(), self.activity.activity_list_tips)
            var = self.into_activity()  # 进入 打卡模板详情页
            self.vue.app_web_switch()  # 切到apk 再切回web

            if self.detail.wait_check_page():  # 页面检查点
                self.activity_template_operation(var)  # 活动模板 详情页
                self.vue.app_web_switch()  # 切到apk 再切回web
            elif self.activity.wait_check_tips_page(var[0]):  # 温馨提示 页面
                print('--------------------------')
                self.activity.tips_title()
                self.activity.no_vanclass_tips_content()
                self.activity.known_button()  # 确定按钮
                self.vue.app_web_switch()  # 切到apk 再切回web
                print('--------------------------')

            self.judge_publish_result_operation(var)  #
        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.back_up_button()  # 返回 主界面

    @teststeps
    def into_activity(self):
        """进入活动列表中的该活动
        """
        self.assertTrue(self.activity.wait_check_template_list_page(), self.activity.activity_list_tips)
        name = self.activity.template_activity_name()  # 名称
        info = self.activity.template_activity_info()  # 模板信息
        status = self.activity.template_activity_type()  # 模板类型

        index = random.randint(0, len(name) - 1)
        print("进入活动:", name[index].text)
        activity = [name[index].text, info[index].text]
        name[index].click()  # 进入活动

        return activity

    @teststeps
    def activity_template_operation(self, activity):
        """编辑打卡活动 详情页"""
        self.assertTrue(self.detail.wait_check_page(), self.detail.detail_vue_tips)
        self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)
        print('-------------------打卡活动 详情页-------------------')
        self.detail.share_preview_button()  # 分享预览 按钮
        self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertTrue(self.detail.wait_check_preview_page(), '★★★ Error- 未加载出图片')
        self.detail.preview_img()
        self.detail.click_block()
        self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertTrue(self.detail.wait_check_page(), self.detail.detail_vue_tips)
        self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)

        name = self.detail.activity_name()
        self.assertEqual(activity[0], name, '★★★ Error- 模板详情页，打卡活动名称与列表中不一致')
        print(self.detail.activity_title(), name)  # 打卡活动名称
        print('-------------------')

        print(self.detail.activity_slogan_title(), self.detail.activity_slogan())  # 打卡活动宣传
        print('-------------------')

        print(self.detail.activity_source_title())  # 打卡活动资源
        source_img = self.detail.activity_source_img()  # 活动资源 图片
        source_name = self.detail.activity_source_name()  # 活动资源 名称
        for i in range(len(source_img)):
            print(source_name[i].text)
        print('-------------------')

        play = self.detail.play_content().split('，')
        day1 = re.sub('\D', '', play[0])  # 每天x本书
        book1 = re.sub('\D', '', play[1])  # 共x本书
        total_day1 = re.sub('\D', '', play[2])  # 需连续x天完成

        info = activity[1].split('  ')
        day2 = re.sub('\D', '', info[1])  # 每日x本
        book2 = re.sub('\D', '', info[0])  # x本书
        var = info[2][2:-3].split('-')  # 请于xxxx-xx-xx前布置
        print(var)
        timestr = time.strftime('%Y-%m-%d', time.localtime()).split('-')

        year = 0  # 布置截至年份
        month = 0  # 布置截至月份
        day = 0  # 布置截至日
        if var[0] > timestr[0]:
            year = 365

        if var[1] != timestr[1]:
            if int(var[1]) in (1, 3, 5, 7, 8, 10, 12):
                var_day = 31
            elif int(var[1]) == 2:
                if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
                    var_day = 29
                else:
                    var_day = 28
            else:
                var_day = 30
            month = (int(var[1]) - int(timestr[1])) * var_day

        if var[2] != timestr[2]:
            day = int(var[2]) - int(timestr[2])
        print(year, month, day)
        total = year + month + day

        assert total > 0
        self.assertEqual(day1, day2, '★★★ Error- 每日书数不一致')
        self.assertEqual(book1, book2, '★★★ Error- 共有书数不一致')
        print(self.detail.play_title(), play)  # 打卡活动玩法

        self.activity_vanclass_list()  # 班级列表
        choose = self.detail.choose_class_operation()  # 选择班级
        if choose[0]:
            self.assertTrue(self.detail.wait_check_page(), self.detail.detail_vue_tips)
            self.detail.assign_button()  # 发布打卡活动 按钮

            self.vue.app_web_switch()  # 切到apk 再切回web
            if self.detail.wait_check_tips_page():
                self.detail.publish_tips_content()
                self.detail.confirm_button()  # 确认 按钮
                self.my_toast.toast_assert(self.name, Toast().toast_vue_operation(TipsData().hw_success))  # 获取toast信息

                self.vue.app_web_switch()  # 切到apk 再切回web

            return choose

    @teststeps
    def activity_vanclass_list(self):
        """班级列表"""
        print('------------------------------')
        self.detail.publish_activity()  # 班级列表 title
        self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)
        self.detail.swipe_vertical_web(0.5, 0.9, 0.2)
        self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)

        van = self.detail.van_info()  # 班级描述
        button = self.detail.choose_button()  # 单选 按钮

        vanclass = []  # 班级名
        if len(button) != len(van):
            print('★★★ Error- 单选框的个数与班级个数不同', len(button), len(van))
        else:
            for k in van:
                if k.text != '':
                    print(k.text)
                    print('------------------')
        return van, vanclass

    @teststeps
    def judge_publish_result_operation(self, name):
        """验证 布置结果 具体操作
        :param name: 名称 & 时间范围
        """
        print('------------------验证布置结果------------------')
        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.published_activities_tab().click()
        if self.activity.wait_check_no_activity_page():
            self.assertTrue(self.activity.wait_check_no_activity_page(), '暂无数据')
            self.assertFalse('暂无数据', '★★★ Error- 布置失败')
        else:
            self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
            title = self.activity.published_activity_name()
            count = []
            for i in range(len(title)):
                if title[0].text == name[0]:
                    count.append(i)
                break

            self.assertFalse(len(count) == 0, '★★★ Error -活动布置不成功, {}'.format(name))
            print('活动布置成功')
