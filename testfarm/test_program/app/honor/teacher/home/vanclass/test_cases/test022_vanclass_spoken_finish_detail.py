#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.spoken_finish_tab_detail_page import SpokenFinishDetailPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.student_type import basics
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassSpoken(unittest.TestCase):
    """本班口语 - 完成情况tab  二三级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.hw_detail = HwDetailPage()
        cls.v_hw = VanclassHwPage()
        cls.speak = SpokenFinishDetailPage()
        cls.van = VanclassPage()
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
        super(VanclassSpoken, self).run(result)

    @testcase
    def test_vanclass_spoken_finish_tab(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
    
        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)
        self.van.vanclass_hw()  # 点击 本班作业 tab
        name = self.v_hw.into_operation(gv.HW_TITLE, gv.VANCLASS, '口语')

        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
        print("题单:", name[0])
        self.finish_situation_operation()  # 完成情况 tab
        
        if self.hw_detail.wait_check_page():  # 页面检查点
            self.v_hw.back_up_button()  # 返回 作业列表
    
        self.vue.app_web_switch()  # 切到apk 再切到vue
        if self.v_hw.wait_check_page(name[1]):  # 页面检查点
            self.v_hw.back_up_button()  # 返回 班级详情页面
            self.vue.app_web_switch()  # 切到apk 再切到vue

            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                self.van.back_up_button()  # 返回主界面
                self.vue.switch_app()  # 切到apk
                    
    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        print('======================完成情况tab======================')
        if self.hw_detail.wait_check_st_list_page():
            self.st_list_statistics()  # 完成情况tab 列表信息

            status = self.hw_detail.st_finish_status()  # 学生完成与否
            st_mode = self.hw_detail.st_type()  # 基础班/提分版/试用期

            for i in range(len(status)):
                if self.hw_detail.wait_check_st_list_page():  # 页面检查点
                    print('===============================================')
                    name = self.hw_detail.st_name()  # 学生name
                    var = name[i].text
                    if status[i].text != '未完成':
                        mode = st_mode[i].get_attribute('src')
                        print('学生%s答题情况:' % var)
                        name[i].click()  # 进入一个学生的 game答题情况页
                        self.vue.app_web_switch()  # 切到apk 再切到vue

                        self.per_game_detail_operation(mode)  # game答题情况页
                        print('------------------------------------------')
                    else:
                        print('学生%s未完成' % var)
        elif self.hw_detail.wait_check_empty_tips_page():
            print('暂无数据')

    @teststeps
    def st_list_statistics(self, content=None):
        """完成情况 tab页信息"""
        if content is None:
            content = []

        name = self.hw_detail.st_name()  # 学生name
        self.hw_detail.st_icon()  # 学生头像
        status = self.hw_detail.st_finish_status()  # 学生完成与否

        if len(name) > 4 and not content:
            for i in range(len(name)-1):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

            content = [name[-2].text, status[len(name)-2].text]  # 最后一个game的name 完成与否
            self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
            self.st_list_statistics(content)
        else:
            var = 0
            if content:
                for k in range(len(name)):
                    if content[0] == name[k].text and content[1] == status[k].text:
                        var += k
                        break

            for j in range(var, len(name)):
                print('学生:', name[j].text, ' ', status[j].text)  # 打印所有学生信息

    @teststeps
    def per_game_detail_operation(self, mode):
        """个人 game答题情况页"""
        self.per_game_list()  # 列表信息

        if self.speak.wait_check_game_list_page():  # 页面检查点
            status = self.speak.game_finish_status()  # 游戏完成情况

            for j in range(len(status)):
                if self.speak.wait_check_game_list_page():  # 页面检查点
                    game = self.speak.game_name()  # 游戏name
                    print('---------------------------------------')
                    game[j].click()  # game答题情况详情页
                    self.vue.app_web_switch()  # 切到apk 再切到vue

                    if mode != basics:  # 提分版/试用期
                        print('答题情况详情:')
                        self.per_answer_detail()  # 答题情况详情
                        if self.speak.wait_check_detail_page():
                            # time.sleep(2)
                            self.v_hw.back_up_button()  # 返回游戏
                            self.vue.app_web_switch()  # 切到apk 再切到vue
                    else:  # 基础版
                        if self.speak.wait_check_detail_page(5):  # 页面检查点
                            print('答题情况详情:')
                            self.per_answer_detail()  # 答题情况详情
                            if self.speak.wait_check_detail_page():
                                # time.sleep(2)
                                self.v_hw.back_up_button()  # 返回游戏
                                self.vue.app_web_switch()  # 切到apk 再切到vue
                        elif self.speak.wait_check_game_list_page():
                            print('学生为基础版，该题为提分版')

            if self.speak.wait_check_game_list_page():  # 页面检查点
                self.v_hw.back_up_button()  # 返回完成情况 tab
                self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def per_game_list(self, content=None):
        """个人 game答题情况页 列表"""
        if content is None:
            content = []

        if self.speak.wait_check_game_list_page():  # 页面检查点
            name = self.speak.game_name()  # 游戏name
            mode = self.speak.game_type()  # 类型
            status = self.speak.game_finish_status()  # 游戏完成情况

            if len(status) > 4 and not content:
                content = [name[len(status)-2].text]
                for i in range(len(status)-1):
                    print(mode[i].text, name[i].text, status[i].text)

                self.v_hw.swipe_vertical_web(0.5, 0.85, 0.1)
                self.per_game_list(content)
            else:
                var = 0
                if content:  # 翻页成功 或者是第一页
                    for k in range(len(name)):
                        if content[0] == name[k].text:
                            var = k + 1
                            break

                for i in range(var, len(status)):
                    print(mode[i].text, name[i].text, status[i].text)

    @teststeps
    def per_answer_detail(self, content=None):
        """game 答题情况详情页"""
        if content is None:
            content = []

        if self.speak.wait_check_detail_page():
            games = self.speak.per_game_item()[1]  # 游戏题目

            if len(games) > 4 and not content:
                self.detail_st_info()  # 学生信息
                content = [games[-2]]
                self.detail_operation(len(games) - 1)  # 详情页 具体操作

                if self.speak.wait_check_detail_page():
                    self.v_hw.swipe_vertical_web(0.5, 0.9, 0.1)
                    self.per_answer_detail(content)
            else:
                var = 0
                if content:  # 翻页成功 或者是第一页
                    for k in range(len(games)):
                        if content[0] == games[k]:
                            var = k + 1
                            break
                else:
                    self.detail_st_info()  # 学生信息

                self.detail_operation(len(games), var)  # 详情页 具体操作

    @teststeps
    def detail_operation(self, length, var=0):
        """详情页 具体操作"""
        speak = self.speak.speak_button()  # 发音按钮
        for j in range(var, length):
            if self.speak.wait_check_detail_page():  # 页面检查点
                if self.speak.wait_check_detail_list_page():
                    # speak[j].click()
                    print(j+1, '.', self.speak.question()[j].text) # 游戏题目

        index = random.randint(var, length-1)
        self.speak.star_ratio()[index].click()  # 过关 按钮
        if self.speak.wait_check_modify_achieve_page():
            # todo 修改成绩
            self.hw_detail.commit_button()
            Toast().toast_vue_operation('修改成功')

    @teststeps
    def detail_st_info(self):
        """三级详情页 学生信息"""
        name = self.speak.detail_st_name()  # 学生name
        self.speak.detail_st_icon()  # 学生头像
        self.speak.detail_st_finish_status()  # 学生完成情况
        print(name)
        # print(name, icon, status)

        self.speak.detail_st_type()  # 学生 提分版/基础版
        self.speak.hint()  # 提示信息
        print('-----------------------------')
