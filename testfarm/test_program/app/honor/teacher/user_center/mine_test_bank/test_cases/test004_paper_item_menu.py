#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from conf.decorator import setup, teardown, testcase, teststeps
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.toast_find import Toast


class MineTestBank(unittest.TestCase):
    """我的题库 -- 试卷条目右侧菜单"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.filter = FilterPage()
        cls.mine = MineTestBankPage()
        cls.paper = PaperDetailPage()
        cls.question = TestBankPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_mine_test_bank_paper_menu(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_bank()  # 点击 我的题库
                if self.mine.wait_check_page():  # 页面检查点
                    self.user.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():
                        self.user.click_test_paper()  # 点击 试卷
                        self.filter.commit_button()  # 点击 确定按钮

                        if self.mine.wait_check_page():  # 页面检查点
                            if self.home.wait_check_empty_tips_page():
                                print('暂无试卷')

                            elif self.mine.wait_check_list_page():  # 是否有题库
                                print('====================我的题库 试卷====================')
                                var = self.item_operation()  # 具体操作
                                self.home.back_up_button()
                                print(var)
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
        name = self.mine.question_name()  # 试卷
        author = self.mine.question_author()  # 老师

        content = []
        for i in range(len(name[1])):
            if self.mine.wait_check_list_page():
                self.mine.menu_button(i)  # 右侧菜单按钮
                self.home.tips_content_commit()  # 提示 页面信息
                if Toast().find_toast('加入成功'):
                    print('加入成功')
                    var = [name[1][i], author[i].text]
                    content.append(var)
                    print(var)
                else:
                    if self.mine.wait_check_list_page():
                        self.mine.menu_button(i)  # 右侧菜单按钮
                        self.home.tips_commit()  # 提示 页面信息
                        Toast().toast_operation('引用题或微课无法加入公共题库')

                if i == 1:
                    break

            print('-----------------------------------------------')

        if content:
            return content

    @teststeps
    def judge_add_public_test_bank_result(self, var):
        """验证 加入公共题库结果"""
        print('----------------验证 加入公共题库结果---------------')
        print(var)
        if self.user.wait_check_page():  # 页面检查点
            self.home.click_tab_test_bank()

            if self.question.wait_check_page():  # 页面检查点
                self.user.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                    self.filter.click_test_paper()  # 点击 试卷
                    self.filter.commit_button()  # 点击 确定按钮
                    if self.question.wait_check_game_type_page():  # 页面检查点
                        self.home.click_tab_hw()

                        for i in range(len(var)):
                            print('-------------------------------------')
                            self.question.search_operation(var[i][0], '试卷')  # 进入首页后 点击 题库tab

                            if self.question.wait_check_game_type_page():  # 页面检查点
                                name = self.question.question_name()  # 获取 小游戏名
                                author = self.question.question_author()  # 作者
                                content = [name[1][0], author[0].text]
                                if content == var[i]:
                                    print('加入公共题库成功')
                                else:
                                    print('★★★ Error- 加入公共题库 失败', content, var[i])

                        if self.question.wait_check_game_type_page():  # 页面检查点
                            self.home.click_tab_hw()
