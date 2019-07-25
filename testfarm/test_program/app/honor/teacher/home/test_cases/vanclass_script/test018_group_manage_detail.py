#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_member_page import VanMemberPage
from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.login.object_page import TloginPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.edit_text import DelEditText
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class GroupManage(unittest.TestCase):
    """小组管理 -- 小组详情页"""

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
    def test_group_manage_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.GROUP)  # 进入 班级
            if self.van.wait_check_page(gv.GROUP):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_member()  # 进入 班级成员
                    if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                        print('班级成员页面:')
                        if self.detail.wait_check_st_list_page():
                            self.group_detail_operation()  # 小组 详情页面
                        elif self.home.wait_check_empty_tips_page():
                            print('该班级暂无学生')

                        if self.member.wait_check_page(gv.GROUP):  # 页面检查点
                            self.home.back_up_button()  # 返回 班级详情 页
                            if self.van.wait_check_page(gv.GROUP):  # 班级详情 页面检查点
                                self.home.back_up_button()  # 返回 主界面
                    else:
                        print('未进入 班级成员页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

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
    def group_member_operation(self):
        """小组成员 页面具体操作"""
        if self.home.wait_check_empty_tips_page():
            print('暂无小组成员')
            return 0
        elif self.member.wait_check_st_list_page(5):
            remark = self.member.st_remark()  # 备注名
            phone = self.member.st_phone()  # 手机号
            vip = self.member.st_vip_expired()  # 时间
            tags = self.member.st_tags()  # 提分/基础/使用

            print('---------当前小组成员---------')
            if len(phone) < 6:  # 少于7个
                if len(remark) != len(phone) != len(vip) != len(tags):
                    print('★★★ Error- 学生、手机号、有效期、是否缴费元素个数不等')
                else:
                    for i in range(len(remark)):
                        print(' 学生:', remark[i].text, '\n',
                              "手机号:", phone[i].text, '\n'
                              "有效期:", vip[i].text)
                        self.member.judge_phone(phone[i].text)  # 验证手机号格式
                        print('-----------------------')
            else:  # 多于8个 todo 多于7个翻页
                for i in range(7):
                    print(' 学生:', remark[i].text, '\n',
                          "手机号:", phone[i].text, '\n',
                          "有效期:", vip[i].text)
                    self.member.judge_phone(phone[i].text)  # 验证手机号格式
                    print('-----------------------')
            return len(remark)

    @teststeps
    def menu_operation(self):
        """右键菜单"""
        print('============修改备注名============')
        remark = self.member.st_remark()  # 备注名
        print('原备注名为:', remark[0].text)
        self.detail.open_menu(remark[0])  # 学生条目 左键长按
        self.detail.menu_item(1)  # 修改备注名
        if self.home.wait_check_tips_page():
            self.home.tips_title()  # 修改窗口title

            var = self.home.input()  # 输入框
            var.send_keys("12")
            print('修改为：', var.text)
            button = self.home.commit()  # 确定按钮
            if self.get.enabled(button):
                button.click()
            print('-----------------------')

        if self.member.wait_check_st_list_page():
            print('=============移出小组=============')
            print('将学生 %s 移出该小组' % remark[0].text)
            self.detail.open_menu(remark[0])  # 学生条目 左键长按
            self.detail.menu_item(0)  # 移出群组

        if self.member.wait_check_st_list_page():
            self.home.back_up_button()  # 返回 班级成员页面

    @teststeps
    def create_group_operation(self):
        """创建小组 具体操作"""
        if self.home.wait_check_tips_page():  # 页面检查点
            self.home.tips_title()  # 修改窗口title
            var = self.home.input()  # 输入框
            var.send_keys(r'demo')
            self.home.commit_button()   # 点击 确定按钮  进入班级成员 页面

    @teststeps
    def recovery_operation(self):
        """恢复测试数据"""
        remark = self.member.st_remark()  # 备注名
        self.detail.open_menu(remark[0])  # 学生条目 左键长按
        self.detail.menu_item(1)  # 修改备注名
        if self.home.wait_check_tips_page():
            DelEditText().edit_text_clear("12")
            self.home.commit_button()  # 确定按钮
