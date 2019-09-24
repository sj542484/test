#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.test_data.assign_hw_name_data import hw_data
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.draft_page import DraftPage
from app.honor.teacher.home.test_data.draft_data import GetVariable as gv
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class TimingHw(unittest.TestCase):
    """修改 定时作业"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.release = ReleasePage()
        cls.question = TestBankPage()
        cls.draft = DraftPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_timing_hw_modify(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.timing_button()  # 定时作业 按钮

            if self.draft.wait_check_page():  # 页面检查点
                if self.home.wait_check_empty_tips_page():
                    print('暂无 定时作业')
                    if self.draft.add_to_basket():  # 若题筐为空，先加题进题筐
                        self.assign_operation()  # 布置定时作业
  
                self.hw_modify_operation()  # 修改定时作业 具体操作
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def assign_operation(self):
        """无定时作业时，布置"""
        if self.release.wait_check_release_list_page():
            name = self.release.hw_name_edit()  # 作业名称 编辑框
            name.send_keys(gv.HW_TIME)  # name

            self.release.hw_vanclass_list()  # 班级列表
            self.release.choose_class_operation()  # 选择学生

            if self.release.wait_check_release_list_page():
                self.release.timing_check_box().click()  # 定时单选框
                self.release.timing_show().click()  # 时间展示 元素
                if self.release.wait_check_time_list_page():
                    date = self.release.get_assign_date()  # 修改时间 并获取修改后时间
                    print('设置发布时间为：', date)
                    self.release.confirm_button()  # 点击 确定按钮

                    if self.release.wait_check_release_list_page():
                        self.release.assign_button()  # 点击 发布作业 按钮

                        if self.question.wait_check_page('题单', 5):
                            self.home.click_tab_hw()  # 返回主界面
                            if self.home.wait_check_page():
                                self.home.timing_button()  # 定时作业 按钮

                                if self.draft.wait_check_page():  # 页面检查点
                                    if not self.draft.wait_check_hw_list_page():
                                        print('★★★ Error- 保存定时作业失败')

    @teststeps
    def hw_modify_operation(self):
        """ 修改定时作业 具体操作"""
        if self.draft.wait_check_hw_list_page():
            title = self.draft.draft_name()  # name 元素
            title[0].click()  # 进入编辑页面

        for i in range(len(hw_data)):
            print('======================================================================')
            if self.detail.wait_check_edit_page():  # 页面检查点
                if self.release.wait_check_release_list_page():
                    print('-------------------编辑作业页面-------------------')

                    self.release.hw_name_edit().send_keys(hw_data[i]['name'])  # 作业名称 编辑框
                    print('修改作业名称为：', hw_data[i]['name'])

                    self.release.hw_mode_operation(hw_data[i]['mode'])  # 作业 达标模式 返回值为
                    if i == 0:
                        self.release.hw_vanclass_list()  # 班级列表
                        self.release.choose_class_operation()  # 选择学生

                    if self.release.wait_check_release_list_page():
                        SwipeFun().swipe_vertical(0.5, 0.15, 0.7)
                        if self.release.wait_check_release_list_page():
                            self.release.timing_show().click()  # 时间展示 元素

                            if self.release.wait_check_time_list_page():
                                length = len(hw_data[i])
                                date = self.modify_publish_time(i, length)  # 修改发布时间

                                if self.release.wait_check_release_list_page():
                                    if length == 3:  # 验证作业名称
                                        self.release.assign_button()  # 点击 发布作业 按钮

                                        if not Toast().find_toast(hw_data[i]['assert_name']):
                                            print('★★★ Error - 未弹toast:', hw_data[i]['assert_name'])
                                        else:
                                            print(hw_data[i]['assert_name'])
                                    elif length == 5:  # 验证发布时间
                                        self.release.assign_button()  # 点击 发布作业 按钮

                                        if not Toast().find_toast(hw_data[i]['assert_date']):
                                            print('★★★ Error - 未弹toast:', hw_data[i]['assert_date'])
                                        else:
                                            print(hw_data[i]['assert_date'])
                                    else:  # 发布成功
                                        self.release.assign_button()  # 点击 发布作业 按钮

                                        if not Toast().find_toast('作业已存入定时作业，点击“首页”右上角图标可查看'):
                                            print('★★★ Error - 未弹toast: "作业已存入定时作业，点击“首页”右上角图标可查看"')
                                        else:
                                            print('作业已存入定时作业，点击“首页”右上角图标可查看')

                                        print('修改发布时间为：', date)
                                        if self.home.wait_check_page():
                                            self.home.timing_button()  # 定时作业 按钮
                                            if self.draft.wait_check_page():
                                                self.judge_result_operation(date, hw_data[i]['name'],
                                                                            hw_data[i]['mode'])

                                                if self.draft.wait_check_hw_list_page():
                                                    title = self.draft.draft_name()  # name 元素
                                                    title[random.randint(0, len(title)-1)].click()  # 进入编辑页面

                                    if length == 5:  #
                                        if self.release.wait_check_release_list_page():
                                            self.release.timing_show().click()  # 时间展示 元素
                                            if self.release.wait_check_time_list_page():
                                                mode = 'up'
                                                if hw_data[i]['dire'] == 'up':
                                                    mode = 'down'
                                                self.release.get_assign_date(int(hw_data[i]['date']), mode)
                                                self.release.confirm_button()  # 点击 确定按钮

    @teststeps
    def modify_publish_time(self, i, length):
        """修改发布时间"""
        if length in (2, 3):
            item = self.release.number_input()  # 获取当前展示的时间
            date = []
            for j in range(len(item)):
                date.append(item[j].text)

            if int(date[1]) < 10:
                date[1] = '0' + date[1]
        else:
            date = self.release.get_assign_date(int(hw_data[i]['date']), hw_data[i]['dire'])
        self.release.confirm_button()  # 点击 确定按钮

        return date

    @teststeps
    def judge_result_operation(self, date, modify, mode):
        """验证 修改结果
        :param date: 创建日期
        :param modify:修改后的作业名称
        :param mode: 修改后的作业模式
        """
        print('-------------------验证修改结果--------------------')
        if self.draft.wait_check_page():  # 页面检查点
            if self.draft.wait_check_hw_list_page():
                hw_name = []
                date_list = []
                self.draft.get_hw_list(hw_name, date_list)  # 定时作业列表

                count = []
                for i in range(len(hw_name)):
                    name = hw_name[i][5:-4].replace(" ", "")
                    modify = modify.replace(" ", "")

                    if name in modify:
                        if date[1:] == date_list[i]:  # 验证布置结果
                            count.append(i)
                            print('保存定时作业成功')
                            break

                if not count:
                    print('★★★ Error -保存定时作业失败', modify, date[1:])
                else:
                    title = self.draft.draft_name()  # name
                    self.home.open_menu(title[count[0]])  # 作业条目 左键长按
                    self.home.menu_item(0)  # 编辑
                    if self.release.wait_check_release_list_page():
                        self.release.judge_hw_mode_operation(mode)
                        self.home.back_up_button()  # 为了与 保存定时作业失败时一致
        else:
            print('★★★ Error -未进入草稿页')
