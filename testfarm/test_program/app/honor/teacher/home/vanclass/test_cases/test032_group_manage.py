#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
import re

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.test_data.group_name_data import group_data
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class GroupManage(unittest.TestCase):
    """小组管理 - 小组列表&创建/删除/修改小组名"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van = VanclassPage()
        cls.member = VanMemberPage()
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
        super(GroupManage, self).run(result)

    @testcase
    def test_001_group_manage_create(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.APPLY)  # 进入 班级
        self.assertTrue(self.van.wait_check_app_page(gv.APPLY), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.van.wait_check_page(gv.APPLY), self.van.van_vue_tips)
        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)
        self.van.vanclass_member()  # 进入 班级成员
        self.vue.switch_app()

        self.assertTrue(self.member.wait_check_page(gv.APPLY), self.member.member_tips)
        print('班级成员页面:')
        if self.home.wait_check_empty_tips_page():
            self.assertFalse(self.home.wait_check_empty_tips_page(), '该班级暂无学生')
            print('该班级暂无学生')
        else:
            self.assertTrue(self.member.wait_check_st_list_page(), self.member.member_list_tips)
            self.member.add_group_button()  # 添加 小组按钮
            for i in range(len(group_data)):
                self.create_group_operation(i)  # 创建小组 具体操作

            if self.member.wait_check_page(gv.APPLY):  # 页面检查点
                self.home.back_up_button()
                self.assertTrue(self.van.wait_check_app_page(gv.APPLY), self.van.van_tips)  # 页面检查点
                self.vue.switch_h5()  # 切到vue

                self.assertTrue(self.van.wait_check_page(gv.APPLY), self.van.van_vue_tips)
                self.van.back_up_button()

    @testcase
    def test_002_group_manage_delete(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.APPLY)  # 进入 班级
        self.assertTrue(self.van.wait_check_app_page(gv.APPLY), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.van.wait_check_page(gv.APPLY), self.van.van_vue_tips)
        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)
        self.van.vanclass_member()  # 进入 班级成员
        self.vue.switch_app()

        self.assertTrue(self.member.wait_check_page(gv.APPLY), self.member.member_tips)

        print('班级成员页面:')
        if self.home.wait_check_empty_tips_page():
            self.assertFalse(self.home.wait_check_empty_tips_page(), '该班级暂无学生')
            print('该班级暂无学生')
        else:
            self.assertTrue(self.member.wait_check_st_list_page(), self.member.member_list_tips)
            print('=================小组列表===================')
            self.group_manage_operation()  # 小组管理 具体操作
            print('===============修改/删除小组=================')
            self.group_menu_operation()  # 小组 右键菜单操作

            if self.member.wait_check_page(gv.APPLY):  # 页面检查点
                self.home.back_up_button()
                self.assertTrue(self.van.wait_check_app_page(gv.APPLY), self.van.van_tips)  # 页面检查点
                self.vue.switch_h5()  # 切到vue

                self.assertTrue(self.van.wait_check_page(gv.APPLY), self.van.van_vue_tips)
                self.van.back_up_button()

    @teststeps
    def group_manage_operation(self, content=None):
        """小组管理 具体操作"""
        if content is None:
            content = []

        if self.member.group_judge():  # 存在小组
            name = self.member.group_name()  # 组名
            count = self.member.st_count()  # 学生人数

            if len(name) > 5 and not content:
                content = [name[-2].text]  # 最后一个小组的name
                for i in range(len(name)-1):
                    print(name[i].text, count[i].text)

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.group_manage_operation(content)
            else:  # <4 &翻页
                var = 0
                if content:  # 翻页
                    for k in range(len(name)):
                        if content[0] == name[k].text:
                            var += k + 1
                            break

                for j in range(var, len(name)):
                    print(name[j].text, count[j].text)

    @teststeps
    def group_menu_operation(self):
        """小组 右键操作"""
        if self.member.group_judge():  # 存在小组
            while True:
                if self.member.wait_check_page(gv.APPLY):  # 页面检查点
                    name = self.member.group_name()  # 组名
                    if len(name) == 1:
                        print('原组名为:', name[0].text)
                        self.edit_group_name(name[0], group_data[2]['name'])  # 修改组名

                        print('----恢复测试数据----')
                        if self.member.wait_check_page(gv.APPLY):  # 页面检查点
                            name = self.member.group_name()  # 组名
                            self.edit_group_name(name[0], "Demo")  # 修改组名
                        break
                    else:
                        print('删除小组:', name[1].text)
                        self.member.open_menu(name[1])  # 小组条目 左键长按
                        self.member.menu_item(1)  # 删除 小组
                        self.home.tips_commit()  # 温馨提示 -- 确定
                        print('------------------------------------')

    @teststeps
    def edit_group_name(self, name, var):
        """修改组名 操作"""
        self.member.open_menu(name)  # 小组条目 左键长按
        self.member.menu_item(0)  # 修改 小组名
        if self.home.wait_check_tips_page():
            self.home.tips_title()  # 修改窗口title

            item = self.home.input()  # 输入框
            item.clear()  # 清除
            item.send_keys(var)
            print('修改为:', item.text)
            button = self.home.commit_button()  # 确定按钮
            if self.get.enabled(button):
                button.click()
            print('------------------------------------')

    @teststeps
    def create_group_operation(self, i):
        """创建小组 具体操作"""
        if self.home.wait_check_tips_page():  # 页面检查点
            button = self.home.commit_button()  # 确定按钮
            if i == 0:
                print('==================创建小组==================')
                self.home.tips_content()  # 修改窗口 提示信息

                if self.get.enabled(button) is 'true':
                    print('★★★ Error- 确定按钮未置灰')
            else:
                if self.get.enabled(button) != 'false':
                    print('★★★ Error- 确定按钮状态有误')

            var = self.home.input()  # 输入框
            var.send_keys(group_data[i]['name'])

            if i == 0:
                length = len(group_data[0]['name'])
                print(group_data[0]['name'])
            else:
                var = self.home.input()  # 输入框
                length = len(var.text)
                print(var.text)

            size = self.home.character_num()  # 字符数
            size1 = re.findall(r'\d+(?#\D)', size)[0]
            size2 = re.findall(r'\d+(?#\D)', size)[1]

            if int(size2) != 30:
                print('★★★ Error- 最大字符数展示有误', size2)
            else:
                if length != int(size1):
                    print('★★★ Error- 字符数展示有误', size2)

            button = self.home.commit_button()  # 确定按钮
            status = self.van.button_enabled_judge(length, button, size1, 30)
            if status == 'true':  # 可点击
                button.click()  # 点击 确定按钮  进入班级成员 页面
                if len(group_data[i]) == 4:
                    self.my_toast.toast_assert(self.name, Toast().toast_operation(group_data[i]['assert']))
                elif self.van.wait_check_page(gv.APPLY):  # 页面检查点
                    if self.member.wait_check_page(group_data[i]['name']):  # 页面检查点
                        group = self.member.group_name()  #
                        item = group[-1].text
                        if group_data[i]['name'] != item:
                            print('★★★ Error- 小组名称展示有误', group_data[i]['name'], item)

                if i != len(group_data)-1:
                    if self.member.wait_check_page(gv.APPLY):  # 页面检查点
                        self.member.add_group_button()  # 添加 小组按钮
        print('----------------------')
