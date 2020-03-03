#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.student.object_page.login_page import LoginPage
from app.honor.student.test_cases.apply_for_vanclass import Vanclass
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.vanclass_apply_page import VanclassApplyPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.object_page.vanclass_student_info_page import StDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext


class VanclassApply(unittest.TestCase):
    """入班申请"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.apply = VanclassApplyPage()
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
        super(VanclassApply, self).run(result)

    @testcase
    def test_vanclass_apply(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        van_id = self.into_vanclass_operation(gv.APPLY)  # 进入 班级  返回班号

        self.assertTrue(self.van.wait_check_app_page(gv.APPLY), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.APPLY), self.van.van_vue_tips)
        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)

        self.van.vanclass_application()  # 进入 入班申请
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.apply.wait_check_page(), self.apply.apply_vue_tips)
        if self.apply.wait_check_empty_tips_page():
            LoginPage().launch_app()
            Vanclass().apply_for_vanclass_operation(van_id)
            LoginPage().close_app()

        print('###################################################################')
        self.assertTrue(self.apply.wait_check_page(), self.apply.apply_vue_tips)  # 页面检查点
        self.apply.swipe_vertical_web(0.5, 0.2, 0.8)
        print('-----------------------')
        print('入班申请页面:')

        result = self.apply_operation()  # 同意 入班申请 具体操作
        self.refuse_apply_operation()  # 拒绝 入班申请

        if result[0]:
            self.verification_result(result[0][0], result[1])  # 验证 入班申请 结果

        self.assertTrue(self.apply.wait_check_page(), self.apply.apply_vue_tips)  # 页面检查点
        self.van.back_up_button()
        self.vue.app_web_switch()  # 切到apk 再切到vue
        if self.van.wait_check_page(gv.APPLY):  # 班级详情 页面检查点
            self.van.back_up_button()  # 返回主界面

    @teststeps
    def apply_operation(self):
        """入班申请 页面具体操作"""
        if self.apply.wait_check_empty_tips_page():
            self.assertFalse(self.apply.wait_check_empty_tips_page(), self.apply.empty_tips)
        else:
            print('-----------------同意入班申请---------------')
            self.assertTrue(self.apply.wait_check_st_list_page(), self.apply.apply_list_tips)  # 页面检查点
            icon = self.apply.icon()  # icon
            remark = self.apply.st_remark()  # 备注名
            nick = self.apply.st_nick()  # 昵称
            more = self.apply.more_button()  # 更多按钮

            count = [len(nick)]  # 申请人数
            item = []  # 同意入班的学生name及备注名
            for i in range(len(nick)):
                self.assertTrue(self.apply.wait_check_st_list_page(), self.apply.apply_list_tips)  # 页面检查点
                print('-----------------------')
                print(' 学生:', remark[i].text, '\n',
                      "昵称:", nick[i].text)

                if i == len(nick)-1:
                    item.append(remark[i].text)
                    item.append(nick[i].text)
                    more[i].click()  # 更多按钮
                    self.assertTrue(self.apply.wait_check_more_page(), self.apply.more_tips)
                    self.apply.more_agree_button()  # 同意按钮
            print('---------------------------------')
            print('同意入班申请：', item)

            return count, item

    @teststeps
    def refuse_apply_operation(self):
        """拒绝入班申请 页面具体操作"""
        if self.apply.wait_check_empty_tips_page():
            self.assertFalse(self.apply.wait_check_empty_tips_page(), self.apply.empty_tips)
        else:
            self.assertTrue(self.apply.wait_check_st_list_page(), self.apply.apply_list_tips)  # 页面检查点
            print('-----------------拒绝入班申请---------------')
            remark = self.apply.st_remark()  # 备注名
            print('拒绝学生 %s 的入班申请' % remark[0].text)
            print('-----------------------')

            self.apply.more_button[0].click()  # 更多按钮
            self.assertTrue(self.apply.wait_check_more_page(), self.apply.more_tips)
            self.apply.more_reject_button()  # 拒绝按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def verification_result(self, var, item):
        """验证 入班申请 结果"""
        print('---------------验证 入班申请 结果-------------')
        self.apply.swipe_vertical_web(0.5, 0.1, 0.8)
        if self.apply.wait_check_st_list_page():
            title = self.apply.st_remark()  # 备注名
            if len(title) < 6:
                self.assertEqual(len(title), var-2, '★★★ Error- 申请数未减2:{}'.format(len(title), var))
            else:
                for k in range(len(title)):
                    if title[k].text == item[0]:
                        nick = self.apply.st_nick()
                        self.assertEqual(nick[k].text, item[1], '★★★ Error- 申请列表还存在该申请信息{}'.format(var))
                        break
        elif self.apply.wait_check_empty_tips_page():
            self.assertTrue(var-2, '★★★ Error- 原申请数为{}'.format(var))

        self.van.back_up_button()  # 返回
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.van.wait_check_page(gv.APPLY), self.van.van_vue_tips)
        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)

        self.van.vanclass_member()  # 班级成员
        self.vue.switch_app()
        self.assertTrue(self.member.wait_check_page(gv.APPLY), self.member.member_tips)
        print('-------------班级成员页面------------')
        if self.home.wait_check_empty_tips_page():
            self.assertFalse(self.home.wait_check_empty_tips_page(), '★★★ Error- 同意入班失败，班级成员页面无数据')
        else:
            self.assertTrue(self.member.wait_check_st_list_page(), self.member.member_list_tips)
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

    @teststeps
    def into_vanclass_operation(self, var):
        """进入 班级"""
        if self.home.wait_check_list_page():
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            if self.home.wait_check_list_page():
                name = self.home.item_detail()  # 班号+班级名

                count = []
                for i in range(len(name)):
                    van = self.home.vanclass_name(name[i].text)  # 班级名
                    if van == var:
                        item = self.home.vanclass_no(name[i].text)
                        print('进入班级:', item)
                        name[i].click()  # 进入班级
                        count.append(i)

                        return item  # 班号

                if not count:
                    index = random.randint(0, len(name)-1)
                    item = self.home.vanclass_no(name[index].text)
                    name[index].click()  # 进入班级

                    return item  # 班号
