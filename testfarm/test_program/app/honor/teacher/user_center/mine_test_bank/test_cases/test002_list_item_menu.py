#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from conf.decorator import setup, teardown, testcase, teststeps
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
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
                    if self.home.wait_check_empty_tips_page():
                        print('暂无大题')
                    elif self.mine.wait_check_list_page():  # 是否有
                        print('-----------------我的题库 题单-------------------')
                        var = self.item_operation()  # 具体操作
                        self.home.back_up_button()

                        if var:
                            self.judge_add_public_test_bank_result(var)  # 加入公共题库结果 验证
                else:
                    print('未进入 我的题库 页面')
            else:
                print('未进入个人中心页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def item_operation(self):
        """条目 的右端菜单具体操作"""
        name = self.mine.question_name()  # 题单
        author = self.mine.question_author()  # 老师

        content = []
        count = 0
        for i in range(len(name[1])):
            if self.mine.wait_check_list_page():
                name[0][i].click()
                if self.detail.wait_check_page():
                    games = self.mine.question_name()[1]  # 题单
                    var = 0
                    for k in games:
                        if '引用' in k:
                            var += 1
                            break

                    self.home.back_up_button()  # 返回列表
                    if var == 0:
                        if self.mine.wait_check_list_page():
                            print(name[1][i], '  ', author[i].text)
                            if '引用' in name[1][i]:
                                self.mine.menu_button(i)  # 右侧菜单按钮
                                self.home.tips_content_commit()  # 提示 页面信息
                                Toast().toast_operation('引用题或微课无法加入我的题库')
                            else:
                                count += 1
                                content.extend([name[1][i], author[i].text])
                                self.mine.menu_button(i)  # 右侧菜单按钮
                                self.home.tips_content_commit()  # 提示 页面信息
                                self.home.tips_content_commit()  # 提示 页面信息
                                break
                            print('---------------------------------------')

        if count != 0:
            return content

    @teststeps
    def judge_add_public_test_bank_result(self, var):
        """验证 加入我的题库结果"""
        print('----------------验证 加入我的题库结果---------------')
        print(var)
        if self.user.wait_check_page():  # 页面检查点
            self.home.click_tab_test_bank()

            if self.question.wait_check_page():  # 页面检查点
                self.question.search_operation(var[0])  # 进入首页后 点击 题库tab

                if self.question.wait_check_game_type_page():  # 页面检查点
                    name = self.question.question_name()  # 获取 小游戏名
                    author = self.question.question_author()  # 作者
                    if name[1][0] == var[0] and author[0].text == var[1]:
                        print('加入我的题库成功')
                    else:
                        print('★★★ Error- 加入我的题库 失败', name[1][0], var)

                if self.question.wait_check_game_type_page():  # 页面检查点
                    self.home.click_tab_hw()
