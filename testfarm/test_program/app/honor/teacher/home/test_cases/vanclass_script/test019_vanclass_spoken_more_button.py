#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Spoken(unittest.TestCase):
    """作业 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.hw = HwDetailPage()
        cls.speak = SpokenDetailPage()
        cls.van = VanclassPage()
        cls.detail = VanclassDetailPage()
        cls.release = ReleasePage()
        cls.info = DynamicPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_spoken_more_button(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.detail.edit_into_operation(gv.VANCLASS, gv.HW_TITLE, self.van.vanclass_hw, gv.SPOKEN)  # 进入 班级作业

            if self.speak.wait_check_page():  # 作业游戏list 页面检查点
                self.hw.delete_cancel_operation()  # 取消删除 具体操作

            if self.speak.wait_check_page():  # 页面检查点
                self.hw.more_button()  # 更多 按钮
                if self.hw.wait_check_more_page():
                    self.hw.edit_delete_button(0)  # 编辑按钮
                    van = self.edit_hw_operation()  # 编辑 具体操作

                    self.judge_result(van)  # 保存编辑,取消删除时，验证结果；成功则进行删除操作
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def edit_hw_operation(self):
        """编辑作业 详情页"""
        self.home.tips_content_commit(5)  # 温馨提示 页面

        if self.hw.wait_check_edit_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                print('-------------------编辑作业 详情页-------------------')
                name = self.release.hw_name_edit()  # 作业名称 编辑框
                var = gv.SPOKEN_EDIT
                name.send_keys(var)  # 修改name
                print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

                print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
                self.release.hw_mode_operation('free')  # 作业模式 操作
                self.release.hw_vanclass_list()  # 班级列表
                choose = self.release.choose_class_operation()  # 选择班级 学生

                if self.release.wait_check_release_page():  # 页面检查点
                    self.release.hw_adjust_order()  # 调整题目顺序

                    if self.release.wait_check_release_page():  # 页面检查点
                        self.hw.assign_button()  # 发布作业 按钮
                        Toast().toast_operation(gv.hw_success)  # 获取toast信息

                        return var, choose

    @teststeps
    def judge_result(self, vanclass):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入作业 最近动态页面

            if self.info.wait_check_hw_page():  # 页面检查点
                if self.info.wait_check_list_page():
                    print('--------------验证 编辑/取消删除 结果--------------')
                    name = self.info.hw_name()  # 作业name
                    van = self.info.hw_vanclass()  # 班级
                    if name[0].text == vanclass[0]:
                        if van[0].text != vanclass[1][0]:
                            print('★★★ Error- 作业编辑不成功', van[0].text, vanclass[1][0])

                            if self.info.wait_check_list_page():
                                self.home.back_up_button()  # 返回主界面
                        else:  # 编辑保存成功, 执行删除操作
                            print('编辑保存成功')
                            self.delete_commit_operation(name[0], vanclass)  # 删除 具体操作
                    else:
                        print('★★★ Error- 取消删除失败')
                elif self.detail.wait_check_empty_tips_page():
                    print('★★★ Error- 取消删除失败')

    @teststeps
    def delete_commit_operation(self, hw, vanclass):
        """删除作业 具体操作"""
        print('---------------------删除作业---------------------')
        hw.click()
        if self.speak.wait_check_page():
            self.hw.more_button()  # 更多 按钮
            if self.hw.wait_check_more_page():
                self.hw.edit_delete_button(1)  # 删除按钮

                if self.hw.wait_check_tips_page():
                    self.home.commit_button().click()  # 确定按钮
                    print('确定删除')

                    if self.info.wait_check_hw_page():  # 页面检查点
                        SwipeFun().swipe_vertical(0.5, 0.2, 0.8)
                        if self.info.wait_check_list_page():
                            print('--------------验证 删除 结果--------------')
                            name = self.info.hw_name()  # 作业name
                            van = self.info.hw_vanclass()  # 班级
                            if name[0].text == vanclass[0]:
                                if van[0].text == vanclass[1][0]:
                                    print('★★★ Error- 作业删除不成功', van[0].text, vanclass[1][0])
                                else:  # 删除成功
                                    print('删除成功')
                            else:
                                print('删除成功')
                        elif self.detail.wait_check_empty_tips_page():
                            print('删除成功')

                        if self.info.wait_check_list_page():
                            self.home.back_up_button()  # 返回主界面
