#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.timing_hw.object_page.draft_page import DraftPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.timing_hw.test_data.tips_data import TipsData
from app.honor.teacher.home.timing_hw.test_data.modify_hw_name_data import hw_data
from app.honor.teacher.home.timing_hw.test_data.hw_name_data import GetVariable as gv

from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class TimingHwModify(unittest.TestCase):
    """修改 定时作业"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.hw_detail = HwDetailPage()
        cls.release = ReleasePage()
        cls.question = TestBankPage()
        cls.draft = DraftPage()
        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(TimingHwModify, self).run(result)

    @testcase
    def test_timing_hw_modify(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        print("1.验证：修改作业名称\n"
              "2.验证：修改时间\n"
              "3.验证：修改选择的班级及学生\n"
              "4.验证：修改设定的发布时间\n"
              "5.验证：修改作业模式\n"
              "6.验证：验证修改结果\n"
              "================================================================")
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        if self.draft.wait_check_empty_tips_page():
            print('暂无 定时作业')
            self.draft.back_up_button()  # 返回按钮
            self.vue.switch_app()

            if self.home.wait_check_page():  # 页面检查点
                self.question.judge_into_tab_question()  # 进入题库tab

                if self.draft.add_to_basket():  # 若题筐为空，先加题进题筐
                    self.assign_operation()  # 布置定时作业

        self.hw_modify_operation()  # 修改定时作业 具体操作

    @teststeps
    def assign_operation(self):
        """无定时作业时，布置"""
        self.assertTrue(self.release.wait_check_release_list_page(), self.release.release_tips)
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(gv.HW_MODIFY)  # name

        self.release.hw_vanclass_list()  # 班级列表
        self.release.choose_class_operation()  # 选择学生

        self.assertTrue(self.release.wait_check_release_list_page(), self.release.release_tips)
        self.release.add_time_button()  # 设定时间 元素
        self.assertTrue(self.release.wait_check_time_list_page(), self.release.choose_time_tips)

        date = self.release.get_assign_date()  # 设定的时间
        print('设置发布时间为：', date)
        self.release.confirm_button()  # 点击 确定按钮

        self.assertTrue(self.release.wait_check_release_list_page(), self.release.release_tips)
        self.release.assign_button()  # 点击 发布作业 按钮

        if self.question.wait_check_page(5):
            self.home.click_tab_hw()  # 返回主界面
            if self.home.wait_check_page():
                self.home.timing_button()  # 定时作业 按钮
                self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
                self.vue.switch_h5()  # 切到vue

                self.assertTrue(self.draft.wait_check_page(), self.draft.timing_tips)
                self.assertTrue(self.draft.wait_check_hw_list_page, '★★★ Error- 保存定时作业失败')

    @teststeps
    def hw_modify_operation(self):
        """ 修改定时作业 具体操作"""
        self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
        title = self.draft.draft_name()  # name 元素
        index = random.randint(0, len(title) - 1)
        print('title:', title[index].text)
        title[index].click()  # 进入编辑页面

        for i in range(len(hw_data)):
            self.vue.switch_app()  # 切到apk
            print('===========================================================')
            self.assertTrue(self.hw_detail.wait_check_edit_page(), self.hw_detail.edit_tips)
            self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)
            print('-------------------编辑作业页面-------------------')
            self.release.hw_name_edit().send_keys(hw_data[i]['name'])  # 作业名称 编辑框
            print('修改作业名称为：', hw_data[i]['name'])

            self.release.hw_mode_operation(hw_data[i]['mode'])  # 作业模式 返回值为
            if i == 0:
                self.release.hw_vanclass_list()  # 班级列表
                self.release.choose_class_operation()  # 选择学生

            self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)
            SwipeFun().swipe_vertical(0.5, 0.15, 0.7)
            if self.release.wait_check_release_list_page():
                delete_time_button = self.release.delete_time_button()
                if len(delete_time_button) > 2:
                    delete_time_button[-1].click()  # 删除上一次设定的时间

                if self.release.wait_check_release_list_page():
                    self.release.delete_time_button()[0].click()
                    self.release.add_time_button()  # 设定时间 元素

                    self.assertTrue(self.release.wait_check_time_list_page(), self.release.choose_time_tips)
                    date = self.modify_publish_time(i, len(hw_data[i]))  # 修改发布时间

                    self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)
                    if len(hw_data[i]) == 3:  # 验证作业名称
                        self.release.assign_button()  # 点击 发布作业 按钮
                        self.my_toast.toast_assert(self.name, Toast().toast_operation(hw_data[i]['assert_name']))
                    else:  # 发布成功 2/4
                        self.release.assign_button()  # 点击 发布作业 按钮
                        self.my_toast.toast_assert(self.name, Toast().toast_operation(TipsData().timing_success))

                        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
                        self.home.timing_button()  # 定时作业 按钮
                        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
                        self.vue.switch_h5()  # 切到vue

                        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
                        index = self.judge_result_operation(date, hw_data[i]['name'], hw_data[i]['mode'])
                        if len(hw_data[i]) == 4:  # 方向为down--恢复数据
                            self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)
                            self.release.delete_time_button()[0].click()  # 删除设定的时间
                            self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)
                            self.release.add_time_button()  # 设定时间 元素
                            self.assertTrue(self.release.wait_check_time_list_page(), self.release.choose_time_tips)
                            self.release.get_assign_date(int(hw_data[i]['date']), hw_data[i]['dire'])
                            self.release.confirm_button()  # 点击 确定按钮

                        self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)
                        self.home.back_up_button()  # 返回列表页
                        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
                        self.vue.switch_h5()  # 切到vue

                        self.assertTrue(self.draft.wait_check_page(), self.draft.timing_tips)  # 页面检查点
                        self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
                        if i != len(hw_data)-1:
                            self.draft.draft_name()[index].click()  # 进入编辑页面
                        else:
                            self.draft.back_up_button()

    @teststeps
    def modify_publish_time(self, i, length):
        """修改发布时间"""
        if length > 1:
            item = self.release.number_input()  # 获取当前展示的时间
            date = []  # 时间列表 length=3
            for i in range(len(item)):
                if i == 0:
                    month = re.sub('\D', '', item[i].text.split('月')[0])
                    day = re.sub('\D', '', item[i].text.split('月')[1])
                    date.extend([month, day])
                else:
                    var = item[i].text
                    if len(var) == 1:
                        var = '0' + item[i].text
                    date.append(var)
        else:
            date = self.release.get_assign_date(int(hw_data[i]['date']), hw_data[i]['dire'])
        self.release.confirm_button()  # 点击 确定按钮

        print('修改发布时间为:', date)
        return date

    @teststeps
    def judge_result_operation(self, date, modify, mode):
        """验证 修改结果
        :param date: 创建日期
        :param modify:修改后的作业名称
        :param mode: 修改后的作业模式
        """
        print('--------------------------验证修改结果------------------------')
        print(modify)
        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
        hw_name = self.draft.draft_name()

        count = []
        for i in range(len(hw_name)):
            name = hw_name[i].text[5:-4].replace(" ", "")
            if name in modify.replace(" ", ""):
                count.append(i)
                self.draft.draft_name()[i].click()  # 编辑页面

                self.vue.switch_app()  # 切到apk
                self.assertTrue(self.hw_detail.wait_check_edit_page(), self.hw_detail.edit_tips)
                self.assertTrue(self.release.wait_check_release_list_page(), self.release.release_list_tips)
                self.judge_time_setting(date)
                self.judge_hw_mode_operation(mode)
                break

        if not count:
            print('★★★ Error -保存定时作业失败', modify, date)
        else:
            return count[0]

    @teststeps
    def judge_hw_mode_operation(self, var='reach'):
        """验证发布作业 - 作业模式"""
        print('-----------------验证 作业模式------------------')
        if var == 'free':
            mode = self.release.hw_mode_free()  # 自由模式
        else:
            mode = self.release.hw_mode_reach()  # 达标模式

        if self.get.checked(mode) is False:
            print('★★★ Error- 选择的作业模式: %s 有误' % var)
        else:
            print('作业模式无误')

    @teststeps
    def judge_time_setting(self, date):
        """验证 设定的时间"""
        print('----------------验证 设定的时间-----------------')
        timing = self.release.timing_show()  # 展示的时间

        count = 0
        for z in range(len(timing)):  # 多个日期
            dates = self.draft.time_types_exchange(timing[z].text)
            print(dates)
            if dates == date:  # 一个日期
                count += 1
                if len(dates) != len(date):
                    print('★★★ Error- 展示的时间 个数与设定的不一致', dates, date)
                else:
                    var = 0
                    for i in range(len(dates)):
                        # todo 早于06：00
                        if dates[i] != date[i]:
                            break
                        else:
                            var += 1

                    if var == len(date):
                        print('保存定时作业成功')
                        return True
                    else:
                        print('★★★ Error -保存定时作业失败', date)
                        return False

        self.assertTrue(count==0, '★★★ Error -设定时间失败, {} {}'.format(date, count))
