#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.test_data.modify_vanclass_data import class_data
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class ModifyVanclass(unittest.TestCase):
    """修改班级名称"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.van = VanclassPage()
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_modify_vanclass(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.into_vanclass_operation(gv.MODIFY_VAN)  # 进入 班级详情页
            if self.van.wait_check_page(gv.MODIFY_VAN):  # 页面检查点
                self.van.more_button()  # 右上角 更多 按钮

                if self.van.wait_check_tips_page():
                    self.van.modify_name(0)  # 班级名称 按钮

                    self.modify_vanclass_operation()  # 修改班级名称

                if self.van.wait_check_page(gv.MODIFY_VAN):
                    self.home.back_up_button()  # 返回主界面
        else:
            Toast().get_toast()  # 获取toast:
            print("未进入主界面")

    @teststeps
    def into_vanclass_operation(self, var):
        """进入 班级"""
        if self.home.wait_check_list_page():
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            if self.home.wait_check_list_page():
                name = self.home.item_detail()  # 班号+班级名
                count = self.home.st_count()  # 学生数
                for i in range(len(name)):
                    van = self.home.vanclass_name(name[i].text)  # 班级名
                    if van == var or int(count[i].text) == 0:  # var 或者 空班
                        print('进入班级:', var)
                        name[i].click()  # 进入班级
                        break

    @teststeps
    def modify_vanclass_operation(self):
        """修改班级名称 具体操作"""
        if self.home.wait_check_tips_page():  # 页面检查点
            if self.get.enabled(self.home.commit_button()) == 'false':  # 确定按钮 enabled值
                print('★★★ Error- 确定按钮不可点击')

            print('--------------------------------')
            self.home.tips_title()  # 修改窗口title
            self.home.tips_content()  # 修改窗口 提示信息

            var = self.home.input()  # 输入框
            if var.text != gv.MODIFY_VAN:
                print('★★★ Error- 班级名称展示有误')

            for i in range(len(class_data)):
                var = self.home.input()
                var.send_keys(class_data[i]['name'])

                if i == 0:
                    length = len(class_data[0]['name'])
                    print('修改为:', class_data[0]['name'])
                else:
                    length = len(var.text)
                    print('修改为:', var.text)

                size = self.home.character_num()  # 字符数
                size1 = re.findall(r'\d+(?#\D)', size)[0]
                size2 = re.findall(r'\d+(?#\D)', size)[1]
                if int(size2) != 10:
                    print('★★★ Error- 最大字符数展示有误', size2)
                else:
                    if length != int(size1):
                        print('★★★ Error- 字符数展示有误', size2)

                button = self.home.commit_button()  # 确定按钮 元素
                status = self.detail.button_enabled_judge(length, button, size1)

                if status != class_data[i]['status']:
                    print('★★★ Error- 确定按钮状态有误', status)
                    self.home.click_block()
                elif status == 'true':  # 可点击
                    button.click()  # 点击 确定按钮  进入班级详情页

                    if len(class_data[i]) == 4:
                        Toast().toast_operation(class_data[i]['assert'])  # 获取toast信息

                        if not self.van.wait_check_page(class_data[i]['name'],3):  # 页面检查点
                            van = self.detail.judge_van_modify()  # 班级名称 不能修改成功验证
                            if class_data[i]['name'] == van:
                                print('★★★ Error- 班级名称修改成功', class_data[i]['name'], van)
                    else:
                        if not self.van.wait_check_page(class_data[i]['name']):  # 页面检查点
                            if i != 5:
                                van = self.detail.judge_van_modify()  # 班级名称 修改成功验证
                                print('★★★ Error- 班级名称修改后展示有误', class_data[i]['name'], van)
                            else:
                                print('修改成功')
                        else:
                            print('修改成功')

                    if i != len(class_data)-1:
                        self.van.more_button()  # 右上角 更多 按钮
                        if self.van.wait_check_tips_page():
                            self.van.modify_name(0)  # 班级名称 按钮 进入修改页面

                            if self.home.wait_check_tips_page():  # 页面检查点
                                button = self.home.commit_button()  # 确定按钮
                                if self.get.enabled(button) != class_data[i]['status']:
                                    print('★★★ Error- 确定按钮不可点击')
                print('--------------------------------')
