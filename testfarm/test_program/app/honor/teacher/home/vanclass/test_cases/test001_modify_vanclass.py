#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.modify_vanclass_data import class_data
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class ModifyVanclass(unittest.TestCase):
    """修改班级名称"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.van_detail = VanclassDetailPage()
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切到apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(ModifyVanclass, self).run(result)

    @testcase
    def test_modify_vanclass(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        van = self.into_vanclass_operation()  # 进入 班级详情页
        self.assertTrue(self.van_detail.wait_check_app_page(van), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.van_detail.wait_check_page(van), self.van_detail.van_vue_tips)
        self.van_detail.more_button()  # 右上角 更多 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_more_tips_page(), self.van_detail.more_tips)
        self.van_detail.modify_van_name()  # 班级名称 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.modify_vanclass_operation(van)  # 修改班级名称
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_page(van), self.van_detail.van_vue_tips)
        self.van_detail.back_up_button()  # 返回主界面

    @teststeps
    def into_vanclass_operation(self):
        """进入 班级"""
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        name = self.home.item_detail()  # 班号+班级名
        count = self.home.st_count()  # 学生数

        van = 0
        for i in range(len(name)):
            if int(count[i].text) == 0:  # var 或者 空班
                van = self.home.vanclass_name(name[i].text)  # 班级名
                print('进入班级:', van)
                name[i].click()  # 进入班级
                break
        return van

    @teststeps
    def modify_vanclass_operation(self, vanclass):
        """修改班级名称 具体操作"""
        self.assertTrue(self.van_detail.wait_check_tips_page(), '★★★ Error- 修改班级名称弹窗')  # 页面加载完成 检查点
        for i in range(len(class_data)):
            var = self.van_detail.input()  # 输入框
            var.clear()
            var.send_keys(class_data[i]['name'])
            print('修改为:', class_data[i]['name'])

            if len(class_data[i]) == 3:
                self.van_detail.tips_commit_button()  # 确定按钮 元素
                self.my_toast.toast_assert(self.name, Toast().toast_vue_operation(class_data[i]['assert']), True, '★★★ Error- 班级名称修改成功')  # 获取toast信息
                van = self.van_detail.judge_van_modify()  # 班级名称 不能修改成功验证
                self.assertNotEqual(class_data[i]['name'], van, '★★★ Error- 班级名称修改成功 {} {}'.format(class_data[i]['name'], van))
                print('修改不成功')
            else:  # 符合规则 ‘班级名称由1~10位中英文及数字组成’
                self.van_detail.tips_commit_button()  # 确定按钮 元素
                self.vue.switch_app()

                if class_data[i]['name'] == '':
                    var = vanclass
                else:
                    var = class_data[i]['name'].rstrip().lstrip()
                    var = ' '.join(var.split())

                self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
                self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
                name = self.home.item_detail()  # 班号+班级名

                modify = 0
                for k in range(len(name)):
                    modify = self.home.vanclass_name(name[k].text)
                    print(modify)
                    if modify in var:  # var 或者 空班
                        name[k].click()
                        self.vue.switch_h5()
                        break

                if self.van_detail.wait_check_page(modify):  # 页面检查点
                    print('修改成功')
                else:
                    if i == 5:
                        van = self.van_detail.judge_van_modify()  # 班级名称 修改成功验证
                        self.assertNotEqual(class_data[i]['name'], van, '★★★ Error- 班级名称修改后展示有误, {} {}'.format(class_data[i]['name'], van))
                        print('修改成功')
                    else:
                        self.assertTrue(self.van_detail.wait_check_page(modify), self.van_detail.van_vue_tips)
                        print('修改成功')

            if i != len(class_data)-1:
                self.vue.app_web_switch()  # 切到apk 再切到vue
                self.van_detail.more_button()  # 右上角 更多 按钮
                self.assertTrue(self.van_detail.wait_check_more_tips_page(), self.van_detail.more_tips)

                self.van_detail.modify_van_name()  # 班级名称 按钮 进入修改页面
                self.vue.app_web_switch()  # 切到apk 再切到vue
                self.assertTrue(self.van_detail.wait_check_tips_page(), '★★★ Error- 修改班级名称弹窗')  # 页面加载完成 检查点

            print('--------------------------------')
