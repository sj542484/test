#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Homework(unittest.TestCase):
    """习题列表 & 答题分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.v_detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_homework_list_and_tab(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    title = gv.HW_TITLE.format(gv.VANCLASS)
                    print(title)
                    if self.v_detail.wait_check_page(title):  # 页面检查点
                        print('本班作业:')
                        if self.v_detail.wait_check_list_page():
                            name = self.v_detail.hw_name()  # 作业name
                            progress = self.v_detail.progress()  # 进度
                            count = 0
                            for i in range(len(name)):
                                pro = progress[i].text  # int(re.sub("\D", "", progress[i].text))
                                if int(pro[3]) != 0:
                                    print('###########################################################')
                                    print('作业:', name[i].text)
                                    name[i].click()  # 进入 作业
                                    count += 1
                                    break
                            if count == 0:
                                print('暂无该作业')
                            else:
                                if self.detail.wait_check_page():  # 页面检查点
                                    self.finish_situation_operation()  # 完成情况 tab
                                    self.answer_analysis_operation()  # 答题分析 tab

                                    if self.detail.wait_check_page():  # 页面检查点
                                        self.home.back_up_button()  # 返回 本班作业
                        elif self.v_detail.wait_check_empty_tips_page():
                            self.v_detail.no_data()  # 暂无数据

                        if self.v_detail.wait_check_page(title):  # 本班作业 页面检查点
                            self.home.back_up_button()  # 返回 班级详情页面
                            if self.van.wait_check_page(gv.VANCLASS):  # 班级详情 页面检查点
                                self.home.back_up_button()  # 返回主界面
                    else:
                        print('!!!未进入本班作业')
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
            print('-------------------完成情况tab-------------------')
            if self.detail.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况 学生列表
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

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
                    print('-------------------答题分析tab-------------------')
                    if self.detail.wait_check_hw_list_page():
                        self.answer_analysis_detail()  # 答题分析 列表
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答题分析 详情页"""
        if content is None:
            content = []

        item = self.detail.game_item()  # 游戏 条目

        if len(item) > 4 and not content:
            content = []
            var = []  # 游戏name
            for i in range(len(item) - 1):
                if len(item[i]) == 4:  # 无提分标志
                    print(item[i][0], '\n', item[i][1], '\n', item[i][2])
                else:
                    print(item[i][0], item[i][1], '\n', item[i][2], '\n', item[i][3])
                print('---------------------------')

            if len(item[-2]) == 4:  # 无提分标志
                var.append(item[-2][1])
            else:
                var.append(item[-2][2])

            content.append(var[0])  # 最后一个game的name
            content.append(item[-2][0])  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content)
        else:
            var = 0
            if content:
                for k in range(len(item)):
                    title = []
                    if len(item[k]) == 4:  # 无提分标志
                        title.append(item[k][1])
                    else:
                        title.append(item[k][2])

                    if content[0] == title[0] and content[1] == item[k][0]:
                        var = k+1
                        break

            for i in range(var, len(item)):
                if len(item[i]) == 4:  # 无提分标志
                    print(item[i][0], '\n', item[i][1], '\n', item[i][2])
                else:
                    print(item[i][0], item[i][1], '\n', item[i][2], '\n', item[i][3])
                print('---------------------------')

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        name = self.detail.st_name()  # 学生name
        icon = self.detail.st_icon()  # 学生头像
        status = self.detail.st_finish_status()  # 学生完成与否 todo
        # arrow = self.detail.arrow_button()  # 转至按钮

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息
        else:
            print('★★★ Error-已完成/未完成 学生列表信息统计', len(icon), len(name))
