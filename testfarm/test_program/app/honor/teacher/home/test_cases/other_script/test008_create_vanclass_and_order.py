#!/usr/bin/env python
# encoding:UTF-8
import re
import time
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.adjust_vanclass_page import AdjustVanOrderPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.test_data import class_data
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class CreateVanclass(unittest.TestCase):
    """创建班级 & 排序调整"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van = VanclassPage()
        cls.detail = VanclassDetailPage()
        cls.adjust = AdjustVanOrderPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_create_vanclass(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_list_page():  # 页面加载完成 检查点

                for i in range(len(class_data)):
                    if self.home.wait_check_van_page():
                        self.home.add_class_button()  # 创建班级 按钮
                        self.create_vanclass_operation(i)  # 创建班级 具体操作
            else:
                print('页面未加载完成')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def create_vanclass_operation(self, i):
        """创建班级 具体操作"""
        if self.home.wait_check_tips_page():  # 页面检查点
            button = self.home.commit()  # 确定按钮
            if i == 0:
                self.home.tips_content()  # 修改窗口 提示信息
                if self.get.enabled(button) is 'true':
                    print('★★★ Error- 确定按钮未置灰')
            else:
                if self.get.enabled(button) is 'false':
                    print('★★★ Error- 确定按钮不可点击')
            print('--------------------------------------')

            var = self.home.input()  # 输入框
            var.send_keys(r'' + class_data[i]['name'])

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

            button = self.home.commit()  # 确定按钮
            status = self.detail.button_enabled_judge(length, button, size1)
            if status != class_data[i]['status']:
                print('★★★ Error- 确定按钮状态有误', status)
                self.home.click_block()  # 点击空白处 取消
            elif status == 'true':  # 可点击
                button.click()  # 点击 确定按钮  进入主界面
                if len(class_data[i]) == 4:
                    if not Toast().find_toast(class_data[i]['assert']):
                        print('★★★ Error- 未弹toast', class_data[i]['assert'])
                    else:
                        print(class_data[i]['assert'])

                    if self.home.wait_check_page(3):  # 页面检查点
                        if self.home.wait_check_van_page():
                            van = self.home.item_detail()
                            item = self.home.vanclass_name(van[0].text)  # 班级名称
                            if class_data[i]['name'] == item:
                                print('★★★ Error- 班级名称不可重复功能有误', class_data[i]['name'], item)
                else:
                    if self.home.wait_check_page:  # 页面检查点
                        if self.home.wait_check_van_page():  # 有班级列表
                            time.sleep(1)
                            van = self.home.item_detail()  # 班级元素
                            item = self.home.vanclass_name(van[0].text)  # 班级名称

                            if class_data[i]['name'] != item:
                                if item in class_data[i]['name'] and i == 5:
                                    print('创建成功')
                                    van[0].click()  # 进入班级名称修改页面
                                    self.delete_vanclass_operation(i, item)  # 删除创建的班级
                                else:
                                    print('★★★ Error- 班级名称创建后展示有误', class_data[i]['name'], item)
                            else:
                                print('创建成功')
                                van[0].click()  # 进入班级名称修改页面
                                self.delete_vanclass_operation(i, item)  # 删除创建的班级
            else:
                self.home.click_block()  # 点击空白处 取消

    @teststeps
    def delete_vanclass_operation(self, i, item):
        """删除创建的班级"""
        if self.van.wait_check_page(item):
            print('---------------', '\n',
                  '删除该班级')
            self.van.more_button()  # 右上角 更多 按钮
            if self.van.wait_check_tips_page():
                self.van.modify_name(2)  # 班级名称 按钮

                if self.home.wait_check_tips_page():  # 页面检查点
                    button = self.home.commit()  # 确定按钮
                    if self.get.enabled(button) is False:
                        print('★★★ Error- 确定按钮不可点击')
                    else:
                        self.home.commit_button()  # 确定按钮
                        if self.home.wait_check_page:  # 页面检查点
                            if self.home.wait_check_van_page():  # 已有班级
                                van = self.home.item_detail()
                                item = self.home.vanclass_name(van[0].text)  # 班级名称
                                if class_data[i]['name'] == item:
                                    print('★★★ Error- 班级删除失败', class_data[i]['name'], item)
