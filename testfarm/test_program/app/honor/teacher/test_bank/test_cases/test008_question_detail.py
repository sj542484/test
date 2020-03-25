#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest
import re

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class QuestionDetail(unittest.TestCase):
    """题单详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.basket = TestBasketPage()
        cls.get = GetAttribute()


    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_question_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                name = []  # 验证结果
                k = 0  # 跳出while循环
                while True:
                    SwipeFun().swipe_vertical(0.5, 0.51, 0.1)
                    item = self.question.question_item()  # 获取
                    for i in range(len(item[0])):
                        count = re.sub("\D", "", item[2][i].text)  # 该题单大题数

                        if int(count) < 15:
                            name.append(item[0][i])  # 题单name
                            item[2][i].click()  # 点击第X道题单
                            k += 1
                            break
                    if name:
                        result = self.detail_operation(name[0])  # 题单详情页

                        self.judge_basket_result(result[0])  # 验证加入题筐结果
                        if self.question.wait_check_page('题单'):  # 验证 -选择本校标签 结果
                            print(result)
                            if result[1]:
                                FilterPage().judge_school_label_result(name[0], result[1][1], '题单')

                        if self.question.wait_check_page(name[0]):
                            self.home.click_tab_profile()  # 个人中心
                            if self.user.wait_check_page():
                                self.user.click_mine_collection()  # 我的收藏
                                CollectionPage().verify_collect_result(name[0])  # 验证 收藏结果

                        if self.user.wait_check_page():
                            self.user.click_mine_recommend()  # 我的推荐
                            RecommendPage().verify_recommend_result(name[0])  # 验证 推荐结果

                        if k != 0:
                            break

                        if self.user.wait_check_page():  # 页面检查点
                            self.home.click_tab_hw()  # 返回首页
                    else:
                        print('暂无可操作题单')
            else:
                print('未进入题库页面')
            if self.question.wait_check_page():  # 页面检查点
                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def detail_operation(self, name):
        """题单详情页"""
        if self.detail.wait_check_page():  # 页面检查点
            if self.detail.wait_check_list_page():  # 题单信息加载完成
                print('题单:', name)
                print('-------------------题单详情页--------------------')
                item = self.question.question_name()  # 获取题目
                check = self.detail.check_button()  # 单选按钮

                if len(item) < 6:
                    for i in range(len(item[0])):
                        if not self.get.checked(check[i]):
                            print('★★★ Error- 未默认全选')
                else:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.25)  # 滑屏一次

                    if self.detail.wait_check_list_page():  # 题单信息加载完成
                        check = self.detail.check_button()  # 单选按钮
                        for i in range(5):
                            if not self.get.checked(check[i]):
                                print('★★★ Error- 未默认全选')

                self.detail.recommend_button()  # 推荐按钮
                school = FilterPage().choose_school_label()  # 选择本校标签
                if Toast().find_toast('加入成功'):  # 获取toast
                    print(' 点击 推荐按钮')
                else:
                    print(' ★★★ Error- 推荐失败')
                print('--------------')

                if self.detail.wait_check_list_page():
                    self.detail.collect_button()  # 收藏按钮
                    print(' 点击收藏按钮')

                if self.detail.wait_check_list_page():
                    ele = self.detail.check_button()  # 单选按钮
                    if self.get.checked(ele[0]) == 'false':  # 第X道题 单选按钮checked 属性
                        ele[0].click()  # 第三道题

                    print('--------------')
                    name1 = item[1][0]
                    print(' 单选加入题筐:', name1)

                    self.detail.put_to_basket_button()  # 加入题筐 按钮
                    if Toast().find_toast('添加题筐成功'):  # 获取toast
                        print(' 点击 加入题筐按钮')

                    if self.detail.wait_check_list_page():
                        ele = self.detail.check_button()  # 单选按钮
                        if self.get.enabled(ele[0]) is False:  # 第三道题 单选按钮enabled 属性
                            print(' ★★★ Error- 单选按钮checked状态')

                        if self.detail.wait_check_page():
                            self.home.back_up_button()  # 返回按钮

                    return name1, school

    @teststeps
    def judge_basket_result(self, name):
        """ 验证 - 加入题筐结果"""
        if self.question.wait_check_page('题单'):
            self.question.question_basket_button()  # 题筐
            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():
                    print('--------------验证 -加入题筐结果---------------')
                    item = self.question.question_name()  # 获取题目
                    name1 = item[1][0]
                    if name != name1:
                        print('★★★ Error- 加入题筐失败', name, name1)
                    else:  # 为了保证脚本每次都可以运行，故将加入题筐的大题移出
                        print('加入题筐成功')

                        button = self.detail.check_button()  # 单选 按钮
                        button[0].click()
                        self.basket.out_basket_button()  # 移出题筐 按钮
                        print('移出题筐:', name1)
                elif self.home.wait_check_empty_tips_page():
                    print('★★★ Error- 加入题筐失败', name)

                if self.basket.wait_check_page():  # 页面检查点
                    self.home.back_up_button()
