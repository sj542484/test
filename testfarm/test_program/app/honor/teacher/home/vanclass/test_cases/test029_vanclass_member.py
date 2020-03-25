#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_student_info_page import StDetailPage
from app.honor.teacher.home.vanclass.test_data.remark_data import remark_dict
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassMember(unittest.TestCase):
    """班级成员"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.st = StDetailPage()
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
        super(VanclassMember, self).run(result)

    @testcase
    def test_vanclass_member(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        van = self.into_vanclass_operation()  # 进入 班级详情页
        print(van)

        print('=====================班级成员列表==================')
        self.member_list_operation()  # 获取学生列表 具体操作
        phone = self.menu_operation_modify(van)  # 学生 修改备注名
        self.menu_operation_delete(phone, van)  # 学生 移出班级

        if self.van_detail.wait_check_page(van):  # 页面检查点
            self.van_detail.back_up_button()
            self.vue.app_web_switch()  # 切到apk 再切到vue
            if self.van_detail.wait_check_page(van):  # 班级详情 页面检查点
                self.van_detail.back_up_button()

    @teststeps
    def into_vanclass_operation(self):
        """进入 班级"""
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 有班级检查点
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 有班级检查点
        vanclass = 0
        name = self.home.item_detail()  # 班号+班级名
        for i in range(len(name)):
            self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 有班级检查点
            name = self.home.item_detail()  # 班号+班级名
            vanclass = self.home.vanclass_name(name[i].text)  # 班级名
            if vanclass == gv.APPLY:
                name[i].click()  # 进入班级

                self.assertTrue(self.van_detail.wait_check_app_page(vanclass), self.van_detail.van_tips)  # 页面检查点
                self.vue.switch_h5()  # 切到web
                self.assertTrue(self.van_detail.wait_check_page(vanclass), self.van_detail.van_vue_tips)

                self.assertTrue(self.van_detail.wait_check_list_page(), self.van_detail.van_list_tips)
                self.van_detail.vanclass_member()  # 进入 班级成员
                self.vue.switch_app()

                self.assertTrue(self.member.wait_check_page(vanclass), self.member.member_tips)
                if self.home.wait_check_empty_tips_page():
                    self.home.back_up_button()  # 返回 班级页面
                    self.assertTrue(self.van_detail.wait_check_app_page(vanclass), self.van_detail.van_tips)  # 页面检查点
                    self.vue.switch_h5()  # 切到web
                    self.assertTrue(self.van_detail.wait_check_page(vanclass), self.van_detail.van_vue_tips)
                    self.van_detail.back_up_button()  # 返回主界面
                    continue
                elif self.member.wait_check_st_list_page():
                    phone = self.member.st_phone()  # 手机号
                    count = []
                    for j in range(len(phone)):
                        if self.member.wait_check_st_list_page():
                            phone = self.member.st_phone()  # 手机号
                            if phone[j].text[-4:] != gv.DETAIL:
                                count.append(j)

                    if count:
                        break
                    else:
                        self.home.back_up_button()  # 返回 班级页面
                        self.assertTrue(self.van_detail.wait_check_app_page(vanclass), self.van_detail.van_tips)  # 页面检查点
                        self.vue.switch_h5()  # 切到web
                        self.assertTrue(self.van_detail.wait_check_page(vanclass), self.van_detail.van_vue_tips)

                        self.van_detail.back_up_button()  # 返回主界面
        return vanclass

    @teststeps
    def member_list_operation(self, content=None):
        """班级成员 页面具体操作"""
        if content is None:
            content = []

        remark = self.member.st_remark()  # 备注名
        phone = self.member.st_phone()  # 手机号
        vip = self.member.st_vip_expired()  # 时间
        tags = self.member.st_tags()  # 提分/基础/使用

        if len(phone) > 7 and not content:  # 多于8个
            self.member_list(remark, phone, vip, len(phone))  # 成员列表信息

            content = [remark[len(phone)-2], phone[-2].text]
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

        print('---------------------------------')

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
    def menu_operation_modify(self, vanclass):
        """学生条目 左键长按菜单 -- 修改备注名"""
        print('=====================修改备注名====================')
        if self.member.wait_check_st_list_page():
            phone = self.member.st_phone()  # 手机号

            modify = 0  # 待修改/删除的学生手机号
            for i in range(len(phone)):
                if self.member.wait_check_st_list_page():
                    phone = self.member.st_phone()  # 手机号
                    if phone[i].text[-4:] != gv.DETAIL:
                        modify = phone[i].text[-4:]
                        self.member.open_menu(phone[i])  # 学生条目 左键长按
                        self.member.menu_item(1)  # 修改备注名

                        for j in range(len(remark_dict)):
                            if self.home.wait_check_tips_page():
                                self.home.tips_title()  # 修改窗口title

                                var = self.home.input()  # 输入框
                                var.clear()
                                var.send_keys(remark_dict[j]['name'])
                                print('修改为:', var.text)

                                self.home.character_num()  # 字符数
                                button = self.home.commit_button()
                                if len(remark_dict[j]) == 4:  # 确定按钮可点击，但不能保存成功
                                    if self.get.enabled(button) == 'true':
                                        button.click()  # 点击确定按钮
                                        Toast().toast_operation(remark_dict[j]['assert'])  # 获取toast

                                        if j != len(remark_dict) - 1:
                                            self.choose_st(modify)  # 选择学生
                                        print('-----------------------')
                                    else:
                                        print('★★★ Error- 确定按钮不可点击', self.get.enabled(button))
                                else:
                                    if remark_dict[j]['status'] == 'true':  # 成功的用例数据
                                        if self.get.enabled(button) == 'true':
                                            button.click()  # 点击确定按钮

                                            result = self.judge_st_remark(modify, vanclass)  # 验证 修改备注名是否成功
                                            if result != remark_dict[j]['name']:
                                                print('★★★ Error- 修改备注名不成功', result, remark_dict[j]['name'])
                                            else:
                                                print(' 修改备注名成功')

                                            if j != len(remark_dict)-1:
                                                self.choose_st(modify)  # 选择学生
                                            print('-----------------------')
                                        else:
                                            print('★★★ Error- 确定按钮不可点击', self.get.enabled(button))
                                    else:  # 确定按钮不可点击的
                                        if self.member.wait_check_st_list_page(3):
                                            print('★★★ Error- 确定按钮可点击')
                                            if j != len(remark_dict) - 1:
                                                self.choose_st(modify)  # 选择学生
                                        elif self.home.wait_check_tips_page():
                                            print('确定按钮不可点击')
                                    print('-----------------------------------------')

                        break
            return modify

    @teststeps
    def choose_st(self, modify):
        """选择学生"""
        if self.member.wait_check_st_list_page():
            phone = self.member.st_phone()  # 手机号
            for i in range(len(phone)):
                if phone[i].text[-4:] == modify:
                    self.member.open_menu(phone[i])  # 学生条目 左键长按
                    self.member.menu_item(1)  # 修改备注名
                    break

    @teststeps
    def menu_operation_delete(self, modify, vanclass):
        """学生条目 左键长按菜单 -- 移出班级"""
        print('======================移出班级=====================')
        if self.member.wait_check_st_list_page():
            remark = self.member.st_remark()
            phone = self.member.st_phone()  # 手机号
            for i in range(len(phone)):
                if phone[i].text[-4:] == modify:
                    name = phone[i].text  # 被移除学生
                    print('被移除学生: %s' % name)
                    self.member.open_menu(remark[i])  # 学生条目 左键长按
                    self.member.menu_item(0)  # 移出班级

                    if self.member.wait_check_page(vanclass):  # 页面检查点
                        SwipeFun().swipe_vertical(0.5, 0.3, 0.8)  # 刷新页面

                        if self.member.wait_check_page(vanclass):  # 页面检查点
                            result = self.member.st_phone()  # 验证 移出班级是否成功
                            if len(result) != len(remark)-1:
                                print('★★★ Error- 移出班级不成功', len(result), len(remark)-1)
                            else:
                                count = 0
                                for j in range(len(result)):
                                    if result[j].text == name:
                                        count += 1
                                        break

                                if count != 0:
                                    print('★★★ Error- 移出班级不成功', name)
                                else:
                                    print('移出班级成功')
                    break

    @teststeps
    def judge_st_remark(self, modify, vanclass):
        """验证 修改备注名是否成功"""
        if self.member.wait_check_page(vanclass):  # 页面检查点
            SwipeFun().swipe_vertical(0.5, 0.1, 0.8)

        if self.member.wait_check_page(vanclass):  # 页面检查点
            remark = self.member.st_remark()  # 备注名
            phone = self.member.st_phone()  # 手机号

            name = 0
            for i in range(len(phone)):
                if phone[i].text[-4:] == modify:
                    name = remark[i].text
                    break

            return name
