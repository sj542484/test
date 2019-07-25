#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page import ReleasePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.object_page import DraftPage
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
                date = 0
                if self.home.wait_check_empty_tips_page():
                    print('暂无 定时作业')
                    if self.draft.add_to_basket():  # 若题筐为空，先加题进题筐
                        self.assign_operation()  # 布置定时作业
                        if self.draft.wait_check_hw_list_page():
                            date = self.hw_modify_operation()  # 修改定时作业 具体操作
                elif self.draft.wait_check_hw_list_page():
                    date = self.hw_modify_operation()  # 修改定时作业 具体操作

                self.judge_result_operation(date)  # 验证具体操作
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def assign_operation(self):
        """无定时作业时，布置"""
        if self.release.wait_check_release_list_page():
            name = self.release.hw_name_edit()  # 作业名称 编辑框
            name.send_keys(r'' + gv.HW_TIME)  # name

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
                        if self.home.wait_check_page():
                            self.home.timing_button()  # 定时作业 按钮

                            if self.draft.wait_check_page():  # 页面检查点
                                if not self.draft.wait_check_hw_list_page():
                                    print('★★★ Error- 保存定时作业失败')

    @teststeps
    def timing_list(self):
        """定时作业列表"""
        title = self.draft.draft_name()  # name
        assign = self.draft.draft_time()  # 发布时间

        print('---------------定时作业列表-----------------')
        content = [title[-1].text, assign[-1].text]
        for i in range(len(assign)):
            print(title[i].text, '\n',
                  assign[i].text)
            print('----------------------')
        return title[-1], content

    @teststeps
    def hw_modify_operation(self):
        """ 修改定时作业 具体操作"""
        title = self.draft.draft_name()  # name 元素
        assign = self.draft.draft_time()  # 发布时间
        var = [title[-1].text, assign[-1].text]

        title[-1].click()  # 进入编辑页面
        if self.detail.wait_check_edit_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                print(var[0], '\n', var[1])
                print('-------------------编辑作业页面-------------------')

                name = self.release.hw_name_edit()  # 作业名称 编辑框
                name.send_keys(r'' + gv.HW_MODIFY)  # name
                print('修改作业名称为：', gv.HW_MODIFY)

                self.release.hw_vanclass_list()  # 班级列表
                self.release.choose_class_operation()  # 选择学生

                if self.release.wait_check_release_list_page():
                    SwipeFun().swipe_vertical(0.5, 0.15, 0.7)
                    if self.release.wait_check_release_list_page():
                        self.release.timing_show().click()  # 时间展示 元素

                        if self.release.wait_check_time_list_page():
                            date = self.release.get_assign_date(4)  # 修改时间 并获取修改后时间
                            print('修改发布时间为：', date)
                            self.release.confirm_button()  # 点击 确定按钮

                            if self.release.wait_check_release_list_page():
                                self.release.assign_button()  # 点击 发布作业 按钮

                                if self.question.wait_check_page('题单', 5):
                                    self.home.click_tab_hw()  # 返回主界面
                                return date

    @teststeps
    def judge_result_operation(self, date):
        """验证 修改结果"""
        if self.home.wait_check_page():  # 页面检查点
            self.home.timing_button()  # 定时作业 按钮

            if self.draft.wait_check_page():  # 页面检查点
                if self.draft.wait_check_hw_list_page():
                    print('-------------------验证修改结果--------------------')
                    var = self.timing_list()  # 定时作业列表

                    item = var[1][1][7:].split()  # 发布时间
                    content = [item[0].split('/')[0], item[0].split('/')[1], item[2].split(':')[0], item[2].split(':')[1]]

                    if var[1][0].split()[1] != gv.HW_MODIFY or date[1:] != content:  # 验证布置结果
                        print('★★★ Error -保存定时作业失败', var[1][0].split()[1], gv.HW_MODIFY, '\n', date[1:], content)
                    else:
                        print('保存定时作业成功')
                        title = self.draft.draft_name()  # name
                        assign = self.draft.draft_time()[-1].text  # 发布时间
                        name = title[-1].text

                        self.home.open_menu(title[-1])  # 作业条目 左键长按
                        self.home.menu_item(1)  # 删除
                        print('-------------------删除定时作业-------------------',
                              '\n', name, '\n', assign)
                        self.judge_delete_operation()  # 验证 删除结果

                    if self.draft.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回主界面

    @teststeps
    def judge_delete_operation(self):
        """验证 删除结果"""
        if self.draft.wait_check_page():  # 页面检查点
            SwipeFun().swipe_vertical(0.5, 0.3, 0.7)  # 下拉刷新
            print('-------------------验证删除结果--------------------')
            if self.draft.wait_check_draft_list_page():
                title = self.draft.draft_name()  # name
                print(title[-1].text.split()[1])
                if title[-1].text.split()[1] == gv.HW_MODIFY:  # 验证布置结果
                    print('★★★ Error -删除定时作业失败', title[-1].text == gv.HW_MODIFY)
                else:
                    print('删除定时作业成功')
            elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                print('删除定时作业成功')
