#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
import re

from app.honor.teacher.home.vanclass.object_page.hw_analysis_tab_ranking_page import HwAnalysisRankPage
from app.honor.teacher.home.vanclass.object_page.hw_finish_tab_student_answer_game_detail_page import StAnswerDetailPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class VanclassHw(unittest.TestCase):
    """习题 - 完成情况tab 详情 &cup"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.hw_detail = HwDetailPage()
        cls.van_detail = VanclassDetailPage()
        cls.v_hw = VanclassHwPage()
        cls.st_answer = StAnswerDetailPage()
        cls.rank = HwAnalysisRankPage()
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
        super(VanclassHw, self).run(result)

    @testcase
    def test_hw_per_detail_and_cup(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)

        self.van_detail.vanclass_hw()  # 点击 本班作业 tab
        title = gv.HW_TITLE.format(gv.VANCLASS)
        self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        if self.v_hw.wait_check_empty_tips_page():
            self.v_hw.no_data()  # 暂无数据
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
        else:
            print('本班作业:')
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
            self.hw_list_operation(title)  # 具体操作

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切回vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
        self.v_hw.back_up_button()  # 返回主界面

    @teststeps
    def hw_list_operation(self, title):
        """作业列表"""
        name = self.v_hw.hw_name()  # 作业name
        count = []
        for i in range(len(name)):
            if self.v_hw.wait_check_page(title):  # 页面检查点
                text = name[i].text
                if self.home.brackets_text_in(text) == '习题':
                    count.append(i)
                    print('###########################################################')
                    print(text)
                    name[i].click()  # 进入作业

                    self.vue.app_web_switch()  # 切到apk 再切回web
                    self.answer_analysis_operation()  # 答题分析tab 具体操作

                    self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)
                    self.v_hw.back_up_button()  # 返回
                    self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertFalse(len(count)==0, '暂无测试数据')

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.hw_detail.analysis_tab()  # 进入 答题分析 tab页
        print('-------------------------答题分析tab-------------------------')
        status = self.hw_detail.wait_check_empty_tips_page()
        if status:
            print('暂无数据')
            self.v_hw.back_up_button()  # 返回
            self.vue.app_web_switch()  # 切到apk 再切到vue
            if self.v_hw.wait_check_page():
                self.v_hw.back_up_button()  # 返回
                self.vue.app_web_switch()  # 切到apk 再切到vue

                if self.van_detail.wait_check_page():  # 页面检查点
                    self.v_hw.back_up_button()  # 返回 主界面
                    self.vue.switch_app()  # 切回apk
            self.assertFalse(status, '暂无数据')
        else:
            self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
            self.answer_analysis_detail()  # 答题分析 列表

    @teststeps
    def answer_analysis_detail(self):
        """答题分析 详情页"""
        no_cup = ['闪卡练习', '微课', '磨耳朵', '单词跟读', '口语看读', '口语跟读', '口语背诵']

        item = self.hw_detail.game_name()  # 游戏 条目
        var = []
        mode = self.hw_detail.game_type()
        finish = self.hw_detail.average_achievement()
        for i in range(len(item)):
            if self.hw_detail.wait_check_page():  # 页面检查点
                print(item[i].text, '\n', mode[i].text, '\n', finish[i].text)
                num = int(re.sub(r"\D", "", finish[i].text))  # 提取 全班首轮平均成绩
                if mode[i].text not in no_cup:
                    var.append(item[i].text)

                print('--------------------')

        cup = self.hw_detail.ranking_list()  # 查看排行榜
        for j in range(len(cup)):
            print(cup[j].get_attribute('style'))
            if cup[j].get_attribute('style') != 'display: none;':
                cup[j].click()  # 点击奖杯 icon
                self.vue.app_web_switch()  # 切到apk 再切回web

                if self.rank.wait_check_list_page():  # 作业 页面检查点
                    self.best_accuracy()  # 奖杯页面 最优成绩tab
                    self.first_accuracy()  # 奖杯页面 首次成绩tab

                    if self.rank.wait_check_list_page():  # 作业 页面检查点
                        self.v_hw.back_up_button()
                        self.vue.app_web_switch()  # 切到apk 再切回web
        print('-----------------------------------------')

    @teststeps
    def best_accuracy(self):
        """单个题目 答题详情 操作"""
        all_hw = self.rank.best_tab()  # 最优成绩 tab
        print('--------最优成绩tab--------')
        if self.rank.wait_check_list_page():
            self.accuracy_detail()
        elif self.v_hw.wait_check_empty_tips_page():
            print('暂无数据')

    @teststeps
    def first_accuracy(self):
        """首次成绩tab 具体操作"""
        incomplete = self.rank.first_tab()  # 首次成绩 tab
        incomplete.click()  # 进入 首次成绩 tab页
        print('--------首次成绩tab--------')
        if self.rank.wait_check_list_page():
            self.accuracy_detail()
        elif self.v_hw.wait_check_empty_tips_page():
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
