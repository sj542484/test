#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.spoken_analysis_tab_detail_question_check_page import SpokenAnalysisDetailQuestionPage
from app.honor.teacher.home.dynamic_info.object_page.spoken_analysis_tab_detail_student_check_page import SpokenAnalysisDetailStudentPage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class VanclassSpoken(unittest.TestCase):
    """本班口语作业 - 答题分析tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.hw_detail = HwDetailPage()
        cls.v_hw = VanclassHwPage()
        cls.ques_check = SpokenAnalysisDetailQuestionPage()
        cls.st_check = SpokenAnalysisDetailStudentPage()
        cls.van = VanclassPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassSpoken, self).run(result)

    @testcase
    def test_vanclass_spoken_analysis_detail(self):
        """按学生查看& 按题查看tab"""
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
    
        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)
        self.van.vanclass_hw()  # 点击 本班作业 tab
        name = self.v_hw.into_operation(gv.HW_TITLE, gv.VANCLASS, '口语')
    
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
        print("题单:", name[0])
        self.answer_analysis_operation()  # 答题分析 tab
    
        if self.hw_detail.wait_check_page():  # 页面检查点
            self.v_hw.back_up_button()  # 返回 作业列表
            self.vue.app_web_switch()  # 切到apk 再切到vue
            if self.v_hw.wait_check_page(name[1]):  # 页面检查点
                self.v_hw.back_up_button()  # 返回班级详情页
                self.vue.app_web_switch()  # 切到apk 再切到vue

                if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                    self.van.back_up_button()
                    self.vue.switch_app()

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        analysis = self.hw_detail.analysis_tab()  # 答题分析 tab
        analysis.click()  # 进入 答题分析 tab
        print('=======================答题分析tab=======================')
        if self.hw_detail.wait_check_hw_list_page():
            name = self.hw_detail.game_name()  # 游戏name
            print(name[0].text)
            name[0].click()  # 进入按学生看/按题查看 tab页
            self.vue.app_web_switch()  # 切到apk 再切到vue

            self.check_st_operation()  # 按学生查看 tab
            self.check_question_operation()  # 按题查看 tab
        elif self.hw_detail.wait_check_empty_tips_page():
            print('暂无数据')

    @teststeps
    def check_st_operation(self):
        """按学生看tab 具体操作"""
        if self.st_check.wait_check_page():
            print('-------------------按学生看tab--------------------')
            if self.st_check.wait_check_list_page():
                self.st_list_detail()  # 学生列表信息统计
                print('=========================================')

                student = self.st_check.st_items()  # 学生条目
                st_mode = self.st_check.st_finish_status()  # 学生 完成与否
                for i in range(len(student)):
                    if self.st_check.wait_check_list_page():  # 页面检查点
                        var = self.hw_detail.st_name()[i].text  # 学生name
                        if st_mode[i].text != '未作答':
                            student[i].click()  # 进入一个学生的 答题情况页

                            self.vue.app_web_switch()  # 切到apk 再切到vue
                            if self.st_check.wait_check_detail_page():  # 页面检查点
                                print('学生%s答题情况:' % var)
                                self.st_check.per_student_answer_detail()  # 答题情况详情

                                if self.st_check.wait_check_detail_list_page():  # 页面检查点
                                    self.v_hw.back_up_button()  # 返回 按学生看tab
                                    self.vue.app_web_switch()  # 切到apk 再切到vue
                        else:
                            print('学生%s未作答' % var)
                        print('----------------------------------------')
            elif self.hw_detail.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def check_question_operation(self):
        """按题查看tab 具体操作"""
        if self.ques_check.wait_check_page():  # 页面检查点
            question_tab = self.ques_check.question_tab()  # 按题查看 tab
            question_tab.click()  # 进入 按题查看 tab页
            print('-------------------按题查看tab--------------------')
            if self.ques_check.wait_check_list_page():
                self.answer_list_detail()  # 按题查看 tab页
                print('=========================================')

                game = self.ques_check.game_items()  # 游戏条目
                for i in range(len(game) - 1):
                    if self.ques_check.wait_check_list_page():
                        self.ques_check.game_items()[i].click()  # 进入小题详情页

                        self.vue.app_web_switch()  # 切到apk 再切到vue
                        if self.ques_check.wait_check_detail_page():
                            if self.ques_check.wait_check_detail_list_page():
                                self.ques_check.per_question_answer_detail()  # 答题情况详情

                                if self.ques_check.wait_check_detail_list_page():  # 页面检查点
                                    self.v_hw.back_up_button()  # 返回 按题查看tab
                                    self.vue.app_web_switch()  # 切到apk 再切到vue
            elif self.hw_detail.wait_check_empty_tips_page():
                print('暂无数据')

            if self.ques_check.wait_check_page():  # 页面检查点
                self.v_hw.back_up_button()  # 返回 答题分析 tab 页
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def st_list_detail(self):
        """按学生查看 详情页
        """
        name = self.hw_detail.st_name()  # 学生name
        icon = self.hw_detail.st_icon()  # 学生头像
        status = self.st_check.st_finish_status()  # 学生已完成/星星数

        for i in range(len(icon)):
            print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

    @teststeps
    def answer_list_detail(self):
        """按题查看 详情页
        """
        sentence = self.ques_check.games_item_list()[1]  # 游戏题目
        speak = self.ques_check.speak_button()  # 发音按钮

        for j in range(len(sentence)):
            print(sentence[j])
            # speak[j].click()
