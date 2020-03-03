#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage, HelpCenter
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import setup, testcase, teardown
from utils.assert_func import ExpectingTest
from utils.screen_shot import ScreenShot
from utils.toast_find import Toast


class Help(unittest.TestCase):
    """帮助中心"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.setting = SettingPage()
        cls.help = HelpCenter()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Help, self).run(result)

    @testcase
    def test_help_center(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_setting()  # 进入设置页面

                if self.setting.wait_check_page():
                    self.setting.help_center()  # 进入帮助中心页面

                    if self.help.wait_check_page():  # 页面检查点
                        if self.help.wait_check_view_page():
                            self.help.title()  # title
                            ScreenShot().get_screenshot(self.help.img())  # 获取截图
                            self.help.view()  # text:'我的助教'

                            self.home.back_up_button()  # 点击 返回按钮
                            if self.setting.wait_check_page():  # 页面检查点
                                self.home.back_up_button()  # 点击 返回按钮
                    else:
                        print("未进入帮助中心页面")

                    if self.user.wait_check_page():  # 页面检查点
                        self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
