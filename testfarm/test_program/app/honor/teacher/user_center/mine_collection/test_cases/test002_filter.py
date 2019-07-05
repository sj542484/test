#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.toast_find import Toast


class Collection(unittest.TestCase):
    """我的收藏 -- 筛选"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.collect = CollectionPage()
        cls.question = TestBankPage()
        cls.filter = FilterPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_collection_filter(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_collection()  # 点击 我的收藏
                if self.collect.wait_check_page():  # 页面检查点
                    self.collect.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():
                        self.collect.source_type_selected()  # 具体操作

                        name = self.collect.label_name()  # 所有标签
                        label = name[6].text  # 标签名
                        name[6].click()  # 选择一个标签
                        self.filter.commit_button()  # 确定按钮
                        print('选择的标签为:', label)

                        if self.collect.wait_check_page():  # 页面检查点
                            self.question.filter_button()  # 筛选按钮

                            if self.filter.wait_check_page():  # 页面检查点
                                self.filter.reset_button()  # 重置按钮
                                print('点击重置按钮')
                                self.filter.commit_button()  # 确定按钮

                                if self.collect.wait_check_page():
                                    self.home.back_up_button()  # 点击 返回按钮
                                    if self.user.wait_check_page():  # 页面检查点
                                        self.home.click_tab_hw()  # 回首页
                else:
                    print('未进入 我的收藏 页面')
            else:
                print('未进入个人中心页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
