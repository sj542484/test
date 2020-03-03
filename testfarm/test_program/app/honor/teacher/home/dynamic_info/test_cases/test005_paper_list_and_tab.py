#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as ge
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_paper_page import DynamicPaperPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class Paper(unittest.TestCase):
    """卷子列表 & 答卷分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.info = DynamicPaperPage()
        cls.report = PaperReportPage()
        cls.get = GetAttribute()

        cls.filter = FilterPage()
        cls.question = TestBankPage()
        cls.paper = PaperDetailPage()
        cls.release = ReleasePage()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切回apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Paper, self).run(result)

    @testcase
    def test_paper_list_tab(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        self.home.paper_icon()  # 进入卷子 最近动态页面
        
        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        if self.info.wait_check_no_hw_page():
            print('最近卷子动态页面为空')
            self.info.back_up_button()
            self.vue.switch_app()  # 切回apk
            self.assign_paper_operation()  # 布置试卷

            self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
            self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
            self.home.paper_icon()  # 进入卷子 最近动态页面
            self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        self.info.help_operation()  # 右上角 提示按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        self.info.hw_list_operation()  # 列表
        self.info.into_hw()  # 进入 作业包
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        self.finish_situation_operation()  # 完成情况 tab
        self.answer_analysis_operation()  # 答卷分析 tab

        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        self.info.back_up_button()  # 返回 卷子动态页面
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        self.info.back_up_button()  # 返回 主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        print('-------------------完成情况tab-------------------')
        if self.report.wait_check_empty_tips_page():
            self.assertFalse(self.report.wait_check_empty_tips_page(), '暂无数据')
        else:
            self.assertTrue(self.report.wait_check_st_list_page(), self.report.st_list_tips)
            self.st_list_statistics()  # 完成情况 学生列表

    @teststeps
    def answer_analysis_operation(self):
        """答卷分析tab 具体操作"""
        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)  # 页面检查点
        analysis = self.report.analysis_tab()  # 答卷分析 tab
        analysis.click()  # 进入 答卷分析 tab页
        print('-------------------答卷分析tab-------------------')
        if self.report.wait_check_empty_tips_page():
            self.assertFalse(self.report.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.report.wait_check_paper_list_page(), self.report.hw_list_tips)
            self.answer_analysis_detail()  # 答卷分析页 list

    @teststeps
    def answer_analysis_detail(self):
        """答卷分析 详情页"""
        mode = self.report.game_type()  # 游戏类型
        name = self.report.game_name()  # 游戏name
        average = self.report.van_average_achievement()  # 全班平均得分x分; 总分x分

        for j in range(len(average)):
            print(mode[j].text, name[j].text, '\n',
                  average[j].text)
            print('----------------------')

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        name = self.report.st_name()  # 学生name
        icon = self.report.st_icon()  # 学生头像
        status = self.report.st_score()  # 学生完成与否

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息
        else:
            print('★★★ Error-已完成/未完成 学生列表信息统计', len(icon), len(name))

    @teststeps
    def assign_paper_operation(self):
        """布置试卷"""
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

        if self.question.wait_check_page():  # 页面检查点
            self.question.filter_button()  # 筛选按钮
            self.assertTrue(self.filter.wait_check_page(), self.filter.filter_tips)
            paper = self.filter.test_paper()
            if GetAttribute().selected(paper) == 'false':
                self.filter.click_test_paper()  # 点击 试卷
            self.filter.commit_button()  # 确定按钮

        item = self.question.question_item()  # 试卷数
        index = random.randint(0, len(item[2]) - 1)  # 随机选择标签
        if self.question.judge_question_lock():
            while True:
                if index in item[3]:  # item[3] 锁定icon
                    continue
                else:
                    break

        item[2][index].click()  # 点击第X个试卷
        self.assertTrue(self.paper.wait_check_page(), self.paper.paper_tips)  # 页面检查点
        self.assign_paper()  # 布置试卷 具体操作

    @teststeps
    def assign_paper(self):
        """布置试卷 具体操作 """
        self.report.assign_button()  # 布置试卷 按钮
        self.assertTrue(self.paper.wait_check_assign_list_page(), self.paper.paper_assign_tips)
        print('--------------------布置试卷页面--------------------')

        self.paper.assign_title()
        self.paper.assign_hint()
        van = self.release.van_name()  # 班级名
        count = self.release.choose_count()  # 班级描述信息
        print('------------------------')
        for i in range(len(count)):
            print('-------')
            print('  ', van[i].text, '\n', count[i].text)
        print('------------------------')

        self.paper.assign_button()  # 布置试卷 按钮
        self.my_toast.toast_assert(self.name, Toast().toast_operation(TipsData().no_student))

        if self.paper.wait_check_assign_list_page():
            button = self.release.choose_button()  # 单选框
            print('------------------------')
            name = 0
            for k in range(len(button)):
                if any([GetAttribute().selected(button[k]) == 'false', k != count,
                        van[k].text != ge.VANCLASS]):
                    print('选择班级:', van[k].text)
                    name = van[k].text
                    button[k].click()  # 选择 一个班
                    break

            self.paper.assign_button()  # 布置试卷 按钮
            self.paper.tips_page_info()
            self.my_toast.toast_assert(self.name, Toast().toast_operation(TipsData().assign_success))

            return name
