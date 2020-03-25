#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.invite_student_page import InviteStPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext


class InviteStudent(unittest.TestCase):
    """邀请学生"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.invite = InviteStPage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(InviteStudent, self).run(result)

    @testcase
    def test_invite_student(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        van = self.into_vanclass_operation()  # 进入 班级
        self.assertTrue(self.van_detail.wait_check_app_page(van), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.van_detail.wait_check_page(van), self.van_detail.van_vue_tips)
        self.assertTrue(self.van_detail.wait_check_list_page(), self.van_detail.van_list_tips)
        self.van_detail.invite_st_button()  # 邀请学生按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.invite.wait_check_page(), self.invite.invite_vue_tips)
        self.invite.vanclass_name()  # 班级名
        self.invite.vanclass_num()  # 班号
        print('---------------------------------')

        self.invite.copy_link_button()  # 复制链接
        print('复制链接:')
        # self.my_toast.toast_assert(self.name, Toast().toast_vue_operation('班级链接已复制到粘贴板'))  # 获取toast信息
        print('---------------------------------')

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.invite.wait_check_page(), self.invite.invite_vue_tips)
        self.invite.copy_no_button()  # 复制班号
        print('复制班号:')
        # self.my_toast.toast_assert(self.name, Toast().toast_vue_operation('班号已复制到粘贴板'))  # 获取toast信息
        print('---------------------------------')

        self.share_operation(van)  # 微信分享 具体操作

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.invite.wait_check_page(), self.invite.invite_vue_tips)  # 页面检查点
        self.van_detail.back_up_button()
        self.vue.app_web_switch()  # 切到apk 再切到vue
        if self.van_detail.wait_check_page(van):  # 班级详情 页面检查点
            self.van_detail.back_up_button()

    @teststeps
    def into_vanclass_operation(self):
        """进入 班级"""
        van = 0
        if self.home.wait_check_list_page():
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            if self.home.wait_check_list_page():
                name = self.home.item_detail()  # 班号+班级名
                index = random.randint(0, len(name)-1)
                van = self.home.vanclass_name(name[index].text)  # 班级名
                name[index].click()  # 进入班级
            return van
                
    @teststeps
    def share_operation(self, van):
        """分享"""
        self.assertTrue(self.invite.wait_check_page(), self.invite.invite_vue_tips)
        self.invite.share_button()  # 分享按钮

        print('分享:')
        if self.invite.wait_check_share_page():
            self.invite.wechat_friend().click()  # 微信好友
            print(' 微信好友')
            if self.invite.wait_check_share_wechat_page():  # 说明 手机安装了微信且未登录
                self.invite.wechat_back_button()

                if self.invite.wait_check_page(van):
                    self.invite.share_button()  # 分享按钮
                    if self.invite.wait_check_share_page():
                        self.invite.wechat_friends().click()  # 微信朋友圈
                        print(' 微信朋友圈')
                        if self.invite.wait_check_share_wechat_page():
                            self.invite.wechat_back_button()
                        elif self.invite.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                            self.invite.back_up_button()
            elif self.invite.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                self.invite.back_up_button()
                if self.invite.wait_check_page(van):
                    self.invite.share_button()  # 分享按钮
                    if self.invite.wait_check_share_page():
                        self.invite.wechat_friends().click()  # 微信朋友圈
                        print(' 微信朋友圈')
                        if self.invite.wait_check_share_wechat_page():
                            self.invite.wechat_back_button()
                        elif self.invite.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                            self.invite.back_up_button()
            elif self.invite.wait_check_page(van):  # 说明 手机未安装微信
                self.invite.share_button()  # 分享按钮
                if self.invite.wait_check_share_page():
                    self.invite.wechat_friends().click()  # 微信朋友圈
                    print(' 微信朋友圈')
