#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.vocabulary_choice_page import VocabularyChoice
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class HwAnalysis(unittest.TestCase):
    """本班作业 - 已完成tab 作业详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.homework = Homework()
        cls.game = VocabularyChoice()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_homework_analysis_finished(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_test_vanclass()  # 班级tab
            if self.van.wait_check_page():  # 页面检查点

                van = self.van.vanclass_name()  # 班级名称
                for i in range(len(van)):
                    if van[i].text == gv.CLASS_NAME:
                        van[i].click()  # 进入班级详情页
                        break
                if self.van.wait_check_vanclass_page(gv.CLASS_NAME):  # 页面检查点

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                        print('%s 本班作业:' % gv.CLASS_NAME)
                        if self.van.empty_tips():
                            print('暂无数据')
                        else:
                            incomplete = self.detail.finished_tab()  # 未完成 tab
                            incomplete.click()  # 进入 未完成 tab页
                            if self.detail.selected(incomplete) is False:
                                print('★★★ Error- 未进入 已完成 tab页')
                            else:
                                print('--------------已完成tab-------------------')
                                if self.van.empty_tips():
                                    print('暂无数据')
                                else:
                                    self.hw_operate()  # 具体操作

                                    self.home.click_back_up_button()  # 返回 作业详情页面
                                    if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                                        self.home.click_back_up_button()  # 返回 本班作业页面

                            if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                                self.home.click_tab_hw()  # 返回主界面
                    else:
                        print('未进入班级 -本班作业tab')
                        self.home.click_back_up_button()
                        if self.van.wait_check_page():  # 班级 页面检查点
                            self.home.click_tab_hw()  # 返回主界面
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def hw_operate(self):
        """作业列表"""
        name = self.detail.hw_name()  # 作业name
        for i in range(len(name)):
            if name[i].text == gv.FINISHED:
                name[i].click()  # 进入作业
                break

        if self.detail.wait_check_page(gv.FINISHED):  # 页面检查点
            # todo 获取toast 无需答题报告  or
            self.answer_detail([])
        else:
            print('未进入作业 %s 页面' % gv.FINISHED)

    @teststeps
    def answer_detail(self, content):
        """答题情况详情页"""
        mode = self.homework.games_type()  # 游戏类型
        name = self.homework.games_title()  # 游戏name
        status = self.homework.status()  # 题目状态
        count = self.homework.count()  # 共X题

        if len(mode) > 6 or len(content) == 0:
            index = []
            content = []
            for j in range(len(status)):  # 最多展示7道题, achievement的个数代表页面内能展示完全的题数
                print(mode[j].text,  name[j].text, status[j].text, count[j].text)
                if mode[j].text == '词汇选择':
                    index.append(j)

                if j == len(status)-1:
                    content.append(name[j].text)
                    content.append(mode[j].text)

            if len(index) != 0:  # 有题
                print('有题：', index)
                for i in range(len(index)):
                    if self.homework.wait_check_game_list_page(gv.FINISHED):
                        print('---------------------------------------')
                        homework_type = self.homework.tv_testbank_name(i)  # 获取小游戏模式
                        self.homework.games_type()[i].click()  # 进入小游戏
                        self.game.diff_type(homework_type)  # 不同模式小游戏的 游戏过程
                        self.game.back_up()  # 返回小游戏列表

            if self.homework.wait_check_game_list_page(gv.FINISHED):
                self.home.screen_swipe_up(0.5, 0.85, 0.1, 1000)
                self.answer_detail(content)

            return content
        else:  # <7 & 翻页
            if len(name) != len(count) != len(name) != len(status):
                print('★★★ Error- 数目不等', len(name), len(count), len(name), len(status))
            else:
                var = 0
                for k in range(len(status)):
                    if content[0] == name[k].text:
                        var = k+1
                        break
                index = []

                for j in range(var, len(status)):
                    print(mode[j].text, name[j].text, status[j].text)
                    if mode[j].text == '词汇选择':
                        index.append(j)

                if len(index) != 0:  # 还有其他题
                    print('有题：', index)
                    for i in range(len(index)):
                        if self.homework.wait_check_game_list_page(gv.FINISHED):
                            print('---------------------------------------')
                            homework_type = self.homework.tv_testbank_name(i)  # 获取小游戏模式
                            self.homework.games_type()[i].click()  # 进入小游戏
                            self.game.diff_type(homework_type)  # 不同模式小游戏的 游戏过程
                            self.game.back_up()  # 返回小游戏列表
