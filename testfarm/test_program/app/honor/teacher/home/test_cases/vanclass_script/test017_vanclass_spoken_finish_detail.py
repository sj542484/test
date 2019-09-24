#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Spoken(unittest.TestCase):
    """本班作业 - 完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.homework = HwDetailPage()
        cls.detail = VanclassDetailPage()
        cls.speak = SpokenDetailPage()
        cls.van = VanclassPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_spoken_finish_tab(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_hw()  # 进入 本班作业
                    title = gv.HW.format(gv.VANCLASS)
                    if self.van.wait_check_page(gv.SPOKEN):  # 页面检查点
                        if self.detail.wait_check_empty_tips_page():  # 无作业作业时
                            self.detail.no_data()  # 暂无数据
                        else:  # 有作业
                            self.detail.into_operation(gv.SPOKEN, title)  # 进入某个作业 游戏列表

                            if self.speak.wait_check_page():  # 页面检查点
                                if self.speak.wait_check_st_list_page():
                                    print("题单:", gv.SPOKEN)
                                    self.finish_situation_operation()  # 完成情况 tab

                                if self.speak.wait_check_page():  # 页面检查点
                                    self.home.back_up_button()  # 返回 作业列表

                        if self.van.wait_check_page(title):  # 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                                self.home.back_up_button()
                    else:
                        print('★★★ Error- 未进入本班作业')
            else:
                print('★★★ Error- 未进入班级页面')
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        analysis = self.homework.finished_tab()  # 完成情况 tab
        if self.get.selected(analysis) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('====================完成情况tab====================')
            if self.speak.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况tab 列表信息
                print('=========================================')

                status = self.speak.st_finish_status()  # 学生完成与否
                for i in range(len(status)):
                    if self.speak.wait_check_st_list_page():  # 页面检查点
                        name = self.speak.st_name()  # 学生name
                        print('学生%s答题情况:' % name[i].text)
                        name[i].click()  # 进入一个学生的 game答题情况页

                        self.per_game_detail_operation()  # game答题情况页

                        if self.speak.wait_check_game_list_page():  # 页面检查点
                            self.home.back_up_button()  # 返回完成情况tab
                        print('----------------------------------------')

            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def st_list_statistics(self, content=None):
        """完成情况 tab页信息"""
        if content is None:
            content = []

        name = self.homework.st_name()  # 学生name
        # icon = self.detail.st_icon()  # 学生头像
        status = self.homework.st_finish_status()  # 学生完成与否

        if len(name) > 4 and not content:
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
    def per_game_detail_operation(self):
        """个人 game答题情况页"""
        self.per_game_list()  # 列表信息

        if self.speak.wait_check_game_list_page():  # 页面检查点
            status = self.speak.game_finish_status()  # 游戏完成情况

            for j in range(len(status)):
                if self.speak.wait_check_game_list_page():  # 页面检查点
                    game = self.homework.game_name()  # 游戏name
                    if status[j] != '未完成':
                        print('--------------------------------')
                        print('答题情况详情:')
                        game[j].click()  # game答题情况详情页
                        self.per_answer_detail()  # 答题情况详情

                        if self.speak.wait_check_detail_page():  # 页面检查点
                            self.home.back_up_button()  # 返回game列表页

    @teststeps
    def per_game_list(self, content=None):
        """个人 game答题情况页 列表"""
        if content is None:
            content = []

        if self.speak.wait_check_game_list_page():  # 页面检查点
            name = self.homework.game_name()  # 游戏name
            mode = self.homework.game_type()  # 类型
            num = self.homework.game_num()  # 小题数
            status = self.speak.game_finish_status()  # 游戏完成情况

            if len(status) > 4 and not content:
                content = [name[len(status)-2].text]
                for i in range(len(status)-1):
                    print(mode[i].text, name[i].text, num[i].text, status[i])

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.per_game_list(content)
            else:
                var = 0
                if content:  # 翻页成功 或者是第一页
                    for k in range(len(name)):
                        if content[0] == name[k].text:
                            var = k + 1
                            break

                for i in range(var, len(status)):
                    print(mode[i].text, name[i].text, num[i].text, status[i])

    @teststeps
    def per_answer_detail(self, content=None):
        """game 答题情况详情页"""
        if content is None:
            content = []

        if self.speak.wait_check_detail_page():  # 页面检查点
            if self.speak.wait_check_detail_list_page():
                sentence = self.speak.sentence()  # 游戏题目
                voice = self.speak.speak_button()  # 发音按钮

                if len(voice) > 4 and not content:
                    content = [sentence[len(voice)-2].text]
                    self.detail_operation(len(voice) - 1)  # 详情页 具体操作

                    if self.speak.wait_check_detail_list_page():
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
                        self.per_answer_detail(content)
                else:
                    var = 0
                    if content:  # 翻页成功 或者是第一页
                        for k in range(len(voice)):
                            if content[0] == sentence[k].text:
                                var = k + 1
                                break

                    self.detail_operation(len(voice), var)  # 详情页 具体操作

    @teststeps
    def detail_operation(self, length, var=0):
        """详情页 具体操作"""
        # self.speak.hint()  # 提示信息
        for j in range(var, length):
            if self.speak.wait_check_detail_page():  # 页面检查点
                if self.speak.wait_check_detail_list_page():
                    self.speak.speak_button()[j].click()  # 发音按钮

                    sentence = self.speak.sentence()  # 游戏题目
                    print(j, '.', sentence[j].text)

        index = random.randint(var, length - 1)
        self.speak.star_num()[index].click()  # 过关 按钮
        if self.speak.wait_check_modify_achieve_page():
            # todo 修改成绩
            self.speak.commit_button()
