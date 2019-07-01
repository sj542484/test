# coding=utf-8
import time
import unittest

from app.student.login.object_page.home_page import HomePage
from app.student.login.object_page.login_page import LoginPage
from app.student.login.test_data.register_data import phone_data, pwd_data
from app.student.user_center.object_page.user_center_page import Setting
from conf.decorator import setup, teardown, testcase, teststeps
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast


class Register(unittest.TestCase):
    """注册"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.set = Setting()

    @classmethod
    @teardown
    def tearDown(cls):
        """"""
        pass

    @testcase
    def test_register(self):
        # 判断APP当前状态
        if self.home.wait_check_home_page():  # 在主界面
            print('已登录')
            self.set.logout_operate()  # 退出登录
        elif self.login.wait_check_page():  # 在登录界面
            print('在登录界面')
        else:
            print('在其他页面')
            self.login.close_app()  # 关闭APP
            self.login.launch_app()  # 重启APP
            if self.home.wait_check_home_page():  # 在主界面
                print('已登录')
                self.set.logout_operate()  # 退出登录
            elif self.login.wait_check_page():  # 在登录界面
                print('在登录界面')
        
        self.register_operate()  # 具体操作

    @teststeps
    def register_operate(self):
        """ 注册 具体操作"""
        for i in range(3):
            if self.login.wait_check_page():
                self.login.register_button()  # 注册帐号 按钮
                if self.login.wait_check_register_page():
                    phone = self.login.input_phone()
                    loc = self.home.get_element_location(self.login.protocol())
                    self.home.driver.tap([(loc[0] + 330, loc[1] + 10), ])
                    if self.login.wait_check_protocol_content_page():
                        self.home.screen_swipe_up(0.5, 0.8, 0.3, 1000)
                        self.home.screen_swipe_down(0.5, 0.4, 0.8, 1000)
                        self.login.switch_tab().click()
                        if self.login.wait_check_switch_page():
                            self.login.close_web_tab_btn().click()
                            if self.login.wait_check_register_page():
                                pass

                    phone.click()  # 激活phone输入框
                    user_phone = phone_data[-1]['account']
                    phone.send_keys(user_phone)  # 输入手机号
                    if i == 0:
                        value = self.login.verification_code_operate(user_phone, 'register')
                    else:
                        value = verify_find(user_phone, 'register')  # 获取验证码

                    if Toast().find_toast('用户已经注册') or self.login.wait_check_page():
                        print('该账号已注册！')
                        continue
                    else:
                        self.login.send_code_operate(value)
                        if self.login.wait_check_register_nick_page():
                            print(phone_data[i]['account'])
                            print('-----------------')
                            nick = self.login.input_nickname()  # 设置昵称
                            pwd = self.login.new_pwd()  # 设置密码
                            confirm = self.login.new_pwd_confirm()  # 密码再次确认

                            nick.send_keys(pwd_data[-1]['nick'])  # 输入昵称
                            print('昵称:', pwd_data[-1]['nick'])

                            pwd.send_keys(pwd_data[-1]['password'])  # 输入密码
                            print('密码:', pwd_data[-1]['password'])

                            confirm.send_keys(pwd_data[-1]['confirm'])  # 密码确认
                            print('密码确认:', pwd_data[-1]['confirm'])

                            self.login.register_button()  # 注册 按钮
                            print('-----------------')
                            if Toast().find_toast('注册成功,请登录'):
                                print('注册成功,请登录')
                            else:
                                print('★★★ Error -注册失败')

                            break
