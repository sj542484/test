#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from testfarm.test_program.app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class VanclassHw(unittest.TestCase):
    """本班作业 - 排行榜"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.homework = Homework()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_homework_ranking(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.login.enter_user_info_page()  # 由 主界面 进入个人信息页
            if UserInfoPage().wait_check_page():
                nickname = UserInfoPage().nickname()  # 获取昵称
                self.homework.back_up_button()  # 返回个人中心页面
                if UserCenterPage().wait_check_page():
                    self.home.click_tab_hw()  # 进入主界面

                    if self.home.wait_check_home_page():  # 页面检查点
                        self.home.click_test_vanclass()  # 班级tab
                        if self.van.wait_check_page():  # 页面检查点

                            van = self.van.vanclass_name()  # 班级名称
                            for i in range(len(van)):
                                if van[i].text == gv.CLASS_NAME:
                                    van[i].click()  # 进入班级详情页
                                    break
                            if self.van.wait_check_vanclass_page(gv.CLASS_NAME):  # 页面检查点

                                self.van.vanclass_hw()  # 点击 本班作业 tab
                                if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                                    print('%s 本班作业:' % gv.CLASS_NAME)
                                    if self.van.empty_tips():
                                        print('暂无数据')
                                    else:
                                        all_hw = self.detail.all_tab()  # 全部 tab
                                        if self.detail.selected(all_hw) is False:
                                            print('★★★ Error- 未默认在 全部页面')
                                        else:
                                            print('--------------全部tab-------------------')
                                            if self.van.empty_tips():
                                                print('暂无数据')
                                            else:
                                                self.hw_operate(nickname)  # 具体操作

                                        self.home.click_back_up_button()  # 返回 本班作业页面
                                        if self.detail.wait_check_page(gv.HW_NAME):  # 页面检查点
                                            self.home.click_back_up_button()  # 返回 班级详情页面
                                        else:
                                            print('未返回 本班作业页面')

                                    if self.detail.wait_check_page(gv.VAN_LIST):  # 页面检查点
                                        self.home.click_back_up_button()  # 返回 班级
                                        if self.van.wait_check_page():  # 班级 页面检查点
                                            self.home.click_tab_hw()  # 返回主界面
                                else:
                                    print('未进入班级 -本班作业tab')
                                    self.home.click_back_up_button()
                                    if self.van.wait_check_page():  # 班级 页面检查点
                                        self.home.click_tab_hw()  # 返回主界面
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def hw_operate(self, nickname):
        """作业列表"""
        name = self.detail.hw_name()  # 作业name
        for i in range(len(name)):
            if name[i].text == gv.HW_NAME:
                print('作业：', gv.HW_NAME)
                name[i].click()  # 进入作业
                break

        if self.detail.wait_check_page(gv.HW_NAME):  # 页面检查点
            print('---------------------------------')
            print('第0道小游戏:')
            self.homework.ranking(0, nickname)
        else:
            print('未进入作业 %s 页面' % gv.HW_NAME)
            self.home.click_back_up_button()
