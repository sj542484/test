#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest
import re

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class QuestionDetail(unittest.TestCase):
    """题单详情 - 再次点击推荐和收藏按钮"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.collect = CollectionPage()
        cls.recommend = RecommendPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_question_detail_again(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab
            if self.question.wait_check_page():  # 页面检查点
                SwipeFun().swipe_vertical(0.5, 0.8, 0.6)
            if self.question.wait_check_page():  # 页面检查点
                item = self.question.question_item()  # 获取 题单

                name = []
                for i in range(len(item[0])):
                    count = re.sub("\D", "", item[2][i].text)  # 该题单大题数
                    if int(count) < 7:
                        name.append(item[0][i])  # 题单name
                        print('题单:', name[-1])
                        item[2][i].click()  # 点击第X道题单
                        break

                if self.detail.wait_check_page():  # 页面检查点
                    if self.detail.wait_check_list_page():  # 题单信息加载完成
                        print('-------------------题单详情页--------------------')
                        self.detail.recommend_button()  # 推荐按钮
                        FilterPage().choose_school_label()  # 选择本校标签
                        print(' 点击推荐按钮')

                        if self.detail.wait_check_list_page():  # 题单信息加载完成
                            self.detail.recommend_button()  # 再次点击 推荐按钮
                            FilterPage().choose_school_label()  # 选择本校标签
                            print(' 再次点击推荐按钮')
                            if Toast().find_toast('加入成功'):  # 获取toast
                                print(' 推荐成功')
                            else:
                                print(' ★★★ Error- 推荐失败')

                        if self.detail.wait_check_list_page():  # 题单信息加载完成
                            print('--------------------------')
                            self.detail.collect_button()  # 收藏按钮
                            print(' 点击收藏按钮')

                        if self.detail.wait_check_list_page():  # 题单信息加载完成
                            self.detail.collect_button()  # 取消收藏
                            print(' 再次点击收藏按钮')

                        if self.detail.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回按钮
                            print('================================================')

                            self.judge_collect_result(name[0])  # 验证 取消收藏结果
                            if self.user.wait_check_page():
                                self.user.click_mine_recommend()  # 我的推荐
                                self.recommend.verify_recommend_result(name[0])  # 验证 推荐结果

                            if self.user.wait_check_page():  # 页面检查点
                                self.home.click_tab_hw()  # 返回首页
                else:
                    print('★★★ Error- 未进入题单详情页')
            else:
                print('★★★ Error- 未进入题库页面')
                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def judge_collect_result(self, menu):
        """ 验证 - 收藏结果"""
        if self.question.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 个人中心
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_collection()  # 我的收藏

                if self.collect.wait_check_page():  # 页面检查点
                    print('-------------------验证 - 收藏结果------------------')
                    print(menu)
                    if self.collect.wait_check_list_page():  # 加载完成
                        item = self.question.question_name()  # 获取
                        menu1 = item[1][0]
                        if menu == menu1:
                            print('★★★ Error- 取消收藏失败', menu, menu1)
                        else:
                            print(' 取消收藏成功')
                    elif self.home.wait_check_empty_tips_page():
                        print(' 暂无数据，取消收藏成功')

                    if self.collect.wait_check_page():
                        self.home.back_up_button()  # 返回 个人中心
