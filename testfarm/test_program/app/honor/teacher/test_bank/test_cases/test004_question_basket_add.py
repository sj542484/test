#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_search_page import SearchPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class QuestionBasket(unittest.TestCase):
    """题库 -- 加题进题筐"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.detail = QuestionDetailPage()
        cls.search = SearchPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_question_basket_add(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                self.question.question_basket()  # 题筐按钮

                if self.basket.wait_check_page():  # 页面检查点
                    if self.basket.wait_check_list_page(5):  # 题筐有题
                        self.basket.all_check_button()  # 全选按钮
                        ele = self.basket.assign_button()  # 布置作业 按钮
                        num = re.sub("\D", "", ele.text)  # 提取所选的题数

                        if int(num) == 50:
                            print('题筐已满', num)
                            self.home.back_up_button()  # 返回按钮
                        else:
                            self.basket.assign_button().click()  # 布置作业 按钮
                            if int(num) > 10:
                                Toast().find_toast('布置作业一次不能超过10道题')  # 获取toast
                            else:
                                self.home.tips_commit()  # 温馨提示 -- 确定
                                self.home.back_up_button()  # 返回题筺主界面

                            if self.basket.wait_check_list_page():  # 题筐有题
                                self.home.back_up_button()  # 返回题库主界面
                                self.add_to_basket()  # 加题进题筐
                    elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                        self.basket.empty_text()
                        print('--------------------------------------')

                        self.home.back_up_button()  # 返回题库主界面
                        self.add_to_basket()  # 加题进题筐
            else:
                print('未进入题库页面')

            if self.question.wait_check_page('题单'):
                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def add_to_basket(self):
        """加题入题筐"""
        self.search_input_clear()  # 用于test002脚本运行失败时，恢复测试数据

        if self.question.wait_check_page('题单'):  # 页面检查点
            k = 0
            while k < 1:
                SwipeFun().swipe_vertical(0.5, 0.75, 0.25)  # 滑屏一次
                item = self.question.question_name()  # 获取 作业包
                for i in range(len(item[0])):
                    count = re.sub("\D", "", self.question.question_num(i))  # 题数
                    if int(count) < 8:
                        print('题单:', item[1][i])
                        item[0][i].click()  # 点击第X道题
                        k += 1
                        break

            if self.detail.wait_check_page():  # 页面检查点
                print('--------------题单详情页--------------')
                if self.detail.wait_check_list_page():  # 判断是否已加载出来
                    item = self.question.question_name()  # 获取 小游戏名
                    if len(item[1]) > 7:
                        length = 7
                    else:
                        length = len(item[1])

                    for j in range(length):  # 依次输出小游戏名
                        print(item[1][j])

                    self.detail.put_to_basket_button()  # 点击加入题筐按钮

                    if self.detail.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回按钮

                        if self.question.wait_check_page('题单'):  # 页面检查点
                            self.question.question_basket()  # 题筐按钮

                            if self.basket.wait_check_page():  # 页面检查点
                                if self.basket.wait_check_list_page():
                                    self.judge_basket_result(item[1])  # 题筐具体操作
                                elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                    print('★★★ Error- 加入题筐失败')

    @teststeps
    def judge_basket_result(self, name):
        """验证题筐具体操作"""
        print('--------------验证结果 -题筐--------------')
        item = self.question.question_name()  # 获取题目
        if name[-1] != item[1][0]:
            for i in range(len(item[1])):
                print(item[1][i])
            print('★★★ Error- 加入题筐失败', name[-1], item[1][0])
        else:
            print('加入题筐成功')
            check = self.basket.check_button()  # 单选按钮
            for i in range(len(name)):
                if self.get.checked(check[i]) == 'false':
                    check[i].click()
                    break

            SwipeFun().swipe_vertical(0.5, 0.75, 0.25)  # 滑屏一次
            check = self.basket.check_button()  # 单选按钮
            for j in range(len(item[1])-1):
                if self.get.checked(check[j]) == 'false':
                    check[j].click()
                    break
            self.basket.out_basket_button()  # 移出题筐按钮

        if self.basket.wait_check_page():  # 页面检查点
            self.home.back_up_button()  # 返回按钮

    @teststeps
    def search_input_clear(self):
        """清空搜索框内容"""
        if self.question.wait_check_page('题单'):  # 页面检查点
            search = self.question.search_input()
            if search.text != '搜索':
                search.click()  # 搜索框
                if self.question.wait_check_page('上传者'):
                    self.search.input_clear_button()  # 清空 按钮
                    self.search.drop_down_button().click()  # 下拉按钮

                    if self.search.judge_search_menu():
                        var = self.search.search_criteria_menu()  # 搜索条件菜单
                        self.search.choose_condition(var)
                        var[0].click()  # 选择

                    self.search.search_button()  # 搜索按钮
