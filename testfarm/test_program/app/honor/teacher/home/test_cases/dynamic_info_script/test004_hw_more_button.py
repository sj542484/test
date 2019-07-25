#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page import ReleasePage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.test_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Homework(unittest.TestCase):
    """习题 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.detail = HwDetailPage()
        cls.info = DynamicPage()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_hw_more_button(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_list_page():  # 页面加载完成 检查点
                self.home.hw_icon()  # 进入习题 最近动态页面

                if self.info.wait_check_hw_page():  # 页面检查点
                    if self.info.wait_check_list_page():
                        var = self.info.into_hw(gv.HW_TITLE)  # 进入 作业包

                        if self.detail.wait_check_page():  # 页面检查点
                            self.detail.delete_cancel_operation()  # 删除 具体操作

                            if self.detail.wait_check_page():  # 页面检查点
                                self.detail.more_button()  # 更多 按钮
                                if self.detail.wait_check_more_page():
                                    self.detail.edit_delete_button(0)  # 编辑按钮
                                    van = self.edit_hw_operation()  # 编辑 具体操作

                                    self.judge_result(var, van)  # 保存编辑,取消删除时，验证 结果
                        else:
                            print('未进入 作业包 %s 页面' % var)
                            self.home.back_up_button()  # 返回 习题动态页面
                    elif self.home.wait_check_empty_tips_page():
                        print('最近习题动态页面为空')
                        self.home.back_up_button()  # 返回主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def edit_hw_operation(self):
        """编辑作业 详情页"""
        self.home.tips_content_commit()  # 温馨提示 页面

        if self.detail.wait_check_edit_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                print('-------------------编辑作业 详情页-------------------')
                name = self.release.hw_name_edit()  # 作业名称 编辑框
                name.send_keys(r'' + gv.HW_TEST)  # 修改name
                print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

                print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
                self.release.hw_mode_operation()  # 作业模式 操作
                self.release.hw_vanclass_list()  # 班级列表
                choose = self.release.choose_class_operation()  # 选择班级 学生

                if self.release.wait_check_release_page():  # 页面检查点
                    self.release.hw_adjust_order()  # 调整题目顺序

                    if self.release.wait_check_release_page():  # 页面检查点
                        self.detail.assign_button()  # 发布作业 按钮
                        if Toast().find_toast('作业已成功布置'):
                            print('作业已成功布置')
                        return choose

    @teststeps
    def judge_result(self, var, vanclass):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入习题 最近动态页面

            if self.info.wait_check_hw_page():  # 页面检查点
                if self.info.wait_check_list_page():
                    print('--------------验证 编辑/删除 结果--------------')
                    name = self.info.hw_name()  # 作业name
                    van = self.info.hw_vanclass()  # 班级
                    for i in range(len(name)):
                        if name[i].text == gv.HW_TEST:
                            if van[i].text != vanclass[0]:
                                print('★★★ Error- 作业编辑不成功', van[i].text, vanclass[0])

                                if self.info.wait_check_list_page():
                                    self.home.back_up_button()  # 返回主界面
                            else:  # 编辑保存成功, 恢复测试数据
                                print('编辑保存成功')
                                name[i].click()
                                if self.detail.wait_check_page():  # 页面检查点
                                    print('-------------恢复测试数据-------------')
                                    self.detail.more_button()  # 更多 按钮
                                    if self.detail.wait_check_more_page():
                                        self.detail.edit_delete_button(0)  # 编辑按钮

                                        if self.home.wait_check_tips_page():  # 温馨提示 页面
                                            self.home.commit_button()  # 确定 按钮

                                        if self.detail.wait_check_edit_page():  # 页面检查点
                                            if self.release.wait_check_release_list_page():
                                                name = self.release.hw_name_edit()  # 作业名称 编辑框
                                                name.send_keys(var)  # 修改name

                                                self.release.hw_mode_free().click()  # 修改 作业模式 操作

                                                self.release.choose_class_operation()  # 取消选择班级
                                                self.detail.assign_button()  # 发布作业 按钮

                            break
