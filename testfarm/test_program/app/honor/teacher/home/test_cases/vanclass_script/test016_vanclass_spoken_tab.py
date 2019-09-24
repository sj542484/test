#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Spoken(unittest.TestCase):
    """口语 完成情况&答题分析 tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.speak = SpokenDetailPage()
        cls.v_detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_spoken_tab(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_hw()  # 进入 本班作业
                    title = gv.HW_TITLE.format(gv.VANCLASS)
                    if self.van.wait_check_page(gv.SPOKEN):  # 页面检查点
                        if self.v_detail.wait_check_empty_tips_page():  # 无口语作业时
                            self.v_detail.no_data()  # 暂无数据
                        else:  # 有作业
                            self.v_detail.into_operation(gv.SPOKEN, title)  # 进入某个作业 游戏列表

                            if self.speak.wait_check_page():  # 页面检查点
                                if self.speak.wait_check_st_list_page():
                                    print("题单:", gv.SPOKEN)
                                    self.finish_situation_operation()  # 完成情况 tab
                                    self.answer_analysis_operation()  # 答题分析 tab
                                    if self.speak.wait_check_page():  # 页面检查点
                                        self.home.back_up_button()  # 返回 本班口语作业

                        if self.van.wait_check_page(title):  # 页面检查点
                            self.home.back_up_button()  # 返回 班级详情页面
                            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                                self.home.back_up_button()  # 返回主界面
                    else:
                        print('!!!未进入本班卷子')
                else:
                    print('!!!暂无 {} 班级'.format(gv.VANCLASS))
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        analysis = self.detail.finished_tab()  # 完成情况 tab
        if self.get.selected(analysis) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('====================完成情况tab====================')
            if self.speak.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况tab 列表信息
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def st_list_statistics(self, content=None):
        """完成情况 tab页信息"""
        if content is None:
            content = []

        name = self.detail.st_name()  # 学生name
        status = self.detail.st_finish_status()  # 学生完成与否

        if len(name) > 7 and not content:
            content = []
            for i in range(len(name)-1):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

            content.append(name[-2].text)  # 最后一个game的name
            content.append(status[len(name)-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.st_list_statistics(content)
        else:
            var = 0
            if content:
                for k in range(len(name)):
                    if content[0] == name[k].text and content[1] == status[k].text:
                        var += k
                        break

            for j in range(var, len(name)):
                print('学生:', name[j].text, ' ', status[j].text)  # 打印所有学生信息

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        if self.detail.wait_check_page():  # 页面检查点
            analysis = self.detail.analysis_tab()  # 答题分析 tab
            if self.get.selected(analysis) is True:
                print('★★★ Error- 默认在 答题分析 tab页')
            else:
                analysis.click()  # 进入 答题分析 tab页
                if self.get.selected(analysis) is False:
                    print('★★★ Error- 进入 答题分析 tab页')
                else:
                    print('====================答题分析tab====================')
                    if self.speak.wait_check_spoken_list_page():
                        self.answer_analysis_detail()  # 答题分析tab 列表信息
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答题分析 tab页信息"""
        if content is None:
            content = []

        mode = self.detail.game_type()  # 游戏类型
        name = self.detail.game_name()  # 游戏name
        average = self.detail.average_achievement()  # 本班完成率

        if len(mode) > 5 and not content[0]:
            content = []
            for j in range(len(mode) - 1):
                print(mode[j].text, name[j].text, average[j].text)

            content.append(name[len(mode)-2].text)  # 最后一个game的name
            content.append(mode[-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content)
        else:
            var = 0
            if content:
                for k in range(len(mode)):
                    if content[0] == name[k].text and content[1] == mode[k].text:
                        var += k
                        break

            for j in range(var, len(mode)):
                print(mode[j].text, name[j].text, average[j].text)
