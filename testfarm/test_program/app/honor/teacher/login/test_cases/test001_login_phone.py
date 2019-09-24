# coding=utf-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.login.test_data.mine_account import phone_data
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Login(unittest.TestCase):
    """登录功能 - 手机号"""

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
    def test_login_phone(self):
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
        
        self.login_operation_phone()  # 具体操作

    @teststeps
    def login_operation_phone(self):
        """登录 操作流程 - 测试手机号"""
        if self.login.wait_check_page():
            self.login.visible_password().click()  # 显示密码
            for i in range(len(phone_data)):
                if self.login.wait_check_page():  # 页面检查点
                    phone = self.login.input_username()
                    pwd = self.login.input_password()

                    phone.click()  # 激活phone输入框
                    phone.send_keys(phone_data[i]['username'])  # 输入手机号
                    print('账号:', phone.text)

                    pwd.click()  # 激活pwd输入框
                    pwd.send_keys(phone_data[i]['password'])  # 输入密码
                    print('密码:', pwd.text)

                    self.login.login_button()  # 登录按钮
                    if len(phone_data[i]) == 3:
                        if not Toast().find_toast(phone_data[i]['assert']):  # toast判断
                            print('★★★ Error- 未获取到toast', phone_data[i]['assert'])

                        if self.login.wait_check_page():
                            print('登录失败')
                    else:
                        if self.home.wait_check_page(5):
                            print('登录成功')
                            if i != len(phone_data)-1:
                                self.set.logout_operation()
                                if self.login.wait_check_page():  # 页面检查点
                                    self.login.visible_password().click()  # 显示密码
                        elif self.login.wait_check_page(5):
                            print('登录失败')
                        elif self.login.wait_check_st_page(5):
                            print('已注册学生账号')
                            self.login.close_app()  # 关闭APP
                            self.login.launch_app()  # 重启APP
                    print('=============================================')
