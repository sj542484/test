#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.test_data.search_content import search_data
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class BankSearch(unittest.TestCase):
    """题库 -搜索 -历史搜索词"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.question = TestBankPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_history_search_word(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab
            
            if not self.question.wait_check_page('搜索'):  # 页面检查点
                if self.question.search_input().text != '搜索':
                    self.question.clear_search_operation()
                
            if self.question.wait_check_page('搜索'):  # 页面检查点
                self.question.search_input().click()  # 点击 搜索框

                if self.question.wait_check_page('资源'):
                    word = self.question.get_history_search_word()  # 历史搜索词
                    print('------------------------------------------')
                    print('历史搜索词：', '\n'
                          , word[0])

                    self.get_word_operation(word[0])  # 准备 历史搜索词
                    if self.question.wait_check_search_page():
                        word = self.question.get_history_search_word()  # 历史搜索词

                    print('------------------------------------------')
                    print('历史搜索词：', '\n'
                          , word[0])
                    if len(word[0]) == 15:
                        print('历史搜索最多15条,目前15条')
                        self.question.delete_button(0)  # 删除按钮
                    elif len(word[0]) > 15:
                        print('★★★ Error - 历史搜索最多15条', len(word[0]))

                    self.home.back_up_button()  # 返回 题库 界面
                    if self.question.wait_check_game_type_page():  # 页面检查点
                        self.home.click_tab_hw()  # 返回首页
                else:
                    print('未进入 搜索 界面')
                    self.home.back_up_button()  # 返回 题库 界面
            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print('未进入主界面')

    @teststeps
    def get_word_operation(self, item):
        """准备 历史搜索词"""
        var = 0
        print('------------------------------------------')
        for i in range(len(item)+1):
            if self.question.wait_check_page('资源'):
                box = self.question.search_input()  # 搜索框

                for j in range(var, len(search_data)):
                    if search_data[j]['resource'] not in item:
                        var = j+1
                        box.send_keys(r'' + search_data[j]['resource'])  # 输入搜索内容
                        print('搜索内容：', box.text)
                        self.question.search_button()  # 搜索按钮

                        if self.question.wait_check_game_type_page():  # 页面检查点
                            self.question.search_input().click()  # 搜索框
                            break

        if self.question.wait_check_page('资源'):
            self.home.back_up_button()  # 由于一次不能展示在历史搜索词列表里，故切换一次页面
            if self.question.wait_check_game_type_page():  # 页面检查点
                self.question.search_input().click()  # 搜索框

