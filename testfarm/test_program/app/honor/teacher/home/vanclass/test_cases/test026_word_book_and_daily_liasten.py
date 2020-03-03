#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.toast_find import Toast
from utils.vue_context import VueContext


class PollImg(unittest.TestCase):
    """轮播图 and 单词本&每日一听 提示信息"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van = VanclassPage()
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
    def test_word_book_daily_listen(self):
        """单词本 & 每日一听 提示信息"""
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)

        print('==================单词本================')
        self.van.word_book()  # 单词本icon
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.van.wait_check_school_tips_page(), '★★★ Error- 未弹 学校名称弹窗')  # 页面加载完成 检查点
        vanclass = self.van.school_tips_content()
        self.van.commit_button()
        Toast().toast_vue_operation('请去电脑端使用单词本,移动端即将上线。')  # 获取toast

        print('================每日一听================')
        self.van.daily_listen()  # 每日一听icon
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.van.wait_check_school_tips_page(), '★★★ Error- 未弹 学校名称弹窗')  # 页面加载完成 检查点
        vanclass = self.van.school_tips_content()
        self.van.commit_button()
        Toast().toast_vue_operation('功能开发中,敬请期待!')  # 获取toast

        if self.van.wait_check_list_page():
            self.van.back_up_button()
