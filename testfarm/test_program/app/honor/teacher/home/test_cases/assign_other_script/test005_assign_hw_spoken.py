#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.test_bank.object_page.test_spoken_detail_page import SpokenPage
from app.honor.teacher.home.test_data.draft_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class AssignHw(unittest.TestCase):
    """布置作业 - 包含口语"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.filter = FilterPage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.detail = SpokenPage()
        cls.hw_detail = HwDetailPage()

        cls.van = VanclassPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_assign_hw_contain_spoken(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 从首页进入题库tab

            if self.question.wait_check_page('题单'):
                self.question.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                    self.filter.click_game_list()  # 点击 大题
                    if self.filter.wait_check_page():
                        title = self.filter.label_name()  # 标签

                        spoken = ['口语看读', '口语跟读']
                        index = random.randint(0, len(spoken)-1)
                        for i in range(len(title)):
                            if title[i].text == spoken[index]:
                                title[i].click()  # 口语跟读/看读
                                break
                        self.filter.commit_button()  # 点击 确定按钮

                        self.add_to_basket()  # 先加题进题筐，后布置

                        if self.question.wait_check_game_type_page():  # 页面检查点
                            self.question.filter_button()  # 筛选按钮

                            if self.filter.wait_check_page():
                                self.filter.click_question_menu()  # 题单
                                self.filter.commit_button()  # 点击 确定按钮
                                if self.question.wait_check_page('题单'):
                                    self.home.click_tab_hw()  # 返回主界面
                else:
                    print('★★★ Error- 未进入筛选界面')
            else:
                print('★★★ Error- 未进入题库主界面')
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def add_to_basket(self):
        """加口语 进 题筐"""
        if self.question.wait_check_game_type_page():  # 页面检查点
            item = self.question.question_name()  # 获取
            item[0][2].click()  # 点击第3道题

            if self.detail.wait_check_page():  # 页面检查点
                if self.detail.wait_check_list_page():
                    print('加题进题筐')
                    self.detail.put_to_basket_button()  # 点击加入题筐按钮

                    if self.detail.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回按钮

                        if self.question.wait_check_game_type_page():  # 页面检查点
                            self.question.question_basket()  # 题筐按钮

                            if self.basket.wait_check_page():  # 页面检查点
                                if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                    print('★★★ Error- 加入题筐失败')

                                    self.home.back_up_button()
                                elif self.basket.wait_check_list_page():
                                    self.assign_operation()  # 获取题筐所有题 & 布置作业
                            else:
                                print('★★★ Error- 未进入 题筐页面')
                        else:
                            print('★★★ Error- 未返回 题库页面')
            else:
                print('★★★ Error- 未进入 题单详情页')

    @teststeps
    def assign_operation(self):
        """获取题筐所有题 & 布置作业"""
        check = self.basket.check_button()  # 单选按钮
        for i in range(len(check)):
            check[i].click()

        self.basket.assign_button().click()  # 点击布置作业 按钮
        self.home.tips_content_commit()  # 温馨提示 页面

        if self.release.wait_check_release_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                print('--------------发布作业 页面--------------')
                self.release.assign_button()  # 发布作业 按钮
                self.release.tips_page_info()  # 提示框

                if Toast().find_toast('请输入作业名称'):
                    print('请先输入作业名称, 再布置')
                    print('---------------------------')

                self.release_hw_operation()  # 发布作业 详情页

    @teststeps
    def release_hw_operation(self):
        """发布作业 详情页"""
        if self.release.wait_check_release_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                name = self.release.hw_name_edit()  # 作业名称 编辑框
                print(name.text)
                name.send_keys(gv.SPOKEN_ASSIGN)  # 修改name
                print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

                print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
                self.release.hw_mode_operation()  # 作业 达标模式
                self.release.hw_vanclass_list()  # 班级列表
                choose = self.release.choose_class_operation()  # 选择班级 学生

                if self.release.wait_check_release_page():  # 页面检查点
                    self.release.hw_adjust_order()  # 调整题目顺序

                    if self.release.wait_check_release_page():  # 页面检查点
                        self.release.assign_button()  # 发布作业 按钮
                        if not Toast().find_toast('达标模式不能包含口语题'):  # 达标模式不能包含口语题
                            print('★★★ Error - 未弹toast:', '达标模式不能包含口语题')
                        else:
                            print('达标模式不能包含口语题')
                            self.release.hw_mode_operation('free')  # 作业 达标模式
                            self.release.assign_button()  # 发布作业 按钮

                        self.release.tips_page_info()  # 提示框

                        if Toast().find_toast('作业名称不能与当天布置的其他作业相同'):  # 若当天布置的作业有重名，获取toast
                            print('作业名称不能与当天布置的其他作业相同')
                            if self.release.wait_check_release_page():  # 页面检查点
                                self.home.back_up_button()
                                if self.basket.wait_check_page():  # 页面检查点
                                    self.home.back_up_button()
                                    if self.question.wait_check_page('搜索'):  # 页面检查点  由题筐进入；else:  由布置作业按钮 进入
                                        self.home.click_tab_hw()  # 返回 主界面
                        else:
                            if self.question.wait_check_page('搜索'):  # 页面检查点
                                self.home.click_tab_hw()  # 返回 主界面

                            self.judge_result_operation(choose[0], gv.SPOKEN_ASSIGN)  # 验证布置结果
                    else:
                        print('选择班级 学生 -未返回 发布作业 页面')
                else:
                    print('调整题目顺序 -未返回 发布作业 页面')
            else:
                print('★★★ Error- 未进入 发布作业 页面')

    @teststeps
    def judge_result_operation(self, van, spoken):
        """验证布置结果 具体操作"""
        if self.home.wait_check_list_page():  # 页面检查点
            print('------------------验证布置结果------------------')
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            if self.home.wait_check_list_page():
                name = self.home.item_detail()  # 条目名称
                for i in range(len(name)):
                    var = self.home.vanclass_name(name[i].text)  # 班级名
                    if var == van:
                        name[i].click()  # 进入班级

                        if self.van.wait_check_page(var):  # 页面检查点
                            if self.van.wait_check_list_page():
                                hw = self.van.hw_name()  # 作业名
                                title = self.home.vanclass_name(hw[0].text)
                                if title != spoken:
                                    print('★★★ Error- 布置作业失败', spoken, title)
                                else:  # 恢复测试数据
                                    print('布置作业成功')
                            elif self.home.wait_check_empty_tips_page():
                                print('★★★ Error-班级动态为空, 布置作业失败')
                        else:
                            print('★★★ Error- 未进入班级:', van)

                            self.home.back_up_button()
                        break
        else:
            self.login.screen_shot('assign_hw_spoken_未返回主界面')
