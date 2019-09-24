#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.student.object_page.login_page import LoginPage
from app.honor.student.test_cases.apply_for_vanclass import Vanclass
from app.honor.teacher.home.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_student_info_page import StDetailPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class VanclassApply(unittest.TestCase):
    """入班申请"""

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
    def test_vanclass_apply(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.APPLY)  # 进入 班级
            if self.van.wait_check_page(gv.APPLY):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_application()  # 进入 入班申请
                    if self.detail.wait_check_page(gv.APPLY):  # 页面检查点
                        if self.home.wait_check_empty_tips_page() or len(self.detail.st_remark()) == 1:
                            LoginPage().launch_app()
                            Vanclass().apply_for_vanclass_operation()
                            LoginPage().close_app()

                        print('###################################################################')
                        if self.detail.wait_check_page(gv.APPLY):  # 页面检查点
                            SwipeFun().swipe_vertical(0.5, 0.1, 0.8)
                            print('-----------------------')
                            print('入班申请页面:')
                            if self.detail.wait_check_st_list_page():
                                result = self.apply_operation()  # 同意 入班申请 具体操作
                                self.refuse_apply_operation()  # 拒绝 入班申请

                                if result[0]:
                                    if self.detail.wait_check_page(gv.APPLY):  # 页面检查点
                                        self.verification_result(result[0][0], result[1])  # 验证 入班申请 结果
                            else:
                                print('★★★ Error- 无入班申请学生')
                        else:
                            print('!!!未进入 入班申请页面')

                        if self.van.wait_check_page(gv.APPLY):  # 入班申请 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.APPLY):  # 班级详情 页面检查点
                                self.home.back_up_button()  # 返回主界面
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def apply_operation(self):
        """入班申请 页面具体操作"""
        print('-----------------同意入班申请---------------')
        count = []  # 申请人数
        item = []  # 同意入班的学生name及备注名
        icon = self.detail.icon()  # icon
        remark = self.detail.st_remark()  # 备注名
        nick = self.detail.st_nick()  # 昵称
        agree = self.detail.agree_button()  # 同意按钮

        if len(nick) < 6:  # 少于6个
            if len(icon) != len(remark) != len(nick) != len(agree):
                count.append(len(nick))
                print('★★★ Error- 学生icon、name、昵称、同意按钮个数不等')

        count.append(len(nick))
        for i in range(len(nick)):
            print('-----------------------')
            print(' 学生:', remark[i].text, '\n',
                  "昵称:", nick[i].text)

            if i == len(nick)-1:
                item.append(remark[i].text)
                item.append(nick[i].text)
                agree[i].click()  # 同意
        print('---------------------------------')
        print('同意入班申请：', item)

        return count, item

    @teststeps
    def refuse_apply_operation(self):
        """拒绝入班申请 页面具体操作"""
        if self.detail.wait_check_page(gv.APPLY):  # 页面检查点
            print('-----------------拒绝入班申请---------------')
            if self.detail.wait_check_st_list_page():
                remark = self.detail.st_remark()  # 备注名
                print('拒绝学生 %s 的入班申请' % remark[0].text)
                print('-----------------------')

                self.detail.open_menu(remark[0])  # 申请学生条目 左键长按
                self.detail.menu_item(0)  # 拒绝 入班申请
            elif self.home.wait_check_empty_tips_page():
                print('暂时没有数据')

    @teststeps
    def verification_result(self, var, item):
        """验证 入班申请 结果"""
        print('---------------验证 入班申请 结果-------------')
        SwipeFun().swipe_vertical(0.5, 0.1, 0.8)
        if self.detail.wait_check_st_list_page():
            title = self.detail.st_remark()  # 备注名
            if len(title) < 6 and len(title) != var-2:
                print('★★★ Error- 申请数未减2:', len(title), var)
            else:
                for k in range(len(title)):
                    if title[k].text == item[0]:
                        nick = self.detail.st_nick()
                        if nick[k].text == item[1]:
                            print('★★★ Error- 申请列表还存在该申请信息', item)
                            break
        elif self.home.wait_check_empty_tips_page():
            if var > 2:
                print('★★★ Error- 原申请数为', var)

        self.home.back_up_button()  # 返回
        if self.van.wait_check_page(gv.APPLY):
            if self.van.wait_check_list_page():

                self.van.vanclass_member()  # 班级成员
                if self.detail.wait_check_page(gv.APPLY):  # 页面检查点
                    print('-------------班级成员页面------------')
                    if self.member.wait_check_st_list_page():
                        st = self.member.st_remark()  # 备注名
                        for j in range(len(st)):
                            if st[j].text == item[0]:
                                st[j].click()  # 进入学生 具体信息页面
                                if self.st.wait_check_page():  # 页面检查点
                                    name = self.st.st_name()  # 学生备注名
                                    nick = self.st.st_nickname()  # 昵称
                                    print('备注名:', name, nick)
                                    if item[0] != name and item[1] != nick:
                                        print('★★★ Error- 同意入班失败，班级成员页面无该学生', item)
                                    else:
                                        print('同意入班成功')

                                    self.home.back_up_button()
                                    break
                    elif self.home.wait_check_empty_tips_page():
                        print('★★★ Error- 同意入班失败，班级成员页面无数据')
            else:
                print('!!!班级页面未加载成功')