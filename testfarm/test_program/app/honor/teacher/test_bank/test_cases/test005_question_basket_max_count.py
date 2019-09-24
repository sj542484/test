#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class QuestionBasket(unittest.TestCase):
    """题库 -- 题筺 最多50题"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.detail = QuestionDetailPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_question_max_num(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab
            # self.clear_basket_questions()  # 清空题筐

            var = 0
            while var == 0:
                if self.question.wait_check_page('题单'):  # 页面检查点
                    item = self.question.question_item()  # 获取 题目

                    for i in range(len(item[0])):
                        result = self.basket_ready_operation()  # 查看目前题筐还差多少题
                        print('题筺还差%s题' % result)

                        if self.question.wait_check_page('题单'):  # 页面检查点
                            count = int(re.sub("\D", "", item[2][i].text))  # 题数
                            item[2][i].click()  # 点击题目

                            if self.detail.wait_check_page():  # 页面检查点
                                if self.detail.wait_check_list_page():
                                    if self.get.enabled(self.basket.check_button()[0]) == 'true':
                                        print('该套题有%s道小题' % count, '   ',item[0][i])
                                        if result < 10 and count > result:
                                            self.detail.put_to_basket_button()  # 点击 加入题筐按钮
                                            Toast().find_toast('题筐最多还能加入%s题' % result)

                                        if result > count:
                                            self.detail.put_to_basket_button()  # 点击 加入题筐按钮
                                        else:
                                            self.detail.all_check_button()  # 全不选 按钮
                                            check = self.basket.check_button()  # 单选按钮

                                            if result > 6:
                                                length = len(check)
                                            else:
                                                length = result

                                            for j in range(length):
                                                if self.get.checked(check[j]) == 'false':
                                                    check[j].click()
                                            self.detail.put_to_basket_button()  # 点击 加入题筐按钮

                                        if result == 0:
                                            var = 1  # 之后跳出while循环
                                            if self.detail.wait_check_page():
                                                self.home.back_up_button()  # 返回 题库主界面
                                            break
                                    else:
                                        print('该题单已加入题筐', '   ', item[1][i])

                                    if self.detail.wait_check_page():
                                        self.home.back_up_button()  # 返回 题库主界面
                        print('-------------------------')

                    if self.question.wait_check_page('题单'):  # 页面检查点
                        SwipeFun().swipe_vertical(0.5, 0.8, 0.1)

            self.judge_full_operation()  # 验证题筐已满 具体操作

            if self.question.wait_check_page('题单'):  # 页面检查点
                self.home.click_tab_hw()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def basket_ready_operation(self):
        """ 查看目前题筐有多少题"""
        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.question.question_basket()  # 题筐 按钮

            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():  # 题筐有题

                    self.basket.all_check_button()  # 全选按钮
                    ele = self.basket.assign_button()  # 布置作业 按钮
                    num = 50 - int(re.sub("\D", "", ele.text))  # 提取 题数

                    self.home.back_up_button()  # 返回 题库主界面
                    return num
                elif self.home.wait_check_empty_tips_page():  # 暂无数据
                    self.basket.empty_text()

                    self.home.back_up_button()  # 返回 题库主界面
                    return 50

    @teststeps
    def clear_basket_questions(self):
        """清空题筐"""
        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.question.question_basket()  # 题筐 按钮
            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():  # 题筐有题
                    self.basket.all_check_button()  # 全选按钮
                    self.basket.out_basket_button() # 移出题筐 按钮

                if self.basket.wait_check_page():  # 页面检查点
                    self.home.back_up_button()

    @teststeps
    def judge_full_operation(self):
        """题筐 验证已满 具体操作"""
        if self.question.wait_check_page('搜索'):  # 页面检查点
            print('------------验证 题筐已满-------------')
            self.question.question_basket()  # 题筐按钮

            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():  # 题筐不为空
                    self.basket.all_check_button()  # 全选按钮
                    ele = self.basket.assign_button()  # 布置作业 按钮
                    num = re.sub("\D", "", ele.text)  # 提取所选的题数
                    if int(num) == 50:
                        print('题筐已满')
                    else:
                        print('★★★ Error- 题筐题数', num)

                self.home.back_up_button()  # 返回 题库主界面
