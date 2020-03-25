#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import sys
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.create_vanclass_data import class_data
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class CreateVanclass(unittest.TestCase):
    """创建班级"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(CreateVanclass, self).run(result)

    @testcase
    def test_create_vanclass(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点

        self.home.add_class_button()  # 创建班级 按钮
        for i in range(len(class_data)):

            self.assertTrue(self.home.wait_check_tips_page(), '★★★ Error- 创建班级名称弹窗')  # 页面加载完成 检查点
            button = self.home.commit_button()  # 确定按钮
            if i == 0:
                self.home.tips_content()  # 修改窗口 提示信息
                if self.get.enabled(button) is 'true':
                    print('★★★ Error- 确定按钮未置灰')
            else:
                if self.get.enabled(button) is 'false':
                    print('★★★ Error- 确定按钮不可点击')
            print('--------------------------------------')

            var = self.home.input()  # 输入框
            var.send_keys(class_data[i]['name'])

            if i != 0:
                length = len(var.text)
                print('创建班级:', var.text)
            else:
                length = len(class_data[0]['name'])
                print('创建班级:', class_data[0]['name'])

            size = self.home.character_num()  # 字符数
            size1 = re.findall(r'\d+(?#\D)', size)[0]
            size2 = re.findall(r'\d+(?#\D)', size)[1]

            if int(size2) != 10:
                print('★★★ Error- 最大字符数展示有误', size2)

            button = self.home.commit_button()  # 确定按钮
            status = self.van_detail.button_enabled_judge(length, button, size1)
            if status != class_data[i]['status']:
                print('★★★ Error- 确定按钮状态有误', status)
            elif status == 'true':  # 可点击
                button.click()  # 点击 确定按钮  进入主界面
                if len(class_data[i]) == 4:
                    self.my_toast.toast_assert(self.name, Toast().toast_operation(class_data[i]['assert']))  # 获取toast信息
                    self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
                    self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点

                    van = self.home.item_detail()
                    if class_data[i]['name'] != '   ':
                        content = [k for k in van if self.home.vanclass_name(k.text) == class_data[i]['name']]  # 班级名称
                        self.assertTrue(len(content) == 1,
                                        '★★★ Error- 班级名称不可重复功能有误, {} {}'.format(class_data[i]['name'], content))
                    else:
                        item = self.home.vanclass_name(van[0].text)  # 班级名称
                        van_text = class_data[i]['name'].rstrip().lstrip()
                        self.assertNotEqual(item, van_text,
                                            '★★★ Error- 班级名称为多空格时, 创建成功 {} {}'.format(class_data[i]['name'], item))
                    print('创建失败')

                else:
                    self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
                    self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
                    van = self.home.item_detail()  # 班级元素
                    item = self.home.vanclass_name(van[0].text)  # 班级名称
                    van_text = class_data[i]['name'].rstrip().lstrip()

                    if van_text != item:
                        self.assertEqual(item, van_text,
                                         '★★★ Error- 班级名称创建后展示有误, {} {}'.format(class_data[i]['name'], item))
                        print('创建成功')
                        van[0].click()  # 进入班级名称修改页面
                        self.delete_vanclass_operation(i, item)  # 删除创建的班级
                    else:
                        print('创建成功')
                        van[0].click()  # 进入班级名称修改页面
                        self.delete_vanclass_operation(i, item)  # 删除创建的班级

                self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
                if i != len(class_data) - 1:
                    self.home.add_class_button()  # 创建班级 按钮

    @teststeps
    def delete_vanclass_operation(self, i, van_class):
        """删除创建的班级"""
        self.assertTrue(self.van_detail.wait_check_app_page(van_class), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(van_class), self.van_detail.van_vue_tips)
        print('---------------', '\n',
              '删除该班级')
        self.van_detail.more_button()  # 右上角 更多 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_more_tips_page(), self.van_detail.more_tips)
        self.van_detail.delete_van_button()  # 删除班级 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_tips_page(), '★★★ Error- 删除班级二次确认弹窗')  # 二次确认弹框
        self.van_detail.tips_commit_button()  # 确定按钮
        self.my_toast.toast_assert(self.name, Toast().toast_vue_operation('成功删除班级'))

        self.vue.switch_app()  # 切回app
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        van = self.home.item_detail()
        item = self.home.vanclass_name(van[0].text)  # 班级名称

        self.assertNotEqual(class_data[i]['name'], item, '★★★ Error- 班级删除失败, {} {}'.format(class_data[i]['name'], item))
