#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
import re
import time
import random

from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.object_page.hw_finish_tab_student_answer_game_detail_page import StAnswerDetailPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.hw_finish_tab_student_answer_result_page import ResultDetailPage
from app.honor.teacher.home.vanclass.test_data.hw_detail_data import game_type_operation
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassHw(unittest.TestCase):
    """本班习题 - 完成情况tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van = VanclassPage()
        cls.v_hw = VanclassHwPage()
        cls.hw_detail = HwDetailPage()
        cls.st_answer = StAnswerDetailPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()
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
    def test_vanclass_hw_per_detail(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)

        self.van.vanclass_hw()  # 点击 本班作业 tab
        title = gv.HW_TITLE.format(gv.VANCLASS)
        self.vue.app_web_switch()  # 切到apk 再切回vue

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        if self.v_hw.wait_check_empty_tips_page():
            self.v_hw.no_data()  # 暂无数据
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
        else:
            print('本班作业:')   # 全部题单都跑
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
            name = self.v_hw.hw_name()  # 作业name
            for i in range(4, len(name)):
                if self.v_hw.wait_check_page(title):  # 页面检查点
                    text = name[i].text
                    if self.home.brackets_text_in(text) == '习题':
                        print('###########################################################')
                        print(text)
                        name[i].click()  # 进入作业

                        self.vue.app_web_switch()  # 切到apk 再切回web
                        self.finish_situation_operation()  # 进入 个人答题详情页
                self.vue.app_web_switch()  # 切到apk 再切回vue
                self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点

            self.v_hw.back_up_button()  # 返回 班级详情页面
            self.vue.app_web_switch()  # 切到apk 再切回vue
            self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
            self.v_hw.back_up_button()  # 返回主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
        status = self.hw_detail.st_finish_status()  # 学生完成与否
        st_mode = self.hw_detail.st_type()  # 基础班/提分版/试用期

        for i in range(len(status)):
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
            st = self.hw_detail.st_name()  # 学生name
            name = st[i].text  # 学生name
            if status[i].text != '未完成':
                mode = st_mode[i].get_attribute('src')
                st[i].click()  # 进入一个学生的答题情况页

                self.vue.app_web_switch()  # 切到apk 再切回vue
                self.assertTrue(self.st_answer.wait_check_page(name), self.st_answer.st_detail_tips)  # 页面检查点
                print('学生 %s 答题情况：' % name)
                self.per_game_list(name)  # 列表信息
                self.per_answer_detail(name, mode)

                self.assertTrue(self.st_answer.wait_check_page(name), self.st_answer.st_detail_tips)  # 页面检查点                        self.v_hw.back_up_button()  # 返回 学生列表
                self.v_hw.back_up_button()  # 返回 学生列表
                self.vue.app_web_switch()  # 切到apk 再切回vue
            else:
                print('学生%s未完成' % name)

        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 本班习题

    @teststeps
    def per_answer_detail(self, st, content=None):
        """个人 答题情况详情页"""
        if content is None:
            content = []

        self.assertTrue(self.st_answer.wait_check_page(st), self.st_answer.st_detail_tips)  # 页面检查点
        item = self.st_answer.per_game_item()[1]  # 游戏条目

        if len(item) > 5 and not content:
            content = [item[-2]]  # 最后一个game的name type
            self.game_type_judge_operation(len(item)-1, st)  # 小游戏 类型判断 及具体操作

            self.assertTrue(self.st_answer.wait_check_page(st), self.st_answer.st_detail_tips)  # 页面检查点
            self.v_hw.swipe_vertical_web(0.5, 0.9, 0.1)
            self.per_answer_detail(st, content)
        else:
            var = 0
            if content:
                for k in range(len(item)):
                    if content == item[k]:
                        var += k+1
                        break

            self.game_type_judge_operation(len(item), st, var)  # 小游戏 类型判断 及具体操作

    @teststeps
    def game_type_judge_operation(self, length, st, index=0):
        """小游戏 类型判断 及具体操作"""
        self.assertTrue(self.st_answer.wait_check_page(st), self.st_answer.st_detail_tips)  # 页面检查点
        item = self.st_answer.per_game_item()  # 游戏条目

        for j in range(index, length):
            print('=================================================================')
            self.assertTrue(self.st_answer.wait_check_page(st), self.st_answer.st_detail_tips)  # 页面检查点
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
                    self.v_hw.back_up_button()   # 返回  游戏列表
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
                print(item[1][j][0], ' --该题还未做')

            self.vue.app_web_switch()  # 切到apk 再切回vue

    @teststeps
    def per_game_list(self, st, content=None):
        """个人 game答题情况页 列表"""
        if content is None:
            content = []

        self.assertTrue(self.st_answer.wait_check_page(st), self.st_answer.st_detail_tips)  # 页面检查点
        name = self.st_answer.game_name()  # 游戏name
        mode = self.st_answer.game_type()  # 类型
        status = self.st_answer.optimal_first_achievement()  # 游戏完成情况

        if len(status) > 4 and not content:
            content = [name[len(status)-2].text, mode[len(status)-2].text]
            for i in range(len(status)-1):
                print(mode[i].text, name[i].text, status[i].text)

            self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            self.per_game_list(st, content)
        else:
            var = 0
            if content:  # 翻页成功 或者是第一页
                for k in range(len(name)):
                    if content == [name[k].text, mode[k].text]:
                        var = k + 1
                        break

            for i in range(var, len(status)):
                print(mode[i].text, name[i].text, status[i].text)
            print('---------------------------------------------')
