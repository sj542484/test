#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.test_data.search_content import search_data
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class BankSearch(unittest.TestCase):
    """题库 -- 搜索 - 上传者"""

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
    def test_search_uploader(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                self.question.search_input().click()  # 搜索框

                if self.question.wait_check_page('资源'):
                    self.question.drop_down_button().click()  # 下拉按钮

                    if self.question.judge_search_menu():
                        var = self.question.search_criteria_menu()  # 搜索条件菜单
                        self.question.choose_condition(var)
                        condition = var[1].text
                        var[1].click()  # 选择 上传者

                        if self.question.wait_check_search_page():
                            ele = self.question.drop_down_button()  # 下拉按钮
                            if condition != ele.text:
                                print('★★★ Error-选定的搜索条件与展示内容不一致', var[0].text, ele.text)

                            name = self.search_operation()  # 搜索 具体操作

                            if self.question.wait_check_page('题单'):  # 页面检查点
                                self.question.search_input().click()  # 点击 搜索框
                                if self.question.wait_check_page('上传者'):
                                    condition1 = self.question.drop_down_button().text  # 下拉按钮

                                    result = self.history_search_operation()  # 点击历史搜索词 搜索

                                    print('--------------------验证结果------------------')
                                    if condition != condition1:
                                        print('★★★ Error-搜索条件不一致', condition, condition1)
                                    else:
                                        print('两次的搜索条件一致')

                                    if name[1] != result[1]:
                                        print('★★★ Error-两次搜索到的内容不一致', name[1], result[1])
                                    else:
                                        print('两次搜索到的内容一致')

                                    if self.question.wait_check_page('题单'):  # 恢复测试数据
                                        self.question.search_input().click()  # 搜索框
                                        if self.question.wait_check_page('上传者'):
                                            self.question.input_clear_button()  # 清空 按钮
                                            self.question.drop_down_button().click()  # 下拉按钮

                                            if self.question.judge_search_menu():
                                                var = self.question.search_criteria_menu()  # 搜索条件菜单
                                                self.question.choose_condition(var)
                                                var[0].click()  # 选择

                                                if self.question.wait_check_page("资源"):
                                                    self.question.search_button()  # 搜索按钮
            else:
                print('未进入题库页面')

            if self.question.wait_check_page('题单'):  # 页面检查点
                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print('未进入主界面')

    @teststeps
    def search_operation(self):
        """搜索 过程"""
        item = self.question.search_input()  # 搜索框
        item.send_keys(r'' + search_data[-1]['uploader'])  # 输入搜索内容
        print('搜索内容：', item.text)
        self.question.search_button()  # 搜索按钮

        if self.question.wait_check_game_type_page():  # 题库页面
            name = self.question.question_name()
            length = 4
            if len(name[1]) < 5:
                length = len(name[1])

            for i in range(length):
                print(' ', name[1][i])
            print('--------------------------------------')

            self.question.search_input().click()  # 因为一次页面跳转 搜索内容无法展示在历史搜索词中
            if self.question.wait_check_page('上传者'):
                self.home.back_up_button()
            return name

    @teststeps
    def history_search_operation(self):
        """点击历史搜索词 搜索"""
        self.get_word([''])  # 历史搜索词

        if self.question.wait_check_game_type_page():  # 题库 页面
            name = self.question.question_name()
            length = 4
            if len(name[1]) < 5:
                length = len(name[1])
            for i in range(length):
                print(' ', name[1][i])
            print('--------------------------------------')
            return name

    @teststeps
    def get_word(self, content):
        """获取历史搜索词"""
        name = self.question.history_word()  # 历史搜索词

        if len(name) > 10 and len(content) == 1:
            for i in range(len(name) - 1):  #
                if name[i].text == search_data[-1]['uploader']:
                    print('---------------------', '\n',
                          '点击历史搜索词:', search_data[-1]['uploader'])
                    name[i].click()  # 点击该历史搜索词
                    break

                if i == len(name) - 2:
                    content.append(name[i].text)
                    SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                    self.get_word(content)
        else:  # <11 & 翻页
            var = 0
            for k in range(len(name)):
                if content[0] == name[k].text:
                    var += k + 1
                    break

            for j in range(var, len(name)):
                if name[j].text == search_data[-1]['uploader']:
                    print('---------------------', '\n',
                          '点击历史搜索词:', search_data[-1]['uploader'])
                    name[j].click()  # 点击该历史搜索词
                    break

