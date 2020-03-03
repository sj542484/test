#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
import time
import re

from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.test_data.hw_detail_data import game_type_operation
from app.honor.teacher.home.dynamic_info.object_page.hw_finish_tab_student_answer_result_page import ResultDetailPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_student_hw_detail_page import StHwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.object_page.vanclass_student_info_page import StDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassMember(unittest.TestCase):
    """班级成员 - 学生详情页"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van = VanclassPage()
        cls.st = StDetailPage()
        cls.st_hw = StHwDetailPage()
        cls.member = VanMemberPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassMember, self).run(result)

    @testcase
    def test_vanclass_member_detail(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级
        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)
        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)
        self.van.vanclass_member()  # 进入 班级成员
        self.vue.switch_app()

        if self.member.wait_check_page(gv.VANCLASS):  # 页面检查点
            print('班级成员页面:')
            if self.member.wait_check_st_list_page():
                self.member_info_operation()  # 学生具体信息页面
            elif self.home.wait_check_empty_tips_page():
                print('暂时没有数据')

            if self.member.wait_check_page(gv.VANCLASS):  # 页面检查点
                self.home.back_up_button()
                self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
                self.vue.switch_h5()  # 切到vue

                self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
                self.van.back_up_button()

    @teststeps
    def member_info_operation(self):
        """班级成员- 学生具体信息页面"""
        remark = self.member.st_phone()
        for i in range(len(remark)):
            if remark[i].text[-4:] == gv.DETAIL:
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
                    print('---------------------------------')

                    self.st.data_statistic()  # 数据统计
                    if self.st.wait_check_per_detail_page(name):
                        print('=========================数据统计 页面=========================')
                        print('已进入数据统计 页面')
                        time.sleep(2)
                        self.home.back_up_button()  # 返回学生信息页面

                    if self.st.wait_check_page():
                        self.picture_page_operation(nick)  # 拼图卡片

                    if self.st.wait_check_page():
                        self.hw_page_operation(name)  # 习题作业

                    if self.st.wait_check_page():
                        self.home.back_up_button()  # 返回学生成员 列表页
                    break

    @teststeps
    def picture_page_operation(self, nick):
        """拼图卡片"""
        self.st.picture_count()  # 拼图
        if self.st.wait_check_per_detail_page(nick[3:]):
            if self.st.wait_check_picture_page():
                print('=========================拼图卡片 页面=========================')
                if self.st.judge_picture():
                    num = self.st.picture_num()
                    print(num[0].text)

                self.st.picture_report()  # 拼图报告
                self.home.back_up_button()  # 返回学生信息页面

    @teststeps
    def hw_page_operation(self, name):
        """作业列表"""
        self.st.hw_count()  # 作业list
        if self.st_hw.wait_check_app_page(name):
            self.vue.switch_h5()
            if self.st_hw.wait_check_page(name):
                print('=========================习题作业 页面=========================')
                self.finished_operation(name)  # 已完成tab
                self.unfinished_operation(name)  # 未完成tab

                if self.st_hw.wait_check_page(name):
                    self.st_hw.back_up_button()  # 返回学生信息页面
                    self.vue.switch_app()
        else:
            print('未进入 习题作业')

    @teststeps
    def finished_operation(self, name):
        """已完成tab 具体操作"""
        if self.st_hw.wait_check_page(name):
            complete = self.st_hw.finished_tab()  # 已完成 tab
            if self.get.selected(complete) is False:
                print('★★★ Error- 未默认在 已完成 tab页')
            else:
                print('-------------------------已完成tab-------------------------')
                if self.st_hw.wait_check_hw_list_page():
                    self.answer_analysis_detail(name)    # 已完成 列表
                    if self.st_hw.wait_check_hw_list_page():
                        self.st_hw.back_up_button()  # 返回 已完成tab
                        self.vue.app_web_switch()
                elif self.st_hw.wait_check_empty_tips_page():
                    print('暂无数据')

    @teststeps
    def unfinished_operation(self, name):
        """未完成tab 具体操作"""
        if self.st_hw.wait_check_page(name):
            unfinished = self.st_hw.unfinished_tab()  # 未完成 tab
            if self.get.selected(unfinished) is True:
                print('★★★ Error- 默认在 未完成 tab页')
            else:
                unfinished.click()  # 进入 未完成 tab页
                self.vue.app_web_switch()
                if self.get.selected(unfinished) is False:
                    print('★★★ Error- 未进入 未完成 tab页')
                else:
                    print('-------------------------未完成tab-------------------------')
                    if self.st_hw.wait_check_hw_list_page():
                        self.answer_analysis_detail(name)  # 未完成页

                        if self.st_hw.wait_check_hw_list_page():
                            self.st_hw.back_up_button()  # 返回 未完成tab
                            self.vue.app_web_switch()
                    elif self.st_hw.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, remark, content=None):
        """未完成/已完成tab 详情页"""
        if content is None:
            content = []

        if self.st_hw.wait_check_hw_list_page():
            name = self.st_hw.hw_title()  # 作业包 名
            finish = self.st_hw.hw_finish()  # 学生 完成与否

            var = 0
            if len(finish) > 5 and not content:
                content = [name[len(finish)-2].text, finish[-2].text]
                length = len(finish)-1
                for i in range(var, length):
                    print(name[i].text, finish[i].text)
                self.random_into_game_operation(remark, name, finish, var, length)  # 游戏列表页及进入游戏详情页

                self.st_hw.swipe_vertical_web(0.5, 0.85, 0.1)
                self.answer_analysis_detail(remark, content)
            else:
                length = len(finish)
                if content:
                    for k in range(len(finish)):
                        if content[0] == name[k].text and content[1] == finish[k].text:
                            var += k+1
                            break

                for i in range(var, length):
                    print(name[i].text, finish[i].text)

                self.random_into_game_operation(remark, name, finish, var, length)  # 游戏列表页及进入游戏详情页

    @teststeps
    def random_into_game_operation(self, remark, name, finish, var, length):
        """游戏列表页及进入游戏详情页"""
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # index = random.randint(var, length)
        text = name[3].text
        print(text)
        print('============================================')
        finish[3].click()  # 进入 作业包 的游戏列表页

        self.vue.app_web_switch()
        if self.st_hw.wait_check_game_page(remark):
            self.games_operation(remark)  # 游戏列表页及进入游戏详情页 具体操作
            if self.st_hw.wait_check_game_page(remark):
                self.st_hw.back_up_button()  # 返回tab页
        else:
            print("★★★ Error- 未进入答题情况 详情页")

    @teststeps
    def games_operation(self, remark, content=None):
        """游戏详情页"""
        if content is None:
            content = []

        name = self.st_hw.game_name()  # 游戏name
        mode = self.st_hw.game_type()  # 游戏类型
        optimal = self.st_hw.optimal_achievement()  # 最优成绩/首次成绩

        if len(optimal) > 4 and not content:
            content = [name[len(optimal) - 2].text, mode[len(optimal) - 2].text]
            self.game_detail_operation(0, len(optimal)-1, remark)

            self.st_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            self.vue.app_web_switch()
            if self.st_hw.wait_check_game_page(remark):
                self.games_operation(remark, content)
        else:
            var = 0
            if content:
                for k in range(len(name)):
                    print(name[k].text, mode[k].text)
                    if content[0] == name[k].text and content[1] == mode[k].text:
                        var += k+1
                        break

            self.game_detail_operation(var, len(name), remark)

    @teststeps
    def game_detail_operation(self, var, length, names):
        """游戏详情页 并返回游戏列表页"""
        for j in range(var, length):
            if self.st_hw.wait_check_game_page(names):
                name = self.st_hw.game_name()  # 游戏name
                mode = self.st_hw.game_type()  # 游戏类型
                optimal = self.st_hw.optimal_achievement()  # 最优成绩/首次成绩

                game = name[j].text  # 游戏name
                style = mode[j].text  # 游戏类型
                achieve = optimal[j].text  # 最优成绩/首次成绩
                score = int(re.sub('\D', '', achieve.split()[-1]))  # 首次成绩
                print(game, style, '\n', achieve)
                print('----------------')

                mode[j].click()  # 点击进入game
                self.vue.app_web_switch()

                value = game_type_operation(style)
                if value == 17:  # 微课
                    self.vue.app_web_switch()  # 切到apk 再切回vue
                    MyToast().toast_assert(self.name, Toast().toast_vue_operation(TipsData().no_report))  # 获取toast
                elif value == 24:  # 单词跟读
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    self.result.word_reading_operation(score)
                elif value in (21, 22, 23):  # 口语
                    print('口语')  # todo 口语
                    time.sleep(2)
                    self.result.back_up_button()   # 返回  游戏列表
                elif value == 14:  # 闪卡练习
                    print(mode)
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    content = []
                    if mode == '句子学习':
                        self.result.flash_sentence_operation(content, score)
                    elif mode in ('单词学习', '单词抄写'):
                        self.result.flash_card_list_operation(content, score)
                elif value == 16:  # 连连看
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    content = []
                    print(mode)
                    if mode == '文字模式':
                        if self.result.wait_check_list_page():
                            self.result.report_score_compare(score)  # 验证 首次成绩 与首次正答

                        self.result.list_operation(content)
                    elif mode == '图文模式':  # 图文模式
                        self.result.match_img_operation(content)
                elif value == 18:  # 磨耳朵
                    self.vue.app_web_switch()  # 切到apk 再切回vue
                    self.result.ears_ergodic_list()
                else:
                    self.vue.app_web_switch()  # 切到apk 再切回vue
                    self.result.hw_detail_operation(value, score)

            self.vue.app_web_switch()  # 切到apk 再切回vue
            print('=================================================================')

    @teststeps
    def judge_first_achieve(self, achieve, report):
        """验证 首次成绩 与 首次正答
        :param achieve: 首次成绩
        :param report: 首次正答
        """
        item = report.split('/')
        value = int(re.sub("\D", "", item[0]))
        if int(item[1]) != 0:
            answer_num = int(value / int(item[1]) * 100)
        else:
            answer_num = 0
        if achieve != answer_num:
            var = achieve - answer_num
            if var < 0:
                var = -var

            if var > 1:
                print(achieve, answer_num)
                print('★★★ Error- 首次成绩 与首次正答 不匹配:', achieve, report)

        return item
