#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.adjust_vanclass_order_page import AdjustVanOrderPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun


class Vanclass(unittest.TestCase):
    """班级 列表 & 排序调整"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.adjust = AdjustVanOrderPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Vanclass, self).run(result)

    @testcase
    def test_vanclass_list_and_order(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        print('----------------班级列表----------------')
        van = self.vanclass_order()  # 班级 列表

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        self.home.class_sort_button()  # 班级排序 按钮
        self.adjust.adjust_vanclass_order()  # 调整班级顺序 具体操作
        self.adjust.confirm_button()  # 确定按钮

        van2 = self.vanclass_order()  # 班级 列表
        count = 0
        for i in range(len(van2)):
            if van2 != van:
                count += 1

        if len(van2) >1:
            if count == 0:
                print('★★★ Error- 班级顺序未调整')
            else:
                print('调整班级顺序保存成功')

    @teststeps
    def list_swipe_operation(self, content):
        """班级列表 滑屏 操作"""
        var = self.vanclass_statistic_operation(content)  # 获取 班级列表信息
        SwipeFun().swipe_vertical(0.5, 0.75, 0.25)

        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        title = []
        item = self.home.item_detail()  # 班级条目
        for i in range(len(item)):
            name = self.home.vanclass_name(item[i].text)  # name
            title.append(name)
        last = item[-1].text  # 最后一个班级的title

        index = []
        if len(title) != 10:  # 到底部
            if var in title:  # todo 列表中可能有多个相同
                if last != var:  # 滑动了
                    # print('滑动后到底部')
                    for i in range(len(title)):
                        if title[i] == var:
                            index.append(i + 1)
                            break
                else:
                    # print('到底了')
                    index.append(len(title))

                self.vanclass_statistic_operation(content, index[0])  # 获取 班级列表信息
        else:
            # print('滑动后未到底部')
            if var in title:  # 未滑够一页
                # print('未滑够一页')
                for i in range(len(title)):
                    if title[i] == var:
                        index.append(i + 1)
                        break
            else:
                index.append(0)

            return self.vanclass_statistic_operation(content, index[0])  # 获取 班级列表信息

    @teststeps
    def vanclass_statistic_operation(self, content, index=0):
        """获取班级列表 及 页面内最后一个name"""
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点

        name = self.home.item_detail()  # 班号+班级名
        count = self.home.st_count()  # 学生人数

        if len(name) != len(count):  # 滑屏后
            length = min(len(name), len(count))
        else:
            length = len(count)

        for i in range(index, length):
            num = self.home.vanclass_no(name[i].text)  # 班号
            van = self.home.vanclass_name(name[i].text)  # 班级名
            print(van, '  班号:', num, '  学生人数:', count[i].text)
            content.append(van)
        last = self.home.vanclass_name(name[-1].text)  # 最后一个作业的title

        return last

    @teststeps
    def vanclass_order(self):
        """班级 列表"""
        van = []
        self.list_swipe_operation(van)  # 已有班级数 统计

        print('--------------------------------------')
        content = []
        for i in range(len(van)):
            for j in range(len(van[i])):
                content.append(van[i][j])

        return content
