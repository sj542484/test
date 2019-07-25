#!/usr/bin/env python
# encoding:UTF-8
import random
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.user_center import TuserCenterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page import FilterPage
from conf.decorator import setup, teardown, testcase
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class QuestionFilter(unittest.TestCase):
    """筛选 -- 大题"""

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
    def test_filter_choose(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_test_bank()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('搜索'):  # 页面检查点
                self.question.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():  # 页面检查点
                    if GetAttribute().selected(self.filter.game_list()) == 'false':  # 大题
                        self.filter.click_game_list()  # 选择大题

                        if self.filter.wait_check_page():  # 页面检查点
                            self.filter.source_type_selected()  # 具体操作

                            name = self.filter.label_name()  # 所有标签
                            label = name[5].text  # 标签名
                            name[5].click()  # 选择一个标签
                            self.filter.commit_button()  # 确定按钮
                            print('选择的标签为:', label)

                            if self.question.wait_check_game_type_page():  # 页面检查点
                                name = self.question.question_name()
                                mode = self.question.question_type(random.randint(0, len(name)-1))  # 大题类型
                                if mode != label:
                                    print('★★★ Error- 筛选出的大题类型与选择的不一致', mode, label)

                                self.question.filter_button()  # 筛选按钮
                                if self.filter.wait_check_page():  # 页面检查点
                                    self.filter.reset_button()  # 重置按钮
                                    print('点击重置按钮')

                                    if self.filter.wait_check_page():  # 页面检查点
                                        self.filter.commit_button()
                                        if self.question.wait_check_page('题单'):  # 页面检查点
                                            self.home.click_tab_hw()  # 返回首页
                            else:
                                print('★★★ Error- 选择标签不成功', label)
                                self.home.click_tab_hw()  # 返回首页
            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
