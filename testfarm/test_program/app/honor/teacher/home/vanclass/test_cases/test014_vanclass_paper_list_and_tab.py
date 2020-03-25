#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class VanclassPaper(unittest.TestCase):
    """卷子列表 & 答卷分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.van_paper = VanclassPaperPage()
        cls.report = PaperReportPage()
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
        super(VanclassPaper, self).run(result)

    @testcase
    def test_paper_list_tab(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)
        self.van_detail.vanclass_paper()  # 进入 本班卷子
        self.vue.app_web_switch()  # 切到apk 再切回web

        title = gv.PAPER_TITLE.format(gv.VANCLASS)
        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        if self.van_paper.wait_check_empty_tips_page():
            self.assertFalse(self.van_paper.wait_check_empty_tips_page(), '★★★ Error-班级试卷为空, {}')
        else:
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)
            print('本班试卷:')
            count = []
            name = self.van_paper.hw_name()  # 试卷name
            progress = self.van_paper.progress()  # 进度
            for i in range(len(name)):
                create = progress[i].text
                pro = int(re.sub("\D", "", create.split()[-1])[0])
                var = name[i].text

                if pro != 0 and '试卷' in self.home.brackets_text_in(var):
                    count.append(i)
                    name[i].click()  # 进入试卷
                    self.vue.app_web_switch()  # 切到apk 再切回web

                    print('###########################################################')
                    print('试卷:', var, '\n', create)
                    self.finish_situation_operation()  # 完成情况 tab
                    self.answer_analysis_operation()  # 答卷分析 tab

                    if self.report.wait_check_page():  # 页面检查点
                        self.van_detail.back_up_button()  # 返回 本班卷子
                    break

            self.assertFalse(len(count)==0, '暂无试卷或者暂无学生完成该试卷')

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        self.van_paper.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
        self.van_detail.back_up_button()  # 返回主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        print('-------------------完成情况tab-------------------')
        if self.report.wait_check_empty_tips_page():
            self.assertTrue(self.report.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.report.wait_check_st_list_page(), self.report.st_list_tips)
            self.st_list_statistics()  # 完成情况 学生列表

    @teststeps
    def answer_analysis_operation(self):
        """答卷分析tab 具体操作"""
        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        self.report.analysis_tab()  # 进入 答卷分析 tab页
        print('-------------------答卷分析tab-------------------')

        if self.report.wait_check_empty_tips_page():
            print('暂无数据')
            self.assertTrue(self.report.wait_check_empty_tips_page(), '暂无数据')
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
