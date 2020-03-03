#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.dynamic_info.test_data.draft_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class Homework(unittest.TestCase):
    """习题 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.detail = HwDetailPage()
        cls.info = DynamicPage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切回apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Homework, self).run(result)

    @testcase
    def test_001_hw_delete(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.hw_icon()  # 进入习题 最近动态页面

        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        if self.info.wait_check_no_hw_page():
            print('最近习题动态页面为空')
            self.info.back_up_button()  # 返回主界面
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        else:
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            var = self.info.into_hw()  # 进入 作业包
            self.vue.app_web_switch()  # 切到apk 再切回web
            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)

            self.detail.delete_commit_operation()  # 删除 具体操作
            self.my_toast.toast_assert(self.name, Toast().toast_vue_operation(TipsData().delete_success))

            self.judge_delete_result(var[0], var[1])  # 验证 删除结果
            if self.info.wait_check_page():  # 页面检查点
                self.info.back_up_button()  # 返回主界面

        self.vue.switch_app()  # 切换apk

    @teststeps
    def judge_delete_result(self, var, van_class):
        """验证 删除 结果"""
        self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        self.info.swipe_vertical_web(0.5, 0.2, 0.8)
        if self.info.wait_check_no_hw_page():
            print('暂无作业包，删除成功')
        else:
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            print('--------------验证 删除 结果--------------')
            name = self.info.hw_name()  # 作业name
            van = self.info.hw_vanclass()  # 班级

            count = 0
            for i in range(len(name)):
                if name[i].text == var:
                    if van[i].text == van_class:
                        count += 1
                        break

            self.assertTrue(count == 0, '★★★ Error -删除失败, {}'.format(var, van_class))
            print('删除成功')

        if self.info.wait_check_page():
            self.info.back_up_button()  # 返回主界面

    @testcase
    def test_002_hw_edit(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.login.app_status_no_check()  # 判断APP当前状态

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.hw_icon()  # 进入习题 最近动态页面
        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点

        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        if self.info.wait_check_no_hw_page():
            print('暂无作业包')
            self.info.back_up_button()
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        else:
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            var = self.info.into_hw()[0]  # 进入 作业包
            self.vue.app_web_switch()  # 切到apk 再切回web

            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
            self.detail.more_button()  # 更多 按钮
            self.assertTrue(self.detail.wait_check_more_page(), self.detail.more_tips)
            self.detail.more_edit_button()  # 编辑按钮

            result = self.edit_hw_operation()  # 编辑 具体操作
            self.judge_edit_result(var, result)  # 保存编辑 验证 结果

    @teststeps
    def edit_hw_operation(self):
        """编辑作业 详情页"""
        self.info.tips_content_commit(5)  # 温馨提示 页面

        self.vue.switch_app()  # 切回app
        self.assertTrue(self.detail.wait_check_edit_page(), self.detail.edit_tips)
        self.assertTrue(self.release.wait_check_release_list_page(), self.detail.edit_list_tips)

        print('-------------------编辑作业 详情页-------------------')
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(gv.HW_TEST)  # 修改name
        var = name.text
        print(self.release.hw_title(), ":", var)  # 打印元素 作业名称

        print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
        self.release.hw_mode_operation('free')  # 作业模式 操作
        self.release.hw_vanclass_list()  # 班级列表
        choose = self.release.choose_class_operation()  # 选择班级 学生

        self.assertTrue(self.release.wait_check_release_list_page(), self.detail.edit_list_tips)
        self.release.hw_adjust_order()  # 调整题目顺序

        self.assertTrue(self.release.wait_check_release_list_page(), self.detail.edit_list_tips)
        self.detail.assign_button()  # 发布作业 按钮
        self.my_toast.toast_assert(self.name, Toast().toast_operation(TipsData().hw_success))

        return var, choose

    @teststeps
    def judge_edit_result(self, var, result):
        """验证 编辑 结果"""
        print('--------------验证 编辑 结果--------------')
        self.vue.switch_app()  # 切回apk
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.hw_icon()  # 进入习题 最近动态页面
        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点

        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)

        name = self.info.hw_name()  # 作业name
        van = self.info.hw_vanclass()  # 班级
        count = 0
        for i in range(len(name)):
            if name[i].text == result[0]:
                if van[i].text == result[1]:
                    count += 1
                    print('编辑保存成功')
                    name[i].click()

                    self.vue.app_web_switch()  # 切到apk 再切回web
                    self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)

                    print('-------------恢复测试数据-------------')
                    self.detail.more_button()  # 更多 按钮
                    self.assertTrue(self.detail.wait_check_more_page(), self.detail.more_tips)
                    self.detail.more_edit_button()  # 编辑按钮

                    if self.detail.wait_check_tips_page():  # 温馨提示 页面
                        self.detail.commit_button()  # 确定 按钮

                    self.vue.switch_app()  # 切回app
                    self.assertTrue(self.detail.wait_check_edit_page(), self.detail.edit_tips)
                    self.assertTrue(self.release.wait_check_release_list_page(), self.detail.edit_list_tips)
                    self.release.hw_name_edit().send_keys(var)  # 作业名称 编辑框
                    self.release.hw_mode_free().click()  # 修改 作业模式 操作

                    SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                    self.release.choose_class_operation()  # 取消选择班级
                    self.detail.assign_button()  # 发布作业 按钮
                    
                    break

        self.assertTrue(count == 0, '★★★ Error -作业编辑失败, {}'.format(var, result))

        if self.info.wait_check_list_page():
            self.info.back_up_button()  # 返回主界面
