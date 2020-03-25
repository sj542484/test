#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.assign_hw_paper.test_data.hw_name_data import GetVariable as gv
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_spoken_detail_page import SpokenPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from conf.log import Log
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class AssignHwSpoken(unittest.TestCase):
    """布置作业 - 包含口语"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.filter = FilterPage()
        cls.question = TestBankPage()
        cls.basket = TestBasketPage()
        cls.detail = SpokenPage()
        cls.tips = TipsData()
        cls.van_detail = VanclassDetailPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.log = Log()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(AssignHwSpoken, self).run(result)

    @testcase
    def test_assign_hw_contain_spoken(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        print("0.验证：添加口语题进题筐\n"
              "1.验证：点击定时帮助按钮, 有正确提示信息\n"
              "2.验证：未填入作业名称, 有正确提示信息\n"
              "3.验证：未选择学生, 有正确提示信息\n"
              "4.验证：调整题目顺序\n"
              "5.验证：作业模式, 达标模式不能包含口语题\n"
              "6.验证：布置成功, 提示信息\n"
              "7.验证：作业名称重复\n"
              "8.验证：验证布置结果\n"
              "=======================================================")
        if self.home.wait_check_page():
            self.question.judge_into_tab_question()  # 从首页进入题库tab
            self.judge_basket_num()  # 验证题筐题数

            if self.question.wait_check_page(): # 页面检查点
                self.question.filter_button()  # 筛选按钮
                if self.filter.wait_check_page():  # 页面检查点
                    self.filter.click_game_list()  # 点击 大题

                    if self.filter.wait_check_page():  # 页面检查点
                        title = self.filter.label_name()  # 标签
                        spoken = ['口语看读', '口语跟读', '口语背诵']
                        index = random.randint(0, len(spoken) - 2)
                        for i in range(len(title)):
                            if title[i].text == spoken[index]:
                                print('点击', title[i].text)
                                title[i].click()  # 口语跟读/看读

                                if self.filter.wait_check_page():  # 页面检查点
                                    self.filter.commit_button()  # 点击 确定按钮
                                break

                        if self.question.wait_check_game_type_page(): # 页面检查点
                            SwipeFun().swipe_vertical(0.5, 0.7, 0.3)
                            self.assertTrue(self.add_to_basket(), '★★★ Error- 加题进题筐失败')  # 先加题进题筐
                            self.assign_operation()  # 获取题筐所有题 & 布置作业

                            if self.home.wait_check_page():  # 恢复测试数据
                                print('-----恢复测试数据-----')
                                self.home.click_tab_test_bank()
                                self.question.wait_check_game_type_page()  # 恢复测试环境
                                self.filter.reset_filter_operation()  # 恢复筛选，并返回主界面

    @teststeps
    def assign_operation(self):
        """获取题筐所有题 & 布置作业"""
        self.assertTrue(self.basket.wait_check_list_page(), self.basket.basket_list_tips)  # 页面检查点
        self.basket.all_check_button()  # 全选按钮
        ele = self.basket.assign_button()  # 布置作业 按钮
        num = 50 - int(re.sub("\D", "", ele.text))  # 提取 题数

        self.assertTrue(self.basket.wait_check_list_page(), self.basket.basket_list_tips)  # 页面检查点
        self.basket.all_check_button()  # 全选按钮
        content = []

        var = num // 6 + 1
        while var > 0:
            self.assertTrue(self.basket.wait_check_list_page(), self.basket.basket_list_tips)  # 页面检查点
            mode = self.basket.question_type()  # 小游戏类型
            index = -1
            length = len(mode)-1
            if len(mode) > 5:
                length = len(mode) - 2
                index = 0
            for i in range(length, index, -1):
                if mode[i].text in ['口语看读', '口语跟读', '口语背诵']:
                    content.append(mode[i].text)

            if not content:
                SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
                var -= 1
            else:
                item = self.basket.question_name()[1]  # 获取题目
                check = self.basket.check_button()  # 单选按钮
                index = -1
                length = len(item)-1
                if len(item) > 5:
                    length = len(item) - 2
                    index = 0
                for i in range(length, index, -1):
                    print(item[i])
                    check[i].click()
                break

        self.assertFalse(len(content) == 0, '无口语题')
        self.basket.assign_button().click()  # 点击布置作业 按钮
        self.home.tips_content_commit()  # 温馨提示 页面

        if self.release.wait_check_release_page():  # 页面检查点
            print('--------------发布作业 页面--------------')
            self.release.assign_button()  # 发布作业 按钮
            self.my_toast.toast_assert(self.name, Toast().toast_operation(TipsData().no_hw_name))  # 作业名称为空 验证
            print('---------------------------')

            self.release_hw_operation()  # 发布作业 详情页

    @teststeps
    def release_hw_operation(self):
        """发布作业 详情页"""
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(gv.SPOKEN_ASSIGN)  # 修改name
        title = name.text
        print(self.release.hw_title(), ":", title)  # 打印元素 作业名称

        print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
        self.release.hw_mode_operation()  # 作业 达标模式
        self.release.hw_vanclass_list()  # 班级列表
        choose = self.release.choose_class_operation()  # 选择班级 学生
        self.release.hw_adjust_order()  # 调整题目顺序
        self.release.assign_button()  # 发布作业 按钮

        self.home.tips_content_commit()  # 达标模式不能包含口语题
        if self.release.wait_check_release_page():  # 页面检查点
            self.release.hw_mode_operation('free')  # 作业 达标模式
            self.release.assign_button()  # 发布作业 按钮

        self.release.tips_page_info()  # 提示框
        if Toast().find_toast(self.tips.hw_only_daily):  # 若当天布置的作业有重名，获取toast
            print(self.tips.hw_only_daily)
            title = self.release.republish_operation()  # 重新命名布置

        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.home.click_tab_hw()  # 返回 主界面

        self.van_detail.judge_vanclass_result_operation(choose[0], title)  # 验证布置结果

    @teststeps
    def judge_basket_num(self):
        """验证题筐题数"""
        result = self.basket.basket_ready_operation()  # 查看目前题筐还差多少题
        if int(result) < 20:  # 还可以添加题筐数
            self.basket.out_basket_button()  # 移出题筐

        self.assertTrue(self.basket.wait_check_page(), self.basket.basket_tips)  # 页面检查点
        self.home.back_up_button()  # 返回 题筐主界面

    @teststeps
    def add_to_basket(self, ques_index=2):
        """加题单 进 题筐"""
        if self.question.wait_check_game_type_page():  # 页面检查点
            self.question.question_name()[0][ques_index].click()  # 点击第ques_index道题

            if self.detail.wait_check_page():  # 页面检查点
                if self.detail.wait_check_list_page():  # 页面检查点
                    print('加题进题筐')
                    self.detail.put_to_basket_button()  # 点击加入题筐按钮
                    if self.detail.wait_check_list_page():  # 页面检查点
                       self.home.back_up_button()  # 返回按钮

                    if self.question.wait_check_page('搜索'):  # 页面检查点
                        self.question.question_basket_button()  # 题筐按钮

                        if self.basket.wait_check_page():  # 页面检查点
                            if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                print('★★★ Error- 加入题筐失败')
                                self.home.back_up_button()  # 返回题库页面

                                if self.question.wait_check_page('搜索'):  # 页面检查点
                                    self.home.click_tab_hw()  # 返回 主界面
                                return False
                            elif self.basket.wait_check_list_page():
                                return True
