#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import setup, teardown, testcase
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class Paper(unittest.TestCase):
    """试卷 -- 收藏/推荐 本校标签"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.filter = FilterPage()
        cls.question = TestBankPage()
        cls.detail = PaperDetailPage()
        cls.release = ReleasePage()
        cls.user = TuserCenterPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page():  # 页面检查点
                self.question.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                    if GetAttribute().selected(self.filter.test_paper()) == 'false':
                        self.filter.click_test_paper()  # 点击 试卷
                        self.filter.commit_button()  # 确定按钮
                    else:
                        self.filter.commit_button()  # 确定按钮

            if self.question.wait_check_page('试卷'):  # 页面检查点
                item = self.question.question_name()  # 获取name

                if self.question.judge_question_lock():
                    lock = self.question.question_lock()  # 锁定的试卷数
                    item[0][len(lock)+2].click()  # 点击第X个试卷
                else:
                    item[0][2].click()  # 点击第X个试卷

                if self.detail.wait_check_page():  # 页面检查点
                    title = self.detail.paper_title()  # 试卷名称

                    self.detail.recommend_button()  # 推荐按钮
                    result = self.filter.choose_school_label()  # 选择本校标签
                    if Toast().find_toast('加入成功'):  # 获取toast
                        print('推荐成功')
                    else:
                        print(' ★★★ Error- 推荐失败')

                    if self.detail.wait_check_page():  # 页面检查点
                        self.detail.collect_button()  # 收藏按钮
                        Toast().toast_operation('成功加入收藏')  # 获取toast

                    if self.detail.wait_check_page():  # 页面检查点
                        self.home.back_up_button()
                        if self.question.wait_check_page('试卷'):  # 验证 -选择本校标签 结果
                            if result:
                                self.filter.judge_school_label_result(title, result[1], '试卷')

                        if self.question.wait_check_page(title):
                            self.home.click_tab_profile()  # 个人中心
                            if self.user.wait_check_page():
                                self.user.click_mine_collection()  # 我的收藏
                                CollectionPage().verify_collect_result(title, '试卷')  # 我的收藏 验证收藏结果

                        if self.user.wait_check_page():
                            self.user.click_mine_recommend()  # 我的推荐
                            RecommendPage().verify_recommend_result(title, '试卷')  # 我的推荐 验证结果

                        if self.user.wait_check_page():
                            self.home.click_tab_hw()  # 返回首页
            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
