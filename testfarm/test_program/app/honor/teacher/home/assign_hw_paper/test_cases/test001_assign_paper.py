#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
import unittest

from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class AssignPaper(unittest.TestCase):
    """布置试卷"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_detail = VanclassDetailPage()
        cls.van_paper = VanclassPaperPage()
        cls.filter = FilterPage()
        cls.bank = TestBankPage()
        cls.paper = PaperDetailPage()
        cls.release = ReleasePage()
        cls.report = PaperReportPage()

        cls.tips = TipsData()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切到apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(AssignPaper, self).run(result)

    @testcase
    def test_assign_paper(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        if self.home.wait_check_page():  # 页面检查点
            vans = self.home.vanclass_statistic_operation()  # 班级列表统计

            self.bank.judge_into_tab_question()  # 进入首页后 点击 题库tab
            if self.bank.wait_check_page():  # 页面检查点
                self.bank.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():  # 筛选 页面检查点
                    paper = self.filter.test_paper()  # 选择试卷
                    if GetAttribute().selected(paper) == 'false':
                        self.filter.click_test_paper()  # 点击 试卷
                    if self.filter.wait_check_page():  # 筛选 页面检查点
                        self.filter.commit_button()  # 确定按钮

            if self.bank.wait_check_page('试卷'):
                item = self.bank.question_item()  # 试卷数
                index = random.randint(0, len(item[2]) - 1)  # 随机选择标签
                if self.bank.judge_question_lock():
                    while True:
                        if index in item[3]:  # item[3] 锁定icon
                            continue
                        else:
                            break

                item[2][index].click()  # 点击第X个试卷
                if self.paper.wait_check_page():  # 页面检查点
                    title = self.paper_detail_operation()  # 试卷详情页 具体操作

                    van = self.assign_paper_operation(vans)  # 布置试卷 具体操作
                    self.home.click_tab_hw()  # 返回主界面

                    self.bank.judge_into_tab_question('试卷')  # 恢复测试数据
                    print('---恢复 筛选页面---')
                    if self.bank.wait_check_page('试卷'):
                        self.bank.filter_button()  # 筛选按钮
                        if self.filter.wait_check_page():  # 筛选 页面检查点
                            self.filter.reset_button()  # 重置按钮
                            if self.filter.wait_check_page():  # 筛选 页面检查点
                                self.filter.commit_button()  # 确定按钮

                                if self.bank.wait_check_page('题单'):  # 页面检查点  由题筐进入；else:  由布置作业按钮 进入
                                    self.home.click_tab_hw()  # 返回 主界面
                                    self.judge_result_operation(title, van)  # 班级页面 验证结果

    @teststeps
    def paper_detail_operation(self):
        """试卷 详情页"""
        if not self.paper.paper_type():
            print('★★★ Error- 试卷详情页的试卷类型')

        var = self.paper.paper_title()  # 返回试卷名称
        print('---------------------试卷详情页---------------------')

        score = self.paper.score()  # 分值
        if score not in ('100', '120', 'A/B'):
            print(score)
            self.assertIs(score, True, '试卷模式错误')
        else:
            title = self.paper.score_type()
            unit = self.paper.score_unit()
            print(title, score, unit)

            # 考试时间
            title = self.paper.time_title()
            timestr = self.paper.time_str()
            unit = self.paper.time_unit()
            print(title, timestr, unit)

            # 小题数
            title = self.paper.num_title()
            num = self.paper.game_num()
            unit = self.paper.num_unit()
            print(title, num, unit)

            if self.paper.limit_judge():  # 限制
                print(self.paper.limit_type(), self.paper.limit_hand(), self.paper.limit_unit())
            else:
                print(self.paper.limit_type(), self.paper.limit_hand())

            print('----------------')
            self.paper.game_list_title()
            name = self.paper.question_name()  # 小游戏名

            length = len(name)
            if length > 5:
                length = 5
            for i in range(length):
                num = self.paper.num(i)  # 每个小游戏 题数
                print(name[i].text, num.text)
            print('------------------------------------------')
            return var

    @teststeps
    def assign_paper_operation(self, vans):
        """布置试卷 具体操作 """
        self.paper.assign_button()  # 布置试卷 按钮
        if self.paper.wait_check_assign_list_page():
            print('--------------------布置试卷页面--------------------')
            self.paper.assign_title()
            self.paper.assign_hint()
            van = self.release.van_name()  # 班级名
            count = self.release.choose_count()  # 班级描述信息
            print('------------------------')

            content = {}
            for i in range(len(count)):
                name = van[i].text
                num = count[i].text
                print(name, num)
                content[name] = int(re.sub('\D', '', num.split('/')[1]))

            var = {k:v for k, v in vans.items() if v != 0}  # 获取学生数不为0的班级

            self.assertEqual(content, var, '★★★ Error- 布置试卷页面 班级不对,{}'.format(len(vans), len(count)))

            self.paper.assign_button()  # 布置试卷 按钮
            self.my_toast.toast_assert(self.name, Toast().toast_operation(self.tips.no_student))

            if self.paper.wait_check_assign_list_page():
                button = self.release.choose_button()  # 单选框
                print('------------------------')
                name = 0
                for k in range(len(button)):
                    if any([GetAttribute().selected(button[k]) == 'false', k != count,
                            van[k].text != GetVariable().VANCLASS]):
                        print('选择班级:', van[k].text)
                        name = van[k].text
                        button[k].click()  # 选择 一个班
                        break

                self.paper.assign_button()  # 布置试卷 按钮
                self.paper.tips_page_info()
                self.my_toast.toast_assert(self.name, Toast().toast_operation(self.tips.assign_success))

                return name

    @teststeps
    def judge_result_operation(self, item, van):
        """验证布置结果 具体操作"""
        print('------------------验证布置结果------------------')
        self.home.wait_check_page()  # 页面检查点
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)

        self.assertTrue(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 有班级检查点
        count = 0
        name = self.home.item_detail()  # 条目名称
        for i in range(len(name)):
            var = self.home.vanclass_name(name[i].text)  # 班级名
            if var == van:
                count += 1
                name[i].click()  # 进入班级
                break

        self.assertNotEqual(count, 0, '★★★ Error- 布置失败，无该班级, %s' % van)
        if self.van_detail.wait_check_app_page(van):  # 页面检查点
            self.vue.switch_h5()  # 切到web
            if self.van_detail.wait_check_page(van):
                self.van_detail.wait_check_no_hw_page()
                if self.van_detail.wait_check_list_page():  # 有作业列表
                    hw = self.van_detail.hw_name()  # 作业名
                    title = self.home.vanclass_name(hw[0].text)
                    self.assertEqual(title, item, '★★★ Error- 布置试卷失败, {} {}'.format(item, title))
                    print('布置试卷成功')
                    print('----恢复测试数据----')
                    hw[0].click()
                    self.vue.app_web_switch()  # 切到apk 再切回web

                    self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
                    self.van_paper.delete_commit_operation()  # 删除试卷 具体操作

                    if self.van_detail.wait_check_page(van):
                        self.van_detail.back_up_button()  # 返回 主界面
