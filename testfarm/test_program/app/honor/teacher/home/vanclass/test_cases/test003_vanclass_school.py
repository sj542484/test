#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.test_data.school_name_data import *
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.vue_context import VueContext


class School(unittest.TestCase):
    """学校名称 - 在校/自由老师"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.van_detail = VanclassDetailPage()
        cls.set = SettingPage()
        cls.my_toast = MyToast()
        cls.vue = VueContext()
        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(School, self).run(result)

    @testcase
    def test_001_vanclass_school_school_teacher(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        school_name = self.get_school_name()  # 获取 当前我的学校名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)
        self.van_detail.more_button()  # 右上角 更多 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_more_tips_page(), self.van_detail.more_tips)
        self.van_detail.modify_school_name()  # 学校名称 按钮
        print('===================在校老师===================')
        self.vue.app_web_switch()  # 切到apk 再切到vue

        if self.van_detail.wait_check_school_tips_page():  # 页面加载完成 检查点
            vanclass = self.van_detail.school_tips_content()
            self.van_detail.commit_button()
            self.assertEqual(vanclass, school_tea['自动化测试'])
            print('--------------------------------', '\n',
                  '在校老师没有修改学校名称的权限', '\n',
                  '学校：', school_name)

            self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)
            self.van_detail.back_up_button()  # 返回主界面
            self.vue.switch_app()
            self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
            self.set.logout_operation()  # 退出登录 操作

    @testcase
    def test_002_free_teacher_operation(self):
        """
            自由老师每个班级可以单独设置学校名称，要是这个班级没设置过，就是暂无学校的提示 电脑端可修改；
            在编老师不可修改；
        """
        print('===================自由老师===================')
        self.assertTrue(self.login.wait_check_page(), self.login.login_tips)  # 页面检查点
        self.login.login_operation(gv.FREE_TEACHER, gv.FREE_PWD)

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        print('-------------------')
        for key in free_school.keys():
            self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)
            self.home.into_vanclass_operation(key)  # 进入 班级详情页
            self.assertTrue(self.van_detail.wait_check_app_page(key), self.van_detail.van_tips)  # 页面检查点
            self.vue.switch_h5()  # 切到vue
            self.assertTrue(self.van_detail.wait_check_page(key), self.van_detail.van_vue_tips)  # 页面检查点
            print('班级：%s' % key)
            self.van_detail.more_button()  # 右上角 更多 按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue

            self.assertTrue(self.van_detail.wait_check_more_tips_page(), self.van_detail.more_school_tips)
            self.van_detail.modify_school_name()  # 学校名称 按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue

            if self.van_detail.wait_check_school_tips_page(): # 页面加载完成 检查点
                vanclass = self.van_detail.school_tips_content()
                self.van_detail.commit_button()
                self.assertEqual(vanclass, free_school[key])

                self.vue.app_web_switch()  # 切到apk 再切到vue
                self.assertTrue(self.van_detail.wait_check_page(key), self.van_detail.van_vue_tips)  # 页面检查点
                self.van_detail.back_up_button()  # 返回主界面
                self.vue.switch_app()
                print('-------------------------------- ')

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        self.set.logout_operation()  # 退出登录 操作

        self.assertTrue(self.login.wait_check_page(), self.login.login_tips)  # 页面检查点
        self.login.login_operation()

        if not self.home.wait_check_page():  # 页面检查点
            print('★★★ Error- 登录失败')

    @teststeps
    def get_school_name(self):
        """获取 当前我的学校名"""
        self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
        self.assertTrue(self.user.wait_check_page(), self.user.user_center_tips)  # 页面检查点
        self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

        self.assertTrue(self.user_info.wait_check_page(), self.user_info.user_info_tips)  # 页面检查点
        school_name = self.user_info.school().text
        self.home.back_up_button()
        self.assertTrue(self.user.wait_check_page(), self.user.user_center_tips)  # 页面检查点
        self.home.click_tab_hw()  # 返回主界面

        return school_name
