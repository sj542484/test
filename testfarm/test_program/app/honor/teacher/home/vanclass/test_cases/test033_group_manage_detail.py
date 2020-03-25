#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.edit_text import DelEditText
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext


class GroupManage(unittest.TestCase):
    """小组管理 -- 小组详情页"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
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
    def test_group_manage_detail(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.APPLY)  # 进入 班级
        self.assertTrue(self.van_detail.wait_check_app_page(gv.APPLY), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.van_detail.wait_check_page(gv.APPLY), self.van_detail.van_vue_tips)
        self.assertTrue(self.van_detail.wait_check_list_page(), self.van_detail.van_list_tips)
        self.van_detail.vanclass_member()  # 进入 班级成员
        self.vue.switch_app()

        if self.member.wait_check_page(gv.APPLY):  # 页面检查点
            print('班级成员页面:')
            if self.member.wait_check_st_list_page():
                self.group_detail_operation()  # 小组 详情页面
            elif self.home.wait_check_empty_tips_page():
                print('该班级暂无学生')

            if self.member.wait_check_page(gv.APPLY):  # 页面检查点
                self.home.back_up_button()  # 返回 班级详情 页
                self.assertTrue(self.van_detail.wait_check_app_page(gv.APPLY), self.van_detail.van_tips)  # 页面检查点
                self.vue.switch_h5()  # 切到vue

                self.assertTrue(self.van_detail.wait_check_page(gv.APPLY), self.van_detail.van_vue_tips)
                self.van_detail.back_up_button()

    @teststeps
    def group_detail_operation(self):
        """小组 详情页面具体操作"""
        if not self.member.group_judge():
            print('暂无小组')
            self.member.add_group_button()  # 添加 小组按钮
            self.create_group_operation()  # 创建小组 具体操作

        if self.member.group_judge():
            name = self.member.group_name()  # 组名
            count = self.member.st_count()  # 学生人数

            for i in range(len(name)):
                var = name[i].text  # 组名
                num = count[i].text  # 当前人数
                name[i].click()  # 进入该小组
                print('小组 %s 详情页：' % var)

                length = 0
                if self.member.wait_check_page(var):
                    if self.home.wait_check_empty_tips_page():
                        if num == '0人':
                            print('暂无学生')
                        else:
                            print('★★★ Error- 页面显示暂无学生，学生人数为:', num)
                        print('-------------------')

                    elif self.member.wait_check_st_list_page():
                        self.menu_operation()  # 修改备注名/移出小组操作

                        print('---------当前小组成员---------')
                        length = self.group_member_operation()  # 当前 小组成员

                    self.add_member_operation(var)  # 添加小组成员

                    if self.member.wait_check_page(var):
                        length1 = self.group_member_operation()  # 小组成员 具体操作

                        if length != length1 - 1:
                            print('★★★ Error- 添加小组成员失败', length, length1)
                        else:
                            self.recovery_operation()  # 恢复测试数据

                    if self.member.wait_check_page(var):
                        self.home.back_up_button()  # 返回 班级详情页
                break

    @teststeps
    def add_member_operation(self, group):
        """添加 小组成员 具体操作"""
        if self.member.wait_check_page(group):  # 小组 成员页面
            print('===========添加小组成员============')
            self.member.add_st_button()  # 添加学生 按钮
            if self.member.wait_check_page(group):  # 添加学生页面
                if self.member.wait_check_st_list_page():
                    choose = self.member.choose_button()  # 单选框
                    phone = self.member.st_phone()  # 手机号
                    print('添加 %s为小组成员' % phone[0].text)
                    choose[0].click()  # 添加第一个
                    self.member.confirm_button()  # 确定按钮

    @teststeps
    def group_member_operation(self, content=None):
        """小组成员 页面具体操作"""
        if content is None:
            content = []

        if self.home.wait_check_empty_tips_page():
            print('暂无小组成员')
            return 0
        elif self.member.wait_check_st_list_page():
            remark = self.member.st_remark()  # 备注名
            phone = self.member.st_phone()  # 手机号
            vip = self.member.st_vip_expired()  # 时间
            tags = self.member.st_tags()  # 提分/基础/使用

            if len(phone) > 7 and not content:  # 多于8个
                self.member_list(remark, phone, vip, len(phone))  # 成员列表信息

                content = [remark[len(phone) - 2], phone[-2].text]
                SwipeFun().swipe_vertical(0.5, 0.9, 0.3)
                self.group_member_operation(content)
            else:  # 少于6个
                var = 0
                if content:
                    for k in range(len(phone), 0, -1):  # 滑屏后 页面中是否有已操作过的元素
                        if remark[k].text == content[0] and phone[k].text == content[1]:
                            var = k + 1
                            break
                else:
                    if len(remark) != len(phone) != len(vip) != len(tags):
                        print('★★★ Error- 学生、手机号、有效期、是否缴费元素个数不等')

                self.member_list(remark, phone, vip, len(phone), var)  # 成员列表信息

            return len(remark)

    @teststeps
    def member_list(self, remark, phone, vip, length, var=0):
        """成员列表信息"""
        for i in range(var, length):
            print('-----------------------')
            print(' 学生:', remark[i].text, '\n',
                  "手机号:", phone[i].text, '\n',
                  "有效期:", vip[i].text)
            self.member.judge_phone(phone[i].text)  # 验证手机号格式

    @teststeps
    def menu_operation(self):
        """右键菜单"""
        print('============修改备注名============')
        remark = self.member.st_remark()  # 备注名
        print('原备注名为:', remark[0].text)
        self.member.open_menu(remark[0])  # 学生条目 左键长按
        self.member.menu_item(1)  # 修改备注名
        if self.home.wait_check_tips_page():
            self.home.tips_title()  # 修改窗口title

            var = self.home.input()  # 输入框
            var.send_keys("12")
            print('修改为：', var.text)
            button = self.home.commit_button()  # 确定按钮
            if self.get.enabled(button):
                button.click()
            print('-----------------------')

        if self.member.wait_check_st_list_page():
            print('=============移出小组=============')
            print('将学生 %s 移出该小组' % remark[0].text)
            self.member.open_menu(remark[0])  # 学生条目 左键长按
            self.member.menu_item(0)  # 移出群组

        if self.member.wait_check_st_list_page():
            self.home.back_up_button()  # 返回 班级成员页面

    @teststeps
    def create_group_operation(self):
        """创建小组 具体操作"""
        if self.home.wait_check_tips_page():  # 页面检查点
            self.home.tips_title()  # 修改窗口title
            var = self.home.input()  # 输入框
            var.send_keys(r'demo')
            self.home.commit_button().click()   # 点击 确定按钮  进入班级成员 页面

    @teststeps
    def recovery_operation(self):
        """恢复测试数据"""
        remark = self.member.st_remark()  # 备注名
        self.member.open_menu(remark[0])  # 学生条目 左键长按
        self.member.menu_item(1)  # 修改备注名
        if self.home.wait_check_tips_page():
            DelEditText().edit_text_clear("12")
            self.home.commit_button().click()  # 确定按钮
