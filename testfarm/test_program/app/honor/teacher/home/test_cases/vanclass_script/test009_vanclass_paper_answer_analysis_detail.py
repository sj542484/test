#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re
import time

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.hw_detail_data import game_type_operation
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.object_page.paper_detail_page import PaperPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.wait_element import WaitElement


class VanclassPaper(unittest.TestCase):
    """本班试卷 - 答题分析tab 详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.hw = HwDetailPage()
        cls.paper = PaperPage()
        cls.get = GetAttribute()
        cls.game = GamesPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_paper_answer_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_PAPER)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_PAPER):  # 页面检查点

                self.van.vanclass_paper()  # 进入 本班卷子
                if self.detail.wait_check_page(gv.PAPER_ANALY):  # 页面检查点
                    if WaitElement().judge_is_exists(self.detail.goto_pool_value):  # 无卷子时
                        print('暂无卷子，去题库看看吧')
                        # self.detail.goto_paper_pool()  # 点击 去题库 按钮
                    else:  # 有卷子
                        print('本班试卷:')
                        self.analysis_operation()  # 答卷分析tab

                    self.home.back_up_button()
                    if self.van.wait_check_page(gv.PAPER_ANALY):  # 本班卷子 页面检查点
                        self.home.back_up_button()
                        if self.van.wait_check_page(gv.VAN_PAPER):  # 班级详情 页面检查点
                            self.home.back_up_button()
                else:
                    print('未进入 本班试卷页面')
                    self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def analysis_operation(self):
        """答卷分析tab 具体操作"""
        name = self.detail.hw_name()  # 试卷name
        progress = self.detail.progress()  # 进度
        for i in range(1, len(name)):
            count = int(re.sub("\D", "", progress[i].text))
            if count != 00:
                var = name[i].text
                name[i].click()  # 进入试卷

                if self.paper.wait_check_page():  # 页面检查点
                    complete = self.paper.analysis_tab()  # 答卷分析 tab
                    complete.click()  # 进入 答卷分析 tab页
                    if self.get.selected(complete) is False:
                        print('★★★ Error- 进入 答卷分析 tab页')
                    else:
                        print('--------------------------答卷分析tab--------------------------')
                        if self.paper.wait_check_paper_list_page():
                            print('###########################################################')
                            print('试卷:', var)
                            self.answer_detail_operation(['', ''])
                break

    @teststeps
    def answer_detail_operation(self, content):
        """答题情况 详情页"""
        name = self.paper.game_name()  # 作业name
        mode = self.paper.game_type()  # 作业type
        average = self.paper.van_average_achievement()  # 全班平均得分x分; 总分x分
        if len(average) > 4 and len(content) == 0:
            content = [name[len(average) - 2].text, mode[len(average) - 2].text]
            for j in range(len(average)-1):  # average的个数代表页面内能展示完全的题数
                self.into_operation(0, len(average), mode)  # 进入游戏详情页 操作

            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_detail_operation(content)
        else:  # <7 & 翻页
            var = 0
            for k in range(len(name)):
                if content[0] == name[k].text and content[1] == mode[k].text:
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
        # if index == 15:  # 听音选图
        #     self.home.back_up_button()

        if index in (8, 9):  #
            if index == 9 and self.game.verify_hint_word():  # 选词填空 有提示词
                self.game.hint_word()  # 提示词：
                self.game.prompt_word()  # 提示的内容

            self.game.article_content()  # 文章
            if index == 8:  # 补全文章
                SwipeFun().swipe_vertical(0.5, 0.7, 0.3)  # 滑屏
                option = self.game.option_char()
                item = self.game.option_item()
                for z in range(len(item)):
                    print(option[z].text, ': ', item[z].text)
                    print('----------------------------')
        elif index in (1, 2, 6, 7):  # 有选项
            if index == 1 and self.game.verify_voice_button():  # 听后选择
                self.game.play_button()  # 播音按钮
            elif index in (6, 7) and self.game.verify_content_text():  # 阅读理解/完形填空
                self.game.article_content()  # 文章
                SwipeFun().swipe_vertical(0.5, 0.6, 0.3)  # 滑屏

            num = self.game.game_num()  # 题数
            self.hw.swipe_operation(int(num))  # 单选题滑屏及具体操作
        elif index in (3, 4, 5):  # 答案+解释
            self.answer_explain_type([''], index)

        if self.game.wait_check_list_page():
            self.home.back_up_button()
            if not self.paper.wait_check_page():  # 页面检查点
                print('未返回 答题详情页面')
        print('=========================================================')

    @teststeps
    def answer_explain_type(self, content, index):
        """答案/解释类型"""
        sentence = self.game.sentence()  # 句子
        hint = self.game.hint()  # 解释

        if len(sentence) > 3 and content[0] == '':
            content = []
            for j in range(len(sentence) - 1):
                print(sentence[j].text, " ", hint[j].text)
                if index in (4, 5):
                    self.drop_down_operation(sentence[j])  # 下拉按钮
                print('----------------------------')

            content.append(sentence[-2].text)  # 最后一个game的name
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_explain_type(content, index)

            return content
        else:
            if content[0] != sentence[-1].text:
                var = 0
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
            self.hw.drop_down_button(var)
            time.sleep(1)
            if int(rate) == 0 and self.game.wait_check_page(3):
                print('该题还没有学生完成')
            else:
                self.hw.drop_down_content()  # 下拉菜单内容
                self.hw.click_block()  # 点击空白处
        elif int(rate) == 100:
            print('该题正确率100%')
        else:
            print('★★★ Error -该题正确率', rate)
