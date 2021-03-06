#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import unittest

from conf.decorator import setup, teardown, testcase, teststeps
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Collection(unittest.TestCase):
    """我的收藏 -- 题单列表&详情页"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()

        cls.user = TuserCenterPage()
        cls.collect = CollectionPage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.filter = FilterPage()
        cls.recommend = RecommendPage()
        cls.basket = TestBasketPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_collection_list_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_collection()  # 点击 我的收藏

                if self.collect.wait_check_page():  # 页面检查点
                    if self.home.wait_check_empty_tips_page():
                        print('暂无 题单收藏')
                        self.add_collection_operation()  # 添加收藏- 题单 else:
                        print('未进入 我的收藏 页面')

                    var = self.collect_list_operation()  # 收藏列表 & 进入题单详情页

                    if self.collect.wait_check_page():
                        self.judge_collect_result(var[0])  # 验证 - 取消收藏结果
                        self.judge_basket_result(var[1])  # 验证 - 加入题筐结果
                        self.judge_recommend_result(var[0])  # 验证 加入我的推荐 结果

                    if self.user.wait_check_page():  # 页面检查点
                        self.home.click_tab_hw()  # 回首页
                else:
                    print('未进入个人中心页面')
            else:
                Toast().get_toast()  # 获取toast
                print("未进入主界面")

    @teststeps
    def collect_list_operation(self):
        """收藏列表 & 进入题单详情页"""
        if self.collect.wait_check_list_page():  # 是否有收藏
            print('-----------------我的收藏 题单-------------------')
            name = self.question.question_name()  # 题单
            author = self.question.question_author()  # 老师

            for i in range(len(author)):
                mode = self.question.question_type(i)
                num = self.question.question_num(i)
                print(mode, '\n', name[1][i], '\n', num, '\n', author[i].text)
                print('------------------------------------')

            var = self.detail_page_operation(name)  # 题单详情页 具体操作

            return name[1][0], var

    @teststeps
    def add_collection_operation(self):
        """添加收藏- 题单"""
        self.home.back_up_button()  # 返回 个人中心页面
        if self.user.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('搜索'):  # 页面检查点
                print('添加收藏- 题单')
                SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                for i in range(1, 3):  # 加2道题
                    if self.question.wait_check_page('搜索'):  # 页面检查点
                        item = self.question.question_name()  # 获取
                        item[0][i].click()  # 点击第X道题单

                        if self.detail.wait_check_page():  # 页面检查点
                            if self.detail.wait_check_list_page():  # 题单信息加载完成
                                self.detail.collect_button()  # 收藏按钮
                                if self.detail.wait_check_page():  # 页面检查点
                                    self.home.back_up_button()

                if self.question.wait_check_page('搜索'):  # 页面检查点
                    self.home.click_tab_profile()  # 个人中心
                    if self.user.wait_check_page():  # 页面检查点
                        self.user.click_mine_collection()  # 点击 我的收藏

                        if self.collect.wait_check_page():  # 页面检查点
                            if not self.collect.wait_check_list_page():  # 是否有收藏
                                if self.home.wait_check_empty_tips_page():
                                    print('★★★ Error- 添加收藏失败')

    @teststeps
    def detail_page_operation(self, name):
        """题单详情页"""
        name[0][0].click()
        if self.detail.wait_check_page():  # 页面检查点
            print('-------------------题单详情页 操作-------------------')
            if self.detail.wait_check_list_page():
                game = self.question.question_name()[1][-1]  # 获取 小游戏名
                self.detail.collect_button()  # 取消 收藏
                print(' 点击 取消收藏')
                if self.detail.wait_check_list_page():
                    self.detail.recommend_button()  # 加入推荐 按钮
                    print(' 点击 推荐按钮')
                    self.filter.choose_school_label()  # 选择本校标签

                    if self.detail.wait_check_list_page():
                        self.detail.all_check_button()  # 全选按钮
                        if self.detail.wait_check_list_page():
                            self.detail.put_to_basket_button()  # 加入题筐按钮
                            print(' 点击 加入题筐按钮')

                            if self.detail.wait_check_page():  # 页面检查点
                                self.home.back_up_button()  # 返回 我的收藏页面

                                return game

    @teststeps
    def judge_collect_result(self, name):
        """ 验证 - 取消收藏结果"""
        print('----------------验证 取消收藏结果---------------')
        if self.collect.wait_check_list_page():  # 是否有收藏
            name1 = self.question.question_name()  # 题单
            if name == name1[1][0]:
                print('★★★ Error- 题单详情页 取消收藏失败', name, name1[1][0])
            else:
                print('取消收藏成功')
        else:
            print('取消收藏成功')

    @teststeps
    def judge_basket_result(self, names):
        """ 验证 - 加入题筐结果"""
        print('----------------验证 加入题筐结果---------------')
        if self.collect.wait_check_page():  # 是否有收藏
            self.question.question_basket_button()  # 题筐 按钮
            self.assertTrue(self.basket.wait_check_page(), self.basket.basket_tips)  # 页面检查点
            self.assertTrue(self.basket.wait_check_list_page(), self.basket.basket_list_tips)  # 页面检查点
            self.basket.all_check_button()  # 全选按钮
            ele = self.basket.assign_button()  # 布置作业 按钮
            num = 50 - int(re.sub("\D", "", ele.text))  # 提取 题数

            count = []
            var = num // 6 + 1
            while var > 0:
                self.assertTrue(self.basket.wait_check_list_page(), self.basket.basket_list_tips)  # 页面检查点
                item = self.basket.question_name()[1]  # 获取题目

                index = -1
                length = len(item)-1
                if len(item) > 5:
                    length = len(item) - 2
                    index = 0
                for i in range(length, index, -1):
                    for j in range(len(names)):
                        if item[i] == names[i]:
                            print(item[i])
                            count.append(i)
                            break

                if not count:
                    SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
                var -= 1

            print('----------------------------')
            self.assertFalse(len(count) == 0, '★★★ Error -加入题筐失败, {}'.format(names))
            print('加入题筐成功')
            if self.basket.wait_check_page():  # 页面检查点
                self.basket.out_basket_button()  # 移出题筐 按钮

            if self.basket.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回 我的收藏 页面

    @teststeps
    def judge_recommend_result(self, var):
        """验证 加入我的推荐 结果"""
        if self.collect.wait_check_page():
            self.home.back_up_button()  # 返回个人中心 页面
            if self.user.wait_check_page():
                self.user.click_mine_recommend()  # 我的推荐
                self.recommend.verify_recommend_result(var)  # 加入我的推荐结果 验证
