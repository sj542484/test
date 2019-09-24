#!/usr/bin/env python
# encoding:UTF-8
import unittest
import time

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class MineTestBank(unittest.TestCase):
    """我的题库 -- 大题条目右侧菜单"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.filter = FilterPage()
        cls.mine = MineTestBankPage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.game = GamesPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_mine_test_bank_game_list(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_bank()  # 点击 我的题库
                if self.mine.wait_check_page():  # 页面检查点
                    self.user.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():
                        self.user.click_game_list()  # 点击 大题
                        self.filter.commit_button()  # 点击 确定按钮

                        if self.mine.wait_check_page():  # 页面检查点
                            if self.home.wait_check_empty_tips_page():
                                print('暂无大题')
                            elif self.mine.wait_check_list_page():  # 是否有收藏
                                print('-----------------我的题库 大题-------------------')
                                var = self.item_operation()  # 具体操作
                                self.home.back_up_button()

                                # self.judge_add_public_test_bank_result(var)  # 加入公共题库结果 验证
                else:
                    print('未进入 我的题库 页面')
            else:
                print('未进入个人中心页面')
            if self.user.wait_check_page():  # 页面检查点
                self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def item_operation(self):
        """条目 的右端菜单具体操作"""
        name = self.question.question_name()  # 大题
        author = self.question.question_author()  # 老师

        content = []

        for i in range(len(name)):
            if '引用' not in name[1][i]:
                var = name[1][i]
                print(name[1][i], '  ', author[i].text)
                content.append(name[1][i])
                content.append(author[i].text)
                self.mine.menu_button(i)  # 右侧菜单按钮
                self.home.tips_content_commit()  # 提示 页面信息
                break

        return content

    @teststeps
    def judge_add_public_test_bank_result(self, var):
        """验证 加入公共题库结果"""
        if self.mine.wait_check_page():  # 页面检查点
            print('----------------验证 加入公共题库结果---------------')
            self.home.back_up_button()
            if self.user.wait_check_page():  # 页面检查点
                self.home.click_tab_test_bank()

                if self.question.wait_check_page('题单'):  # 页面检查点
                    self.user.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():
                        self.user.click_game_list()  # 点击 大题
                        self.filter.commit_button()  # 点击 确定按钮
                        if self.question.wait_check_game_type_page():  # 页面检查点
                            self.home.click_tab_hw()
                            self.question.search_operation(var[0])  # 进入首页后 点击 题库tab

                            if self.question.wait_check_game_type_page():  # 页面检查点
                                name = self.question.question_name()  # 获取 小游戏名
                                if name[1][0] == var[0]:
                                    print('加入公共题库成功')
                                else:
                                    print('★★★ Error- 加入题筐 失败', name[1][0], var[0])

                            if self.question.wait_check_game_type_page():  # 页面检查点
                                self.home.click_tab_hw()
