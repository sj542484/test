#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import time
import unittest

from app.honor.teacher.home.punch_card_activity.object_page.activity_finish_tab_student_answer_game_detail_page import \
    StAnswerDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.activity_finish_tab_student_answer_result_page import \
    ResultDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.published_activity_analysis_page import \
    PublishedActivityAnalysisSummaryPage, PublishedActivityAnalysisSummaryDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.published_activity_detail_page import PublishedActivityDetailPage
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
    """已发布活动 分析汇总详情页-完成统计"""

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
        cls.analysis = PublishedActivityAnalysisSummaryPage()
        cls.analysis_detail = PublishedActivityAnalysisSummaryDetailPage()
        cls.st_answer = StAnswerDetailPage()
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
    def test_published_activity_analysis_summary_finish(self):
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
                        self.assertFalse(self.activity.wait_check_no_activity_page(), '暂无数据')
                        print('暂无数据')
                    else:
                        self.assertTrue(self.activity.wait_check_published_list_page(), self.activity.activity_list_tips)
                        self.activity.into_activity()  # 进入 已发布活动详情页

                        if self.published.wait_check_page():
                            self.published.analysis_button()  # 分析汇总 按钮
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                            self.activity_analysis_operation()  # 分析汇总 详情页
                            if self.published.wait_check_page():
                                self.activity.back_up_button()  # 返回 打卡活动list 页面
                                self.vue.app_web_switch()  # 切到apk 再切到vue

                    if self.activity.wait_check_page():
                        self.activity.back_up_button()  # 返回 主界面
                        self.vue.switch_app()  # 切到app

    @teststeps
    def activity_analysis_operation(self):
        """分析汇总页 具体操作"""
        if self.analysis.wait_check_page():
            days = self.analysis.day_name()
            dates = self.analysis.date_name()
            index = random.randint(0, len(dates) - 1)
            day = days[index].text
            print("进入:", day)
            days[index].click()  # 进入 分析汇总详情页
            self.vue.app_web_switch()  # 切到apk 再切到vue

            self.activity_analysis_detail_operation(day.lower())  # 分析汇总 详情页具体操作

            if self.analysis.wait_check_page():
                self.activity.back_up_button()  # 返回 分析汇总页
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def activity_analysis_detail_operation(self, title):
        """分析汇总 详情页具体操作"""
        if self.analysis_detail.wait_check_page(title):
            self.assertTrue(self.analysis_detail.wait_check_st_list_page(), self.analysis_detail.st_list_tips)
            status = self.analysis_detail.st_finish_status()  # 学生完成与否
            st_mode = self.analysis_detail.st_type()  # 基础班/提分版/试用期

            for i in range(len(status)):
                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                self.assertTrue(self.analysis_detail.wait_check_st_list_page(), self.analysis_detail.st_list_tips)
                st = self.analysis_detail.st_name()  # 学生name
                name = st[i].text  # 学生name
                print(status[i].text)
                if status[i].text != '未完成':
                    mode = st_mode[i].get_attribute('src')  #
                    st[i].click()  # 进入一个学生的答题情况页

                    self.vue.app_web_switch()  # 切到apk 再切回vue
                    if self.st_answer.wait_check_page(name):  # 页面检查点
                        print('学生 %s 答题情况：' % name)
                        self.per_game_list(name)  # 列表信息
                        self.per_answer_detail(name)

                        if self.st_answer.wait_check_page(name):  # 页面检查点                        self.v_hw.back_up_button()  # 返回 学生列表
                            self.activity.back_up_button()  # 返回 学生列表
                            self.vue.app_web_switch()  # 切到apk 再切回vue
                else:
                    print('学生%s未完成' % name)

            if self.analysis_detail.wait_check_page(title):  # 页面检查点
                self.activity.back_up_button()  # 返回 分析汇总 页
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def per_answer_detail(self, st):
        """个人 答题情况详情页"""
        if self.st_answer.wait_check_page(st):  # 页面检查点
            item = self.st_answer.per_game_item()  # 游戏条目

            for j in range(len(item[1])):
                print('=================================================================')
                if self.st_answer.wait_check_page(st):  # 页面检查点
                    mode = self.st_answer.game_mode(item[1][j][-2])
                    var = item[1][j][-1].split()  # '最优成绩100% 首轮成绩100%'
                    best = re.sub("\D", "", var[0])
                    score = re.sub("\D", "", var[-1])

                    if best != '' and int(best) >= int(score):  # 已做
                        value = game_type_operation(item[1][j][0])
                        print(item[1][j][0], value)
                        print('--------------------答题情况 详情页---------------------')

                        if value == 17:  # 微课
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue
                            MyToast().toast_assert(self.name, Toast().toast_vue_operation(TipsData().no_report))  # 获取toast
                        elif value == 24:  # 单词跟读
                            item[0][j].click()  # 点击进入game
                            self.vue.app_web_switch()  # 切到apk 再切回vue

                            self.result.word_reading_operation(score)
                        elif value in (21, 22, 23):  # 口语
                            print('口语')  #
                            time.sleep(2)
                            self.activity.back_up_button()   # 返回  游戏列表
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
                        print(item[1][j][0], item[1][j][-2], ' --该题还未做')

                    self.vue.app_web_switch()  # 切到apk 再切回vue

    @teststeps
    def per_game_list(self, st):
        """个人 game答题情况页 列表"""
        if self.st_answer.wait_check_page(st):  # 页面检查点
            name = self.st_answer.game_name()  # 游戏name
            mode = self.st_answer.game_type()  # 类型
            status = self.st_answer.optimal_first_achievement()  # 游戏完成情况

            for i in range(len(status)-1):
                print(mode[i].text, name[i].text, status[i].text)

            print('---------------------------------------------')
