#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import time
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.timing_hw.object_page.draft_page import DraftPage
from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.home.assign_hw_paper.test_data.hw_name_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class AssignHwMulti(unittest.TestCase):
    """布置 多定时的作业"""

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
        cls.draft = DraftPage()
        cls.get = GetAttribute()
        cls.toast = Toast()
        cls.tips = TipsData()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(AssignHwMulti, self).run(result)

    @testcase
    def test_assign_hw_timing_multi(self):
        print("1.验证：点击定时帮助按钮 有正确提示信息\n"
              "2.验证：未填入作业名称, 有正确提示信息\n"
              "3.验证：未选择学生 有正确提示信息\n"
              "4.验证：设定发布时间, 最多7个\n"
              "5.验证：布置成功 提示信息\n"
              "6.验证：验证布置成功及设定的时间\n"
              "===========================================================================")
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.assign_hw_button()  # 布置作业 按钮

        self.assertTrue(self.basket.wait_check_page(), self.basket.basket_tips)  # 页面检查点
        if self.home.wait_check_empty_tips_page():
            self.basket.empty_text()  # 空白文案
            self.home.back_up_button()  # 返回按钮

            self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
            self.question.judge_into_tab_question()  # 进入题库tab
            if self.draft.add_to_basket():  # 若题筐为空，先加题进题筐
                self.timing_operation()  # 布置定时作业 具体操作
        elif self.basket.wait_check_list_page():
            self.assertTrue(self.draft.question_bank_operation(),
                            '★★★ Error- 获取题筐所有题 并选择布置失败')  # 题筐内获取题筐所有题 并选择布置

            self.timing_operation()  # 布置定时作业 具体操作

    @teststeps
    def timing_operation(self):
        """布置定时作业 具体操作"""
        print('------------------布置定时作业------------------')
        self.release.hint_help_button()  # 点击定时 帮助按钮
        self.my_toast.toast_assert(self.name, self.toast.toast_operation(self.tips.timing_hw))
        print('------------------------------------------')

        self.release.assign_button()  # 点击 发布作业 按钮
        self.my_toast.toast_assert(self.name, self.toast.toast_operation(self.tips.no_hw_name))  # 作业名称为空 验证
        time.sleep(3)  # 等待弹框消失，否则 获取不到 ‘请选择学生’

        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(gv.HW_TIME_MUL)  # name
        title = name.text
        print('作业名称：', title)
        self.release.assign_button()  # 点击 发布作业 按钮
        self.my_toast.toast_assert(self.name, self.toast.toast_operation(self.tips.no_choose_st))  # 未选择学生 toast验证

        self.release.hw_vanclass_list()  # 班级列表
        self.release.choose_class_operation()  # 选择学生

        date = []
        for i in range(8):
            if i != 7:
                index = random.randint(0, 2)
                self.time_setting(date, index)  # 设置 定时时间
            else:
                if self.release.judge_not_add_time_button():
                    print('★★★ Error- 已设置7个定时时间，设定时间按钮还存在')
                else:
                    print('最多设定7个发布时间')

        if not self.draft.judge_time_setting(date):
            print('★★★ Error- 设定时间失败,未获取到展示的时间')
        else:
            self.release.assign_button()  # 点击 发布作业 按钮
            self.my_toast.toast_assert(self.name, self.toast.toast_operation(self.tips.timing_success))  # 成功发布
            if self.question.wait_check_page('题单', 3):
                self.home.click_tab_hw()  # 返回主界面

            self.judge_assign_operation(date, title)  # 验证具体操作

    @teststeps
    def time_setting(self, date, index, dire='up'):
        """验证 设定的时间
        :param dire: 时间调节方向
        :param index: 第几个时间元素按钮
        :param date:统计时间
        """
        self.release.add_time_button()  # 设定时间 元素
        date.append(self.release.get_assign_date(index, dire))  # 修改时间 并获取修改后时间
        print('设置发布时间为:', date[-1])
        self.release.confirm_button()  # 点击 确定按钮

    @teststeps
    def judge_assign_operation(self, date, var):
        """验证布置结果"""
        print('----------------------验证布置结果----------------------')
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到web

        self.assertTrue(self.draft.wait_check_page(), self.draft.timing_tips)
        if self.draft.wait_check_empty_tips_page():
            self.assertFalse(self.draft.wait_check_empty_tips_page(),
                             '★★★ Error -暂无数据，保存定时作业失败, {} {}'.format(var, date))
        else:
            self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_list_tips)
            name = []  # 定时作业名 //
            date_list = []  # 发布日期
            hw = self.draft.draft_name()  # 作业条目
            self.draft.get_hw_list(name, date_list)  # 作业 名称/日期列表

            count = []
            for i in range(len(name)):
                if name[i] == var:  # name
                    for j in range(len(date_list)):  # 发布时间
                        # for k in date_list[i]: # todo  早于6点钟
                        # if int(date[j][-2]) < 0o6:
                        #     date[j][-2] = '06'
                        #
                        if date[0] == date_list[j]:
                            count.append(j)
                            print('保存定时作业成功')

                            hw[i].click()  # 编辑页面
                            self.vue.switch_app()  # 切到web
                            if HwDetailPage().wait_check_edit_page():  # 页面检查点
                                if self.release.wait_check_release_list_page():
                                    self.draft.judge_time_setting(date)

                            break

            self.assertFalse(len(count) == 0, '★★★ Error -保存定时作业失败, {} {}'.format(var, date))

        self.home.back_up_button()  # 返回主界面
