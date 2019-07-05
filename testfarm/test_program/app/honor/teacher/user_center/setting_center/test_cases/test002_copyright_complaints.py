# coding=utf-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage, Copyright
from testfarm.test_program.app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class CopyrightComplaints(unittest.TestCase):
    """版权申诉"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.setting = SettingPage()
        cls.privacy = Copyright()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_copyright_complaints(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_setting()  # 进入设置页面

                if self.setting.wait_check_page():
                    self.setting.copyright_complaints()  # 进入版权申诉页面

                    if self.privacy.wait_check_page():  # 页面检查点
                        value = []  # 条款内容
                        for i in range(3):
                            if self.privacy.wait_check_view_page():  # 页面检查点
                                self.privacy.content_view(value)  # 条款内容
                                SwipeFun().swipe_vertical(0.5, 0.8, 0.2)

                        if self.privacy.wait_check_page():  # 页面检查点
                            print('下拉一次')
                            SwipeFun().swipe_vertical(0.5, 0.2, 0.9)
                            if self.privacy.wait_check_page():  # 页面检查点
                                self.setting.back_up_button()

                                if self.setting.wait_check_page():  # 页面检查点
                                    print('success')
                                else:
                                    print('failed')

                                self.home.back_up_button()  # 点击 返回按钮
                        else:
                            print('未进入 版权申诉 页面')

                    if self.user.wait_check_page():  # 页面检查点
                        self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
