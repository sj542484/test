#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.vue_context import VueContext


class PollImg(unittest.TestCase):
    """单词本&每日一听 提示信息"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.release = ReleasePage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(PollImg, self).run(result)

    @testcase
    def test_word_book(self):
        """单词本 提示信息"""
        self.login.app_status()  # 判断APP当前状态
        if self.home.wait_check_page():
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

            if self.van_detail.wait_check_app_page(gv.VANCLASS):
                self.vue.switch_h5()  # 切到vue
                if self.van_detail.wait_check_page(gv.VANCLASS):
                    print('==================单词本================')
                    self.van_detail.word_book()  # 单词本icon
                    self.vue.app_web_switch()  # 切到apk 再切到vue

                    if self.van_detail.wait_check_word_listen_tips_page():  # 页面加载完成 检查点
                        info = self.van_detail.word_listen_tips_content()
                        self.assertEqual(info, '请去电脑端使用单词本,移动端即将上线。')
                        self.van_detail.commit_button()
                        self.vue.app_web_switch()  # 切到apk 再切到vue

                        if self.van_detail.wait_check_page(gv.VANCLASS):
                            self.van_detail.back_up_button()
    @testcase
    def test_daily_listen(self):
        """每日一听 提示信息"""
        self.login.app_status()  # 判断APP当前状态
        if self.home.wait_check_page():
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

            if self.van_detail.wait_check_app_page(gv.VANCLASS):
                self.vue.switch_h5()  # 切到vue
                if self.van_detail.wait_check_page(gv.VANCLASS):
                    print('================每日一听================')
                    self.van_detail.daily_listen()  # 每日一听icon
                    self.vue.app_web_switch()  # 切到apk 再切到vue

                    if self.van_detail.wait_check_word_listen_tips_page():  # 页面加载完成 检查点
                        info = self.van_detail.word_listen_tips_content()
                        self.assertEqual(info, '功能开发中,敬请期待!')
                        self.van_detail.commit_button()
                        self.vue.app_web_switch()  # 切到apk 再切到vue

                        if self.van_detail.wait_check_page(gv.VANCLASS):
                            self.van_detail.back_up_button()
