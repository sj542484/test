# coding=utf-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.login.test_data import phone_data, pwd_data
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.reset_phone_toast import get_verify
from utils.toast_find import Toast


class Register(unittest.TestCase):
    """注册"""

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
    def test_register(self):
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
        for i in range(len(phone_data)):
            if self.login.wait_check_page():
                self.login.register_button()  # 注册帐号 按钮
                if self.login.wait_check_register_page(5):
                    phone = self.login.input_phone()
                    code = self.login.input_code()

                    phone.send_keys(r'' + phone_data[i]['account'])  # 输入手机号

                    self.login.get_code_button().click()  # 获取验证码 按钮
                    value = get_verify(phone_data[i]['account'], 'register')  # 获取验证码

                    if Toast().find_toast('用户已经注册') or self.login.wait_check_page(3):
                        print('用户已注册', phone_data[i]['account'])
                        continue
                    else:
                        code.send_keys(value)  # 输入 验证码
                        self.login.next_button()  # 下一步 按钮

                        if self.login.wait_check_register_nick_page(3):
                            print(phone_data[i]['account'])
                            print(value)
                            print('-----------------')
                            self.login.visible_password().click()  # 显示密码

                            nick = self.login.input_nickname()  # 设置昵称
                            pwd = self.login.new_pwd()  # 设置密码
                            confirm = self.login.new_pwd_confirm()  # 密码再次确认

                            nick.send_keys(r'' + pwd_data[-1]['nick'])  # 输入昵称
                            print('昵称:', nick.text)

                            pwd.send_keys(r'' + pwd_data[-1]['password'])  # 输入密码
                            print('密码:', pwd.text)

                            confirm.send_keys(r'' + pwd_data[-1]['confirm'])  # 密码确认
                            print('密码确认:', confirm.text)

                            self.login.register_button()  # 注册 按钮
                            print('-----------------')
                            if Toast().find_toast('注册成功,请登录'):
                                print('注册成功,请登录')
                            else:
                                print('★★★ Error -注册失败')

                            break