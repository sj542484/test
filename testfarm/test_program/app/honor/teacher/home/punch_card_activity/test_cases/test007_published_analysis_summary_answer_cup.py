#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import unittest

from app.honor.teacher.home.punch_card_activity.object_page.activity_analysis_tab_ranking_page import HwAnalysisRankPage
from app.honor.teacher.home.punch_card_activity.object_page.activity_finish_tab_student_answer_game_detail_page import \
    StAnswerDetailPage
from app.honor.teacher.home.punch_card_activity.object_page.published_activity_analysis_page import \
    PublishedActivityAnalysisSummaryPage, PublishedActivityAnalysisSummaryDetailPage
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
    """已发布活动 分析汇总详情页-大题分析"""

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
        cls.rank = HwAnalysisRankPage()
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
    def test_published_activity_analysis_summary_answer(self):
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
        """分析汇总 详情页 答题分析tab 具体操作"""
        if self.analysis_detail.wait_check_page(title):
            analysis = self.analysis_detail.answer_analysis_tab()  # 答题分析 tab
            analysis.click()  # 进入 答题分析 tab页
            print('-------------------------答题分析tab-------------------------')
            if self.analysis_detail.wait_check_hw_list_page():
                self.answer_analysis_detail(title)  # 答题分析 列表
            elif self.analysis_detail.wait_check_empty_tips_page():
                print('暂无数据')
                self.assertFalse(self.analysis_detail.wait_check_empty_tips_page(), '暂无数据')

            if self.analysis_detail.wait_check_page(title):
                self.activity.back_up_button()  # 返回 分析汇总 页
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def per_answer_detail(self):
        """个人 答题情况详情页"""
        mode = self.st_answer.game_type()  # 游戏类型
        name = self.st_answer.game_name()  # 游戏name
        optimal = self.st_answer.optimal_first_achievement()  # 最优成绩 首次成绩

        for j in range(len(optimal) - 1):
            print(mode[j].text, '\n',
                  name[j].text, '\n',
                  optimal[j].text)
            print('--------------------')

    @teststeps
    def answer_analysis_detail(self, title):
        """答题分析 详情页"""
        no_cup = ['闪卡练习', '微课', '磨耳朵', '单词跟读', '口语看读', '口语跟读', '口语背诵']

        item = self.analysis_detail.game_name()  # 游戏 条目
        var = []
        mode = self.analysis_detail.game_type()
        finish = self.analysis_detail.average_achievement()
        for i in range(len(item)):
            if self.analysis_detail.wait_check_page(title):  # 页面检查点
                print(item[i].text, '\n', mode[i].text, '\n', finish[i].text)
                num = int(re.sub(r"\D", "", finish[i].text))  # 提取 全班首轮平均成绩
                if mode[i].text not in no_cup:
                    var.append(item[i].text)

                print('--------------------')

        print('------------------------------查看排行榜------------------------')
        cup = self.analysis_detail.ranking_list()  # 查看排行榜
        for j in range(len(cup)):
            print(cup[j].get_attribute('style'))
            if cup[j].get_attribute('style') != 'display: none;':
                cup[j].click()  # 点击奖杯 icon
                self.vue.app_web_switch()  # 切到apk 再切回web

                if self.rank.wait_check_list_page():  # 作业 页面检查点
                    self.best_accuracy()  # 奖杯页面 最优成绩tab
                    self.first_accuracy()  # 奖杯页面 首次成绩tab

                    if self.rank.wait_check_list_page():  # 作业 页面检查点
                        self.activity.back_up_button()
                        self.vue.app_web_switch()  # 切到apk 再切回web
        print('-----------------------------------------')

    @teststeps
    def best_accuracy(self):
        """单个题目 答题详情 操作"""
        all_hw = self.rank.best_tab()  # 最优成绩 tab
        print('--------最优成绩tab--------')
        if self.rank.wait_check_list_page():
            self.accuracy_detail()
        elif self.analysis_detail.wait_check_empty_tips_page():
            print('暂无数据')

    @teststeps
    def first_accuracy(self):
        """首次成绩tab 具体操作"""
        incomplete = self.rank.first_tab()  # 首次成绩 tab
        incomplete.click()  # 进入 首次成绩 tab页
        print('--------首次成绩tab--------')
        if self.rank.wait_check_list_page():
            self.accuracy_detail()
        elif self.analysis_detail.wait_check_empty_tips_page():
            print('暂无数据')

    @teststeps
    def accuracy_detail(self):
        """首次成绩/最优成绩 详情"""
        index = self.rank.st_index()  # 序号
        icon = self.rank.st_icon()  # 头像
        name = self.rank.st_name()  # 昵称
        spend = self.rank.spend_time()  # 用时

        for j in range(len(icon)):
            print(index[j].text, icon[j].text, name[j].text, spend[j].text)
