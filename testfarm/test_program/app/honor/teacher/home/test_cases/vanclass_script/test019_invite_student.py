#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.invite_student_page import InviteStPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class InviteStudent(unittest.TestCase):
    """邀请学生"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.invite = InviteStPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_invite_student(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.GROUP)  # 进入 班级
            if self.van.wait_check_page(gv.GROUP):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.invite_st_button()  # 邀请学生按钮
                    if self.invite.wait_check_page(gv.INVITE):
                        self.invite.vanclass_name()  # 班级名
                        self.invite.vanclass_num()  # 班号
                        print('---------------------------------')

                        self.invite.copy_link_button()  # 复制链接
                        Toast().find_toast('班级链接已复制到粘贴板')
                        print('复制链接:')
                        print(' 班级链接已复制到粘贴板', '\n',
                              '---------------------------------')

                        if self.invite.wait_check_page(gv.GROUP):
                            self.invite.copy_no_button()  # 复制班号
                            Toast().find_toast('班号已复制到粘贴板')
                            print('复制班号:')
                            print(' 班号已复制到粘贴板', '\n',
                                  '---------------------------------')

                        self.share_operation()  # 分享 具体操作

                        if self.invite.wait_check_page(gv.INVITE):  # 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.GROUP):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('未进入 邀请学生页面')
                        self.home.back_up_button()
                        if self.van.wait_check_page(gv.GROUP):  # 班级详情 页面检查点
                            self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def share_operation(self):
        """分享"""
        if self.invite.wait_check_page(gv.GROUP):
            self.invite.share_button()  # 分享按钮
            print('分享:')
            if self.invite.wait_check_share_page():
                self.invite.wechat_friend().click()  # 微信好友
                print(' 微信好友')
                if self.invite.wait_check_share_wechat_page():  # 说明 手机安装了微信且未登录
                    self.invite.wechat_back_button()

                    if self.invite.wait_check_page(gv.GROUP):
                        self.invite.share_button()  # 分享按钮
                        if self.invite.wait_check_share_page():
                            self.invite.wechat_friends().click()  # 微信朋友圈
                            print(' 微信朋友圈')
                            if self.invite.wait_check_share_wechat_page():
                                self.invite.wechat_back_button()
                            elif self.invite.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                                self.invite.back_up_button()
                elif self.invite.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                    self.invite.back_up_button()
                    if self.invite.wait_check_page(gv.GROUP):
                        self.invite.share_button()  # 分享按钮
                        if self.invite.wait_check_share_page():
                            self.invite.wechat_friends().click()  # 微信朋友圈
                            print(' 微信朋友圈')
                            if self.invite.wait_check_share_wechat_page():
                                self.invite.wechat_back_button()
                            elif self.invite.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                                self.invite.back_up_button()
                elif self.invite.wait_check_page(gv.GROUP):  # 说明 手机未安装微信
                    self.invite.share_button()  # 分享按钮
                    if self.invite.wait_check_share_page():
                        self.invite.wechat_friends().click()  # 微信朋友圈
                        print(' 微信朋友圈')
