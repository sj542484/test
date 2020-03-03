#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.test_data.draft_data import GetVariable as ge
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
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
        cls.hw_detail = HwDetailPage()
        cls.van = VanclassPage()
        cls.v_hw = VanclassHwPage()

        cls.basket = TestBasketPage()
        cls.question = TestBankPage()
        cls.van = VanclassPage()
        cls.tips = TipsData()
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
    def test_001_hw_more_button_add(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        var = self.v_hw.edit_into_operation()  # 进入 班级 作业
        title = gv.HW_TITLE.format(var[1])

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        name = self.add_hw_operation()  # 加入题筐 具体操作

        self.vue.app_web_switch()  # 切到apk 再切回web
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.info.back_up_button()  # 返回 作业列表
        self.vue.app_web_switch()  # 切到apk 再切回web

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切回vue
        self.assertTrue(self.van.wait_check_page(var[1]), self.van.van_vue_tips)  # 班级详情 页面检查点
        self.van.back_up_button()  # 返回主界面

        self.vue.switch_app()  # 切到apk
        self.judge_basket_result(name)  # 验证 加入题筐 结果

        if self.question.wait_check_page():
            self.home.click_tab_hw()

    @teststeps
    def add_hw_operation(self):
        """加入题筐"""
        self.hw_detail.more_button()  # 更多 按钮
        self.assertTrue(self.hw_detail.wait_check_more_page(), self.hw_detail.more_tips)

        self.hw_detail.more_add_button()  # 加入题筐 按钮
        self.my_toast.toast_assert(self.name, Toast().toast_vue_operation('成功加入题筐'))

        self.vue.app_web_switch()  # 切到apk 再切回web
        self.assertTrue(self.hw_detail.wait_check_more_page(), self.hw_detail.more_tips)
        self.hw_detail.analysis_tab().click()  # 进入 答题分析 tab页
        if self.hw_detail.wait_check_empty_tips_page():
            self.assertTrue(self.hw_detail.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
            name = self.hw_detail.game_name()  # 游戏 名称
            content = [k.text for k in name]
            return content

    @teststeps
    def judge_basket_result(self, name):
        """验证题筐具体操作"""
        print('--------------验证添加题筐结果--------------')
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.click_tab_test_bank()
        if self.question.wait_check_page():  # 页面检查点
            self.question.question_basket()  # 题筐按钮

            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():
                    item = self.basket.question_name()  # 获取题目

                    count = 0
                    for j in range(len(name)):
                        print(name[j])
                        for i in range(len(item[1])):
                            print(item[1][i])
                            if name[j] == item[1][i]:
                                count += 1
                                break

                    self.assertFalse(count == 0, '★★★ Error- 加入题筐失败, {}'.format(item[1][0]))
                    print('加入题筐成功')

            if self.basket.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回 题库页面

    @testcase
    def test_002_hw_publish_again(self):
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

            self.info.into_hw()  # 进入 作业包
            self.vue.app_web_switch()  # 切到apk 再切回web

            self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)
            self.hw_detail.more_button()  # 更多 按钮
            self.assertTrue(self.hw_detail.wait_check_more_page(), self.hw_detail.more_tips)
            self.hw_detail.more_publish_button()  # 再次发布 按钮

            self.vue.switch_app()  # 切到apk
            self.release_hw_operation()  # 发布作业

    @teststeps
    def release_hw_operation(self):
        """发布作业 详情页"""
        print('===================================================')
        self.assertTrue(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        self.assertTrue(self.release.wait_check_release_list_page(), self.release.release_tips)
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(ge.VAN_HW_ASSIGN)  # 修改name
        assign = name.text
        print(self.release.hw_title(), ":", assign)  # 打印元素 作业名称

        print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
        self.release.hw_mode_operation()  # 作业模式 操作
        self.release.hw_vanclass_list()  # 班级列表
        choose = self.release.choose_class_operation()  # 选择班级 学生

        self.assertTrue(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        self.release.hw_adjust_order()  # 调整题目顺序

        self.assertTrue(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        self.release.hint_help_button()  # 定时提示信息
        self.my_toast.toast_assert(self.name, Toast().toast_operation(self.tips.timing_hw))

        self.release.assign_button()  # 发布作业 按钮
        self.release.tips_page_info()  # 提示框

        if Toast().find_toast(self.tips.hw_only_daily):  # 若当天布置的作业有重名，获取toast
            print(self.tips.hw_only_daily)
            self.home.back_up_button()
            if self.basket.wait_check_page():
                self.home.back_up_button()
                if self.question.wait_check_page('搜索'):  # 页面检查点  由题筐进入；else:  由布置作业按钮 进入
                    self.home.click_tab_hw()  # 返回 主界面
        else:
            if self.question.wait_check_page('搜索'):  # 页面检查点  由题筐进入；else:  由布置作业按钮 进入
                self.home.click_tab_hw()  # 返回 主界面

            self.judge_result_operation(choose[0], assign)  # 验证布置结果

    @teststeps
    def judge_result_operation(self, van, assign):
        """验证布置结果 具体操作"""
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        print('------------------验证布置结果------------------')
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
        if self.home.wait_check_list_page():
            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                print(var)
                if var == van:
                    name[i].click()  # 进入班级

                    self.assertTrue(self.van.wait_check_app_page(var), self.van.van_tips)  # 页面检查点
                    self.vue.switch_h5()  # 切到web

                    self.assertTrue(self.van.wait_check_page(var), self.van.van_vue_tips)
                    if self.van.wait_check_no_hw_page():
                        print('★★★ Error-班级动态为空, 布置作业失败')
                        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)
                    else:
                        self.assertTrue(self.van.wait_check_list_page(), self.van.van_list_tips)
                        hw = self.van.hw_name()  # 作业名
                        title = self.home.vanclass_name(hw[0].text)
                        self.assertEqual(title, assign,  '★★★ Error- 布置作业失败, {}'.format(title))
                        print('布置作业成功')

                    if self.van.wait_check_page(van):
                        self.van.back_up_button()  # 返回 主界面

                    break
