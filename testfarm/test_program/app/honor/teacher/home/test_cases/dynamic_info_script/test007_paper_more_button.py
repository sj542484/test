#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from testfarm.test_program.app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.paper_detail_page import PaperPage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.test_data.dynamic_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


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
        cls.info = DynamicPage()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_more_button(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_list_page():  # 页面加载完成 检查点
                self.home.paper_icon()  # 进入卷子 最近动态页面

                if self.info.wait_check_paper_page():  # 页面检查点
                    if self.info.wait_check_list_page():
                        var = self.info.into_hw(gv.PAPER_TITLE)  # 进入 作业包

                        if self.paper.wait_check_page():  # 页面检查点
                            self.paper.more_button()  # 更多 按钮
                            if self.paper.wait_check_more_page():
                                self.paper.edit_delete_button(0)  # 编辑按钮
                                if self.paper.wait_check_edit_page():  # 页面检查点
                                    van = self.edit_paper_operation()  # 编辑 具体操作

                                    self.judge_result(var, van)  # 保存编辑时，验证 结果
                        else:
                            print('未进入试卷 %s 页面' % var)
                            self.home.back_up_button()  # 返回 试卷动态页面
                    else:
                        print('最近卷子动态页面为空')
                        self.home.back_up_button()  # 返回主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

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
                    name = self.info.hw_name()  # 作业name
                    van = self.info.hw_vanclass()  # 班级
                    for i in range(len(name)):
                        if name[i].text == var:
                            if van[i].text != vanclass[0]:
                                print('★★★ Error- 作业编辑不成功', van[i].text, vanclass[0])

                                if self.info.wait_check_paper_page():  # 页面检查点
                                    self.home.back_up_button()  # 返回主界面
                            else:  # 恢复测试数据
                                print('编辑保存成功')
                                name[i].click()
                                if self.paper.wait_check_page():  # 页面检查点
                                    self.paper.delete_cancel_operation()  # 删除试卷 具体操作

                                if self.paper.wait_check_page():  # 页面检查点
                                    print('-------------恢复测试数据-------------')
                                    self.paper.more_button()  # 更多 按钮
                                    if self.paper.wait_check_more_page():
                                        self.paper.edit_delete_button(0)  # 编辑按钮
                                        if self.paper.wait_check_edit_page():  # 页面检查点
                                            self.release.choose_class_operation()  # 取消选择班级

                                            self.paper.assign_button()  # 布置试卷 按钮
                                            self.home.tips_content_commit()  # 温馨提示 页面

                            break
