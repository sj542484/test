#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest
import re
import time

from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.object_page.vanclass_game_detail_page import VanclassGameDetailPage
from app.honor.teacher.home.vanclass.test_data.hw_detail_data import game_type_operation
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassPaper(unittest.TestCase):
    """本班试卷 - 答题分析tab 详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_paper = VanclassPaperPage()
        cls.detail = VanclassGameDetailPage()
        cls.van = VanclassPage()
        cls.report = PaperReportPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassPaper, self).run(result)

    @testcase
    def test_vanclass_paper_answer_detail(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)

        self.van.vanclass_paper()  # 进入 本班卷子
        self.vue.app_web_switch()  # 切到apk 再切回web
        title = gv.PAPER_TITLE.format(gv.VANCLASS)

        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        if self.van_paper.wait_check_empty_tips_page():  # 无卷子时
            self.van_paper.no_data()  # 暂无数据
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)  # 页面检查点
        else:
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)  # 页面检查点
            print('本班试卷:')
            self.analysis_operation()  # 答卷分析tab

        self.van.back_up_button()
        self.vue.app_web_switch()  # 切到apk 再切回web
        
        self.assertTrue(self.van.wait_check_page(title), self.van.van_vue_tips)  # 本班卷子 页面检查点
        self.van.back_up_button()
        self.vue.app_web_switch()  # 切到apk 再切回web
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
        self.van.back_up_button()  # 返回主界面

    @teststeps
    def analysis_operation(self):
        """答卷分析tab 具体操作"""
        name = self.van_paper.hw_name()  # 试卷name
        progress = self.van_paper.progress()  # 进度
        count = []
        for i in range(len(name)):
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)  # 有卷子
            name = self.van_paper.hw_name()  # 试卷name
            pro = progress[i].text  # int(re.sub("\D", "", progress[i].text))
            if int(pro[3]) != 0 and self.home.brackets_text_in(name[i].text) == '试卷':
                count.append(i)

        self.assertEqual(len(count), 0, '暂无可用试卷')
        index = random.randint(0, len(count) - 1)
        text = name[count[index]].text
        name[count[index]].click()  # 进入试卷
        self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        self.report.analysis_tab().click()  # 进入 答卷分析 tab页

        print('--------------------------答卷分析tab--------------------------')
        print('###########################################################')
        print('试卷:', text)
        self.answer_detail_operation()

    @teststeps
    def answer_detail_operation(self, content=None):
        """答题情况 详情页"""
        self.assertTrue(self.report.wait_check_paper_list_page(), self.report.hw_list_tips)
        if content is None:
            content = []
            
        name = self.report.game_name()  # 作业name
        mode = self.report.game_type()  # 作业type
        average = self.report.van_average_achievement()  # 全班平均得分x分; 总分x分

        if len(average) > 3 and not content:
            content = [name[len(average) - 2].text]
            self.into_operation(0, len(average)-1, mode)  # 进入游戏详情页 操作

            self.van_paper.swipe_vertical_web(0.5, 0.9, 0.2)
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
                self.vue.app_web_switch()  # 切到apk 再切回web
                
                self.assertTrue(self.detail.wait_check_page(), self.detail.game_tips)
                self.assertTrue(self.detail.wait_check_list_page(), self.detail.game_list_tips)
                self.game_detail_operation(value)
            else:
                print(mode[j].text)
                mode[j].click()
                MyToast().toast_assert(self.name, Toast().toast_vue_operation(TipsData().no_report))  # 获取toast
                print('---------------------------------------------')

    @teststeps
    def game_detail_operation(self, index):
        """游戏详情页"""
        print('=======================游戏详情页=======================')
        self.detail.game_title()  # title
        print(self.detail.game_info())  # info
        self.detail.teacher_nickname()  # 老师昵称
        print('---------------------------------------------')
        # if index == 15:  # 听音选图
        #     self.home.back_up_button()

        if index in (8, 9):  #
            if index == 9 and self.detail.verify_hint_word():  # 选词填空 有提示词
                self.detail.hint_word()  # 提示词：
                self.detail.prompt_word()  # 提示的内容

            self.detail.article_content()  # 文章
            if index == 8:  # 补全文章
                self.van_paper.swipe_vertical_web(0.5, 0.7, 0.3)  # 滑屏
                option = self.detail.option_char()
                item = self.detail.option_item()
                for z in range(len(item)):
                    print(option[z].text, ': ', item[z].text)
                    print('----------------------------')
        elif index in (1, 2, 6, 7):  # 有选项
            if index == 1 and self.detail.verify_voice_button():  # 听后选择
                self.detail.play_button()  # 播音按钮
            elif index in (6, 7) and self.detail.verify_content_text():  # 阅读理解/完形填空
                self.detail.article_content()  # 文章
                self.van_paper.swipe_vertical_web(0.5, 0.9, 0.4)  # 滑屏

            num = self.detail.game_num()  # 题数
            self.detail.swipe_operation(int(num))  # 单选题滑屏及具体操作
        elif index in (3, 4, 5):  # 答案+解释
            self.answer_explain_type(index)

        if self.detail.wait_check_list_page():
            self.van.back_up_button()
            self.vue.app_web_switch()  # 切到apk 再切回web
            if not self.report.wait_check_page():  # 页面检查点
                print('未返回 答题详情页面')
        print('=========================================================')

    @teststeps
    def answer_explain_type(self, index, content=None):
        """答案/解释类型"""
        if content is None:
            content = []

        sentence = self.detail.sentence()  # 句子
        hint = self.detail.hint()  # 解释

        if len(sentence) > 3 and not content:
            content = []
            for j in range(len(sentence) - 1):
                print(sentence[j].text, " ", hint[j].text)
                if index in (4, 5):
                    self.drop_down_operation(sentence[j])  # 下拉按钮
                print('----------------------------')

            content.append(sentence[-2].text)  # 最后一个game的name
            self.van_paper.swipe_vertical_web(0.5, 0.9, 0.2)
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
            self.detail.drop_down_button(var)
            time.sleep(1)
            if int(rate) == 0 and self.detail.wait_check_page(3):
                print('该题还没有学生完成')
            else:
                self.detail.drop_down_content()  # 下拉菜单内容
                self.detail.click_block()  # 点击空白处
        elif int(rate) == 100:
            print('该题正确率100%')
        else:
            print('★★★ Error -该题正确率', rate)
