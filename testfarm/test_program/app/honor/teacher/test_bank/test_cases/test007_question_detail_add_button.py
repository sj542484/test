#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.test_bank.object_page import QuestionDetailPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class QuestionBasket(unittest.TestCase):
    """题库 -- 题单详情页 加题进题筐按钮"""

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
    def test_question_add_button(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                item = self.question.question_name()  # 获取 题目
                count = re.sub("\D", "", self.question.question_num(2))  # 题数
                print(item[1][2])
                item[0][2].click()  # 点击第X道题

                if self.detail.wait_check_page():  # 页面检查点
                    if self.basket.wait_check_list_page():  # 题筐有题
                        print('-----------------题单详情页-------------------')
                        self.detail.put_to_basket_button()  # 点击 加入题筐按钮
                        if Toast().find_toast('添加题筐成功'):
                            print('点击 加入题筐按钮')
                        if self.detail.wait_check_list_page():
                            self.detail.put_to_basket_button()  # 再次点击 加入题筐按钮

                            if Toast().find_toast('已经全部加入题筐'):
                                print('再次点击 加入题筐按钮')
                            if self.detail.wait_check_list_page():
                                self.home.back_up_button()  # 返回 题库 主界面
                                self.already_add_operation(int(count))  # 从题筐移出 具体操作

                                if self.question.wait_check_page('题单'):  # 页面检查点
                                    item = self.question.question_name()  # 获取 题目
                                    item[0][2].click()  # 点击第X道题

                                    if self.detail.wait_check_page():  # 页面检查点
                                        print('-----------------题单详情页-------------------')
                                        self.detail.put_to_basket_button()  # 点击 加入题筐按钮
                                        if Toast().find_toast('添加题筐成功'):
                                            print('再次添加题筐成功')
                                        else:
                                            print('★★★ Error- 再次添加题筐失败')
                                        if self.detail.wait_check_list_page():
                                            self.home.back_up_button()  # 返回 题库 主界面

                                            if self.question.wait_check_page('题单'):  # 页面检查点
                                                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def already_add_operation(self, var):
        """toast为: 已经加入题筐成功 时, 移出题筐中该题的具体操作"""
        if self.question.wait_check_page('题单'):  # 页面检查点
            self.question.question_basket()  # 题筐按钮

            if self.basket.wait_check_page():  # 页面检查点
                self.basket.all_check_button()  # 全选按钮
                ele = self.basket.assign_button()  # 布置作业 按钮
                num = re.sub("\D", "", ele.text)  # 提取所选的题数
                self.basket.all_check_button()  # 取消全选

                print('-----------------题筐-----------------')
                if self.basket.wait_check_list_page():  # 题筐不为空
                    name = self.basket.question_name()  # 小游戏name
                    check = self.basket.check_button()  # 单选按钮

                    if int(var) > len(check):
                        length = len(check)
                    else:
                        length = int(var)

                    for i in range(length):
                        if self.get.checked(check[i]) == 'false':
                            print(name[i].text)
                            check[i].click()

                    count = 0
                    if int(num) > 7:
                        SwipeFun().swipe_vertical(0.5, 0.75, 0.25)  # 滑屏一次
                        item = self.question.question_name()  # 获取题目
                        check = self.basket.check_button()  # 单选按钮
                        for j in range(len(check)-1):
                            if self.get.checked(check[j]) == 'false':
                                print(item[1][j])
                                count += 1
                                check[j].click()
                        print('---------------------')
                    self.basket.out_basket_button()  # 移出题筐按钮

                    if self.basket.wait_check_page():
                        num1 = 0
                        if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                            print('题筐已空')
                        elif self.basket.wait_check_list_page():
                            self.basket.all_check_button()  # 全选按钮
                            ele = self.basket.assign_button()  # 布置作业 按钮
                            num1 = re.sub("\D", "", ele.text)  # 提取所选的题数

                        if int(num1) + count + length != int(num):
                            print('★★★ Error -移出题筐题目数有误', num, int(num1) + count + length)
                        else:
                            print('题目移除成功')
                elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                    print('★★★ Error- 加入题筐失败,空白页')

                print('----------------------')
                self.home.back_up_button()  # 返回题库主界面

    # todo 验证题筐
