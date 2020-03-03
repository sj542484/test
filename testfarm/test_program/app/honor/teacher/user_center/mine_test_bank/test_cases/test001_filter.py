#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from conf.decorator import setup, teardown, testcase, teststeps
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
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
    def test_mine_test_bank_filter(self):
        self.login.app_status()  # 判断APP当前状态
        """ 筛选标签展示规则：
            自定义标签：自己的自定义标签
            系统标签：是否有带系统标签的内容
        """
        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_bank()  # 点击 我的题库
                if self.mine.wait_check_page():  # 页面检查点
                    self.switch_label_mode_operation()  # 切换不同类型 题单/大题/试卷

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

    @teststeps
    def switch_label_mode_operation(self):
        """切换不同类型"""
        k = 3
        while k > 0:
            if self.mine.wait_check_page():  # 页面检查点
                self.user.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():  # 页面检查点
                    if k == 3:
                        game = self.user.game_list()  # 大题
                        if GetAttribute().selected(game) == 'false':  # 大题
                            self.user.click_game_list()  # 点击 大题
                    elif k == 2:
                        game = self.user.test_paper()  # 试卷
                        if GetAttribute().selected(game) == 'false':  # 试卷
                            self.user.click_test_paper()  # 点击 试卷
                    else:
                        game = self.user.question_menu()  # 题单
                        if GetAttribute().selected(game) == 'false':  # 题单
                            self.user.click_question_menu()  # 点击 题单

                    if self.filter.wait_check_page():  # 页面检查点
                        content = self.user.source_type_selected()  # 具体操作
                        self.user.judge_label_title(content[0], content[1])

                        if len(content[1]) > 1:
                            name = self.user.label_names()  # 所有标签
                            print('选择的标签为:', name[3].text)
                            name[3].click()  # 选择一个标签

                            if self.mine.wait_check_page():  # 页面检查点
                                self.question.filter_button()  # 筛选按钮

                        if self.filter.wait_check_page():  # 页面检查点
                            self.filter.reset_button()  # 重置按钮
                            if self.filter.wait_check_page():  # 页面检查点
                                if GetAttribute().selected(self.user.question_menu()) == 'false':  # 题单
                                    print('★★★ Error-点击重置按钮 重置失败')
                        self.filter.commit_button()  # 确定按钮

                        k -= 1
