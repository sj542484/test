#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.user_center import TuserCenterPage
from app.honor.teacher.user_center import ChangeImage
from app.honor.teacher.user_center import UserInfoPage
from conf.decorator import setup, teardown, testcase
from utils.screen_shot import ScreenShot
from utils.toast_find import Toast


class AvatarProfileChange(unittest.TestCase):
    """相册修改头像"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.change_image = ChangeImage()
        cls.screen_shot = ScreenShot()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_change_avatar_profile_album(self):
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
                        self.user_info.click_album()  # 从相册选择

                        self.change_image.album_upload_save()  # 上传照片具体操作
                        if self.user_info.wait_check_page():
                            ele = self.user_info.avatar_profile()  # 头像
                            if not self.screen_shot.same_as_screenshot(ele, avatar):  # 获取修改后的头像截图, 截图不相同时
                                print('修改成功')
                            else:
                                print('★★★ Error - 修改失败')
                else:
                    print('未进入个人信息页面')
                self.user_info.back_up()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
