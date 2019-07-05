#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_member_page import VanMemberPage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.app.honor.teacher.home.test_data.group_name_data import group_data
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class GroupManage(unittest.TestCase):
    """小组管理 - 小组列表&创建/删除/修改小组名"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.member = VanMemberPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_group_manage(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.GROUP)  # 进入 班级
            if self.van.wait_check_page(gv.GROUP):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_member()  # 进入 班级成员
                    if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                        print('班级成员页面:')

                        if self.detail.wait_check_st_list_page():
                            for i in range(len(group_data)-1):
                                self.member.add_group_button()  # 添加 小组按钮
                                self.create_group_operation(i)  # 创建小组 具体操作

                            if self.member.wait_check_page(gv.GROUP):
                                print('=================小组列表===================')
                                self.group_manage_operation([''])  # 小组管理 具体操作
                                print('===============修改/删除小组=================')
                                self.group_menu_operation([''])  # 小组 右键菜单操作

                                if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                                    self.home.back_up_button()
                                    if self.van.wait_check_page(gv.GROUP):  # 班级详情 页面检查点
                                        self.home.back_up_button()
                        elif self.home.wait_check_empty_tips_page():
                            print('暂时没有数据')
                else:
                    print('未进入 班级成员页面')
                    self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def group_manage_operation(self, content):
        """小组管理 具体操作"""
        if self.member.group_judge():  # 存在小组
            name = self.member.group_name()  # 组名
            count = self.member.st_count()  # 学生人数

            if len(name) > 5 and content[0] == '':
                content = [name[-2].text]  # 最后一个game的name
                for i in range(len(name)-1):
                    print(name[i].text, count[i].text)

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.group_manage_operation(content)
            else:  # <4 &翻页
                var = 0
                if content[0] != name[-1].text:  # 翻页 成功
                    for k in range(len(name)):
                        if content[0] == name[k].text:
                            var += k + 1
                            break

                for j in range(var, len(name)):
                    print(name[j].text, count[j].text)

    @teststeps
    def group_menu_operation(self, content=None):
        """小组 右键操作"""
        if content == None:
            content=[]

        if self.member.group_judge():  # 存在小组
            name = self.member.group_name()  # 组名

            if len(name) < 5 and not content:
                content = [name[-1].text]  # 第一个game的name

                self.specific_operation(0, len(name))  # 具体操作

                if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                    SwipeFun().swipe_vertical(0.5, 0.3, 0.95)
                    self.group_menu_operation(content)
            else:  # >6 & 下拉翻页
                var = 0
                if content:
                    if content[0] != name[-1].text:  # 下拉翻页 不成功
                        for k in range(len(name)):
                            if content[0] == name[k].text:
                                var += k + 1
                                break

                self.specific_operation(var, len(name))  # 具体操作

    @teststeps
    def specific_operation(self, var, length):
        """具体操作"""
        for i in range(var, length):
            if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                name = self.member.group_name()  # 组名
                if len(name) == 1:
                    print('原组名为:', name[0].text)
                    self.edit_group_name(name[0], group_data[2]['name'])  # 修改组名
                    #
                    # print('----恢复测试数据----')
                    # if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                    #     name = self.member.group_name()  # 组名
                    #     self.edit_group_name(name[0], "demo")  # 修改组名
                    break
                else:
                    print('删除小组:', name[1].text)
                    self.detail.open_menu(name[1])  # 小组条目 左键长按
                    self.detail.menu_item(1)  # 删除 小组
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
            # item.clear()  # 清除
            item.send_keys(r'' + var)
            print('修改为:', item.text)
            button = self.home.commit()  # 确定按钮
            if self.get.enabled(button):
                button.click()
            print('------------------------------------')

    @teststeps
    def create_group_operation(self, i):
        """创建小组 具体操作"""
        if self.home.wait_check_tips_page():  # 页面检查点
            button = self.home.commit()  # 确定按钮
            if i == 0:
                print('==================创建小组==================')
                self.home.tips_content()  # 修改窗口 提示信息

                if self.get.enabled(button) is 'true':
                    print('★★★ Error- 确定按钮未置灰')
            else:
                if self.get.enabled(button) != 'false':
                    print('★★★ Error- 确定按钮状态有误')

            var = self.home.input()  # 输入框
            var.send_keys(r'' + group_data[i]['name'])

            if i == 0:
                length = len(group_data[0]['name'])
                print(group_data[0]['name'])
            else:
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

            button = self.home.commit()  # 确定按钮
            status = self.detail.button_enabled_judge(length, button, size1, 30)
            if status == 'true':  # 可点击
                button.click()  # 点击 确定按钮  进入班级成员 页面
                if len(group_data) == 4:
                    if Toast().find_toast(group_data[i]['assert']):  # 获取toast
                        print(group_data[i]['assert'])
                elif self.detail.wait_check_page(gv.GROUP):  # 页面检查点
                    if self.member.wait_check_page(group_data[i]['name']):  # 页面检查点
                        group = self.member.group_name()  # todo
                        item = group[-1].text
                        if group_data[i]['name'] != item:
                            print('★★★ Error- 小组名称展示有误', group_data[i]['name'], item)
            else:
                self.home.click_block()  # 点击 取消按钮

        print('----------------------')
