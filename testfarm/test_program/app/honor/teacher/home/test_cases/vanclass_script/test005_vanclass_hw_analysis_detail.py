#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re

from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page import PictureDictation
from app.honor.teacher.home.object_page.vanclass_game_detail_page import VanclassGameDetailPage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.test_data.hw_detail_data import game_type_operation
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class VanclassHw(unittest.TestCase):
    """本班习题 - 答题分析tab 详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.v_detail = VanclassDetailPage()
        cls.hw = VanclassGameDetailPage()
        cls.van = VanclassPage()
        cls.detail = HwDetailPage()
        cls.game = GamesPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_hw_answer_analysis(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_ANALY)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    if self.v_detail.wait_check_page(gv.HW_ANALY):  # 页面检查点
                        print('本班作业:')
                        if self.v_detail.wait_check_list_page():
                            self.hw_list_operation()  # 具体操作
                        elif self.home.wait_check_empty_tips_page():
                            print('暂无数据')

                        if self.v_detail.wait_check_page(gv.HW_ANALY):  # 页面检查点
                            self.home.back_up_button()  # 返回 答题详情页面
                            if self.van.wait_check_page(gv.VAN_ANALY):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('未进入 习题作业页面业')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def hw_list_operation(self):
        """作业列表"""
        name = self.v_detail.hw_name()  # 作业name
        for i in range(len(name)):
            if self.v_detail.wait_check_page(gv.HW_ANALY):  # 页面检查点
                text = name[i].text
                if text != 'result':
                    print('###########################################################')
                    print(text)
                    name[i].click()  # 进入作业

                    if self.detail.wait_check_page():  # 页面检查点
                        complete = self.detail.analysis_tab()  # 答题分析 tab
                        complete.click()  # 进入 答题分析 tab页
                        if self.detail.wait_check_hw_list_page():
                            self.answer_detail_operation()  # 具体操作
                        elif self.home.wait_check_empty_tips_page():
                            print('暂无数据')

                        if self.detail.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回
                    else:
                        print('未进入作业 %s 页面' % text)

    @teststeps
    def answer_detail_operation(self, content=None):
        """答题情况 详情页"""
        if content is None:
            content = []

        mode = self.detail.game_type()  # 游戏类型
        if len(mode) > 4 and not content:
            content = [mode[-2].text]
            self.into_operation(0, len(mode)-1, mode)  # 进入游戏详情页 操作

            SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
            self.answer_detail_operation(content)
        else:  # <7 & 翻页
            var = 0
            if content:
                for k in range(len(mode)):
                    if content[0] == mode[k].text:
                        var = k + 1
                        break

            self.into_operation(var, len(mode), mode)  # 进入游戏详情页 操作

    @teststeps
    def into_operation(self, var, length, mode):
        """进入游戏详情页 操作
        :param mode:游戏类型
        """
        for j in range(var, length):
            if mode[j].text in ('单项选择', '强化炼句', "听音连句", "句型转换", "阅读理解", "听后选择", "完形填空", "补全文章", "选词填空", "听音选图"):
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(mode[j].text)
                value = game_type_operation(mode[j].text)
                mode[j].click()  # 点击game

                if self.game.wait_check_page():
                    if self.game.wait_check_list_page():
                        self.game_detail_operation(value)
            else:
                print(mode[j].text)
                mode[j].click()
                if Toast().find_toast('无需答题报告，答对即可'):
                    print('无需答题报告，答对即可', '\n',
                          '---------------------------------------------')

    @teststeps
    def game_detail_operation(self, index):
        """游戏详情页"""
        print('=======================游戏详情页=======================')
        self.game.game_title()  # title
        print(self.game.game_info())  # info
        self.game.teacher_nickname()  # 老师昵称
        print('---------------------------------------------')

        num = self.game.game_num()  # 题数
        if index == 15:  # 听音选图
            PictureDictation().error_sum(num)  # 选图题滑屏及具体操作
        elif index in (8, 9):  #
            if index == 9 and self.game.verify_hint_word():  # 选词填空 有提示词
                self.game.hint_word()  # 提示词：
                self.game.prompt_word()  # 提示的内容

            self.hw.article_content()  # 文章
            if index == 8:  # 补全文章
                while True:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.6)  # 滑屏
                    if self.game.verify_options():
                        self.complete_article_operation(num)  # 具体操作
                        break
        elif index in (1, 2, 6, 7):  # 有选项
            if index == 1 and self.game.verify_voice_button():  # 听后选择
                self.game.play_button()  # 播音按钮
            elif index in (6, 7) and self.hw.verify_content_text():  # 阅读理解/完形填空
                self.hw.article_content()  # 文章

                while True:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.5)  # 滑屏
                    if self.game.verify_options():
                        break
            self.hw.swipe_operation(num)  # 单选题滑屏及具体操作
        elif index in (3, 4, 5):  # 答案+解释
            self.answer_explain_type(num)

        if self.game.wait_check_page():
            self.home.back_up_button()
            if not self.detail.wait_check_page():  # 页面检查点
                print('未返回 答题详情页面')
        print('=========================================================')

    @teststeps
    def complete_article_operation(self, num, content=None):
        """补全文章"""
        if content is None:
            content = []

        option = self.game.option_char()
        item = self.game.option_item()

        if len(option) < num and not content:
            content = [option[-1].text]
            for z in range(len(item)):
                print(option[z].text, ': ', item[z].text)

            SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
            self.complete_article_operation(num, content)
        else:
            if content:
                var = 0
                for k in range(len(option)):
                    if content[0] == option[k].text:
                        var += k + 1
                        break

                for z in range(var, len(item)):
                    print(option[z].text, ': ', item[z].text)
                print('----------------------------')

    @teststeps
    def answer_explain_type(self, index, content=None):
        """答案/解释类型"""
        if content is None:
            content = []

        sentence = self.game.sentence()  # 句子
        hint = self.game.hint()  # 解释

        if len(sentence) > 3 and not content:
            content = [sentence[-2].text]  # 最后一个game的name

            for j in range(len(sentence) - 1):
                print(sentence[j].text, "\n", hint[j].text)
                if index in (4, 5):
                    self.drop_down_operation(sentence[j])  # 下拉按钮
                print('----------------------------')

            if self.game.wait_check_page():
                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.answer_explain_type(index, content)
        else:
            if content:
                var = 0
                for k in range(len(sentence)):
                    if content[0] == sentence[k].text:
                        var += k + 1
                        break

                for j in range(var, len(sentence)):
                    print(sentence[j].text, "\n", hint[j].text)
                    if index in (4, 5):
                        self.drop_down_operation(sentence[j])  # 下拉按钮
                    print('----------------------------')

    @teststeps
    def drop_down_operation(self, var):
        """下拉按钮"""
        rate = re.sub("\D", "", var.text.split()[-1])  # 准确率

        if rate == '' and '未作答' in var.text.split()[-1]:
            print('该题还没有学生完成')
        else:
            if int(rate) < 100:
                self.hw.drop_down_button(var)
                if self.hw.verify_drop_down_content():
                    self.hw.drop_down_content()  # 下拉菜单内容
                    self.hw.click_block()  # 点击空白处
            elif int(rate) == 100:
                print('该题正确率100%')
            else:
                print('★★★ Error -该题正确率', rate)
