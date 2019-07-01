#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.student.login.object_page.home_page import HomePage
from app.student.login.object_page.login_page import LoginPage
from app.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.student.user_center.object_page.change_image_page import ChangeImage
from app.student.user_center.object_page.user_Info_page import UserInfoPage
from app.student.user_center.object_page.user_center_page import UserCenterPage
from conf.decorator import setup, teardown, testcase
from utils.screen_shot import ScreenShot
from utils.toast_find import Toast


class ImageChange(unittest.TestCase):
    """拍照修改头像 -- 修改后不保存"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home = HomePage()
        cls.user_center = UserCenterPage()
        cls.user_info = UserInfoPage()
        cls.change_image = ChangeImage()
        cls.screen_shot = ScreenShot()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_change_image(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user_center.wait_check_page():  # 页面检查点
                self.user_center.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作
                if self.user_info.wait_check_page():  # 页面检查点

                    # 获取登录后的头像截图
                    # image1 = self.user_info.image()
                    # t = self.screen_shot.screenshot(image1)
                    # self.assertTrue(t)

                    self.user_info.click_image()  # 点击头像条目，进入设置页面
                    if self.home.wait_check_tips_page():
                        self.home.tips_title()  # 弹框信息
                        self.user_info.click_photograph()

                        self.change_image.pixel_permission_allow()  # 拍照权限
                        if self.change_image.photo_upload_cancel():  # 上传照片具体操作
                            if self.user_info.wait_check_page():  # 页面检查点
                                # # 获取修改后的头像截图
                                # image2 = self.user_info.image()
                                # result = self.screen_shot.same_as_screenshot(image2,t)
                                # self.assertTrue(result)
                                print('choose cancel success')
                            else:
                                print('choose cancel failed')
                        else:
                            print('模拟器不具备拍照功能')

                        self.user_info.back_up()
                    else:
                        print('未进入拍照页面')
                else:
                    print('未进入个人信息页面')
            else:
                print('未进入个人中心页面')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")
