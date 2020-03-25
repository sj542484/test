#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_paper_page import DynamicPaperPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps
from conf.decorator_pc import teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.vue_context import VueContext


class Paper(unittest.TestCase):
    """试卷 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.info = DynamicPaperPage()
        cls.release = ReleasePage()
        cls.report = PaperReportPage()
        cls.my_toast = MyToast()
        cls.vue = VueContext()
        cls.van_paper = VanclassPaperPage()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Paper, self).run(result)

    @testcase
    def test_paper_more_button(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        if self.home.wait_check_page():  # 页面检查点
            self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 有班级检查点
            self.home.paper_icon()  # 进入卷子 最近动态页面

            if self.info.wait_check_app_page():  # 页面检查点
                self.vue.switch_h5()  # 切到web

                if self.info.wait_check_page():  # 页面检查点
                    if self.info.wait_check_no_hw_page():
                        print('最近卷子动态页面为空')
                        self.info.back_up_button()
                        self.assertFalse(self.info.wait_check_no_hw_page(), self.info.dynamic_empty_tips)
                    else:
                        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                        self.info.help_operation()  # 右上角 提示按钮

                        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                        self.info.hw_list_operation()  # 列表
                        var = self.info.into_hw()[0]  # 进入 作业包
                        self.vue.app_web_switch()  # 切到apk 再切到vue

                        if self.report.wait_check_page():
                            self.van_paper.more_button()  # 更多 按钮
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                            if self.van_paper.wait_check_more_page():
                                self.van_paper.more_edit_button()  # 编辑按钮
                                self.vue.switch_app()  # 切到apk
                                van = self.edit_paper_operation()  # 编辑 具体操作

                                self.judge_result(var, van)  # 保存编辑时，验证 结果

    @teststeps
    def edit_paper_operation(self):
        """编辑试卷 详情页"""
        self.home.tips_content_commit(5)  # 温馨提示 页面
        if self.report.wait_check_edit_page():  # 编辑页面检查点
            if self.release.wait_check_release_list_page():
                print('------------------编辑试卷 详情页------------------')
                van = self.release.van_name()  # 班级 元素
                button = self.release.choose_button()  # 单选
                count = self.release.choose_count()  # 班级描述

                van_class = []  # 班级名
                if len(button) != len(van):
                    print('★★★ Error- 单选框的个数与班级个数不同', len(button), len(van))
                else:
                    for i in range(len(count)):
                        print(van[i].text, '\n',
                              count[i].text)
                        print('-------')
                        van_class.append(van[i].text)

                choose = self.release.choose_class_operation()  # 选择班级 学生

                if self.report.wait_check_edit_page():
                    self.report.assign_button()  # 布置试卷 按钮
                    self.home.tips_content_commit()  # 温馨提示 页面
                    # self.my_toast.toast_assert(self.name, Toast().toast_operation('布置成功'))
                    print('保存编辑该试卷')

                    return choose

    @teststeps
    def judge_result(self, var, van_class):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():
            self.home.paper_icon()  # 进入试卷 最近动态页面

            if self.info.wait_check_app_page():  # 页面检查点
                self.vue.switch_h5()  # 切到web

                if self.info.wait_check_page():  # 页面检查点
                    self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                    print('-------------------验证 编辑 结果-------------------')
                    name = self.info.hw_name()  # 作业name
                    van = self.info.hw_vanclass()  # 班级

                    count = []
                    for i in range(len(name)):
                        if name[i].text == var:
                            count.append(i)
                            if van[i].text != van_class[0]:
                                print('★★★ Error- 试卷编辑不成功', van[i].text, van_class[0])

                                if self.info.wait_check_page():  # 页面检查点
                                    self.info.back_up_button()  # 返回主界面
                            else:  # 恢复测试数据
                                print('编辑保存成功')
                                break

                    self.assertFalse(len(count) == 0, '★★★ Error -试卷编辑保存不成功, {}'.format(var, van_class))

                    name[count[0]].click()
                    self.vue.app_web_switch()  # 切到apk 再切到vue
                    if self.report.wait_check_page():
                        self.van_paper.delete_cancel_operation()  # 删除试卷 具体操作

                        if self.report.wait_check_page():
                            print('-------------恢复测试数据-------------')
                            self.van_paper.more_button()  # 更多 按钮
                            self.vue.app_web_switch()  # 切到apk 再切到vue

                            if self.van_paper.wait_check_more_page():
                                self.van_paper.more_edit_button()  # 编辑按钮
                                self.vue.switch_app()  # 切到apk 再切到vue

                                if self.report.wait_check_edit_page():
                                    self.release.choose_class_operation()  # 取消选择班级

                                    self.report.assign_button()  # 布置试卷 按钮
                                    self.home.tips_content_commit()  # 温馨提示 页面
