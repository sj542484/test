#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_paper_page import DynamicPaperPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext


class VanclassPaper(unittest.TestCase):
    """试卷 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.report = PaperReportPage()
        cls.van = VanclassPage()
        cls.van_paper = VanclassPaperPage()
        cls.info = DynamicPaperPage()
        cls.vue = VueContext()

        cls.my_toast = MyToast()
        cls.vue = VueContext()
    
        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况
    
    def run(self, result=None):
        self.ass_result = result
        super(VanclassPaper, self).run(result)
        
    @testcase
    def test_paper_more_button(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        var = self.edit_into_operation(gv.VANCLASS, gv.PAPER_TITLE, self.van.vanclass_paper)  # 进入 班级试卷

        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        self.van_paper.more_button()  # 更多 按钮
        self.vue.app_web_switch()  # 切到apk 再切回web
        self.assertEqual(self.van_paper.wait_check_more_page(), True, self.van_paper.more_tips)
        self.van_paper.more_edit_button()  # 编辑按钮
        if self.report.wait_check_edit_page():  # 页面检查点
            choose = self.edit_paper_operation()  # 编辑 具体操作
            if choose:
                self.judge_result(var[0], choose)  # 保存编辑时，验证 结果

    @teststeps
    def edit_paper_operation(self):
        """编辑试卷 详情页"""
        self.home.tips_content_commit()  # 温馨提示 页面

        if self.report.wait_check_edit_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                print('------------------编辑试卷 详情页------------------')
                van = self.release.van_name()  # 班级 元素
                button = self.release.choose_button()  # 单选
                count = self.release.choose_count()  # 班级描述

                vanclass = []  # 班级名
                if len(button) != len(van):
                    print('★★★ Error- 单选框的个数与班级个数不同', len(button), len(van))
                else:
                    for i in range(len(count)):
                        print(van[i].text, '\n',
                              count[i].text)
                        print('-------')
                        vanclass.append(van[i].text)

                choose, cancel = self.release.choose_class_operation()  # 选择班级 学生
                if self.report.wait_check_edit_page():  # 页面检查点
                    self.report.assign_button()  # 布置试卷 按钮
                    self.home.tips_content_commit()  # 温馨提示 页面
                    print('保存编辑该试卷')

                    return choose, cancel

    @teststeps
    def judge_result(self, var, vanclass):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():  # 页面检查点
            SwipeFun().swipe_vertical(0.5, 0.2, 0.8)

        if self.home.wait_check_page():  # 页面检查点
            self.home.paper_icon()  # 进入试卷 最近动态页面
            self.vue.app_web_switch()  # 切到apk 再切回web

            self.assertTrue(self.info.wait_check_page(), self.info.dynamic_tips)  # 页面检查点
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            print('-------------------验证 编辑 结果-------------------')
            name = self.info.hw_name()  # 试卷name
            van = self.info.hw_vanclass()  # 班级

            paper = self.home.brackets_text_out(var)
            print(paper)
            for i in range(len(name)):
                print(name[i].text)
                if name[i].text in paper:
                    if van[i].text != vanclass[0]:
                        print('★★★ Error- 试卷编辑不成功', van[i].text, vanclass[0])

                        if self.info.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回主界面
                    else:  # 恢复测试数据
                        print('编辑保存成功')
                        name[0].click()
                        self.delete_commit_operation(vanclass)  # 删除 具体操作
                    break

    @teststeps
    def delete_commit_operation(self, vanclass):
        """删除试卷 具体操作"""
        print('---------------------删除试卷---------------------')
        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)  # 页面检查点
        self.van_paper.delete_cancel_operation()  # 删除试卷 取消具体操作

        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)  # 页面检查点
        self.van_paper.delete_commit_operation()  # 删除试卷 具体操作

        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_tips)  # 页面检查点
        self.info.swipe_vertical_web(0.5, 0.2, 0.8)
        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)

        if self.info.wait_check_list_page():
            print('--------------验证 删除 结果--------------')
            name = self.info.hw_name()  # 试卷name
            van = self.info.hw_vanclass()  # 班级
            self.assertEqual(name[0].text, vanclass[0], '★★★ Error- 试卷删除不成功, {} {}'.format(van[0].text, vanclass[1][0]))
            self.assertEqual(van[0].text, vanclass[1][0], '★★★ Error- 试卷删除不成功, {} {}'.format(van[0].text, vanclass[1][0]))
            print('删除成功')
        elif self.van_paper.wait_check_empty_tips_page():
            print('删除成功')

        if self.info.wait_check_list_page():
            self.info.back_up_button()  # 返回主界面

    @teststeps
    def edit_into_operation(self, vanclass, title, func):
        """进入 有试卷的班级
        :param vanclass: 不进行编辑的班级
        :param title:  本班/试卷title
        :param func: 进入本班试卷 tab的函数
        """
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点

        van_name = self.home.item_detail()  # 班号+班级名
        for i in range(len(van_name)):
            self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
            van_name = self.home.item_detail()  # 班号+班级名
            van = self.home.vanclass_name(van_name[i].text)  # 班级名
            if van != vanclass:
                van_name[i].click()  # 进入班级

                self.vue.switch_h5()
                self.assertTrue(self.van_paper.wait_check_page(van), self.van_paper.paper_tips)  # 页面检查点
                self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)  # 页面检查点
                func()  # 点击进入 本班试卷/试卷 tab

                self.vue.app_web_switch()  # 切到apk 再切回web
                if self.van_paper.wait_check_empty_tips_page():
                    if self.van_paper.wait_check_page(title.format(van)):  # 页面检查点
                        self.van.back_up_button()  # 返回 答题详情页面
                        if self.van_paper.wait_check_page(van):  # 班级详情 页面检查点
                            self.van.back_up_button()
                else:
                    print('班级:', van)
                    hw_name = self.random_into_operation()  # 随机进入某个试卷 游戏列表
                    print('=====================================')
                    return hw_name, van

    @teststeps
    def random_into_operation(self):
        """随机进入列表中 某个卷子 具体操作
        """
        hw_name = 0
        count = 0
        hw = self.van_paper.hw_name()  # 卷子 name
        for i in range(len(hw)):
            index = 0
            if len(hw) != 1:
                index = random.randint(0, len(hw)-1)

            hw_name = hw[index].text
            print("口语/试卷/卷子:", hw_name)
            hw[index].click()  # 进入试卷
            count += 1
            break

        self.vue.app_web_switch()  # 切到apk 再切回web
        if count == 0:
            print('★★★ Error- 没有可测试的数据')

        return hw_name
