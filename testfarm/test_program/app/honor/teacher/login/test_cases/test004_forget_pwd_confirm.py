#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.login.test_data.forget_pwd_data import phone_data, pwd_data
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.reset_phone_toast import get_verify
from utils.toast_find import Toast


class Login(unittest.TestCase):
    """忘记密码 - 密码"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.set = SettingPage()
        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Login, self).run(result)

    @testcase
    def test_forget_pwd_password(self):
        # 判断APP当前状态
        if self.home.wait_check_page():  # 在主界面
            print('已登录')
            self.set.logout_operation()  # 退出登录
        elif self.login.wait_check_page():  # 在登录界面
            print('在登录界面')
        else:
            print('在其他页面')
            self.login.close_app()  # 关闭APP
            self.login.launch_app()  # 重启APP
            if self.home.wait_check_page():  # 在主界面
                print('已登录')
                self.set.logout_operation()  # 退出登录
            elif self.login.wait_check_page():  # 在登录界面
                print('在登录界面')
        
        self.forget_pwd_operation()  # 具体操作

    @teststeps
    def forget_pwd_operation(self):
        """ 忘记密码 具体操作"""
        if self.login.wait_check_page():
            self.login.forget_password()  # 忘记密码按钮
            if self.login.wait_check_forget_page():
                phone = self.login.input_phone()
                code = self.login.input_code()

                phone.send_keys(phone_data[-1]['account'])  # 输入手机号
                print('账号:', phone.text)

                self.login.get_code_button().click()  # 点击 获取验证码 按钮
                value = get_verify(phone_data[-1]['account'], 'resetPassword')  # 获取验证码
                code.send_keys(value)  # 输入 验证码
                print(value)

                self.login.next_button()  # 下一步 按钮

                if self.login.wait_check_reset_page():
                    self.login.visible_password().click()  # 显示密码
                    for i in range(len(pwd_data)):
                        print('--------------------------------------')
                        pwd = self.login.new_pwd()  # 设置密码
                        confirm = self.login.new_pwd_confirm()  # 密码再次确认

                        pwd.send_keys(pwd_data[i]['password'])  # 输入密码
                        confirm.send_keys(pwd_data[i]['confirm'])  # 再次输入密码

                        print('新密码:', pwd.text)
                        print('确认密码:', confirm.text)

                        self.login.reset_button()  # 重置 按钮

                        print('--------------------')
                        if len(pwd_data[i]) == 3:
                            if pwd_data[i]['assert'] != '' and not Toast().find_toast(pwd_data[i]['assert']):
                                print('★★★ Error- 未获取到toast:', pwd_data[i]['assert'])
                        else:
                            if Toast().find_toast('修改成功,请登录'):
                                print('修改成功,请登录')
                            else:
                                print('★★★ Error -修改失败')
