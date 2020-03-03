#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.object_page.vanclass_student_info_page import StDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_member_search import search_data
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext


class VanclassMember(unittest.TestCase):
    """班级成员 - 搜索功能"""

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
        cls.member = VanMemberPage()
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
    def test_vanclass_member_search(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)
        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)
        self.van.vanclass_member()  # 进入 班级成员

        self.vue.switch_app()
        if self.member.wait_check_page(gv.VANCLASS):  # 页面检查点
            print('班级成员页面:')
            self.search_operation()  # 搜索 具体操作

            self.assertTrue(self.member.wait_check_page(gv.VANCLASS))  # 页面检查点
            self.home.back_up_button()
            self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
            self.vue.switch_h5()  # 切到vue
            self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
            self.van.back_up_button()

    @teststeps
    def search_operation(self):
        """班级成员- 搜索功能"""
        if self.member.wait_check_page(gv.VANCLASS):
            self.member.search_button()  # 搜索按钮

        for i in range(len(search_data)):
            if self.member.wait_check_search_page():
                search = self.member.search_input()  # 搜索框
                search.send_keys(search_data[i]['search'])
                print('搜索词:', search.text)
                self.member_list_operation()  # 搜索结果页 具体操作

        if self.member.wait_check_search_page():
            self.home.back_up_button()  # 返回班级成员页面

    @teststeps
    def member_list_operation(self, content=None):
        """搜索结果页 具体操作"""
        if self.member.wait_check_st_list_page(3):
            if content is None:
                content = []

            remark = self.member.st_remark()  # 备注名
            phone = self.member.st_phone()  # 手机号
            vip = self.member.st_vip_expired()  # 时间
            tags = self.member.st_tags()  # 提分/基础/使用

            if len(phone) > 7 and not content:  # 多于8个
                self.member_list(remark, phone, vip, len(phone))  # 成员列表信息

                content = [remark[len(phone) - 2], phone[-2].text]
                SwipeFun().swipe_vertical(0.5, 0.9, 0.3)
                self.member_list_operation(content)
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

        elif self.member.wait_check_empty_page(3):
            self.member.no_st_info()  # 没有匹配到学生
        print('=============================================')

    @teststeps
    def member_list(self, remark, phone, vip, length, var=0):
        """成员列表信息"""
        for i in range(var, length):
            print('-----------------------')
            print(' 学生:', remark[i].text, '\n',
                  "手机号:", phone[i].text, '\n',
                  "有效期:", vip[i].text)
            self.member.judge_phone(phone[i].text)  # 验证手机号格式
