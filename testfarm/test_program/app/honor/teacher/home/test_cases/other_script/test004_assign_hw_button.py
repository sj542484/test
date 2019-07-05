#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.draft_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class AssignHw(unittest.TestCase):
    """布置 作业"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.filter = FilterPage()
        cls.detail = QuestionDetailPage()
        cls.hw_detail = HwDetailPage()

        cls.van = VanclassPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_assign_button(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.assign_hw_button()  # 布置作业 按钮

            if self.basket.wait_check_page():  # 页面检查点
                # 由题筐进入还是布置作业按钮进入返回界面不同
                if self.home.wait_check_empty_tips_page():
                    self.basket.empty_text()  # 空白文案
                    self.add_to_basket()  # 若题筐为空，先加题进题筐
                elif self.basket.wait_check_list_page():
                    self.assign_operation()  # 获取题筐所有题 & 布置作业
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def add_to_basket(self):
        """加题单 进 题筐"""
        self.home.back_up_button()  # 返回按钮
        if self.home.wait_check_page():
            self.question.judge_into_tab_question()  # 从首页进入题库tab

            if self.question.wait_check_page('题单'):
                self.question.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                        title = self.filter.label_name()  # 标签
                        title[9].click()  # 口语跟读/看读
                        self.filter.commit_button()  # 点击 确定按钮

                        if self.question.wait_check_game_type_page():  # 页面检查点
                            item = self.question.question_name()  # 获取
                            item[0][2].click()  # 点击第3道题

                            if self.detail.wait_check_page():  # 页面检查点
                                if self.detail.wait_check_list_page():
                                    print('加题进题筐')
                                    self.detail.put_to_basket_button()  # 点击加入题筐按钮

                                    if self.detail.wait_check_page():  # 页面检查点
                                        self.home.back_up_button()  # 返回按钮

                                        if self.question.wait_check_page('搜索'):  # 页面检查点
                                            self.question.question_basket()  # 题筐按钮

                                            if self.basket.wait_check_page():  # 页面检查点
                                                if self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                                    print('★★★ Error- 加入题筐失败')

                                                    self.home.back_up_button()
                                                    if self.question.wait_check_page('搜索'):  # 页面检查点
                                                        self.home.click_tab_hw()  # 返回 主界面
                                                elif self.basket.wait_check_list_page():
                                                    var = self.assign_operation()  # 获取题筐所有题 & 布置作业

                                                    return var
                                            else:
                                                print('未进入 题筐页面')
                                        else:
                                            print('未返回 题库页面')
                            else:
                                print('未进入 题单详情页')

    @teststeps
    def assign_operation(self):
        """获取题筐所有题 & 布置作业"""
        var = self.basket.question_name()  # 获取题筐所有题
        check = self.basket.check_button()  # 单选按钮
        type = self.basket.question_type()  # 小游戏类型

        if len(var) > 1:
            for i in range(len(type)-1):
                if type[i].text not in ['口语看读', '口语跟读']:
                    check[i].click()
                    if i ==1:
                        break
        else:
            check[0].click()

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

                choose = self.release_hw_operation()  # 发布作业 详情页

                return choose

    @teststeps
    def release_hw_operation(self):
        """发布作业 详情页"""
        if self.release.wait_check_release_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                name = self.release.hw_name_edit()  # 作业名称 编辑框
                print(name.text)
                name.send_keys(r'' + gv.HW_ASSIGN)  # 修改name
                print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

                print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
                self.release.hw_mode_operation()  # 作业模式 操作
                self.release.hw_vanclass_list()  # 班级列表
                choose = self.release.choose_class_operation()  # 选择班级 学生

                if self.release.wait_check_release_page():  # 页面检查点
                    self.release.hw_adjust_order()  # 调整题目顺序

                    if self.release.wait_check_release_page():  # 页面检查点
                        self.release.assign_button()  # 发布作业 按钮
                        self.release.tips_page_info()  # 提示框

                        if Toast().find_toast('作业名称不能与当天布置的其他作业相同'):  # 若当天布置的作业有重名，获取toast
                            print('作业名称不能与当天布置的其他作业相同')
                            self.home.back_up_button()
                            if self.basket.wait_check_page():
                                self.home.back_up_button()
                                if self.question.wait_check_page('搜索'):  # 页面检查点  由题筐进入；else:  由布置作业按钮 进入
                                    self.home.click_tab_hw()  # 返回 主界面
                        else:
                            if self.question.wait_check_page('搜索'):  # 页面检查点  由题筐进入；else:  由布置作业按钮 进入
                                self.home.click_tab_hw()  # 返回 主界面

                            self.judge_result_operation(choose[0])  # 验证布置结果
                    else:
                        print('选择班级 学生 -未返回 发布作业 页面')
                else:
                    print('调整题目顺序 -未返回 发布作业 页面')
            else:
                print('未进入 发布作业 页面')

    @teststeps
    def judge_result_operation(self, van):
        """验证布置结果 具体操作"""
        if self.home.wait_check_page():  # 页面检查点
            print('------------------验证布置结果------------------')
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                print(var)
                if var == van:
                    name[i].click()  # 进入班级

                    if self.van.wait_check_page(var):  # 页面检查点
                        if self.van.wait_check_list_page():
                            hw = self.van.hw_name()  # 作业名
                            title = self.home.vanclass_name(hw[0].text)
                            if title != gv.HW_ASSIGN:
                                print('★★★ Error- 布置作业失败', gv.HW_ASSIGN, title)
                            else:  # 恢复测试数据
                                print('布置作业成功')
                                hw[0].click()
                                if self.hw_detail.wait_check_page():  # 页面检查点
                                    self.hw_detail.delete_commit_operation()  # 删除作业 具体操作
                        elif self.home.wait_check_empty_tips_page():
                            print('★★★ Error-班级动态为空, 布置作业失败')

                        if self.van.wait_check_page(van):
                            self.home.back_up_button()  # 返回 主界面
                    else:
                        print('未进入班级:', van)
                    break
