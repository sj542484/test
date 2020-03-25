#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_star_page import VanclassStarPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class StarRanking(unittest.TestCase):
    """星星排行榜"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassStarPage()
        cls.van_detail = VanclassDetailPage()
        cls.get = GetAttribute()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(StarRanking, self).run(result)

    @testcase
    def test_star_ranking(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)

        self.van_detail.star_ranking()  # 进入 星星排行榜
        self.vue.app_web_switch()  # 切到apk 再切到vue
        if self.detail.wait_check_star_page():  # 页面检查点
            print('星星排行榜:')
            self.this_week_operation()  # 本周
            self.last_week_operation()  # 上周
            self.this_month_operation()  # 本月
            self.all_score_operation()  # 全部

            self.van_detail.back_up_button()
            self.vue.app_web_switch()  # 切到apk 再切到vue
            if self.van_detail.wait_check_page(gv.VANCLASS):  # 班级详情 页面检查点
                self.van_detail.back_up_button()
        else:
            print('未进入 星星排行榜页面')
            self.van_detail.back_up_button()

    @teststeps
    def this_week_operation(self):
        """本周tab 具体操作"""
        this_week = self.detail.this_week_tab()  # 本周
        print('-------------本周 tab-------------')
        if self.detail.wait_check_empty_tips_page():
            print('暂无数据')
        elif self.detail.wait_check_tab_list_page():
            self.star_operation()  # 具体操作

    @teststeps
    def last_week_operation(self):
        """上周tab 具体操作"""
        last = self.detail.last_week_tab()  # 上周
        last.click()  # 进入 上周 页面
        print('-------------上周 tab-------------')
        if self.detail.wait_check_empty_tips_page():
            print('暂无数据')
        elif self.detail.wait_check_tab_list_page():
            self.star_operation(2)  # 具体操作

    @teststeps
    def this_month_operation(self):
        """本月tab 具体操作"""
        this_month = self.detail.this_month_tab()  # 本月
        this_month.click()  # 进入 本月 页面
        print('-------------本月 tab-------------')
        if self.detail.wait_check_empty_tips_page():
            print('暂无数据')
        elif self.detail.wait_check_tab_list_page():
            self.star_operation(3)  # 具体操作

    @teststeps
    def all_score_operation(self):
        """全部tab 具体操作"""
        all_score = self.detail.all_tab()  # 全部
        all_score.click()  # 进入 全部 页面
        print('-------------全部 tab-------------')
        if self.detail.wait_check_empty_tips_page():
            print('暂无数据')
        elif self.detail.wait_check_tab_list_page():
            self.star_operation(4)  # 具体操作

    @teststeps
    def star_operation(self, var=1):
        """星星排行榜页面 具体操作"""
        order = self.detail.st_order()  # 编号
        icon = self.detail.st_icon()  # 头像
        name = self.detail.st_name()  # 昵称
        num = self.detail.num()  # 星星数

        self.compare_operation(order, name, num, 4*var, 4*(var-1))  # 具体比较操作

    @teststeps
    def compare_operation(self, order, name, num, length, var=1):
        """具体比较操作
        :param order: 编号
        :param name:昵称
        :param num: 星星
        :param length: 学生个数
        :param var: 循环起始值 滑屏后可能会不为1
        """

        print(order[var].text, name[var].text, num[var].text)
        if order[var].text != "1":   # 第一名 只能与后面同学比较 ，且星星大于其他同学
            if int(num[1].text) < int(num[0].text):
                print('★★★ Error- 星星排行有误：', num[1].text, num[0].text)
            else:
                print('星星排行无误')
            print('------------------------------')

        for i in range(var+1, length):
            print(order[i].text, name[i].text, num[i].text)
            if i not in (1, 4, 8, 16):
                if int(num[i].text) > int(num[i - 1].text):   # 除第一名以外的同学，星星只能比前一名少
                    print('★★★ Error- 星星排行有误：', num[i].text, num[i - 1].text)
                else:
                    print('星星排行无误')
            print('------------------------------')
