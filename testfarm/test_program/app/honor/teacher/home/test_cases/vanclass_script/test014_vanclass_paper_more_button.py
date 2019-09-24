#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.paper_detail_page import PaperPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Homework(unittest.TestCase):
    """试卷 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.paper = PaperPage()
        cls.van = VanclassPage()
        cls.detail = VanclassDetailPage()
        cls.info = DynamicPage()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_more_button(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            var = self.detail.edit_into_operation(gv.VANCLASS, gv.PAPER_TITLE, self.van.vanclass_paper, gv.PAPER)  # 进入 班级试卷

            if self.paper.wait_check_page():  # 页面检查点
                self.paper.more_button()  # 更多 按钮
                if self.paper.wait_check_more_page():
                    self.paper.edit_delete_button(0)  # 编辑按钮
                    if self.paper.wait_check_edit_page():  # 页面检查点
                        van = self.edit_paper_operation()  # 编辑 具体操作

                        self.judge_result(var, van)  # 保存编辑时，验证 结果
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def edit_paper_operation(self):
        """编辑试卷 详情页"""
        self.home.tips_content_commit()  # 温馨提示 页面

        if self.paper.wait_check_edit_page():  # 页面检查点
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

                choose = self.release.choose_class_operation()  # 选择班级 学生
                if self.paper.wait_check_edit_page():  # 页面检查点
                    self.paper.assign_button()  # 布置试卷 按钮
                    self.home.tips_content_commit()  # 温馨提示 页面
                    print('保存编辑该试卷')

                    return choose

    @teststeps
    def judge_result(self, var, vanclass):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():  # 页面检查点
            self.home.paper_icon()  # 进入试卷 最近动态页面

            if self.info.wait_check_paper_page():  # 页面检查点
                if self.info.wait_check_list_page():
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

                                if self.info.wait_check_paper_page():  # 页面检查点
                                    self.home.back_up_button()  # 返回主界面
                            else:  # 恢复测试数据
                                print('编辑保存成功')
                                self.delete_commit_operation(name[0], vanclass)  # 删除 具体操作
                            break

    @teststeps
    def delete_commit_operation(self, hw, vanclass):
        """删除作业 具体操作"""
        print('---------------------删除作业---------------------')
        hw.click()
        if self.paper.wait_check_page():  # 页面检查点
            self.paper.delete_cancel_operation()  # 删除试卷 具体操作

        if self.paper.wait_check_page():  # 页面检查点
            print('-------------恢复测试数据-------------')
            self.paper.more_button()  # 更多 按钮
            if self.paper.wait_check_more_page():
                self.paper.edit_delete_button(1)  # 删除按钮
                if self.paper.wait_check_tips_page():
                    self.home.commit_button().click()  # 确定按钮
                    print('确定删除')

                    if self.info.wait_check_paper_page():  # 页面检查点
                        SwipeFun().swipe_vertical(0.5, 0.2, 0.8)
                        if self.info.wait_check_list_page():
                            print('--------------验证 删除 结果--------------')
                            name = self.info.hw_name()  # 作业name
                            van = self.info.hw_vanclass()  # 班级
                            if name[0].text == vanclass[0]:
                                if van[0].text == vanclass[1][0]:
                                    print('★★★ Error- 作业删除不成功', van[0].text, vanclass[1][0])
                                else:  # 删除成功
                                    print('删除成功')
                            else:
                                print('删除成功')
                        elif self.detail.wait_check_empty_tips_page():
                            print('删除成功')

                        if self.info.wait_check_list_page():
                            self.home.back_up_button()  # 返回主界面
