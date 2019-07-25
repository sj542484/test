#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.single_choice_page import SingleChoice
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class HwAnalysis(unittest.TestCase):
    """本班作业 - 全部tab 作业详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.homework = Homework()
        cls.game = SingleChoice()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_homework_analysis_all(self):
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
                            all_hw = self.detail.all_tab()  # 全部 tab
                            if self.detail.selected(all_hw) is False:
                                print('★★★ Error- 未默认在 全部页面')
                            else:
                                print('--------------全部tab-------------------')
                                if self.van.empty_tips():
                                    print('暂无数据')
                                else:
                                    self.hw_operate()  # 具体操作

                            self.home.click_back_up_button()  # 返回 作业详情页面
                            if self.detail.wait_check_page(gv.HW_ANALY_GAME):  # 页面检查点
                                self.home.click_back_up_button()  # 返回 本班作业
                            else:
                                print('未返回 本班作业页面')

                        if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                            self.home.click_back_up_button()  # 返回 班级详情页面
                            if self.van.wait_check_vanclass_page(gv.CLASS_NAME):  # 班级详情 页面检查点
                                self.van.click_back_up_button()
                                if self.van.wait_check_page():  # 班级 页面检查点
                                    self.home.click_tab_hw()  # 返回主界面
                    else:
                        print('未进入班级 -本班作业tab')
                        self.van.click_back_up_button()
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
            if name[i].text == gv.HW_ANALY_GAME:
                name[i].click()  # 进入作业
                break

        if self.detail.wait_check_page(gv.HW_ANALY_GAME):  # 页面检查点
            # todo 获取toast 无需答题报告  or
            self.answer_detail([])
        else:
            print('未进入作业 %s 页面' % gv.HW_ANALY_GAME)
            self.home.click_back_up_button()

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
                if mode[j].text == '单项选择':
                    index.append(j)

                if j == len(status)-1:
                    content.append(name[j].text)
                    content.append(mode[j].text)

            if len(index) != 0:  # 有题
                name[index[0]].click()  # 点击game单项选择
                if self.game.wait_check_page():
                    print('---------------------------------------')
                    self.game.single_choice_operate()

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
                    if mode[j].text == '单项选择':
                        index.append(j)

                if len(index) != 0:  # 还有其他题
                    for i in range(len(index)):
                        text = name[index[i]].text

                        name[index[i]].click()  # 点击 单项选择
                        if self.detail.wait_check_page(text):
                            print('---------------------------------------')
                            self.game.single_choice_operate()
