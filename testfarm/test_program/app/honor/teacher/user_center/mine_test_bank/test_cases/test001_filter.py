#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.test_bank.object_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center import MineTestBankPage
from app.honor.teacher.user_center import TuserCenterPage
from conf.decorator import setup, teardown, testcase
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class MineTestBank(unittest.TestCase):
    """我的题库 -- 筛选"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.question = TestBankPage()
        cls.filter = FilterPage()
        cls.mine = MineTestBankPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test__mine_test_bank_filter(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_bank()  # 点击 我的题库
                if self.mine.wait_check_page():  # 页面检查点
                    self.user.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():  # 页面检查点
                        game = self.filter.game_list()  # 大题
                        if GetAttribute().selected(game) == 'false':  # 试卷
                            self.user.click_game_list()  # 点击 大题

                        if self.filter.wait_check_page():  # 页面检查点
                            self.user.source_type_selected()  # 具体操作

                            name = self.user.label_title()  # 所有标签
                            label = name[0].text  # 标签名
                            name[0].click()  # 选择一个标签
                            print('选择的标签为:', label)

                            if self.mine.wait_check_page():  # 页面检查点
                                self.question.filter_button()  # 筛选按钮

                                if self.filter.wait_check_page():  # 页面检查点
                                    self.filter.reset_button()  # 重置按钮
                                    print('点击重置按钮')
                                    self.filter.commit_button()  # 确定按钮

                                    if self.mine.wait_check_page():
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
