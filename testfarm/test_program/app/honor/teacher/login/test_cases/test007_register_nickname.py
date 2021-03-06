#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest
import random

from conf.base_page import BasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.login.test_data.register_data import nick_data
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.reset_phone_toast import get_verify
from utils.toast_find import Toast


class Register(unittest.TestCase):
    """注册 - 昵称"""

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
        super(Register, self).run(self.ass_result)

    @testcase
    def test_register_nickname(self):
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

        self.register_operation()  # 具体操作

    @teststeps
    def register_operation(self):
        """ 注册 具体操作"""
        data = []
        if self.login.wait_check_page():
            index = 0
            for i in range(len(nick_data)):
                if self.login.wait_check_page():
                    print('========================================')
                    self.login.register_button()  # 注册帐号 按钮

                    if self.login.wait_check_register_page(3):
                        phone = self.login.input_phone()
                        code = self.login.input_code()

                        phone.click()  # 激活phone输入框
                        account = ('185243' + str(i) + str(random.randint(1000, 9999)))
                        phone.send_keys(account)  # 输入手机号
                        account = phone.text

                        self.login.get_code_button()  # 获取验证码 按钮
                        value = get_verify(account, 'register')  # 获取验证码

                        if Toast().find_toast('用户已经注册') or self.login.wait_check_page(3):
                            print('用户已注册', account)
                            continue
                        else:
                            code.click()  # 激活 验证码输入框
                            code.send_keys(value)  # 输入 验证码
                            self.login.next_button()  # 下一步 按钮

                            if self.login.wait_check_register_nick_page(3):
                                self.login.visible_password().click()  # 显示密码
                                print('账号:', account)
                                data.append(account)
                                print(value)

                                nick = self.login.input_nickname()  # 设置昵称
                                pwd = self.login.new_pwd()  # 设置密码
                                confirm = self.login.new_pwd_confirm()  # 密码再次确认

                                print('--------填写注册信息---------')
                                for j in range(index, len(nick_data)):
                                    nick.send_keys(nick_data[j]['nick'])  # 输入昵称
                                    print('昵称:', nick.text)

                                    print('-----------------------')
                                    pwd.send_keys(nick_data[j]['password'])  # 输入密码
                                    print('密码:', pwd.text)

                                    confirm.send_keys(nick_data[j]['confirm'])  # 密码确认
                                    print('密码确认:', confirm.text)

                                    self.login.register_button()  # 注册 按钮
                                    if len(nick_data[j]) == 4:
                                        if Toast().find_toast(nick_data[j]['assert']):
                                            print(nick_data[j]['assert'])
                                    else:
                                        Toast().toast_operation('注册成功,请登录')
                                        if self.login.wait_check_page(7):
                                            index = j + 1
                                            break

                            if index == len(nick_data) - 1:
                                break
        return data

