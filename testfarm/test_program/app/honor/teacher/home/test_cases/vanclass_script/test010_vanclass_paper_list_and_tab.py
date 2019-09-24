#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.paper_detail_page import PaperPage
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


class Paper(unittest.TestCase):
    """卷子列表 & 答卷分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.v_detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.paper = PaperPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_list_tab(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():

                    self.van.vanclass_paper()  # 进入 本班卷子
                    title = gv.PAPER_TITLE.format(gv.VANCLASS)
                    if self.v_detail.wait_check_page(title):  # 页面检查点
                        if self.v_detail.wait_check_empty_tips_page():  # 无卷子时
                            self.v_detail.no_data()  # 暂无数据
                            # self.detail.goto_paper_pool()  # 点击 去题库 按钮
                        else:  # 有卷子
                            print('本班试卷:')
                            count = 0
                            pro = 0
                            name = self.v_detail.hw_name()  # 试卷name
                            progress = self.v_detail.progress()  # 进度
                            for i in range(len(name)):
                                pro = progress[i].text  # int(re.sub("\D", "", progress[i].text))
                                if int(pro[3]) != 0 and name[i].text == gv.PAPER:
                                    name[i].click()  # 进入试卷
                                    count += 1
                                    break

                            if count == 0:
                                print('暂无该试卷: {}或者暂无学生完成该试卷'.format(gv.PAPER))
                            else:
                                if self.paper.wait_check_page():  # 页面检查点
                                    print('###########################################################')
                                    print('试卷:', gv.PAPER, '\n', pro)
                                    self.finish_situation_operation()  # 完成情况 tab
                                    self.answer_analysis_operation()  # 答卷分析 tab
                                    if self.paper.wait_check_page():  # 页面检查点
                                        self.home.back_up_button()  # 返回 本班卷子
                        if self.van.wait_check_page(title):  # 本班卷子 页面检查点
                            self.home.back_up_button()  # 返回 班级详情页面
                            if self.van.wait_check_page(gv.VANCLASS):  # 班级详情 页面检查点
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
        complete = self.paper.finished_tab()  # 完成情况 tab
        if self.get.selected(complete) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('-------------------完成情况tab-------------------')
            if self.paper.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况 学生列表
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def answer_analysis_operation(self):
        """答卷分析tab 具体操作"""
        if self.paper.wait_check_page():  # 页面检查点
            analysis = self.paper.analysis_tab()  # 答卷分析 tab
            if self.get.selected(analysis) is True:
                print('★★★ Error- 默认在 答卷分析 tab页')
            else:
                analysis.click()  # 进入 答卷分析 tab页
                if self.get.selected(analysis) is False:
                    print('★★★ Error- 进入 答卷分析 tab页')
                else:
                    print('-------------------答卷分析tab-------------------')
                    if self.paper.wait_check_paper_list_page():
                        self.answer_analysis_detail()  # 答卷分析页 list
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答卷分析 详情页"""
        if content is None:
            content = []

        mode = self.paper.game_type()  # 游戏类型
        name = self.paper.game_name()  # 游戏name
        average = self.paper.van_average_achievement()  # 全班平均得分x分; 总分x分

        if len(mode) > 4 and not content:
            content = []
            for j in range(len(average) - 1):
                print(mode[j].text, name[j].text, '\n',
                      average[j].text)
                print('----------------------')

            content.append(name[len(average) - 2].text)  # 最后一个game的name
            # content.append(mode[len(average) -2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.80, 0.1)
            self.answer_analysis_detail(content)
        else:
            mode = self.paper.game_type()  # 游戏类型
            name = self.paper.game_name()  # 游戏name
            average = self.paper.van_average_achievement()  # 全班平均得分x分; 总分x分

            var = 0
            if content:
                if content[0] != name[-1].text:
                    for k in range(len(name)):
                        if content[0] == name[k].text:
                            var += k
                            break

            for j in range(var, len(mode)):
                print(mode[j].text, name[j].text, '\n',
                      ' ', average[j].text)
                print('----------------------')

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        name = self.paper.st_name()  # 学生name
        icon = self.paper.st_icon()  # 学生头像
        status = self.paper.st_score()  # 学生完成与否 todo

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息
        else:
            print('★★★ Error-已完成/未完成 学生列表信息统计', len(icon), len(name))
