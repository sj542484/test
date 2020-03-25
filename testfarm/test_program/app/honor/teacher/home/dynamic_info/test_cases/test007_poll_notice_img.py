#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.toast_find import Toast


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
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(PollImg, self).run(result)

    @testcase
    def test_001_poll_img(self):
        """轮播图"""
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        if self.home.wait_check_page():  # 页面检查点
            self.assertTrue(self.home.wait_check_image_page(), '★★★ Error- 轮播图')  # 页面加载完成 检查点
            print('================轮播图================')
            button = self.home.poll_button()  # 轮播按钮
            index = random.randint(1, len(button) - 1)
            button[index].click()

            if len(button) != 3:
                print('★★★ Error -轮播图个数有误', len(button))
            else:
                print('共{}张轮播图，点击第{}张' .format(len(button),index))
            self.home.back_up_button()  # 返回首页

            print('======================================')
            self.home.poll_img()  # 点击 轮播图
            if self.home.wait_check_poll_img_page(3):  # 班级年报 页面检查点
                print('班级年报')
            self.home.back_up_button()  # 返回首页

    @testcase
    def test_002_word_book_daily_listen(self):
        """单词本 & 每日一听 提示信息"""
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        if self.home.wait_check_page():  # 页面检查点
            print('==================单词本================')
            self.home.word_icon()  # 单词本icon
            self.my_toast.toast_assert(self.name, Toast().toast_operation('请去电脑端使用单词本,移动端即将上线。'))

        if self.home.wait_check_page():  # 页面检查点
            print('================每日一听================')
            self.home.listen_icon()  # 每日一听icon
            self.my_toast.toast_assert(self.name, Toast().toast_operation('功能开发中,敬请期待!'))
