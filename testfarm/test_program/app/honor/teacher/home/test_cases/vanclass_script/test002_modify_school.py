#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class School(unittest.TestCase):
    """学校名称 - 在校/自由老师"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.van = VanclassPage()
        cls.set = SettingPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_school_diff_teacher(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.school_teacher_operation()  # 在校老师
            self.free_teacher_operation()  # 自由老师
        else:
            Toast().get_toast()  # 获取toast:
            print("未进入主界面")

    @teststeps
    def school_teacher_operation(self):
        """在校老师"""
        school = self.get_school_name()  # 获取 当前我的学校名

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_ANALY)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                print('班级：%s' % gv.VAN_ANALY)

                self.van.more_button()  # 右上角 更多 按钮
                if self.van.wait_check_tips_page():
                    self.van.modify_name(1)  # 学校名称 按钮
                    print('===================在校老师===================')
                    if not Toast().find_toast(school):
                        print('★★★ Error- 未弹 学校名称 toast')
                    else:
                        print('--------------------------------', '\n',
                              '在校老师没有修改学校名称的权限', '\n',
                              '学校：', school)

                    if self.van.wait_check_page(gv.VAN_ANALY):
                        self.home.back_up_button()  # 返回主界面

    @teststeps
    def free_teacher_operation(self):
        """
            自由老师每个班级可以单独设置学校名称，要是这个班级没设置过，就是暂无学校的提示 电脑端可修改；
            在编老师不可修改；
        """
        if self.home.wait_check_page():  # 页面检查点
            self.set.logout_operation()  # 退出登录 操作
            print('===================自由老师===================')
            if self.login.wait_check_page():  # 页面检查点
                phone = self.login.input_username()
                pwd = self.login.input_password()

                phone.click()  # 激活phone输入框
                phone.send_keys('18711111237')  # 输入手机号

                pwd.click()  # 激活pwd输入框
                pwd.send_keys('456789')  # 输入密码

                self.login.login_button()  # 登录按钮
                school = {'block': '123学校', '自动化测试': '暂无学校'}
                if self.home.wait_check_page():
                    for key in school:
                        self.home.into_vanclass_operation(key)  # 进入 班级详情页
                        if self.van.wait_check_page(key):  # 页面检查点
                            print('班级：%s' % key)

                            self.van.more_button()  # 右上角 更多 按钮
                            if self.van.wait_check_tips_page():
                                self.van.modify_name(1)  # 学校名称 按钮
                                if not Toast().find_toast(school[key]):
                                    print('★★★ Error- 未弹toast')
                                else:
                                    print('弹框信息：', school[key])
                                if self.van.wait_check_page(key):
                                    self.home.back_up_button()  # 返回主界面
                                print('-------------------------------- ')

                    if self.home.wait_check_page():  # 页面检查点
                        self.set.logout_operation()  # 退出登录 操作
                        if self.login.wait_check_page():  # 页面检查点
                            phone = self.login.input_username()
                            pwd = self.login.input_password()

                            phone.send_keys('18711111234')  # 输入手机号
                            pwd.send_keys('456789')  # 输入密码

                            self.login.login_button()  # 登录按钮
                            if not self.home.wait_check_page():  # 页面检查点
                                print('★★★ Error- 18711111234 登录失败')

    @teststeps
    def get_school_name(self):
        """获取 当前我的学校名"""
        self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
        if self.user.wait_check_page():  # 页面检查点
            self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

            if self.user_info.wait_check_page():  # 页面检查点
                school = self.user_info.school().text
                self.home.back_up_button()
                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 返回主界面

                return school
