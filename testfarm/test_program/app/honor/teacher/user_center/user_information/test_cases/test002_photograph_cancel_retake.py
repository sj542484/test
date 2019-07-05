#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.conf.decorator import setupclass, teardown, testcase
from testfarm.test_program.utils.screen_shot import ScreenShot
from testfarm.test_program.utils.toast_find import Toast


class AvatarProfileChange(unittest.TestCase):
    """拍照修改头像 -- 修改后不保存&重拍"""

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
    def test_001_change_avatar_profile_cancel(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                if self.user_info.wait_check_page():  # 页面检查点
                    ele = self.user_info.avatar_profile()  # 头像
                    avatar = self.screen_shot.get_screenshot(ele)  # 获取登录后的头像截图

                    self.user_info.click_avatar()  # 点击头像条目，进入设置页面
                    if self.home.wait_check_tips_page():
                        self.home.tips_title()  # 弹框信息
                        self.user_info.click_photograph()  # 拍照

                        self.change_image.permission_allow()  # 拍照权限
                        if self.change_image.photo_upload_cancel():  # 上传照片具体操作
                            if self.user_info.wait_check_page():
                                ele = self.user_info.avatar_profile()  # 头像
                                if self.screen_shot.same_as_screenshot(ele, avatar):  # 获取修改取消后的头像截图
                                    print('取消修改成功')
                                else:
                                    print('取消修改失败')
                            else:
                                print('未返回个人信息页面')
                else:
                    print('未进入个人信息页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @testcase
    def test_002_change_image_retake(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                if self.user_info.wait_check_page():  # 页面检查点
                    ele = self.user_info.avatar_profile()  # 头像
                    avatar = self.screen_shot.get_screenshot(ele)  # 获取登录后的头像截图

                    self.user_info.click_avatar()  # 点击头像条目，进入设置页面
                    if self.home.wait_check_tips_page():
                        self.home.tips_title()  # 弹框信息
                        self.user_info.click_photograph()  # 拍照

                        self.change_image.permission_allow()  # 拍照权限
                        if self.change_image.photo_upload_retake():  # 页面检查点
                            if self.user_info.wait_check_page():
                                ele = self.user_info.avatar_profile()  # 头像
                                if not self.screen_shot.same_as_screenshot(ele, avatar):  # 获取修改后的头像截图, 截图不相同时
                                    print('重拍修改成功')
                                else:
                                    print('★★★ Error - 重拍修改失败')
                            else:
                                print('未返回个人信息页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
