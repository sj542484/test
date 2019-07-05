#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.draft_page import DraftPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class TimingHw(unittest.TestCase):
    """定时作业 - 切换班级/时间tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.draft = DraftPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_timing_hw_list(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.timing_button()  # 定时作业 按钮

            if self.draft.wait_check_page():  # 页面检查点
                if self.draft.wait_check_hw_list_page():
                    self.timing_list_operation()  # 获取目前 定时作业数
                elif self.home.wait_check_empty_tips_page():
                    print('暂无 定时作业')

            if self.draft.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def timing_list_operation(self):
        """定时作业 列表 具体操作"""
        self.draft.all_vanclass()  # 点击 班级
        if self.draft.wait_check_tab_page(5):
            vanclass = self.draft.check_text()  # 班级元素
            print('------------------所有班级-----------------')
            for i in range(len(vanclass)):
                print(vanclass[i].text)

            var = 0  # 为节省运行时间，只 切换班级3次
            for k in range(len(vanclass)):
                print('+++++++++++++++++++++++++++++++++++++++++++')
                van = vanclass[k].text  # 班级名
                vanclass[k].click()  # 选择班级
                var += 1
                print('班级:', van)
                if self.draft.wait_check_page(5):
                    self.draft.all_time()  # 发布时间元素
                    if self.draft.wait_check_tab_page(5):
                        spend = self.draft.check_text()  # 时间元素

                        for j in range(len(spend)):
                            title = spend[j].text  # 发布时间
                            spend[j].click()  # 选择时间
                            print('--------------%s---------------' % title)

                            if self.home.wait_check_empty_tips_page():
                                print('暂无 定时作业')
                            elif self.draft.wait_check_hw_list_page(5):
                                name = self.draft.draft_name()
                                create = self.draft.draft_time()
                                for i in range(len(create)):
                                    print(name[i].text, '\n',
                                          create[i].text)
                                    print('-------------------')

                            if j != len(spend)-1:
                                self.draft.all_time()  # 发布时间元素
                                if self.draft.wait_check_tab_page(5):
                                    spend = self.draft.check_text()  # 时间元素

                if var != 2:
                    self.draft.all_vanclass()  # 点击 班级
                    if self.draft.wait_check_tab_page(5):
                        vanclass = self.draft.check_text()  # 班级元素
                else:
                    break
