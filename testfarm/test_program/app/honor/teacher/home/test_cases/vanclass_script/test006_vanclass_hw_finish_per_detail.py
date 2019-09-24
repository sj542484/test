#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import unittest
import re
import time

from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.result_detail_page import ResultDetailPage
from app.honor.teacher.home.test_data.hw_detail_data import game_type_operation
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class VanclassHw(unittest.TestCase):
    """本班习题 - 完成情况tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.v_detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.detail = HwDetailPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_hw_per_detail(self):
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
                            count = []
                            for i in range(len(name)):
                                text = name[i].text
                                if self.v_detail.wait_check_list_page():
                                    if self.home.brackets_text_in(text) == '习题':
                                        count.append(i)

                            if len(count) == 0:
                                print('暂无习题作业包')
                            else:
                                index = random.randint(0, len(count) - 1)
                                text = name[count[index]].text
                                print('#########################################################################')
                                print(text)
                                name[count[index]].click()  # 进入作业
                                self.finish_situation_operation()  # 进入 个人答题详情页
                        elif self.v_detail.wait_check_empty_tips_page():
                            self.v_detail.no_data()  # 暂无数据

                        if self.van.wait_check_page(title):  # 本班作业 页面检查点
                            self.home.back_up_button()  # 返回 班级详情页面
                            if self.van.wait_check_page(gv.VANCLASS):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('★★★ Error- 未进入 习题作业页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        if self.detail.wait_check_page():  # 页面检查点
            analysis = self.detail.finished_tab()  # 完成情况 tab
            if self.get.selected(analysis) is False:
                print('★★★ Error- 未默认在 完成情况 tab页')
            else:
                if self.detail.wait_check_st_list_page():
                    st = self.detail.st_name()  # 学生name
                    length = len(st)
                    if len(st) != 1:
                        length = 2
                    for i in range(length):
                        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        if self.detail.wait_check_st_list_page():
                            st = self.detail.st_name()  # 学生name
                            name = st[i].text  # 学生name
                            st[i].click()  # 进入一个学生的答题情况页

                            if self.v_detail.wait_check_page(name):  # 页面检查点
                                print('学生 %s 答题情况：' % name)
                                self.per_answer_detail(name)

                                if self.v_detail.wait_check_page(name):  # 页面检查点
                                    self.home.back_up_button()  # 返回 学生列表

                    if self.detail.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回 本班习题
                elif self.home.wait_check_empty_tips_page():
                    print('暂无学生')
        else:
            print('★★★ Error- 未进入作业页面')
            time.sleep(2)
            self.home.back_up_button()  # 返回 本班习题 页面

    @teststeps
    def per_answer_detail(self, st, content=None):
        """个人 答题情况详情页"""
        if content is None:
            content = []

        if self.detail.wait_check_per_detail_page():
            if self.detail.wait_check_per_detail_page():
                item = self.detail.per_game_item()  # 游戏条目

                if len(item[1]) > 5 and not content:
                    var = []  # 游戏name
                    if len(item[1][-2]) == 4:  # 无提分标志
                        var.append(item[1][-2][2])
                    else:
                        var.append(item[1][-2][3])

                    content.append(var[0])  # 最后一个game的name
                    content.append(item[1][-2][0])  # 最后一个game的type
                    self.game_type_judge_operation(len(item[1])-1, st)  # 小游戏 类型判断 及具体操作

                    if self.detail.wait_check_per_detail_page():
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
                        self.per_answer_detail(st, content)
                else:
                    var = 0
                    if content:
                        for k in range(len(item[1])):
                            title = []
                            if len(item[1][k]) == 4:  # 无提分标志
                                title.append(item[1][k][2])
                            else:
                                title.append(item[1][k][3])

                            if content[0] == title[0] and content[1] == item[1][k][0]:
                                var += k+1
                                break

                    self.game_type_judge_operation(len(item[1]), st, var)  # 小游戏 类型判断 及具体操作

    @teststeps
    def game_type_judge_operation(self, length, st, index=0):
        """小游戏 类型判断 及具体操作"""
        if self.v_detail.wait_check_page(st):  # 页面检查点
            item = self.detail.per_game_item()  # 游戏条目

            for j in range(index, length):
                if self.v_detail.wait_check_page(st):  # 页面检查点
                    title = []
                    var = item[1][j][-1].split()

                    best = re.sub("\D", "", var[1])
                    score = re.sub("\D", "", var[-1])
                    if len(item[1][j]) == 4:  # 无提分标志
                        title.append(item[1][j][2])
                        count = int(re.sub("\D", "", item[1][j][1]))  # 小题数
                    else:
                        title.append(item[1][j][3])
                        count = int(re.sub("\D", "", item[1][j][2]))  # 小题数

                    item[0][j].click()  # 点击进入game
                    if best != '' and int(best) >= int(score):  # 已做
                        print(item[1][j][0], title[0])
                        value = game_type_operation(item[1][j][0])

                        if self.result.wait_check_page(title[0]):
                            if value == 17:
                                Toast().toast_operation('无需答题报告，答对即可')  # 获取toast信息 '无需答题报告，答对即可'

                                print('==========================================================')
                            elif value in (21, 22):
                                print('口语')  # todo 口语
                                time.sleep(2)
                                self.home.back_up_button()
                            else:
                                print('=====================答题情况 详情页======================')
                                self.result.hw_detail_operation(value, count, score)

                                if self.result.wait_check_page(title[0]):
                                    self.home.back_up_button()  # 返回  游戏列表
                        elif value == 16:  # 连连看
                            content = []
                            self.result.answer_explain_type(content, self.result.ergodic_list, self.result.result_answer)  # 不需要统计答对的小题
                    elif best == score == '':
                        print(item[1][j][0], '\n', title[0], ' --该题还未做')
                        print('==========================================================')
