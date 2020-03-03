#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import time
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_search_page import SearchPage
from app.honor.teacher.test_bank.test_data.tips_data import TipsData
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
        cls.basket = TestBasketPage()
        cls.detail = QuestionDetailPage()
        cls.search = SearchPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_001_question_basket_add(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page():  # 页面检查点
                self.question.question_basket()  # 题筐按钮

                if self.basket.wait_check_page():  # 页面检查点
                    if self.basket.wait_check_list_page():  # 题筐有题
                        self.basket.all_check_button()  # 全选按钮
                        ele = self.basket.assign_button()  # 布置作业 按钮
                        num = re.sub("\D", "", ele.text)  # 提取所选的题数

                        if int(num) == 50:
                            print('题筐已满', num)
                            self.basket.out_basket_button()  # 移出题筐按钮
                            if self.basket.wait_check_list_page():  # 题筐有题
                                self.home.back_up_button()  # 返回按钮
                        else:
                            if int(num) > 10:
                                self.basket.assign_button().click()  # 布置作业 按钮
                                Toast().toast_operation('布置作业一次不能超过10道题')  # 获取toast
                                print('------------------------------------------------')
                    elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                        self.basket.empty_text()
                        print('--------------------------------------')

                    self.home.back_up_button()  # 返回题库主界面
                    self.add_to_basket()  # 加题进题筐
            else:
                print('未进入题库页面')

            if self.question.wait_check_page():
                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def add_to_basket(self):
        """加题入题筐"""
        self.search_input_clear()
        if self.question.wait_check_page():  # 页面检查点
            k = 0
            while k < 1:
                SwipeFun().swipe_vertical(0.5, 0.75, 0.25)  # 滑屏一次
                if self.question.wait_check_page():  # 页面检查点
                    item = self.question.question_name()  # 获取 作业包
                    for i in range(len(item[0])):
                        count = re.sub("\D", "", self.question.question_num(i))  # 题数

                        if int(count) < 20:
                            print('题单:', item[1][i])
                            item[0][i].click()  # 点击第X道题
                            k += 1
                            break

            if self.detail.wait_check_page():  # 页面检查点
                print('---------------------题单详情页---------------------')
                SwipeFun().swipe_vertical(0.5, 0.95, 0.1)  # 滑屏一次
                if self.detail.wait_check_list_page():  # 判断是否已加载出来
                    item = self.question.question_name()[1]  # 获取 小游戏名
                    print(item)  # 依次输出小游戏名
                    self.detail.all_check_button()  # 全选按钮
                    if self.basket.wait_check_list_page():
                        self.detail.put_to_basket_button()  # 点击加入题筐按钮
                        Toast().toast_operation(TipsData().add_basket)

                        if self.detail.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回按钮
                            if self.question.wait_check_page():  # 页面检查点
                                self.question.question_basket()  # 题筐按钮

                                self.judge_basket_result(item)  # 验证题筐结果具体操作

    @teststeps
    def search_input_clear(self):
        """清空搜索框内容"""
        if self.question.wait_check_page():  # 页面检查点
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

    @testcase
    def test_002_question_add_button(self):
        """题库 -- 题单详情页 加题进题筐按钮"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page():  # 页面检查点
                item = self.question.question_name()  # 获取 题目
                print('题单:', item[1][2])
                item[0][2].click()  # 点击第X道题

                if self.detail.wait_check_page():  # 页面检查点
                    if self.basket.wait_check_list_page():  # 题筐有题
                        print('---------------------题单详情页-------------------')
                        self.detail.all_check_button()  # 全选按钮
                        if self.basket.wait_check_list_page():
                            self.detail.put_to_basket_button()  # 点击 加入题筐按钮
                            Toast().toast_operation(TipsData().add_basket)

                            if self.detail.wait_check_list_page():
                                time.sleep(2)  # toast 3秒消失
                                self.detail.all_check_button()  # 全选按钮
                                if self.basket.wait_check_list_page():
                                    self.detail.put_to_basket_button()  # 再次点击 加入题筐按钮
                                    Toast().toast_operation(TipsData().add_basket_again)

                                    if self.detail.wait_check_list_page():
                                        games = self.question.question_name()[1]  # 获取 小游戏名
                                        print(games)
                                        self.home.back_up_button()  # 返回 题库 主界面
                                        self.judge_add_result_delete_operation(games)  # 题筐验证并移除 具体操作

                                        if self.question.wait_check_page():  # 页面检查点
                                            items = self.question.question_name()  # 获取 题目
                                            for i in range(len(items[1])):
                                                if items[1][i] == item[1][2]:
                                                    items[0][2].click()  # 点击第X道题

                                                    if self.detail.wait_check_page():  # 页面检查点
                                                        if self.detail.wait_check_list_page():  # 页面检查点
                                                            print('---------------------题单详情页-------------------')
                                                            games = self.question.question_name()[1]  # 获取 小游戏名
                                                            print(games)
                                                            self.detail.all_check_button()  # 全选按钮
                                                            if self.basket.wait_check_list_page():
                                                                self.detail.put_to_basket_button()  # 点击 加入题筐按钮
                                                                if Toast().find_toast(TipsData().add_basket):
                                                                    print('再次添加题筐成功')
                                                                else:
                                                                    print('★★★ Error- 再次添加题筐未弹-添加成功toast')
                                                                if self.detail.wait_check_list_page():
                                                                    self.home.back_up_button()  # 返回 题库 主界面

                                                                    if self.question.wait_check_page():  # 页面检查点
                                                                        self.question.question_basket()  # 进入题筐
                                                                        self.judge_basket_result(games, '再次添加题筐')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def judge_basket_result(self, name, var='添加题筐'):
        """验证题筐具体操作"""
        print('--------------验证 {} 结果--------------'.format(var))
        if self.basket.wait_check_page():  # 页面检查点
            if self.basket.wait_check_list_page():
                count = []
                self.basket_list(name, count)  # 题筐列表
                print('------------------------')
                if count:
                    print('加入题筐成功')
                else:
                    print('★★★ Error- 加入题筐失败', name)

                self.basket.all_check_button()  # 全选按钮
                if self.basket.wait_check_list_page():
                    self.basket.out_basket_button()  # 移出题筐按钮

                    if self.basket.wait_check_list_page(5):
                        self.basket.all_check_button()  # 全选按钮
                        if self.basket.wait_check_list_page():
                            self.basket.out_basket_button()  # 移出题筐按钮
                    if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                        print('全部移除成功')
                print('----------------------')

            if self.basket.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回题库主界面

    @teststeps
    def judge_add_result_delete_operation(self, name):
        """toast为: 已经加入题筐成功 时, 移出题筐中该题的具体操作"""
        print('--------------验证 添加题筐 结果--------------')
        if self.question.wait_check_page():  # 页面检查点
            self.question.question_basket()  # 题筐按钮
            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():
                    count = []
                    self.basket_list(name, count)  # 题筐列表
                    self.basket.out_basket_button()  # 移出题筐按钮

                    print('------------------------')
                    if count:
                        print('加入题筐成功')
                    else:
                        print('★★★ Error- 加入题筐失败', name)
                elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                    print('★★★ Error- 暂无数据，加入题筐失败')

            if self.basket.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回按钮

    # 39EUJP
    @teststeps
    def basket_list(self, name, count, content=None):
        """题筐列表"""
        if content is None:
            content = []

        if self.basket.wait_check_list_page():
            item = self.question.question_name()[1]  # 获取题目
            print(item)
            if len(item) > 6 and not content:
                self.basket_question_list(name, item, count, len(item)-1)  # 题筐 题目列表

                content = [name[-1]]
                SwipeFun().swipe_vertical(0.5, 0.6, 0.3)  # 滑屏一次
                if self.basket.wait_check_list_page():
                    self.basket_list(name, count, content)
            else:
                var = 0
                if content:
                    for k in item:
                        if content[0] == k:
                            var = 1
                            break
                    if var == 0:
                        var = 1
                self.basket_question_list(name, item, count, len(item), var)  # 题筐 题目列表

    @teststeps
    def basket_question_list(self, name, item, count, length, var=0):
        """题筐 题目列表"""
        check = self.basket.check_button()  # 单选按钮
        for j in range(len(name) - 1, -1, -1):
            print(name[j])
            for i in range(var, length):
                if name[j] in item[i]:
                    count.append(i)
                if self.get.checked(check[i]) == 'false':
                    check[i].click()
