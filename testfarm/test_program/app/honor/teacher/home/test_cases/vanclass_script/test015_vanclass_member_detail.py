#!/usr/bin/env python
# encoding:UTF-8
import unittest
import time
import re

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.result_detail_page import ResultDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_member_page import VanMemberPage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_student_info_page import StDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class VanclassMember(unittest.TestCase):
    """班级成员 - 学生详情页"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.v_detail = VanclassDetailPage()
        cls.detail = HwDetailPage()
        cls.van = VanclassPage()
        cls.st = StDetailPage()
        cls.member = VanMemberPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_member_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_ANALY)  # 进入 班级
            if self.van.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_member()  # 进入 班级成员
                    if self.member.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                        print('班级成员页面:')
                        if self.member.wait_check_st_list_page():
                            self.member_info_operation()  # 学生具体信息页面
                        elif self.home.wait_check_empty_tips_page():
                            print('暂时没有数据')

                        if self.member.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.VAN_ANALY):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('未进入 班级成员页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def member_info_operation(self):
        """班级成员- 学生具体信息页面"""
        remark = self.v_detail.st_remark()
        for i in range(len(remark)):
            if remark[i].text == gv.DETAIL:
                remark[i].click()  # 进入学生 具体信息页面

                if self.st.wait_check_page():
                    print('---------------------------------')
                    print('学生 %s 详情页面:' % gv.DETAIL)
                    name = self.st.st_name()  # 备注名
                    nick = self.st.st_nickname()  # 昵称
                    print(name)
                    print(nick)
                    if not self.st.judge_st_tags():  # 提分/试用/基础
                        print('★★★ Error-  无提分/试用/基础元素')

                    self.st.phone_title()  # 手机号
                    print('  ', self.st.st_phone().text)
                    self.st.data_title()  # 数据统计
                    self.st.card_title()  # 拼图卡片
                    self.st.hw_title()  # 习题作业
                    self.st.paper_title()  # 本班试卷
                    self.st.spoken_title()  # 本班口语
                    print('---------------------------------')

                    self.st.data_statistic()  # 数据统计
                    if self.st.wait_check_per_detail_page(name):
                        print('=======================数据统计 页面=======================')
                        print('已进入数据统计 页面')
                        time.sleep(2)
                        self.home.back_up_button()

                    if self.st.wait_check_page():
                        self.picture_page_operation(nick)  # 拼图卡片

                    if self.st.wait_check_page():
                        self.hw_page_operation(name)  # 习题作业

                    if self.st.wait_check_page():
                        self.home.back_up_button()
                break

    @teststeps
    def picture_page_operation(self, nick):
        """拼图卡片"""
        self.st.picture_count()  # 拼图
        if self.st.wait_check_per_detail_page(nick[3:]):
            print('=======================拼图卡片 页面=======================')
            if self.st.judge_picture():
                num = self.st.picture_num()
                print(num[0].text)

            self.st.picture_report()  # 拼图报告
            self.home.back_up_button()

    @teststeps
    def hw_page_operation(self, name):
        """作业列表"""
        self.st.hw_count()  # 作业list
        if self.st.wait_check_per_detail_page(name):
            if self.st.wait_check_hw_page():
                print('=======================习题作业 页面=======================')
                self.unfinished_operation(name)  # 未完成tab
                self.finished_operation(name)  # 已完成tab

                if self.st.wait_check_hw_page():
                    self.home.back_up_button()

    @teststeps
    def unfinished_operation(self, name):
        """未完成tab 具体操作"""
        analysis = self.st.unfinished_tab()  # 未完成 tab
        if self.get.selected(analysis) is False:
            print('★★★ Error- 未默认在 未完成 tab页')
        else:
            print('-------------------------未完成tab-------------------------')
            if self.st.wait_check_hw_list_page():
                self.answer_analysis_detail(['', ''], name)  # 未完成页

            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def finished_operation(self, name):
        """已完成tab 具体操作"""
        if self.st.wait_check_hw_page():
            complete = self.st.finished_tab()  # 已完成 tab
            if self.get.selected(complete) is True:
                print('★★★ Error- 默认在 已完成 tab页')
            else:
                complete.click()  # 进入 已完成 tab页
                if self.get.selected(complete) is False:
                    print('★★★ Error- 进入 已完成 tab页')
                else:
                    print('-------------------------已完成tab-------------------------')
                    if self.st.wait_check_hw_list_page():
                        self.answer_analysis_detail(['', ''], name)    # 已完成 列表
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, content, remark):
        """未完成/已完成tab 详情页"""
        name = self.st.hw_name()  # 作业包 名
        finish = self.st.st_finish_status()  # 学生 完成与否

        if len(finish) > 5 and content[0] == '':
            content = [name[len(finish)-2].text, finish[-2].text]
            for i in range(0, len(finish) - 1):
                print(name[i].text, finish[i].text)

            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content, remark)

            return content
        else:
            var = 0
            for k in range(len(finish)):
                if content[0] == name[k].text and content[1] == finish[k].text:
                    var += k
                    break
            for i in range(var, len(finish)):
                print(name[i].text, finish[i].text)

            self.into_operation(name[0].text, finish[0], remark)  # 进入详情页 具体操作

    @teststeps
    def into_operation(self, name, finish, title):
        """进入详情页"""
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
        if name != 'result':
            print(name)
            finish.click()  # 进入详情页

            if self.st.wait_check_per_detail_page(title):
                mode = self.detail.game_type()  # 游戏类型

                for j in range(len(mode)):
                    if self.detail.wait_check_per_detail_page():
                        name = self.detail.game_name()  # 游戏name
                        mode = self.detail.game_type()  # 游戏类型
                        optimal = self.detail.optimal_achievement()  # 最优成绩/首次成绩

                        game = name[j].text  # 游戏name
                        style = mode[j].text  # 游戏类型
                        achieve = optimal[j].text.split()  # 最优成绩/首次成绩
                        print(game, style)
                        mode[j].click()  # 点击进入game

                        if self.st.wait_check_detail_list_page(3):
                            print('----------答题情况 详情页----------')
                            value = self.result.first_report()  # 首次正答
                            self.judge_first_achieve(achieve[-1], value)  # 验证 首次成绩 与首次正答

                            if self.st.wait_check_per_detail_page(game):
                                self.home.back_up_button()  # 返回游戏列表页
                        elif self.detail.wait_check_per_detail_page(3):
                            print(optimal[j].text)
                        print('----------------------------------')

                if self.detail.wait_check_per_detail_page():
                    self.home.back_up_button()  # 返回tab页

    @teststeps
    def judge_first_achieve(self, achieve, report):
        """验证 首次成绩 与首次正答"""
        num = int(re.sub("\D", "", achieve))
        var = report.split('/')
        value = int(re.sub("\D", "", var[0]))

        if num != int(value/int(var[1])*100):
            print('★★★ Error- 首次成绩 与首次正答 不匹配:', achieve, report)
