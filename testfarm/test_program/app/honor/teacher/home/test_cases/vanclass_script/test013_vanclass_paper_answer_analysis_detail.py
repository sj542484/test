#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest
import re
import time

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.vanclass_game_detail_page import VanclassGameDetailPage
from app.honor.teacher.home.test_data.hw_detail_data import game_type_operation
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.object_page.paper_detail_page import PaperPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class VanclassPaper(unittest.TestCase):
    """本班试卷 - 答题分析tab 详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.v_hw = VanclassGameDetailPage()
        cls.van = VanclassPage()
        cls.hw = HwDetailPage()
        cls.paper = PaperPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_paper_answer_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():

                    self.van.vanclass_paper()  # 进入 本班卷子
                    title = gv.PAPER_TITLE.format(gv.VANCLASS)
                    if self.detail.wait_check_page(title):  # 页面检查点
                        if self.detail.wait_check_empty_tips_page():  # 无卷子时
                            self.detail.no_data()  # 暂无数据
                            # self.detail.goto_paper_pool()  # 点击 去题库 按钮
                        else:  # 有卷子
                            print('本班试卷:')
                            self.analysis_operation()  # 答卷分析tab

                        self.home.back_up_button()
                        if self.van.wait_check_page(title):  # 本班卷子 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.VANCLASS):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('★★★ Error- 未进入 本班试卷页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def analysis_operation(self):
        """答卷分析tab 具体操作"""
        name = self.detail.hw_name()  # 试卷name
        progress = self.detail.progress()  # 进度
        count = 0
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
                complete = self.paper.analysis_tab()  # 答卷分析 tab
                complete.click()  # 进入 答卷分析 tab页
                if self.get.selected(complete) is False:
                    print('★★★ Error- 进入 答卷分析 tab页')
                else:
                    print('--------------------------答卷分析tab--------------------------')
                    if self.paper.wait_check_paper_list_page():
                        print('###########################################################')
                        print('试卷:', gv.PAPER)
                        self.answer_detail_operation()

    @teststeps
    def answer_detail_operation(self, content=None):
        """答题情况 详情页"""
        if self.paper.wait_check_paper_list_page():
            if content is None:
                content = []
            name = self.paper.game_name()  # 作业name
            mode = self.paper.game_type()  # 作业type
            average = self.paper.van_average_achievement()  # 全班平均得分x分; 总分x分

            if len(average) > 3 and not content:
                content = [name[len(average) - 2].text]
                self.into_operation(0, len(average)-1, mode)  # 进入游戏详情页 操作

                SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                self.answer_detail_operation(content)
            else:  # <4 & 翻页
                var = 0
                if content:
                    for k in range(len(name)):
                        if content[0] == name[k].text:
                            var = k + 1
                            break

                self.into_operation(var, len(mode), mode)  # 进入游戏详情页 操作

    @teststeps
    def into_operation(self, var, length, mode):
        """进入游戏详情页 操作"""
        for j in range(var, length):
            if mode[j].text in ('单项选择', '强化炼句', "听音连句", "句型转换", "阅读理解", "听后选择", "完形填空", "补全文章", "选词填空", "听音选图"):
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(mode[j].text)
                value = game_type_operation(mode[j].text)
                mode[j].click()  # 点击game
                if self.v_hw.wait_check_page():
                    if self.v_hw.wait_check_list_page():
                        self.game_detail_operation(value)
            else:
                print(mode[j].text)
                mode[j].click()
                Toast().toast_operation('无需答题报告，答对即可')
                print('---------------------------------------------')

    @teststeps
    def game_detail_operation(self, index):
        """游戏详情页"""
        print('=======================游戏详情页=======================')
        self.v_hw.game_title()  # title
        print(self.v_hw.game_info())  # info
        self.v_hw.teacher_nickname()  # 老师昵称
        print('---------------------------------------------')
        # if index == 15:  # 听音选图
        #     self.home.back_up_button()

        if index in (8, 9):  #
            if index == 9 and self.v_hw.verify_hint_word():  # 选词填空 有提示词
                self.v_hw.hint_word()  # 提示词：
                self.v_hw.prompt_word()  # 提示的内容

            self.v_hw.article_content()  # 文章
            if index == 8:  # 补全文章
                SwipeFun().swipe_vertical(0.5, 0.7, 0.3)  # 滑屏
                option = self.v_hw.option_char()
                item = self.v_hw.option_item()
                for z in range(len(item)):
                    print(option[z].text, ': ', item[z].text)
                    print('----------------------------')
        elif index in (1, 2, 6, 7):  # 有选项
            if index == 1 and self.v_hw.verify_voice_button():  # 听后选择
                self.v_hw.play_button()  # 播音按钮
            elif index in (6, 7) and self.v_hw.verify_content_text():  # 阅读理解/完形填空
                self.v_hw.article_content()  # 文章
                SwipeFun().swipe_vertical(0.5, 0.9, 0.4)  # 滑屏

            num = self.v_hw.game_num()  # 题数
            self.v_hw.swipe_operation(int(num))  # 单选题滑屏及具体操作
        elif index in (3, 4, 5):  # 答案+解释
            self.answer_explain_type(index)

        if self.v_hw.wait_check_list_page():
            self.home.back_up_button()
            if not self.paper.wait_check_page():  # 页面检查点
                print('未返回 答题详情页面')
        print('=========================================================')

    @teststeps
    def answer_explain_type(self, index, content=None):
        """答案/解释类型"""
        if content is None:
            content = []

        sentence = self.v_hw.sentence()  # 句子
        hint = self.v_hw.hint()  # 解释

        if len(sentence) > 3 and not content:
            content = []
            for j in range(len(sentence) - 1):
                print(sentence[j].text, " ", hint[j].text)
                if index in (4, 5):
                    self.drop_down_operation(sentence[j])  # 下拉按钮
                print('----------------------------')

            content.append(sentence[-2].text)  # 最后一个game的name
            SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
            self.answer_explain_type(index, content)
        else:
            var = 0
            if content:
                for k in range(len(sentence)):
                    if content[0] == sentence[k].text:
                        var += k + 1
                        break

            for j in range(var, len(sentence)):
                print(sentence[j].text, " ", hint[j].text)
                if index in (4, 5):
                    self.drop_down_operation(sentence[j])  # 下拉按钮
                print('----------------------------')

    @teststeps
    def drop_down_operation(self, var):
        """下拉按钮"""
        sentence = var.text  # 题目
        rate = re.sub("\D", "", sentence.split(' ')[-1])

        if int(rate) < 100:
            self.v_hw.drop_down_button(var)
            time.sleep(1)
            if int(rate) == 0 and self.v_hw.wait_check_page(3):
                print('该题还没有学生完成')
            else:
                self.v_hw.drop_down_content()  # 下拉菜单内容
                self.v_hw.click_block()  # 点击空白处
        elif int(rate) == 100:
            print('该题正确率100%')
        else:
            print('★★★ Error -该题正确率', rate)
