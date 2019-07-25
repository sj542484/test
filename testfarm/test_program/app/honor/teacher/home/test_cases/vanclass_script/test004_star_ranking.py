#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class StarRanking(unittest.TestCase):
    """星星排行榜"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_star_ranking(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_ANALY)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.star_ranking()  # 进入 星星排行榜
                    if self.detail.wait_check_star_page():  # 页面检查点
                        print('星星排行榜:')
                        self.this_week_operation()  # 本周
                        self.last_week_operation()  # 上周
                        self.this_month_operation()  # 本月
                        self.all_score_operation()  # 全部

                        self.home.back_up_button()
                        if self.van.wait_check_page(gv.VAN_ANALY):  # 班级详情 页面检查点
                            self.home.back_up_button()
                    else:
                        print('未进入 星星排行榜页面')
                        self.home.back_up_button()

        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def this_week_operation(self):
        """本周tab 具体操作"""
        this_week = self.detail.this_week_tab()  # 本周
        if self.get.selected(this_week) is False:
            print('★★★ Error- 默认在 本周页面')
        else:
            print('-------------本周 tab-------------')
            if self.home.wait_check_empty_tips_page():
                print('暂无数据')
            elif self.detail.wait_check_tab_list_page():
                self.star_operation()  # 具体操作

    @teststeps
    def last_week_operation(self):
        """上周tab 具体操作"""
        last = self.detail.last_week_tab()  # 上周
        if self.get.selected(last) is True:
            print('★★★ Error- 默认在 上周页面')
        else:
            last.click()  # 进入 上周 页面
            if self.get.selected(last) is False:
                print('★★★ Error- 未进入 上周页面')
            else:
                print('-------------上周 tab-------------')
                if self.home.wait_check_empty_tips_page():
                    print('暂无数据')
                elif self.detail.wait_check_tab_list_page():
                    self.star_operation()  # 具体操作

    @teststeps
    def this_month_operation(self):
        """本月tab 具体操作"""
        this_month = self.detail.this_month_tab()  # 本月
        if self.get.selected(this_month) is True:
            print('★★★ Error- 默认在 本月页面')
        else:
            this_month.click()  # 进入 本月 页面
            if self.get.selected(this_month) is False:
                print('★★★ Error- 未进入 本月页面')
            else:
                print('-------------本月 tab-------------')
                if self.home.wait_check_empty_tips_page():
                    print('暂无数据')
                elif self.detail.wait_check_tab_list_page():
                    self.star_operation()  # 具体操作

    @teststeps
    def all_score_operation(self):
        """全部tab 具体操作"""
        all_score = self.detail.all_tab()  # 全部
        if self.get.selected(all_score) is True:
            print('★★★ Error- 默认在 全部页面')
        else:
            all_score.click()  # 进入 全部 页面
            if self.get.selected(all_score) is False:
                print('★★★ Error- 未进入 全部页面')
            else:
                print('-------------全部 tab-------------')
                if self.home.wait_check_empty_tips_page():
                    print('暂无数据')
                elif self.detail.wait_check_tab_list_page():
                    self.star_operation()  # 具体操作

    @teststeps
    def star_operation(self, content=None):
        """星星排行榜页面 具体操作"""
        if content is None:
            content = []

        order = self.detail.st_order()  # 编号
        icon = self.detail.st_icon()  # 头像
        name = self.detail.st_name()  # 昵称
        num = self.detail.num()  # 星星数

        if len(order) > 6 and  not content:  # 多于8个
            content = [name[-2].text]
            self.compare_operation(order, name, num, len(order) - 1)  # 具体比较操作

            SwipeFun().swipe_vertical(0.5, 0.9, 0.3)
            self.star_operation(content)
        else:  # 少于7个 todo
            var = 1
            if content:
                for k in range(len(order) - 1, 0, -1):  # 滑屏后 页面中是否有已操作过的元素
                    if name[k].text == content[0]:
                        var = k + 1
                        break
            else:
                if len(order) != len(icon) != len(name) != len(num):
                    print('★★★ Error- 学生 编号、头像、昵称、星星的个数不等')

            self.compare_operation(order, name, num, len(order), var)  # 具体比较操作

    @teststeps
    def compare_operation(self, order, name, num, length, var=1):
        """具体比较操作
        :param order: 编号
        :param name:昵称
        :param num: 星星
        :param length: 学生个数
        :param var: 循环起始值 滑屏后可能会不为1
        """
        if var == 1:
            print(order[0].text, name[0].text, num[0].text)
            if order[0].text != "1":   # 第一名 只能与后面同学比较 ，且星星大于其他同学
                if int(num[1].text) < int(num[0].text):
                    print('★★★ Error- 星星排行有误：', num[1].text, num[0].text)
                else:
                    print('星星排行无误')
            print('------------------')

        for i in range(var, length):
            print(order[i].text, name[i].text, num[i].text)
            if i != 1:
                if int(num[i].text) > int(num[i - 1].text):   # 除第一名以外的同学，星星只能比前一名少
                    print('★★★ Error- 星星排行有误：', num[i].text, num[i - 1].text)
                else:
                    print('星星排行无误')
            print('------------------')
