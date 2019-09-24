#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest
import re

from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Homework(unittest.TestCase):
    """习题 - 完成情况tab 详情 &cup"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.van = VanclassPage()
        cls.v_detail = VanclassDetailPage()
        cls.get = GetAttribute()
        cls.info = DynamicPage()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_hw_per_detail_and_cup(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    title = gv.HW_TITLE.format(gv.VANCLASS)
                    if self.v_detail.wait_check_page(title):  # 页面检查点
                        print('本班作业:')
                        if self.v_detail.wait_check_list_page():
                            self.hw_list_operation(title)  # 具体操作
                        elif self.v_detail.wait_check_empty_tips_page():
                            self.v_detail.no_data()  # 暂无数据

                        if self.v_detail.wait_check_page(title):  # 页面检查点
                            self.home.back_up_button()  # 返回 答题详情页面
                            if self.van.wait_check_page(gv.VANCLASS):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('★★★ Error- 未进入 习题作业页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def hw_list_operation(self, title):
        """作业列表"""
        name = self.v_detail.hw_name()  # 作业name
        for i in range(len(name)):
            if self.v_detail.wait_check_page(title):  # 页面检查点
                text = name[i].text
                if self.home.brackets_text_in(text) == '习题':
                    print('###########################################################')
                    print(text)
                    name[i].click()  # 进入作业

                    if self.detail.wait_check_page():  # 页面检查点
                        self.finish_situation_operation()  # 完成情况tab 具体操作
                        self.answer_analysis_operation()  # 答题分析tab 具体操作

                        if self.detail.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回
                    else:
                        print('★★★ Error- 未进入作业 %s 页面' % text)

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        analysis = self.detail.finished_tab()  # 完成情况 tab
        if self.get.selected(analysis) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('-------------------------完成情况tab-------------------------')
            if self.detail.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况tab 学生
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
                    print('-------------------------答题分析tab-------------------------')
                    if self.detail.wait_check_hw_list_page():
                        self.answer_analysis_detail()  # 答题分析 列表
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def st_list_statistics(self):
        """完成情况tab 学生信息"""
        name = self.detail.st_name()  # 学生name
        icon = self.detail.st_icon()  # 学生头像
        status = self.detail.st_finish_status()  # 学生完成与否

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                if self.detail.wait_check_page():  # 页面检查点
                    status = self.detail.st_finish_status()  # 学生完成与否
                    name = self.detail.st_name()  # 学生name
                    text = name[i].text
                    if status[i].text == '未完成':
                        print('学生 %s 未完成该作业' % text)
                    else:
                        name[i].click()  # 进入一个学生的答题情况页
                        if self.v_detail.wait_check_page(text):  # 页面检查点
                            print('学生 %s 答题情况:' % text)
                            self.per_answer_detail()  # 答题情况详情页 展示不全 滑屏

                            if self.v_detail.wait_check_page(text):  # 页面检查点
                                self.home.back_up_button()

                    print('-----------------------------------------')
        else:
            print('★★★ Error-完成情况tab 列表信息统计', len(icon), len(name))

    @teststeps
    def per_answer_detail(self, content=None):
        """个人 答题情况详情页"""
        if content is None:
            content = []

        mode = self.detail.game_type()  # 游戏类型
        name = self.detail.game_name()  # 游戏name
        num = self.detail.game_num()  # 游戏 小题数
        optimal = self.detail.optimal_achievement()  # 最优成绩

        if len(optimal) > 4 and not content:
            content = []
            for j in range(len(optimal) - 1):
                print(mode[j].text, num[j].text, '\n',
                      name[j].text, '\n',
                      optimal[j].text)
                print('--------------------')

            content.append(name[len(optimal)-2].text)  # 最后一个game的name
            content.append(mode[-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.per_answer_detail(content)
        else:
            var = 0
            if content:
                if content[0] != name[-1].text and content[1] != mode[-1].text:
                    for k in range(len(name)):
                        if content[0] == name[k].text and content[1] == mode[k].text:
                            var += k + 1
                            break

            for j in range(var, len(name)):
                print(mode[j].text, num[j].text, '\n',
                      name[j].text, '\n',
                      optimal[j].text)
                print('--------------------')

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答题分析 详情页"""
        if content is None:
            content = []

        item = self.detail.game_item()  # 游戏 条目

        if len(item) > 4 and not content:
            content = [item[-2][2]]
            self.cup_operation(item, len(item)-1)  # 进入cup页面 及具体操作

            if self.detail.wait_check_hw_list_page():
                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.answer_analysis_detail(content)
        else:
            var = 0
            if content:
                for k in range(len(item)):
                    if content[0] in item[k]:
                        var += k+1
                        break

            self.cup_operation(item, len(item)-1, var)  # 进入cup页面 及具体操作

    @teststeps
    def cup_operation(self, item, length, index=0):
        """进入cup页面 及具体操作"""
        for i in range(index, length):
            var = []
            if self.detail.wait_check_page():  # 页面检查点
                if len(item[i]) == 4:  # 无提分标志
                    print(item[i][0], '\n', item[i][1], '\n', item[i][2])
                    num = int(re.sub(r"\D", "", item[i][2]))  # 提取 全班首轮平均成绩
                    var.append(item[i][1])
                else:
                    print(item[i][0], item[i][1], '\n', item[i][2], '\n', item[i][3])
                    num = int(re.sub(r"\D", "", item[i][3]))  # 提取 全班首轮平均成绩
                    var.append(item[i][2])

                if num != 0:
                    if self.get.enabled(item[i][-1]) == 'true':
                        item[i][-1].click()  # 点击奖杯 icon

                        if self.info.wait_check_page(var[0]):  # 作业 页面检查点
                            self.best_accuracy()  # 奖杯页面 最优成绩tab
                            self.first_accuracy()  # 奖杯页面 首次成绩tab

                            if self.v_detail.wait_check_achievement_list_page():  # 作业 页面检查点
                                self.home.back_up_button()
                    else:
                        print('cup不可点击')
                print('-----------------------------------------')

    @teststeps
    def best_accuracy(self):
        """单个题目 答题详情 操作"""
        all_hw = self.v_detail.best_tab()  # 最优成绩 tab

        if self.get.selected(all_hw) == 'false':
            print('★★★ Error- 未默认在 最优成绩页面')
        else:
            print('--------最优成绩tab--------')
            if self.v_detail.wait_check_achievement_list_page():
                self.accuracy_detail()
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def first_accuracy(self):
        """首次成绩tab 具体操作"""
        incomplete = self.v_detail.first_tab()  # 首次成绩 tab
        print(self.get.selected(incomplete))
        if self.get.selected(incomplete) == 'true':
            print('★★★ Error- 默认在 首次成绩 tab页')
        else:
            incomplete.click()  # 进入 首次成绩 tab页
            if self.get.selected(incomplete) == 'false':
                print('★★★ Error- 进入 首次成绩 tab页')
            else:
                print('--------首次成绩tab--------')
                if self.v_detail.wait_check_achievement_list_page():
                    self.accuracy_detail()
                elif self.home.wait_check_empty_tips_page():
                    print('暂无数据')

    @teststeps
    def accuracy_detail(self, content=None):
        """首次成绩/最优成绩 详情"""
        if content is None:
            content = []

        order = self.v_detail.st_order()  # 编号
        icon = self.v_detail.st_icon()  # 头像
        name = self.v_detail.st_name()  # 昵称
        accuracy = self.v_detail.accuracy()  # 正答率
        spend = self.v_detail.spend_time()  # 用时

        if len(order) > 5 and not content:
            content = [name[len(order) - 2].text]  # 最后一个game的name
            for j in range(len(order) - 1):
                print(order[j].text, name[j].text, accuracy[j].text, spend[j].text)

            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.accuracy_detail(content)
        else:
            var = 0
            if content:
                for k in range(len(icon)):
                    if content[0] == name[k].text:
                        var += k
                        break

            for j in range(var, len(icon)):
                print(order[j].text, name[j].text, accuracy[j].text, spend[j].text)
