#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.decorator import setupclass, teardown, testcase
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.screen_shot import ScreenShot
from utils.toast_find import Toast


class QrCode(unittest.TestCase):
    """修改微信二维码 -- 拍照 修改后不保存&重拍"""

    @classmethod
    @setupclass
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.change_image = ChangeImage()
        cls.screen_shot = ScreenShot()

    @teardown
    def tearDown(self):
        """返回主界面"""
        if self.user_info.wait_check_page():  # 页面检查点
            self.home.back_up_button()  # 返回按钮
            if self.user.wait_check_page():  # 页面检查点
                self.home.click_tab_hw()  # 回首页

    @testcase
    def test_001_qr_code_photo_cancel(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()   # 点击登录头像按钮，进行个人信息操作

                if self.user_info.wait_check_page():  # 页面检查点
                    ele = self.user_info.qr_code()
                    avatar = self.screen_shot.get_screenshot(ele)  # 获取二维码截图

                    self.user_info.click_qr_code()  # 点击二维码条目，进入设置页面
                    if self.home.wait_check_tips_page():
                        self.user_info.click_photograph()  # 拍照

                        self.change_image.permission_allow()  # 拍照权限
                        if self.change_image.photo_upload_cancel():
                            if self.user_info.wait_check_page():  # 页面检查点
                                ele = self.user_info.qr_code()
                                if self.screen_shot.same_as_screenshot(ele, avatar):  # 获取二维码截图, 截图不相同时
                                    print('取消修改成功')
                                else:
                                    print('★★★ Error - 取消修改失败')
                else:
                    print('未进入个人信息页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @testcase
    def test_002_qr_code_photo_retake(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                if self.user_info.wait_check_page():  # 页面检查点
                    ele = self.user_info.qr_code()
                    avatar = self.screen_shot.get_screenshot(ele)  # 获取二维码截图

                    self.user_info.click_qr_code()  # 点击二维码条目，进入设置页面
                    if self.home.wait_check_tips_page():
                        self.user_info.click_photograph()  # 拍照

                        self.change_image.permission_allow()  # 拍照权限
                        if self.change_image.photo_upload_save():
                            if self.user_info.wait_check_page():  # 页面检查点
                                ele = self.user_info.qr_code()
                                if not self.screen_shot.same_as_screenshot(ele, avatar):  # 获取二维码截图, 截图不相同时
                                    print('重拍修改成功')
                                else:
                                    print('★★★ Error - 重拍修改失败')
                else:
                    print('未进入个人信息页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
