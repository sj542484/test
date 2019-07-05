##!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.reset_phone_page import PhoneReset
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.test_data.reset_phone import reset_phone_data
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.reset_phone_toast import get_verify
from testfarm.test_program.utils.toast_find import Toast


class ExchangePhone(unittest.TestCase):
    """修改手机号"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.phone = PhoneReset()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_exchange_phone(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                for i in range(len(reset_phone_data)):
                    if self.user_info.wait_check_page():  # 页面检查点
                        print('-----------------------------------')
                        phone1 = self.user_info.phone()  # 获取修改前手机号
                        self.user_info.click_phone_number()  # 点击手机号条目，进入设置页面

                        if self.home.wait_check_tips_page():
                            self.home.tips_title()
                            text = self.user_info.input()  # 验证之前密码
                            text.send_keys(r'' + reset_phone_data[i]['password'])
                            self.user_info.click_positive_button()  # 确定按钮

                            if self.phone.wait_check_page():  # 手机号 修改页面
                                phone = self.phone.et_phone()
                                phone.send_keys(r'' + reset_phone_data[i]['reset'])
                                print('修改为：', phone.text)

                                self.phone.count_time()  # 获取 验证码
                                if len(reset_phone_data[i]) == 3:
                                    if Toast().find_toast(reset_phone_data[i]["toast"]):
                                        print(reset_phone_data[i]["toast"])
                                    self.home.back_up_button()  # 返回个人信息 页面
                                else:
                                    value = get_verify(reset_phone_data[i]['reset'])  # 获取验证码
                                    
                                    if i == len(reset_phone_data) - 1:
                                        self.phone.verify().send_keys('1234')
                                        self.phone.btn_certain()  # 确定按钮

                                        if Toast().find_toast('验证码验证失败'):
                                            print('验证码验证失败: 1234')

                                    self.phone.verify().send_keys(value)
                                    print('验证码:', value)
                                    self.phone.btn_certain()  # 确定按钮

                                    if self.user_info.wait_check_page():
                                        self.home.back_up_button()  # 数据更新需要刷新页面
                                        if self.user.wait_check_page():  # 页面检查点
                                            self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作
                                            if self.user_info.wait_check_page():
                                                phone2 = self.user_info.phone()   # 获取修改后的手机号
                                                if phone1 != phone2:
                                                    print('手机号修改成功')
                                                else:
                                                    print('★★★ Error - 手机号修改失败')
                            else:
                                print('未进入修改手机号页面')
                        else:
                            print('未进入 确认密码页面')
                    else:
                        print('未进入个人信息页面')
                self.user_info.back_up()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
