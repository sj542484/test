#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class Spoken(unittest.TestCase):
    """本班口语 - 答题分析tab 二级详情"""

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
    def test_vanclass_spoken_tab(self):
        """按学生查看& 按题查看tab"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_SPOKE)  # 进入 班级
            if self.van.wait_check_page(gv.VAN_SPOKE):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_spoken()  # 进入 本班口语
                    if self.van.wait_check_page(gv.SPOKEN_ANALY):  # 页面检查点
                        if self.home.wait_check_empty_tips_page():  # 无口语作业时
                            print('暂无口语作业')
                        else:  # 有作业
                            self.detail.into_operation(gv.SPOKEN, gv.SPOKEN_ANALY)  # 进入某个作业 游戏列表

                            if self.speak.wait_check_page():  # 页面检查点
                                print("题单:", gv.SPOKEN)
                                if self.speak.wait_check_st_list_page():
                                    self.answer_analysis_operation()  # 答题分析 tab

                                if self.speak.wait_check_page():  # 页面检查点
                                    self.home.back_up_button()  # 返回 作业列表

                        if self.van.wait_check_page(gv.SPOKEN_ANALY):  # 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.VAN_SPOKE):  # 页面检查点
                                self.home.back_up_button()
                    else:
                        print('未进入本班口语')
            else:
                print('未进入班级页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        if self.homework.wait_check_page():  # 页面检查点
            analysis = self.homework.analysis_tab()  # 答题分析 tab
            if self.get.selected(analysis) is True:
                print('★★★ Error- 默认在 答题分析 tab页')
            else:
                analysis.click()  # 进入 答题分析 tab页
                if self.get.selected(analysis) is False:
                    print('★★★ Error- 进入 答题分析 tab页')
                else:
                    print('=======================答题分析tab=======================')
                    if self.speak.wait_check_spoken_list_page():

                        name = self.homework.game_name()  # 游戏name
                        print(name[0].text)
                        name[0].click()  # 进入按学生看/按题查看 tab页

                        if self.speak.wait_check_st_page():
                            self.check_st_operation()  # 按学生查看 tab
                            self.check_question_operation()  # 按题查看 tab
                        else:
                            print('!!!未进入进入按学生看/按题查看 tab页')
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def check_st_operation(self):
        """按学生看tab 具体操作"""
        complete = self.speak.check_st_tab()  # 按学生看 tab
        if self.get.selected(complete) is True:
            print('★★★ Error- 未默认在 按学生看 tab页')
        else:
            print('-------------------按学生看tab--------------------')
            if self.speak.wait_check_st_page():
                self.st_list_detail()  # 学生列表信息统计
                print('=========================================')

                status = self.speak.star_num()  # 学生完成情况 星星数
                for i in range(len(status)):
                    if self.speak.wait_check_detail_list_page():  # 页面检查点
                        name = self.speak.st_name()  # 学生name
                        print('学生%s答题情况:' % name[i].text)
                        self.speak.click_st_star()[i].click()  # 进入一个学生的 答题情况页

                        self.per_st_detail()  # 答题情况页

                        if self.speak.wait_check_detail_list_page():  # 页面检查点
                            self.home.back_up_button()  # 返回 按学生看tab
                        print('----------------------------------------')

                        break
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def check_question_operation(self):
        """按题查看tab 具体操作"""
        if self.speak.wait_check_st_page():  # 页面检查点
            analysis = self.speak.check_question_tab()  # 按题查看 tab
            if self.get.selected(analysis) is False:
                print('★★★ Error- 默认在 按题查看 tab页')
            else:
                analysis.click()  # 进入 按题查看 tab页
                if self.get.selected(analysis) is False:
                    print('★★★ Error- 未进入 按题查看 tab页')
                else:
                    print('-------------------按题查看tab--------------------')
                    if self.speak.wait_check_question_page():
                        self.answer_list_detail()  # 按题查看 tab页
                        print('---------------------------------------')

                        finish = self.speak.finish_ratio()  # 游戏完成率
                        for i in range(len(finish) - 1):
                            if self.speak.wait_check_question_page():
                                sentence = self.speak.sentence()  # 游戏题目
                                sentence[i].click()  # 进入小题详情页
                                self.per_question_detail(i)  # 各小题 答题情况

                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

                    if self.speak.wait_check_question_page():  # 页面检查点
                        self.home.back_up_button()  # 返回 答题分析 tab 页

    @teststeps
    def st_list_detail(self, content=None):
        """按学生查看 详情页
        :param content:（最后一个容易展示不全，故不做操作），翻页后的操作判断
        """
        if content is None:
            content = []

        name = self.speak.st_name()  # 学生name
        icon = self.speak.st_icon()  # 学生头像
        status = self.speak.st_unfinished_or_star()  # 学生已完成/星星数

        if len(icon) > 4 and len(content) == 0:
            content = []
            for i in range(len(icon) - 1):
                print('学生:', name[i].text, ' ', status[i])  # 打印所有学生信息

            content.append(name[len(icon)-2].text)  # 最后一个学生name
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.st_list_detail(content)
        else:
            if len(name) != len(icon) != len(status):
                print('★★★ Error- 学生信息元素数目不一致', len(name), len(icon), len(status))

            var = 0
            if content:
                for k in range(len(icon)):
                    if content[0] == name[k].text:
                        var += k
                        break

            for i in range(var, len(icon)):
                print('学生:', name[i].text, ' ', status[i])  # 打印所有学生信息

    @teststeps
    def answer_list_detail(self, content=None):
        """按题查看 详情页
        :param content: 游戏题目 （最后一题容易展示不全，故不做操作），翻页后的操作判断
        """
        if content is None:
            content = []

        sentence = self.speak.sentence()  # 游戏题目
        finish = self.speak.finish_ratio()  # 游戏完成率

        if len(finish) > 4 and not content:
            content = []
            for j in range(len(finish) - 1):
                print(sentence[j].text, finish[j].text)

            content.append(sentence[len(finish)-2].text)  # 最后一个game的name
            content.append(finish[-2].text)  # 最后一个game的完成率
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_list_detail(content)
        else:
            var = 0
            if content:  # 翻页成功 或者是第一页
                for k in range(len(finish)):
                    if content[0] == sentence[k].text and content[1] == finish[k].text:
                        var += k+1
                        break

            for j in range(var, len(finish)):
                print(sentence[j].text, finish[j].text)

    @teststeps
    def per_st_detail(self, content=None):
        """game 答题情况详情页
        :param content:  游戏题目 （最后一题容易展示不全，故不做操作），翻页后的操作判断
        """
        if content is None:
            content = []

        if self.speak.wait_check_detail_page():  # 页面检查点
            if self.speak.wait_check_detail_list_page():
                # self.speak.hint()  # 提示信息
                sentence = self.speak.sentence()  # 游戏题目
                voice = self.speak.speak_button()  # 发音按钮

                if len(voice) > 4 and not content:
                    content = [sentence[len(voice) - 2].text]
                    self.detail_operation(len(voice) - 1)  # 详情页 具体操作

                    if self.speak.wait_check_detail_list_page():
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
                        self.per_st_detail(content)
                else:
                    var = 0
                    if content:  # 翻页成功
                        for k in range(len(voice)):
                            if content[0] == sentence[k].text:
                                var = k + 1
                                break

                    self.detail_operation(len(voice), var)  # 详情页 具体操作

    @teststeps
    def detail_operation(self, length, var=0):
        """详情页 具体操作
        :param length:
        :param var:
        """
        if self.speak.wait_check_detail_page():
            for j in range(var, length):  # 依次操作每一道题目
                if self.speak.wait_check_detail_list_page():  # 页面检查点
                    speak = self.speak.speak_button()  # 发音按钮
                    speak[j].click()

                    sentence = self.speak.sentence()  # 游戏题目
                    print(j+1, '.', sentence[j].text)

                    button = self.speak.star_num()  # 过关 按钮
                    button[j + 1].click()
                    if self.speak.wait_check_modify_achieve_page():
                        # todo 修改成绩
                        self.speak.commit_button()

    @teststeps
    def per_question_detail(self, var):
        """各小题 答题情况详情页
        :param var: 第X小题
        """
        if self.speak.wait_check_detail_page():
            if self.speak.wait_check_detail_list_page():
                if var == 0:
                    explain = self.speak.explain()  # 说明
                    report = self.speak.total_report()  # 总报告
                    print(explain, '\n', report)
                print('-----------------------')
                print(var+1, '.', self.speak.sentence()[0].text)
                voice = self.speak.speak_button()  # 发音按钮
                st = self.speak.st_name()  # 学生name

                if len(voice) == len(st):
                    for j in range(len(st)):
                        if self.speak.wait_check_detail_list_page():
                            print('  ', st[j].text)

                            if self.get.enabled(voice[j]) == 'true':
                                voice[j].click()  # 点击
                                button = self.speak.star_num()  # 过关 按钮
                                button[j].click()
                                if self.speak.wait_check_modify_achieve_page():
                                    # todo 修改成绩
                                    self.speak.commit_button()  # 确定 按钮
                else:
                    print('★★★ Error- 发音按钮个数和学生人数不同', len(voice), len(st))

                if self.speak.wait_check_detail_list_page():
                    self.home.back_up_button()  # 返回  按题查看tab
