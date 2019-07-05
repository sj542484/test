#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class QuestionFilter(unittest.TestCase):
    """筛选 -- 题单/试卷"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.question = TestBankPage()
        cls.filter = FilterPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_filter(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_test_bank()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('搜索'):  # 页面检查点
                self.paper_operation()  # 选择试卷
                self.question_menu_operation()  # 选择题单
            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def paper_operation(self):
        """选择试卷"""
        if self.question.wait_check_page('题单'):  # 页面检查点
            self.question.filter_button()  # 筛选按钮

            if self.filter.wait_check_page():  # 页面检查点
                paper = self.filter.test_paper()  # 试卷
                if GetAttribute().selected(paper) == 'false':  # 试卷
                    self.filter.click_test_paper()  # 点击 试卷

                if self.filter.wait_check_page():  # 页面检查点
                    self.filter.source_type_selected()  # 具体操作

                    name = self.filter.label_name()  # 所有标签
                    label = name[0].text  # 标签名
                    name[0].click()  # 选择一个标签
                    self.filter.commit_button()  # 确定按钮
                    print('选择的标签为:', label)

                    if not self.question.wait_check_page('试卷'):  # 页面检查点
                        print('★★★ Error- 选择标签不成功', label)

    @teststeps
    def question_menu_operation(self):
        """选择题单"""
        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.question.filter_button()  # 筛选按钮

            if self.filter.wait_check_page():  # 页面检查点
                menu = self.filter.question_menu()  # 题单
                if GetAttribute().selected(menu) == 'false':  # 题单
                    self.filter.click_question_menu()  # 点击 题单

                if self.filter.wait_check_page():  # 页面检查点
                    self.filter.source_type_selected()  # 具体操作

                    name = self.filter.label_name()  # 所有标签
                    label = name[6].text  # 标签名
                    name[6].click()  # 选择一个标签
                    self.filter.commit_button()  # 确定按钮
                    print('选择的标签为:', label)

                    if self.question.wait_check_page('搜索'):  # 页面检查点
                        self.question.filter_button()  # 筛选按钮

                        if self.filter.wait_check_page():  # 页面检查点
                            self.filter.reset_button()  # 重置按钮
                            print('点击重置按钮')
                            self.filter.commit_button()
                            if self.question.wait_check_page('题单'):  # 页面检查点
                                self.home.click_tab_hw()  # 返回首页
                    else:
                        print('★★★ Error- 选择标签不成功', label)
                        self.home.click_tab_hw()  # 返回首页

