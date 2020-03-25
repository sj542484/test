#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class Homework(unittest.TestCase):
    """作业列表 & 答题分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.info = DynamicPage()
        cls.detail = HwDetailPage()
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
        super(Homework, self).run(result)

    @testcase
    def test_homework_list_and_tab(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入习题 最近动态页面
            if self.info.wait_check_app_page():  # 页面检查点
                self.vue.switch_h5()  # 切到web

                if self.info.wait_check_page():  # 页面检查点
                    if self.info.wait_check_no_hw_page():
                        print('最近习题动态页面为空')
                        self.info.back_up_button()
                        self.assertFalse(self.info.wait_check_no_hw_page(), self.info.dynamic_empty_tips)
                    else:
                        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                        self.info.hw_list_operation()  # 列表
                        self.info.into_hw()  # 进入 作业包
                        self.vue.app_web_switch()  # 切到apk 再切回web

                        if self.detail.wait_check_page():
                            status = self.finish_situation_operation()  # 完成情况 tab
                            score = self.answer_analysis_operation()  # 答题分析 tab
                            self.judge_data_operation(status, score)  # 验证 两个tab页的数据一致

                            if self.detail.wait_check_page():
                                self.info.back_up_button()  # 返回 作业list 页面
                                self.vue.app_web_switch()  # 切到apk 再切回web

                                if self.info.wait_check_page():  # 页面检查点
                                    self.info.back_up_button()  # 返回 主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        print('===================完成情况tab===================')
        status = self.detail.wait_check_empty_tips_page()
        if status:
            print('暂无数据')
            self.info.back_up_button()  # 返回
            self.vue.app_web_switch()  # 切到apk 再切回web

            if self.info.wait_check_page():  # 页面检查点
                self.info.back_up_button()  # 返回 主界面
                self.vue.switch_app()  # 切回apk
            self.assertFalse(status, '暂无数据')
        else:
            self.assertTrue(self.detail.wait_check_st_list_page(), self.detail.st_list_tips)
            return self.st_list_statistics()  # 完成情况 学生列表

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        if self.detail.wait_check_page():
            self.detail.analysis_tab()  # 进入 答题分析 tab页
            print('===================答题分析tab===================')
            status = self.detail.wait_check_empty_tips_page()
            if status:
                print('暂无数据')
                self.info.back_up_button()  # 返回
                self.vue.app_web_switch()  # 切到apk 再切回web

                if self.info.wait_check_page():  # 页面检查点
                    self.info.back_up_button()  # 返回 主界面
                    self.vue.switch_app()  # 切回apk
                self.assertFalse(status, '暂无数据')
            else:
                self.assertTrue(self.detail.wait_check_hw_list_page(), self.detail.hw_list_tips)
                return self.answer_analysis_detail()  # 答题分析 列表

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        st = self.detail.st_name()  # 学生name
        icon = self.detail.st_icon()  # 学生头像
        status = self.detail.st_finish_status()  # 学生完成与否
        st_mode = self.detail.st_type()  # 基础班/提分版/试用期

        content = []
        for i in range(len(st)):
            print('--------------------------------------')
            var = status[i].text
            print(icon[i].get_attribute('src'), '\n',
                  st[i].text, st_mode[i].text, '\n',
                  status[i].text)
            content.append(var)
        return content


    @teststeps
    def answer_analysis_detail(self):
        """答题分析 详情页"""
        name = self.detail.game_name()  # 游戏名称
        mode = self.detail.game_type()  # 游戏类型
        num = self.detail.game_num()  # 小题数
        average = self.detail.average_achievement()  # 本班完成率

        content = {}
        for j in range(len(mode)):
            print('--------------------------------------')
            item = num[j].text
            var = average[j].text
            print(mode[j].text, item, '\n',
                  name[j].text, '\n',
                  var)

            content[int(re.sub('\D', '', item))] = int(re.sub('\D', '', var))
        return content

    @teststeps
    def judge_data_operation(self, status, score):
        """验证 两个tab页的数据一致
        全部未完成:有两种情况,未开始答题,或者完成一部分;结果就是:至少有一个‘全班首轮平均成绩0%’的game
        全部已完成/部分已完成：都有可能
        """
        print('=============验证 两个tab页的数据一致=============')
        print(status)
        print(score)
        count = []
        finish = []
        for k in range(len(status)):
            if status[k] == '未完成':
                count.append(k)
            else:
                finish.append(k)

        if len(count) == len(status):
            content = [score[k] for k in score if score[k] == 0]
            self.assertTrue(len(content) != 0, '两个tab页的数据不一致, 所有为未完成，至少有一个‘全班首轮平均成绩0%’的game')
            print('两个tab页的数据一致')
        else:  # 最优成绩72% 积分9 星星16
            integral = 0  # 积分
            star = 0  # 星星
            for i in finish:
                var = status[i].split()
                integral += int(re.sub('\D', '', var[1]))  # 积分
                star += int(re.sub('\D', '', var[2]))  # 星星

            average = 0
            for key, value in score.items():
                average += round(value / 100 * key)

            print('比较：', integral, average)
            if integral < average:
                self.assertTrue('', '全班首轮平均成绩比学生积分数高')
            print('数据一致')
