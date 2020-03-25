#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Recommend(unittest.TestCase):
    """我的推荐 -- 题单列表"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()

        cls.recommend = RecommendPage()
        cls.question = TestBankPage()
        cls.basket = TestBasketPage()
        cls.detail = QuestionDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_recommend_list_and_menu(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_recommend()  # 点击 我的推荐
                if self.recommend.wait_check_page():  # 页面检查点
                    if self.home.wait_check_empty_tips_page():
                        print('暂无 题单推荐')
                        self.recommend.add_recommend_operation(self.detail.wait_check_list_page)  # 添加 题单推荐

                        if self.recommend.wait_check_page():  # 页面检查点
                            if not self.recommend.wait_check_list_page():  # 是否有推荐列表
                                if self.home.wait_check_empty_tips_page():
                                    print('★★★ Error- 添加推荐失败')

                    if self.recommend.wait_check_list_page():  # 页面检查点
                        print('-----------------我的推荐 题单-------------------')
                        self.item_operation()  # 具体 推荐操作
                        # self.recommend.cancel_recommend_operation()  # 删除推荐

                    if self.recommend.wait_check_page():  # 页面检查点
                        self.question.question_basket_button()  # 题筐 按钮
                        if self.basket.wait_check_page():  # 页面检查点
                            self.home.back_up_button()

                    if self.recommend.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 点击 返回按钮
                else:
                    print('未进入 我的推荐 页面')
                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
            else:
                print('未进入个人中心页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def item_operation(self):
        """推荐条目 的右端菜单具体操作"""
        name = self.question.question_name()  # 题单
        author = self.question.question_author()  # 老师
        for i in range(len(author)):
            mode = self.question.question_type(i)
            num = self.question.question_num(i)
            print(mode, '\n', name[1][i], '\n', num, '\n', author[i].text)
            print('------------------------------------')

        print(name[1][0], '  ', author[0].text)
        name[0][0].click()  # 进入题单详情页

        if self.detail.wait_check_page():
            self.home.back_up_button()  # 返回 我的推荐 页面
