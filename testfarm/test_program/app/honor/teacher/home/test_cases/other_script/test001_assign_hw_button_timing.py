#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest
import os,sys
print('当前路径：',os.getcwd())
sys.path.append('./testfarm/test_program/')
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.object_page.draft_page import DraftPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.home.test_data.draft_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class AssignHw(unittest.TestCase):
    """布置 定时作业"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.draft = DraftPage()
        cls.get = GetAttribute()
        cls.toast = Toast()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_assign_hw_timing(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_page():  # 页面检查点
                self.home.assign_hw_button()  # 布置作业 按钮

                if self.basket.wait_check_page():  # 页面检查点
                    date = 0
                    if self.home.wait_check_empty_tips_page():
                        self.basket.empty_text()  # 空白文案
                        if self.draft.add_to_basket():  # 若题筐为空，先加题进题筐
                            date = self.timing_operation()  # 布置定时作业 具体操作
                    elif self.basket.wait_check_list_page():
                        if self.draft.question_bank_operation():  # 题筐内具体操作
                            date = self.timing_operation()  # 布置定时作业 具体操作
                    self.judge_assign_operation(date)  # 验证具体操作
        else:
            self.toast.get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def timing_operation(self):
        """布置定时作业 具体操作"""
        print('------------------布置定时作业------------------')
        self.release.help_button()  # 点击定时 帮助按钮
        if not self.toast.find_toast('1. 无定时，作业将立即布置。\n2. 有定时，作业将存入“首页” - “定时作业”中，在您设定的时间自动布置。'):
            print('★★★ Error- 点击定时 帮助按钮 未弹toast')

        check = self.release.timing_check_box()  # 定时单选框
        if not self.get.checked(check):  # 定时单选框 验证
            print("★★★ Error- 定时单选框 默认勾选")
        else:
            item = self.release.timing_show()  # 时间展示 元素
            if self.get.enabled(item) != 'false':  # 时间展示 元素 验证
                print("★★★ Error- 未勾选 单选框时, 时间展示元素enabled属性为true")
            else:
                item.click()  # 时间展示 元素

        check.click()  # 勾选 单选框
        self.release.assign_button()  # 点击 发布作业 按钮
        if not self.toast.find_toast('请输入作业名称'):  # 作业名称 验证
            print('★★★ Error- 未弹toast: 请输入作业名称')

        name = self.release.hw_name_edit()  # 作业名称 编辑框
        name.send_keys(r'' + gv.HW_TIME)  # name
        print('作业名称：', gv.HW_TIME)
        self.release.assign_button()  # 点击 发布作业 按钮

        if not self.toast.find_toast("请选择学生"):  # 选择学生 验证
            print('★★★ Error- 未弹toast: 请选择学生')

        self.release.hw_vanclass_list()  # 班级列表
        self.release.choose_class_operation()  # 选择学生
        if self.release.wait_check_release_list_page():
            self.release.assign_button()  # 点击 发布作业 按钮
            if not self.toast.find_toast('请选择发送时间'):  # 发送时间 验证
                print('★★★ Error- 未弹toast: 请选择发送时间')

            if self.release.wait_check_release_list_page():
                SwipeFun().swipe_vertical(0.5, 0.15, 0.7)
                self.release.timing_show().click()  # 时间展示 元素
                if self.release.wait_check_time_list_page():
                    self.release.confirm_button()  # 点击 确定按钮
                    if self.release.wait_check_release_list_page():
                        self.release.assign_button()  # 点击 发布作业 按钮
                        if not self.toast.find_toast('可选当前时间5分钟后的时间'):  # 当前时间5分钟后的时间 验证
                            print('★★★ Error- 未弹toast: 可选当前时间5分钟后的时间')

            if self.release.wait_check_release_list_page():
                self.release.timing_show().click()  # 时间展示 元素
                if self.release.wait_check_time_list_page():
                    date = self.release.get_assign_date()  # 修改时间 并获取修改后时间
                    print('设置发布时间为：', date)
                    self.release.confirm_button()  # 点击 确定按钮

                    if self.release.wait_check_release_list_page():
                        self.release.assign_button()  # 点击 发布作业 按钮

                        if not self.toast.find_toast('作业已存入定时作业，点击“首页”右上角图标可查看'):  # 当前时间5分钟后的时间 验证
                            print('★★★ Error- 未弹toast: 作业已存入定时作业，点击“首页”右上角图标可查看')

                        if self.question.wait_check_page('题单', 5):
                            self.home.click_tab_hw()  # 返回主界面

                        return date

    @teststeps
    def judge_assign_operation(self, date):
        """验证布置结果"""
        print('------------------验证布置结果-------------------')
        if self.home.wait_check_page():
            self.home.timing_button()  # 定时作业 按钮

            if self.draft.wait_check_page():  # 页面检查点
                if self.draft.wait_check_hw_list_page():
                    name = self.draft.draft_name()  # name
                    create = self.draft.draft_time()  # 发布时间

                    var = []
                    datelist = []
                    for i in range(len(create)):
                        print(name[i].text, '\n',
                              create[i].text)
                        print('----------------------')

                        content = []
                        var.append(name[i].text.split()[1])  # name
                        item = create[i].text[7:].split()  # 发布时间
                        content.extend([item[0].split('/')[0], item[0].split('/')[1], item[2].split(':')[0], item[2].split(':')[1]])

                        datelist.append(content)
                    print('---------------------------------------')

                    if gv.HW_TIME not in var:  # 验证布置结果
                        print('★★★ Error -保存定时作业失败', var, gv.HW_TIME)
                    elif date[1:] not in datelist:
                        print('★★★ Error -保存定时作业失败', date[1:], datelist)
                    else:
                        print('保存定时作业成功')
                elif self.home.wait_check_empty_tips_page():
                    print('★★★ Error -暂无数据，保存定时作业失败')

                self.home.back_up_button()  # 返回主界面

