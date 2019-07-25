# coding=utf-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.login.test_data import phone_data, nick_data
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.reset_phone_toast import get_verify
from utils.toast_find import Toast


class Register(unittest.TestCase):
    """注册 - 昵称"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.set = SettingPage()

    @classmethod
    @teardown
    def tearDown(cls):
        """"""
        pass

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
        if self.login.wait_check_page():
            index = 0
            for i in range(len(phone_data)):
                if self.login.wait_check_page():
                    print('========================================')
                    self.login.register_button()  # 注册帐号 按钮

                    if self.login.wait_check_register_page(3):
                        phone = self.login.input_phone()
                        code = self.login.input_code()

                        phone.click()  # 激活phone输入框
                        phone.send_keys(r'' + phone_data[i]['account'])  # 输入手机号
                        account = phone.text

                        self.login.get_code_button().click()  # 获取验证码 按钮
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
                                print(value)

                                nick = self.login.input_nickname()  # 设置昵称
                                pwd = self.login.new_pwd()  # 设置密码
                                confirm = self.login.new_pwd_confirm()  # 密码再次确认


                                print('--------填写注册信息---------')

                                for j in range(index, len(nick_data)):
                                    nick.send_keys(r'' + nick_data[j]['nick'])  # 输入昵称
                                    print('昵称:', nick.text)

                                    print('-----------------------')
                                    pwd.send_keys(r'' + nick_data[j]['password'])  # 输入密码
                                    print('密码:', pwd.text)

                                    confirm.send_keys(r'' + nick_data[j]['confirm'])  # 密码确认
                                    print('密码确认:', confirm.text)

                                    self.login.register_button()  # 注册 按钮
                                    if len(nick_data[j]) == 4:
                                        if Toast().find_toast(nick_data[j]['assert']):
                                            print(nick_data[j]['assert'])
                                    else:
                                        if self.login.wait_check_page(5):
                                            if Toast().find_toast('注册成功,请登录'):
                                                print('注册成功,请登录')
                                            else:
                                                print('★★★ Error -未弹toast：注册成功，请登录')
                                            index = j
                                            break
                                        else:
                                            self.home.page_source()

                            if index == len(nick_data) - 1:
                                break
