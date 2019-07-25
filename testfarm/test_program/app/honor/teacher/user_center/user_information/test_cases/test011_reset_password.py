##!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.user_center import TuserCenterPage
from app.honor.teacher.user_center import PwdReset
from app.honor.teacher.user_center import UserInfoPage
from app.honor.teacher.user_center import reset_pwd
from conf.decorator import setup, teardown, testcase
from utils.toast_find import Toast


class ExchangePhone(unittest.TestCase):
    """更改密码"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.pwd = PwdReset()

    @classmethod
    @teardown
    def tearDown(cls):
        """关闭应用"""
        pass

    @testcase
    def test_change_password(self):
        """修改密码 -- 正常流程"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                if self.user_info.wait_check_page():  # 页面检查点
                    self.user_info.click_password()  # 点击修改密码
                    if self.pwd.wait_check_page():  # 页面检查点
                        self.pwd.visible_pwd()  # 点击 显示密码

                    for i in range(len(reset_pwd)):
                        if self.pwd.wait_check_page():  # 页面检查点
                            # 原密码
                            old = self.pwd.pwd_origin()
                            old.send_keys(r'' + reset_pwd[i]['old'])

                            # 输入新的密码
                            new = self.pwd.pwd_new()
                            new.send_keys(r'' + reset_pwd[i]['new'])

                            # 再次输入密码
                            confirm = self.pwd.pwd_confirm()
                            confirm.send_keys(r'' + reset_pwd[i]['commit'])

                            print('新密码:', new.text)
                            print('确认密码:', confirm.text)

                            self.pwd.confirm_button()  # 点击完成按钮
                            if len(reset_pwd[i]) == 4:
                                if not Toast().find_toast(reset_pwd[i]['assert']):  # 页面检查点
                                    print('★★★ Error- 未获取到toast:', reset_pwd[i]['assert'])
                            else:
                                if self.user_info.wait_check_page(10):  # 页面检查点
                                    print('密码修改成功')
                                    if i != len(reset_pwd) - 1:
                                        self.user_info.click_password()  # 点击修改密码
                                        if self.pwd.wait_check_page():  # 页面检查点
                                            self.pwd.visible_pwd()  # 点击 显示密码
                                else:
                                    print('★★★ Error - 密码修改失败')

                            print('---------------------------------')
                else:
                    print('未进入个人信息页面')

                self.user_info.back_up()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
