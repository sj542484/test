#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from conf.decorator import setup, teardown, testcase, teststeps
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Collection(unittest.TestCase):
    """我的收藏 -- 大题条目右侧菜单"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.filter = FilterPage()
        cls.collect = CollectionPage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.game = GamesPage()

        cls.recommend = RecommendPage()
        cls.basket = TestBasketPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_collection_game_list_menu(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_collection()  # 点击 我的收藏
                if self.collect.wait_check_page():  # 页面检查点
                    self.user.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():
                        self.user.click_game_list()  # 点击 大题
                        self.filter.commit_button()  # 点击 确定按钮

                        if self.collect.wait_check_page():  # 页面检查点
                            if self.home.wait_check_empty_tips_page():
                                print('暂无大题收藏')
                                self.add_collection_operation()  # 添加收藏

                            if self.collect.wait_check_list_page():  # 是否有收藏
                                print('-----------------我的收藏 大题-------------------')
                                var = self.item_operation()  # 具体操作

                                self.judge_basket_result(var[0])  # 加入题筐结果 验证
                                self.collect.cancel_collection_operation()  # 恢复测试数据 - 取消收藏
                                self.judge_recommend_result(var[0])  # 验证 加入我的推荐 结果
                else:
                    print('未进入 我的收藏 页面')
            else:
                print('未进入个人中心页面')
            if self.user.wait_check_page():  # 页面检查点
                self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def item_operation(self):
        """收藏条目 的右端菜单具体操作"""
        name = self.question.question_name()  # 大题
        author = self.question.question_author()  # 老师
        teacher = author[0].text
        print(name[1][0], '  ', teacher)

        self.collect.menu_button(0)  # 右侧菜单按钮
        if self.home.wait_check_tips_page():
            self.collect.recommend_to_school()  # 推荐到学校
            if self.filter.wait_check_school_label_page():
                self.filter.confirm_button()

        print('推荐到学校:')
        Toast().toast_operation('加入成功')
        print('----------------')

        if self.collect.wait_check_list_page():  # 是否有收藏
            self.collect.menu_button(0)  # 右侧菜单按钮
            if self.home.wait_check_tips_page():
                print('加入题筐:')
                self.collect.put_to_basket()  # 加入题筐
                Toast().toast_operation('添加成功')
                print('----------------')

        if self.collect.wait_check_list_page():  # 是否有收藏
            self.collect.menu_button(0)  # 右侧菜单按钮
            if self.home.wait_check_tips_page():
                print('贴标签：')
                self.collect.stick_label()  # 贴标签

            if self.collect.wait_check_label_page():
                self.collect.check_box(0)  # 选择标签
                self.collect.save_button()  # 保存按钮
                Toast().toast_operation('贴标签成功')
        return name[1][0], teacher,

    @teststeps
    def add_collection_operation(self):
        """添加收藏- 大题"""
        self.home.back_up_button()  # 返回 个人中心页面
        if self.user.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page():  # 页面检查点
                self.question.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                    self.filter.click_game_list()  # 点击 大题
                    self.filter.commit_button()  # 点击 确定按钮

                    if self.question.wait_check_game_type_page():  # 页面检查点
                        print('添加收藏- 大题')
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                        for i in range(1, 3):  # 加3道题
                            if self.question.wait_check_game_type_page():  # 页面检查点
                                item = self.question.question_name()  # 获取
                                item[0][i].click()  # 点击第X道大题

                                if self.game.wait_check_page():  # 页面检查点
                                    if self.game.wait_check_list_page():  # 信息加载完成
                                        self.detail.collect_button()  # 收藏按钮
                                        if self.game.wait_check_list_page():  # 页面检查点
                                            self.home.back_up_button()

                        # 恢复测试数据！！
                        if self.question.wait_check_page('搜索'):  # 页面检查点
                            self.question.filter_button()  # 筛选按钮

                            if self.filter.wait_check_page():
                                self.filter.click_question_menu()  # 点击 题单
                                self.filter.commit_button()  # 点击 确定按钮

                                if not self.question.wait_check_page():  # 页面检查点
                                    print('★★★ Error- 恢复测试数据失败')

                                # 回到我的收藏
                                if self.question.wait_check_page('搜索'):  # 页面检查点
                                    self.home.click_tab_profile()  # 个人中心
                                    if self.user.wait_check_page():  # 页面检查点
                                        self.user.click_mine_collection()  # 点击 我的收藏

                                        if self.collect.wait_check_page():  # 页面检查点
                                            self.user.filter_button()  # 筛选按钮

                                            if self.filter.wait_check_page():
                                                self.user.click_game_list()  # 点击 大题
                                                self.filter.commit_button()  # 点击 确定按钮

                                                if self.collect.wait_check_page():  # 页面检查点
                                                    if not self.collect.wait_check_list_page():  # 是否有收藏
                                                        if self.home.wait_check_empty_tips_page():
                                                            print('★★★ Error- 添加收藏失败')
                    else:
                        print('筛选器选择 大题 失败')
                else:
                    print('未打开筛选器')
            else:
                print('未进入题库tab')

    @teststeps
    def judge_basket_result(self, names):
        """验证 加入题筐结果"""
        if self.collect.wait_check_page():  # 页面检查点
            print('----------------验证 加入题筐结果---------------')
            self.question.question_basket_button()
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
                self.recommend.verify_recommend_result(var, '大题')  # 加入我的推荐结果 验证
