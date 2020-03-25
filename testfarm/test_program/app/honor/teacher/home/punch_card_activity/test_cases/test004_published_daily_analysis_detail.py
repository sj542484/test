#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import time
import unittest

from app.honor.teacher.home.punch_card_activity.object_page.published_activity_daily_detail_student_answer_result_page import \
    ResultDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.published_activity_detail_page import \
    PublishedActivityDetailPage, PublishedActivityDailyAnalysisPage, PublishedActivityDailyAnalysisDetailPage
from app.honor.teacher.home.punch_card_activity.test_data.activity_type_data import game_type_operation
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
        cls.daily = PublishedActivityDailyAnalysisPage()
        cls.daily_detail = PublishedActivityDailyAnalysisDetailPage()
        cls.result = ResultDetailPage()
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
                        self.assertTrue(self.activity.wait_check_published_list_page(),
                                        self.activity.activity_list_tips)
                        self.activity.into_activity()  # 进入 已发布活动详情页
                        self.published_activity_operation()  # 已发布活动 详情页

                        if self.detail.wait_check_page():
                            self.activity.back_up_button()  # 返回 打卡活动list 页面
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                    if self.activity.wait_check_page():
                        self.activity.back_up_button()  # 返回 主界面
                        self.vue.switch_app()  # 切到app

    @teststeps
    def published_activity_operation(self):
        """已发布活动 详情页"""
        if self.detail.wait_check_page():
            if self.detail.wait_check_empty_tips_page():
                print('暂无数据')
                self.assertFalse(self.detail.wait_check_empty_tips_page(), '暂无数据')
            else:
                self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)
                title = '全部班级'
                count = 0
                length = 1
                while count < length:
                    print('######################################已发布活动 详情页######################################')
                    self.assertTrue(self.detail.wait_check_list_page(), self.detail.detail_list_tips)

                    print('-----------------------------')
                    if count != 0:
                        self.detail.down_button()  # 下拉按钮
                        self.vue.app_web_switch()  # 切到apk 再切到vue
                        if self.detail.wait_check_menu_page():
                            menu_item = self.detail.menu_item()
                            length = len(menu_item)
                            title = self.detail.menu_item_text()[count].text
                            menu_item[count].click()
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                    print(title)
                    self.activity_vanclass_operation(title)  # 已发布活动 列表具体操作

                    count += 1

    @teststeps
    def activity_vanclass_operation(self, title):
        """已发布活动 详情页 具体操作"""
        if self.detail.wait_check_choose_result_page(title):
            st_info = []  # 学生 、班级信息
            st = self.detail.student_name()
            van = self.detail.van_name()
            for i in range(len(st)):
                st_info.append([st[i].text, van[i].text])

            num = self.detail.published_activity_num()
            unit = self.detail.published_activity_unit()
            titles = self.detail.published_activity_title()

            content = []  # 打卡/缺卡/邀请人数/分享等信息
            for i in range(0, len(num), 4):
                item = []
                for j in range(4):
                    var = num[j].text, unit[j].text, titles[j].text
                    item.append(var)
                content.append(item)

            index = random.randint(0, len(content) - 1)
            print("进入:", st_info[index], '\n', content[index])
            st[index].click()  # 进入 每日详情
            self.vue.app_web_switch()  # 切到apk 再切到vue

            self.daily_analysis_operation()  # 每日详情页 具体操作

    @teststeps
    def daily_analysis_operation(self):
        """每日详情页"""
        print('+++++++++++++++++++++++++++++++++每日详情 页+++++++++++++++++++++++++++++++++')
        if self.daily.wait_check_page():
            if self.daily.wait_check_list_page():
                st_name = self.daily.st_tab().text
                days = self.daily.day_name()  # 天名
                dates = self.daily.date_name()  # 日期
                status = self.daily.status()  # 每天的状态 - 待打卡/缺卡/等待发布

                day_content = []
                date_content = []
                publish_date = []  # 发布日期
                for i in range(len(days)):
                    print('-----------------------------')
                    day = days[i].text
                    date = dates[i].text
                    print(day, status[i].text, '\n', date)

                    day_var = day.split()[1]
                    if i == 0:
                        self.assertEqual(day.split()[1], '1', '★★★ Error -第一个不是Day 1')
                        date_content = date[3:]
                    else:
                        self.assertEqual(int(day_var) - int(day_content[-1]), 1, '★★★ Error -Day不是递增')

                        publish_date.append(self.activity.offline_publish_date_operation(date[3:], date_content))
                    day_content.append(day_var)

                self.assertTrue(self.activity.is_arithmetic(publish_date), '★★★ Error -每日详情页面 发布日期未按递增顺序排序')
                print('每日详情页面 日期Day按递增顺序排序')
                print('每日详情页面 发布日期按递增顺序排序')

                self.into_daily_analysis_detail_operation(st_name, publish_date)  # 进入 每日详情页-详情页面

    @teststeps
    def into_daily_analysis_detail_operation(self, st_name, publish_date):
        """进入 每日详情页-详情页面"""
        print('----------------------------------------------')
        content = self.status_complete_operation(publish_date)
        for key, value in content.items():
            print("进入:", st_name, value)
            value[1].click()  # 进入 某一日详情页
            self.vue.app_web_switch()

            if key == '正常':
                self.per_answer_detail(st_name)  # 每日详情-详情页面
            elif key == '缺卡':
                self.per_answer_detail_miss(st_name)  # 每日详情-详情页面
            elif key == '等待发布':
                self.per_answer_detail_unpublish(st_name)  # 每日详情-详情页面

            if self.daily_detail.wait_check_page(st_name):  # 页面检查点
                self.activity.back_up_button()  # 返回 每日详情页
                self.vue.app_web_switch()  # 切到apk 再切回vue

        if self.daily.wait_check_list_page():
            self.activity.back_up_button()  # 返回 已发布活动 详情页
            self.vue.app_web_switch()  # 切到apk 再切回vue

    @teststeps
    def per_answer_detail_miss(self, st):
        """个人 答题情况详情页 - 缺卡"""
        print('========================{} 每日详情-缺卡 详情页面========================'.format(st))
        if self.daily_detail.wait_check_page(st):  # 页面检查点
            self.assertFalse(self.daily_detail.wait_check_empty_page(), self.daily_detail.empty_tips)

    @teststeps
    def per_answer_detail_unpublish(self, st):
        """个人 答题情况详情页 - 等待发布"""
        print('========================{} 每日详情-等待发布 详情页面========================'.format(st))
        if self.daily_detail.wait_check_page(st):  # 页面检查点
            self.assertTrue(self.daily_detail.wait_check_list_page(), self.daily_detail.st_detail_tips)
            name = self.daily_detail.game_name()  # 游戏条目
            average = self.daily_detail.optimal_first_achievement()
            for i in range(len(name)):
                print(name[i].text, '\n', average[i].text)
                self.assertEqual(average[i].text, '最优成绩-- 首轮成绩--', '★★★ Error- 等待发布 详情页面"最优成绩-- 首轮成绩--"有误')

    @teststeps
    def per_answer_detail(self, st):
        """个人 答题情况详情页 - 待/已打卡"""
        print('========================{} 每日详情- 待/已打卡 详情页面========================'.format(st))
        if self.daily_detail.wait_check_page(st):  # 页面检查点
            self.assertTrue(self.daily_detail.wait_check_list_page(), self.daily_detail.st_detail_tips)
            item = self.daily_detail.per_game_item()  # 游戏条目

            for j in range(len(item[1])):
                print('==========================================================')
                if self.daily_detail.wait_check_list_page():  # 页面检查点
                    mode = self.daily_detail.game_mode(item[1][j][-2])
                    var = item[1][j][-1].split()  # '最优成绩100% 首轮成绩100%'
                    best = re.sub("\D", "", var[0])
                    score = re.sub("\D", "", var[-1])

                    if best != '' and int(best) >= int(score):  # 已做
                        value = game_type_operation(item[1][j][0])
                        print(item[1][j][0], value)
                        print('------------------游戏答题情况详情页-----------------')

                        if value == 17:  # 微课
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue
                            MyToast().toast_assert(self.name,
                                                   Toast().toast_vue_operation(TipsData().no_report))  # 获取toast
                        elif value == 24:  # 单词跟读
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue

                            self.result.word_reading_operation(score)
                        elif value in (21, 22, 23):  # 口语
                            print('口语')  #
                            time.sleep(2)
                            self.activity.back_up_button()  # 返回  游戏列表
                            self.vue.app_web_switch()  # 切到apk 再切回vue
                        elif value == 14:  # 闪卡练习
                            print(mode)
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue

                            content = []
                            if mode == '句子学习':
                                self.result.flash_sentence_operation(content, score)
                            elif mode in ('单词学习', '单词抄写'):
                                self.result.flash_card_list_operation(content, score)
                        elif value == 16:  # 连连看
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue

                            content = []
                            print(mode)
                            if mode == '文字模式':
                                if self.result.wait_check_list_page():
                                    self.result.report_score_compare(score)  # 验证 首次成绩 与首次正答

                                self.result.list_operation(content)
                            elif mode == '图文模式':  # 图文模式
                                self.result.match_img_operation(content, score)
                        elif value == 18:  # 磨耳朵
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue
                            self.result.ears_ergodic_list()
                        else:
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue
                            self.result.hw_detail_operation(value, score)
                    elif best == score == '':
                        print(item[1][j][0], item[1][j][-2], '\n--该题还未做')

                    self.vue.app_web_switch()  # 切到apk 再切回vue

    @teststeps
    def status_complete_operation(self, publish_date):
        """每天的状态"""
        dates = self.daily.date_name()  # 日期
        status = self.daily.status()  # 状态

        content = {}
        for i in range(len(status)):
            var = dates[i].text

            if status[i].text in ('待打卡', '正常'):
                content['正常'] = [var, status[i]]
            elif status[i].text == '缺卡':
                content['缺卡'] = [var, status[i]]
            elif status[i].text == '等待发布':
                content['等待发布'] = [var, status[i]]

                for k in range(i, len(status)):
                    self.assertEqual(status[k].text, '等待发布', '★★★ Error- 每日详情页面 状态 排序有误')
                    item = True
                    if publish_date[k] < 0:
                        item = False
                    self.assertTrue(item, '★★★ Error- 每日详情页面 早于今天的时间展示‘等待发布’有误')
                break

        print('每日详情页面 晚于今天的时间展示‘等待发布’无误')
        print('----------------------------------------------')
        return content
