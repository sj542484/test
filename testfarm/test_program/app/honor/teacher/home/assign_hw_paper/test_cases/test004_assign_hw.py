#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import sys
import time
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.home.assign_hw_paper.test_data.hw_name_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class AssignHw(unittest.TestCase):
    """布置 作业"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.question = TestBankPage()
        cls.basket = TestBasketPage()
        cls.filter = FilterPage()
        cls.detail = QuestionDetailPage()
        cls.vue = VueContext()
        cls.van_detail = VanclassDetailPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(AssignHw, self).run(result)

    @testcase
    def test_assign_hw(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        print("1.验证：点击定时帮助按钮, 有正确提示信息\n"
              "2.验证：未填入作业名称, 有正确提示信息\n"
              "3.验证：未选择学生, 有正确提示信息\n"
              "4.验证：调整题目顺序\n"
              "5.验证：作业模式\n"
              "6.验证：布置成功, 提示信息\n"
              "7.验证：作业名称重复\n"
              "8.验证：验证布置结果\n"
              "=======================================================")
        if self.home.wait_check_page():
            vans = self.home.vanclass_statistic_operation()  # 班级列表统计
            self.home.assign_hw_button()  # 布置作业 按钮

            if self.basket.wait_check_page():
                title = 0
                choose = 0
                if self.home.wait_check_empty_tips_page():  # 由题筐进入，返回 题库界面
                    self.basket.empty_text()  # 空白文案
                    self.home.back_up_button()  # 返回按钮
                    self.question.judge_into_tab_question()  # 从首页进入题库tab

                    if self.question.wait_check_page():  # 页面检查点
                        self.assertTrue(self.basket.add_to_basket(), '★★★ Error- 加题进题筐失败')  # 若题筐为空，先加题进题筐
                        title, choose = self.assign_operation(vans)  # 加题单 进 题筐
                        if self.question.wait_check_page():  # ！！由题筐进入；else:  由布置作业按钮 进入
                            self.home.click_tab_hw()  # 返回 主界面
                elif self.basket.wait_check_list_page():  # 布置作业按钮进入，返回主界面
                    title, choose = self.assign_operation(vans)  # 获取题筐所有题 & 布置作业

                timestr = time.strftime('%m:%d:%H:%M:%S', time.localtime(time.time())).split(':')
                date = timestr[0]
                hour = int(timestr[-2])
                if hour > 5:
                    self.van_detail.judge_vanclass_result_operation(choose[0], title)  # 验证布置结果
                else:
                    self.judge_vanclass_hw_result_operation(choose[0], title, date)  # 验证布置结果

    @teststeps
    def assign_operation(self, vans):
        """获取题筐所有题 & 布置作业"""
        var = self.basket.question_name()[1]  # 获取题筐所有题
        check = self.basket.check_button()  # 单选按钮
        mode = self.basket.question_type()  # 小游戏类型

        if len(var) > 1:
            for i in range(len(mode) - 1):
                if mode[i].text not in ['口语看读', '口语跟读', '口语背诵']:
                    check[i].click()
                    if i == 3:
                        break
        else:
            check[0].click()

        self.basket.assign_button().click()  # 点击布置作业 按钮
        self.home.tips_content_commit()  # 温馨提示 页面

        if self.release.wait_check_release_page():  # 页面检查点
            print('--------------发布作业 页面--------------')
            self.release.assign_button()  # 发布作业 按钮
            self.my_toast.toast_assert(self.name, Toast().toast_operation(TipsData().no_hw_name))  # 作业名称为空 验证
            print('---------------------------')

            title, choose = self.release_hw_operation(vans)  # 发布作业 详情页
            return title, choose

    @teststeps
    def release_hw_operation(self, vans):
        """发布作业 详情页"""
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        print(name.text)
        name.send_keys(gv.HW_ASSIGN)  # name
        title = name.text
        print(self.release.hw_title(), ":", title)  # 打印元素 作业名称

        print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
        self.release.hw_mode_operation('free')  # 作业模式 操作
        self.release.hw_vanclass_list(vans)  # 班级列表
        choose = self.release.choose_class_operation()  # 选择班级 学生
        self.release.hw_adjust_order()  # 调整题目顺序

        self.release.assign_button()  # 发布作业 按钮
        self.release.tips_page_info()  # 提示框

        if Toast().find_toast(TipsData().hw_only_daily):  # 若当天布置的作业有重名，获取toast
            print(TipsData().hw_only_daily)
            title = self.release.republish_operation()  # 重新命名布置

        return title, choose

    @teststeps
    def judge_vanclass_hw_result_operation(self, van, assign, date):
        """验证 早于5点作业 的布置结果 具体操作
        :param date: 当前日期：月日
        :param van:班级
        :param assign:名称
        """
        print('------------------验证布置结果------------------')
        if self.home.wait_check_page():
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)

            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                if var == van:
                    name[i].click()  # 进入班级

                    if self.van_detail.wait_check_app_page(var):  # 页面检查点
                        self.vue.switch_h5()  # 切到web
                        if self.van_detail.wait_check_page(var):  # 页面检查点
                            if self.van_detail.wait_check_no_hw_page():
                                self.assertFalse(self.van_detail.wait_check_no_hw_page(),
                                                 '★★★ Error -布置时间早于5点钟的作业未布置成功, {}'.format(assign))
                            else:
                                self.assertTrue(self.van_detail.wait_check_list_page(), self.van_detail.van_list_tips)
                                hw = self.van_detail.hw_name()  # 作业名
                                create = self.van_detail.hw_create_time()  # 创建日期
                                title = self.home.vanclass_name(hw[0].text)

                                dates = create[0].text
                                self.assertNotEqual([title, re.findall('/D', dates.split()[0])], [assign, date],
                                                    '★★★ Error- 布置时间早于5点钟的作业布置成功, {} {}'.format(assign, title))
                                print('布置时间早于5点钟的作业未布置成功')

                                if self.van_detail.wait_check_page(van):
                                    self.van_detail.back_up_button()  # 返回 主界面
                    break
