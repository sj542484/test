#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.test_data.draft_data import GetVariable as gv
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as ge
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.dynamic_info.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class Homework(unittest.TestCase):
    """习题 更多按钮 -加入题筐&再次发布"""

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
        cls.basket = TestBasketPage()
        cls.info = DynamicPage()
        cls.question = TestBankPage()
        cls.van_detail = VanclassDetailPage()
        cls.tips = TipsData()
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
    def test_001_hw_add_basket(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入习题 最近动态页面
            if self.info.wait_check_app_page():  # 页面检查点
                self.vue.switch_h5()  # 切到web

                if self.info.wait_check_page():  # 页面检查点
                    if self.info.wait_check_no_hw_page():
                        print('最近习题动态页面为空')
                        self.info.back_up_button()
                        self.assertFalse(self.info.wait_check_no_hw_page(), self.info.dynamic_empty_tips)
                    else:
                        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                        self.into_hw()  # 进入 作业包
                        name = self.add_hw_operation()  # 加入题筐 具体操作

                        self.vue.app_web_switch()  # 切到apk 再切到web
                        if self.info.wait_check_page():  # 页面检查点
                            self.info.back_up_button()
                            self.judge_basket_result(name)  # 验证 加入题筐 结果

                    self.vue.switch_app()  # 切回
                    if self.question.wait_check_page('搜索'):
                        self.home.click_tab_hw()

    @teststeps
    def into_hw(self):
        """进入作业/口语列表中的该作业/口语
        """
        count = 0
        van_name = []
        name = []
        if self.info.wait_check_list_page():
            hw = self.info.hw_name()  # 作业名
            van = self.info.hw_vanclass()  # 班级名

            for i in range(len(hw)):
                print('-----------------')
                if (van[i].text != ge.VANCLASS) and ('spoken assign' not in hw[i].text):  # 班级 （近期作业中 不能进行编辑的）
                    print("进入作业:", hw[i].text, van[i].text)
                    name.append(hw[i].text)
                    van_name.append(van[i].text)
                    van[i].click()  # 进入作业
                    self.vue.app_web_switch()  # 切到apk 再切回web

                    if self.detail.wait_check_page():
                        self.detail.analysis_tab()
                        if self.detail.wait_check_hw_list_page():
                            count += 1
                            break
                        elif self.detail.wait_check_empty_tips_page():
                            self.info.back_up_button()
                            self.vue.app_web_switch()  # 切到apk 再切回web

        elif self.info.wait_check_no_hw_page():
            print('暂无数据')

        if count == 0:
            print('★★★ Error- 没有可测试的数据')
        else:
            return name[0], van_name[0]

    @teststeps
    def add_hw_operation(self):
        """加入题筐"""
        self.detail.more_button()  # 更多 按钮
        if self.detail.wait_check_more_page():
            self.detail.more_add_button()  # 加入题筐 按钮

            self.vue.app_web_switch()  # 切到apk 再切回web
            self.my_toast.toast_assert(self.name, Toast().toast_vue_operation(TipsData().add_basket_success))

            if self.detail.wait_check_page():
                self.detail.analysis_tab()  # 进入 答题分析 tab页

                if self.detail.wait_check_hw_list_page():
                    name = self.detail.game_name()
                    content = [k.text for k in name]
                    print('加入题筐 -游戏：', content)
                    self.info.back_up_button()  # 返回 最近习题动态页面
                    return content  # 游戏 名称
                elif self.detail.wait_check_empty_tips_page():
                    print('暂无数据')

                self.info.back_up_button()  # 返回 最近习题动态页面

    @teststeps
    def judge_basket_result(self, names):
        """验证题筐具体操作"""
        print('--------------验证 添加题筐 结果--------------')
        print(names)
        self.vue.switch_app()  # 切回app
        if self.home.wait_check_page():
            self.home.click_tab_test_bank()

            if self.question.wait_check_page('搜索'):
                self.question.question_basket_button()  # 题筐按钮
                self.basket.judge_add_basket_operation(names)  # 加入题筐 验证具体操作

    @testcase
    def test_002_hw_publish_again(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入习题 最近动态页面
            if self.info.wait_check_app_page():  # 页面检查点
                self.vue.switch_h5()  # 切到web

                if self.info.wait_check_page():  # 页面检查点
                    if self.info.wait_check_no_hw_page():
                        print('最近习题动态页面为空')
                        self.info.back_up_button()
                        self.assertFalse(self.info.wait_check_no_hw_page(), self.info.dynamic_empty_tips)
                    else:
                        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                        self.info.into_hw()  # 进入 作业包
                        self.vue.app_web_switch()  # 切到apk 再切回web

                        if self.detail.wait_check_page():
                            self.detail.more_button()  # 更多 按钮
                            if self.detail.wait_check_more_page():
                                self.detail.more_publish_button()  # 再次发布 按钮
                                self.vue.switch_app()  # 切到apk

                                if self.release.wait_check_release_page():  # 页面检查点
                                    print('------------------再次发布作业------------------')
                                    if self.release.wait_check_release_list_page():
                                        name = self.release.hw_name_edit()  # 作业名称 编辑框
                                        name.send_keys(gv.ASSIGN_AGAIN)  # 修改name
                                        title = name.text
                                        print(title)

                                        van = self.release.choose_class_operation()[0]  # 选择班级 学生
                                        self.release.assign_button()  # 发布作业 按钮
                                        self.release.tips_page_info()  # 提示框

                                        self.judge_result_operation(title, van)  # 验证布置结果

    @teststeps
    def judge_result_operation(self, hw_name, van):
        """验证布置结果 具体操作"""
        if self.home.wait_check_page():
            print('------------------验证布置结果------------------')
            print(hw_name, van)
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)

            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                if var == van:
                    name[i].click()  # 进入班级
                    if self.van_detail.wait_check_app_page(var):  # 页面检查点
                        self.vue.switch_h5()  # 切到web

                        if self.van_detail.wait_check_page(var):
                            if self.van_detail.wait_check_no_hw_page():
                                print('★★★ Error-班级动态为空, 布置作业失败')
                                self.assertFalse(self.van_detail.wait_check_no_hw_page(), self.van_detail.van_no_tips)
                            else:
                                self.assertTrue(self.van_detail.wait_check_list_page(), self.van_detail.van_list_tips)
                                hw = self.van_detail.hw_name()  # 作业名
                                title = self.home.vanclass_name(hw[0].text)
                                self.assertEqual(title, hw_name, '★★★ Error- 布置作业失败, {}'.format(van, title))
                                print('布置作业成功')

                            if self.van_detail.wait_check_page(van):
                                self.van_detail.back_up_button()  # 返回 主界面

                    break
