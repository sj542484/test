#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class QuestionBasket(unittest.TestCase):
    """题库 -- 移出题筐"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.detail = QuestionDetailPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_question_basket_remove(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                self.question.question_basket()  # 题筐按钮

                if self.basket.wait_check_page():  # 页面检查点
                    if self.basket.wait_check_list_page():  # 题筐有题
                        self.basket_operation()  # 题筐具体操作
                    elif self.home.wait_check_empty_tips_page():
                        self.home.back_up_button()  # 返回题库主界面
                        self.add_to_basket()  # 加题进题筐

                    if self.question.wait_check_page('题单'):
                        self.home.click_tab_hw()  # 返回首页
            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def add_to_basket(self):
        """加题入题筐"""
        if self.question.wait_check_page('题单'):  # 页面检查点
            print('-----------------------------')
            print('题筺为空,加题进题筐:')
            item = self.question.question_name()  # 获取
            item[0][3].click()  # 点击第一道题

            if self.detail.wait_check_page():  # 页面检查点
                if self.detail.wait_check_list_page():  # 判断是否已加载出来
                    self.detail.put_to_basket_button()  # 点击加入题筐按钮
                    if Toast().find_toast('添加题筐成功'):
                        print('添加题筐成功')
                        print('----------------------')

                    if self.detail.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回按钮

                        if self.question.wait_check_page('题单'):  # 页面检查点
                            self.question.question_basket()  # 题筐按钮

                            if self.basket.wait_check_page():  # 页面检查点
                                if self.basket.wait_check_list_page():  # 题筐有题
                                    self.basket_operation()  # 题筐具体操作

    @teststeps
    def basket_operation(self):
        """题筐具体操作"""
        print('-----------------题筐-------------------')
        self.basket.out_basket_button()  # 移出题筐按钮
        print('不选择任何题目，直接点击 <移出题筐> 按钮')
        if Toast().find_toast('请选择要移除的题目'):
            print(' 请选择要移除的题目')
            print('-----------------------')

        if self.basket.wait_check_list_page():
            self.basket.all_check_button()  # 全选按钮
            print('点击全选按钮')
            ele = self.basket.assign_button()  # 布置作业 按钮
            num = re.sub("\D", "", ele.text)  # 提取所选的题数
            print('共有%s道题目' % num)
            self.basket.out_basket_button()  # 移出题筐按扭

            if self.basket.wait_check_page():  # 页面检查点
                print('---------------------------')
                if self.home.wait_check_empty_tips_page():
                    print('全部移出题筐成功')
                elif self.basket.wait_check_list_page():
                    ele = self.basket.assign_button()  # 布置作业 按钮
                    num1 = re.sub("\D", "", ele.text)  # 提取所选的题数
                    print('★★★ Error -全部移出题筐有误', num1)

                if self.basket.wait_check_page():  # 页面检查点
                    self.home.back_up_button()  # 返回题库主界面
