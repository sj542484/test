#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import time
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
    """已发布活动 信息验证"""

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
    def test_001_published_activity_info(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.login.app_status()  # 判断APP当前状态

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.punch_activity_icon()  # 进入打卡活动页面
        self.assertTrue(self.activity.wait_check_app_page(), self.activity.activity_tips)
        self.vue.switch_h5()  # 切到web

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.published_activities_tab().click()
        self.vue.app_web_switch()  # 切到app 再切回vue
        if self.activity.wait_check_no_activity_page():
            self.assertTrue(self.activity.wait_check_no_activity_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
            self.published_activity_operation()  # 已发布活动页

        self.assertTrue(self.activity.wait_check_page(), self.activity.activity_vue_tips)
        self.activity.back_up_button()  # 返回 主界面
        self.vue.switch_app()  # 切到app

    @teststeps
    def published_activity_operation(self):
        """已发布活动页"""
        name = self.activity.published_activity_name()  # 名称
        dates = self.activity.published_activity_date()  # 日期
        status = self.activity.published_activity_status()  # 状态

        current_day = self.activity.published_activity_current_day_info()  # 当前天数
        total_day = self.activity.published_activity_total_day_info()  # 总天数
        publish_date = []  # 发布日期
        offline_date = []  # 截至日期

        for i in range(len(name)):
            print('=============================================================')
            date = dates[i].text
            print(name[i].text, '    ', status[i].text, '\n',
                  date)

            print('-------------------------')

            var = date.split('/')
            publish_date.append(self.publish_date_operation(var[0]))
            offline_date.append(self.offline_publish_date_operation(var[1], var[0]))

        print(publish_date)
        self.assertTrue(self.activity.is_arithmetic(publish_date), '★★★ Error -发布日期未按递减顺序排序')

        # 当前天数 判断
        print('---------------------当前天数 判断---------------------')
        count = []
        now_time = time.strftime("%Y%m%d", time.localtime())   # 生成当前时间
        for j in range(len(current_day)):
            if status[j].text != "已结束":
                if int(now_time) - publish_date[j] != int(current_day[j][1]):
                    count.append(j)
            else:
                self.assertEqual(current_day[j][1], '–', '★★★ Error -已结束的活动，当前天数不对{}'.format(name[j].text, dates[j].text))
        self.assertFalse(len(count) == 0, '★★★ Error -当前天数有误, {}'.format(publish_date, now_time))
        print('所有活动当前天数无误\n', publish_date)

        # 总天数 判断
        print('---------------------总天数 判断---------------------')
        for k in range(len(total_day)):
            if offline_date[k] != int(total_day[k][1]):
                count.append(k)
        self.assertFalse(len(count) == 0, '★★★ Error -总天数有误, {}'.format(publish_date, now_time))
        print('所有活动总天数无误\n', offline_date)


    @teststeps
    def publish_date_operation(self, dates):
        """日期处理
        :param dates:待处理日期
        """
        print('待处理日期:', dates)
        now_time = time.strftime("%Y-%m-%d", time.localtime())   # 生成当前时间
        now = now_time.split('-')
        date = dates.split('-')

        year = int(date[0])
        var = 30
        if int(date[1]) in (1, 3, 5, 7, 8, 10, 12):
            var = 31
        elif int(date[1]) == 2:
            if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
                var = 29
            else:
                var = 28

        days = 365 * (int(now[0]) - year) + var * (int(now[1]) - int(date[1])) + int(now[2]) - int(date[2]) + 1
        print('差值：', days)

        return days

    @teststeps
    def offline_publish_date_operation(self, dates, now_time):
        """日期处理
        :param dates:待处理日期
        :param now_time: 比对日期
        """
        print('待处理日期:', dates)
        print('比对日期：', now_time)
        now = now_time.split('-')
        date = dates.split('-')

        year = int(now[0])
        var = 30
        if int(now[1]) in (1, 3, 5, 7, 8, 10, 12):
            var = 31
        elif int(now[1]) == 2:
            if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
                var = 29
            else:
                var = 28
        days = 365 * (int(date[0]) - year) + var * (int(date[1]) - int(now[1])) + int(date[2]) - int(now[2]) + 1
        print('差值：', days)
        return days

    @testcase
    def test_002_published_activity_detail(self):
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
                        self.published_activity_detail_operation()  # 已发布活动 详情页

                        if self.detail.wait_check_page():
                            self.activity.back_up_button()  # 返回 打卡活动list 页面
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                    if self.activity.wait_check_page():
                        self.activity.back_up_button()  # 返回 主界面
                        self.vue.switch_app()  # 切到app

    @teststeps
    def published_activity_detail_operation(self):
        """已发布活动 详情页"""
        if self.detail.wait_check_page():
            if self.detail.wait_check_empty_tips_page():
                print('暂无数据')
                self.assertFalse(self.detail.wait_check_empty_tips_page(), '暂无数据')
            else:
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

                    print('菜单选择:', title)
                    if self.detail.wait_check_choose_result_page(title):
                        st = self.detail.student_name()
                        van = self.detail.van_name()
                        info = self.activity_vanclass_info()  # 已发布活动 列表
                        for i in range(len(st)):
                            print('老师&班级:', st[i].text, van[i].text)

                            print(info[i])

                    count += 1

    @teststeps
    def activity_vanclass_info(self):
        """已发布活动 列表"""
        num = self.detail.published_activity_num()
        unit = self.detail.published_activity_unit()
        title = self.detail.published_activity_title()

        content = []  # 打卡/缺卡/邀请人数/分享等信息
        for i in range(0, len(num), 4):
            item = []
            for j in range(4):
                var = num[j].text, unit[j].text, title[j].text
                item.append(var)
            content.append(item)
        return content
