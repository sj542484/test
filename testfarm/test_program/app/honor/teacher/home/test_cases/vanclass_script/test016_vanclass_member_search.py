#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_member_page import VanMemberPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_member_search import search_data
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_student_info_page import StDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.app.utils.toast_find import Toast


class VanclassMember(unittest.TestCase):
    """班级成员 - 搜索功能"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.st = StDetailPage()
        cls.member = VanMemberPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_member_search(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_ANALY)  # 进入 班级
            if self.van.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_member()  # 进入 班级成员
                    if self.member.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                        print('班级成员页面:')
                        self.search_operation()  # 搜索 具体操作

                        if self.detail.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.VAN_ANALY):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('未进入 班级成员页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            self.member.page_source()
            print("未进入主界面")

    @teststeps
    def search_operation(self):
        """班级成员- 搜索功能"""
        if self.member.wait_check_page(gv.VAN_ANALY):
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
    def member_list_operation(self):
        """搜索结果页 具体操作"""
        if self.member.wait_check_st_list_page(3):
            remark = self.member.st_remark()  # 备注名
            phone = self.member.st_phone()  # 手机号
            vip = self.member.st_vip_expired()  # 时间
            tags = self.member.st_tags()  # 提分/基础/使用

            if len(phone) < 5:  # 少于6个
                if len(remark) != len(phone) != len(vip) != len(tags):
                    print('★★★ Error- 学生、手机号、有效期、是否缴费元素个数不等')
                else:
                    for i in range(len(remark)):
                        print('-----------------------')
                        print(' 学生:', remark[i].text, '\n',
                              "手机号:", phone[i].text, '\n',
                              "有效期:", vip[i].text)
                        self.judge_phone(phone[i].text)  # 验证手机号格式
            else:  # 多于5个 todo 多于5个翻页
                for i in range(7):
                    print('-----------------------')
                    print(' 学生:', remark[i].text, '\n',
                          "手机号:", phone[i].text, '\n',
                          "有效期:", vip[i].text)
                    self.judge_phone(phone[i].text)  # 验证手机号格式
            print('---------------------------------')
        elif self.member.wait_check_empty_page(3):
            self.member.no_st_info()  # 没有匹配到学生
        print('=============================================')

    @teststeps
    def judge_phone(self, var):
        """验证 手机号格式 （中间4位显示成*）-- 根据校长端设置！！！"""
        # 中间4位不显示成*
        if not self.member.isDigit(var):
            print('★★★ Error- 不为数字：', var)
