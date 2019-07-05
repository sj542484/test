# coding=utf-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage, HelpCenter
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.toast_find import Toast


class Help(unittest.TestCase):
    """帮助中心"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.setting = SettingPage()
        cls.help = HelpCenter()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_help_center(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_setting()  # 进入设置页面

                if self.setting.wait_check_page():
                    self.setting.help_center()  # 进入帮助中心页面

                    if self.help.wait_check_page():  # 页面检查点
                        if self.help.wait_check_view_page():
                            self.help.view()  # text:'我的助教'
                            self.home.back_up_button()  # 点击 返回按钮

                            if self.setting.wait_check_page():  # 页面检查点
                                self.home.back_up_button()  # 点击 返回按钮
                    else:
                        print("未进入帮助中心页面")

                    if self.user.wait_check_page():  # 页面检查点
                        self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

