#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
import ddt

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.test_data.assign_hw_name_data import hw_data
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.timing_hw.object_page.draft_page import DraftPage
from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


@ddt.ddt
class AssignTimingHw(unittest.TestCase):
    """布置 定时作业"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.bank = TestBankPage()
        cls.basket = TestBasketPage()
        cls.draft = DraftPage()

        cls.toast = Toast()
        cls.tips = TipsData()
        cls.get = GetAttribute()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切到apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(AssignTimingHw, self).run(result)

    @ddt.data(*hw_data)
    @testcase
    def test_assign_hw_timing(self, data):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        if self.home.wait_check_page():  # 页面检查点
            vans = self.home.vanclass_statistic_operation()  # 班级列表统计
            self.home.assign_hw_button()  # 布置作业 按钮

            if self.basket.wait_check_page():  # 页面检查点
                assign_result = []
                if '题筐为空' in data['name']:
                    print(data)
                    if self.basket.wait_check_list_page(5):
                        self.basket.all_check_button()  # 全选移除
                        self.basket.out_basket_button()  # 移出题筐 按钮

                    self.home.back_up_button()  # 返回主界面
                    self.bank.judge_into_tab_question()  # 进入题库tab

                    if self.draft.add_to_basket():  # 先加题进题筐
                        assign_result = self.timing_operation(data, vans)  # 布置定时作业 具体操作
                        if self.bank.wait_check_page('题单'):
                            self.home.click_tab_hw()  # 返回主界面
                else:
                    if self.home.wait_check_empty_tips_page():
                        self.basket.empty_text()  # 空白文案
                        self.home.back_up_button()  # 返回按钮
                        self.bank.judge_into_tab_question()  # 进入题库tab

                        if self.draft.add_to_basket():  # 若题筐为空，先加题进题筐
                            print(data)
                            assign_result = self.timing_operation(data, vans)  # 布置定时作业 具体操作
                            if self.bank.wait_check_page('题单'):
                                self.home.click_tab_hw()  # 返回主界面
                    elif self.basket.wait_check_list_page():
                        print(data)
                        self.assertTrue(self.draft.question_bank_operation(),
                                        '★★★ Error- 获取题筐所有题 并选择布置失败')  # 题筐内获取题筐所有题 并选择布置
                        assign_result = self.timing_operation(data, vans)  # 布置定时作业 具体操作

                self.assertTrue(assign_result, '★★★ Error- 作业布置失败')
                if '作业名称重复' in data['mode']:
                    self.judge_assign_duplicate_name_operation(assign_result)  # 验证具体操作
                else:
                    self.judge_assign_operation(assign_result)  # 验证具体操作

    @teststeps
    def timing_operation(self, data, vans):
        """布置定时作业 具体操作"""
        print('------------------布置定时作业------------------')
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(data['name'])  # name
        title = name.text
        print('作业名称：{}'.format(title))
        self.release.assign_button()  # 点击 发布作业 按钮
        self.my_toast.toast_assert(self.name, self.toast.toast_operation(self.tips.no_choose_st), True)  # 未选择学生 toast验证

        self.release.hw_vanclass_list(vans)  # 班级列表
        self.release.choose_class_operation()  # 选择学生

        self.release.add_time_button()  # 设定时间 元素
        date = self.release.get_assign_date()  # 设定时间
        print('设置发布时间为：{}'.format(date))
        self.release.confirm_button()  # 点击 确定按钮

        if not self.judge_time_setting(date):
            print('★★★ Error- 设定时间失败, 未获取到展示的时间')
        else:
            self.release.assign_button()  # 点击 发布作业 按钮

            self.my_toast.toast_assert(self.name, self.toast.toast_operation(data['assert']), True)  # 成功发布
            return date, title

    @teststeps
    def judge_time_setting(self, date):
        """验证 设定的时间"""
        print('-----验证 设定的时间------')
        time_text = self.release.timing_show()[-1].text  # 展示的时间
        dates = self.draft.time_types_exchange(time_text)

        count = 0
        for i in range(len(dates)):
            if dates[i] != date[i]:
                count += 1
                break

        if count == 0:
            print('展示的时间与设定的一致')
            return True
        else:
            print('★★★ Error- 展示的时间与设定的不一致{}\n{}'.format(dates, date))
            return False

    @teststeps
    def judge_assign_operation(self, content):
        """验证布置结果"""
        print('------------------验证布置结果-------------------')
        if self.home.wait_check_page():
            self.home.timing_button()  # 定时作业 按钮
            if self.draft.wait_check_app_page():
                self.vue.switch_h5()  # 切到web

                if self.draft.wait_check_page():
                    if self.draft.wait_check_empty_tips_page():
                        self.assertFalse(self.draft.wait_check_empty_tips_page(),
                                         '★★★ Error -暂无数据，保存定时作业失败, {}'.format(content))
                    elif self.draft.wait_check_hw_list_page():
                        name = []  # 定时作业名
                        date_list = []  # 发布日期
                        self.draft.get_hw_list(name, date_list)  # 作业列表
                        count = []
                        for i in range(len(name)):
                            if name[i] == content[1]:  # name
                                for j in range(len(content[0])):  # 发布时间
                                    if content[0][j] == date_list[i][j]:
                                        count.append(j)
                                        print('保存定时作业成功')
                                        break
                        self.assertFalse(len(count) == 0, '★★★ Error -保存定时作业失败, {}'.format(content))

                    if self.draft.wait_check_page():
                        self.draft.back_up_button()  # 返回主界面

    @teststeps
    def judge_assign_duplicate_name_operation(self, content):
        """验证 重名布置结果"""
        print('------------------验证重名作业布置结果-------------------')
        if self.home.wait_check_page():
            self.home.timing_button()  # 定时作业 按钮
            if self.draft.wait_check_app_page():
                self.vue.switch_h5()  # 切到web

                if self.draft.wait_check_page():
                    if self.draft.wait_check_empty_tips_page():
                        self.assertTrue(self.draft.wait_check_hw_list_page(),
                                        '★★★ Error -暂无数据，保存定时作业失败, {}'.format(content))
                    elif self.draft.wait_check_hw_list_page:
                        name = []  # 定时作业名
                        date_list = []  # 发布日期
                        self.draft.get_hw_list(name, date_list)  # 作业列表

                        count = []
                        for i in range(len(name)):
                            if name[i] == content[1]:  # name
                                for j in range(len(date_list)):  # 发布时间
                                    if content[0] == date_list[j]:
                                        count.append(j)
                                        break

                        self.assertFalse(len(count) == 0, '★★★ Error -保存定时作业失败, {}'.format(content))
                        print('保存定时作业成功')

                    if self.draft.wait_check_page():
                        self.draft.back_up_button()  # 返回主界面
