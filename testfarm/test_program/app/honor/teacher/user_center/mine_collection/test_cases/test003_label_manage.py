#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest
import time

from conf.decorator import setup, teardown, testcase, teststeps
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_collection.test_data.add_label import label_data
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class Collection(unittest.TestCase):
    """我的收藏 -- 标签管理"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.filter = FilterPage()
        cls.collect = CollectionPage()
        cls.question = TestBankPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_collection_label_manage(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_collection()  # 点击 我的收藏
                if self.collect.wait_check_page():  # 页面检查点
                    content = self.create_label_operation()  # 创建标签 具体操作
                    modify = self.modify_label_operation(content)  # 修改标签 操作
                    remove = self.remove_label_operation()  # 移除标签 操作
                    self.judge_operation(remove, modify)  # 验证 移除/修改标签 结果

                    if self.collect.wait_check_manage_page():
                        self.home.back_up_button()  # 返回收藏页面
                else:
                    print('未进入 我的收藏 页面')

                if self.collect.wait_check_page():
                    self.home.back_up_button()  # 返回个人中心页
            else:
                print('未进入个人中心页面')
            if self.user.wait_check_page():  # 页面检查点
                self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def create_label_operation(self):
        """创建标签 具体操作"""
        self.collect.more_button()
        if self.collect.wait_check_label_manage_page():
            self.collect.label_manage_button()  # 标签管理按钮

            content = []  # 创建的标签
            if self.collect.wait_check_manage_page():
                self.label_list(content)  # 已有标签列表
                print('---------------创建标签----------------')
                k = 0
                for j in range(len(label_data)):
                    if self.collect.wait_check_manage_list_page():
                        if label_data[j]['label'] not in content:
                            self.collect.add_label()  # 创建标签
                            if self.home.wait_check_tips_page():
                                self.home.tips_title()
                                item = self.home.input()
                                item.send_keys(label_data[j]['label'])
                                print('标签：', item.text)
                                if self.get.enabled(self.home.commit_button()):
                                    self.home.commit_button().click()  # 点击 确定按钮

                                    if self.collect.wait_check_manage_list_page():
                                        label = self.collect.label_title()  # 已有标签
                                        if len(label) != len(content)+1:
                                            time.sleep(1)
                                            label = self.collect.label_title()  # 已有标签

                                        if label[-1].text != label_data[j]['label']:
                                            print('★★★ Error- 创建标签失败')
                                        else:
                                            k += 1
                                            print('创建标签成功')
                                        print('--------------------')

                                        if k == 2:
                                            break
                return content

    @teststeps
    def label_list(self, content):
        """已有标签列表"""
        if self.collect.wait_check_manage_list_page():
            print('已有标签:')
            label = self.collect.label_title()  # 已有标签
            for i in range(len(label)):
                content.append(label[i].text)
                print(label[i].text)
        elif self.home.wait_check_empty_tips_page():
            print('暂无标签')

    @teststeps
    def modify_label_operation(self, content):
        """修改 标签"""
        if self.collect.wait_check_manage_list_page():
            print('------------移除/修改 标签-------------')
            label = self.collect.label_title()  # 已有标签
            print('标签：', label[-2].text)
            self.collect.open_menu(label[-2])  # 标签条目 左键长按
            self.collect.menu_item(1)  # 修改 该标签

            if self.home.wait_check_input_page():
                name = self.home.input()
                name.send_keys(r'' + content[-1])
                print('重命名为：', name.text)
                self.home.commit_button().click()  # 确定 按钮
                Toast().toast_operation("自定义标签名重复")
                print('--------------------')

            if self.collect.wait_check_manage_page():
                self.collect.open_menu(label[-2])  # 标签条目 左键长按
                self.collect.menu_item(1)  # 修改 该标签

                if self.home.wait_check_input_page():
                    item = 0
                    name = self.home.input()
                    for i in range(len(label)):
                        if label_data[i]['label'] not in content:
                            name.send_keys(r'' + label_data[i]['label'])
                            print('重命名为：', name.text)
                            item = label_data[i]['label']
                            self.home.commit_button().click()  # 确定 按钮

                            if self.collect.wait_check_manage_page():
                                print('--------------------')
                                break
                    return item

    @teststeps
    def remove_label_operation(self):
        """移除 标签"""
        if self.collect.wait_check_manage_page():
            if self.collect.wait_check_manage_list_page():
                label = self.collect.label_title()  # 已有标签
                var = label[-1].text
                self.collect.open_menu(label[-1])  # 标签条目 左键长按
                self.collect.menu_item(0)  # 移除该标签
                if Toast().find_toast("删除自定义标签成功"):
                    print('移除标签 %s 成功' % var)
                    print('--------------------')
                else:
                    print('★★★ Error- 未弹toast: 删除自定义标签成功')

                return var

    @teststeps
    def judge_operation(self, remove, modify):
        """验证 移除/修改标签 结果"""
        if self.collect.wait_check_manage_page():
            print('----------验证 移除/修改 标签 结果----------')
            if self.collect.wait_check_manage_list_page():
                item = self.collect.label_title()  # 已有标签
                for i in range(len(item)):
                    print(item[i].text)
                print('--------------------')

                if item[-1].text in remove:
                    print('★★★ Error- 移除标签失败', item[-1].text)
                if item[-1].text != modify:
                    print('★★★ Error- 重命名标签失败', item[-1].text)
                else:  # 恢复测试数据
                    self.collect.open_menu(item[-1])  # 标签条目 左键长按
                    self.collect.menu_item(0)  # 移除该标签
                    if Toast().find_toast("删除自定义标签成功"):
                        print('恢复测试数据')
                    else:
                        print('★★★ Error- 未弹toast: 删除自定义标签成功')
            elif self.home.wait_check_empty_tips_page():
                print('★★★ Error- 暂无数据')
