#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page import PaperPage
from app.honor.teacher.home.object_page import ReleasePage
from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.test_bank.object_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from app.honor.teacher.user_center import CollectionPage
from app.honor.teacher.user_center import RecommendPage
from app.honor.teacher.user_center import TuserCenterPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class AssignPaper(unittest.TestCase):
    """布置试卷"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.filter = FilterPage()
        cls.question = TestBankPage()
        cls.detail = PaperDetailPage()
        cls.release = ReleasePage()

        cls.paper = PaperPage()
        cls.van = VanclassPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_assign_paper(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                self.question.filter_button()  # 筛选按钮

                if FilterPage().wait_check_page():
                    paper = self.filter.test_paper()
                    if GetAttribute().selected(paper) == 'false':
                        self.filter.click_test_paper()  # 点击 试卷
                        self.filter.commit_button()  # 确定按钮
                    else:
                        self.filter.commit_button()  # 确定按钮

            if self.question.wait_check_page('试卷'):  # 页面检查点
                item = self.question.question_name()  # 获取name

                if self.question.judge_question_lock():
                    lock = self.question.question_lock()  # 锁定的试卷数
                    item[0][len(lock)+2].click()  # 点击第X个试卷  todo 根据lock数点击未lock的
                else:
                    item[0][2].click()  # 点击第X个试卷

                if self.detail.wait_check_page():  # 页面检查点
                    title = self.detail.paper_detail_operation()  # 试卷详情页 具体操作

                    self.detail.recommend_button()  # 推荐按钮
                    if Toast().find_toast('操作成功'):  # 获取toast
                        print('推荐成功')

                    if self.detail.wait_check_page():  # 页面检查点
                        self.detail.collect_button()  # 收藏按钮
                        if Toast().find_toast('成功加入收藏'):  # 获取toast
                            print('加入收藏成功')

                    if self.detail.wait_check_page():  # 页面检查点
                        van = self.assign_paper_operation()  # 布置试卷 具体操作

                        CollectionPage().verify_collect_result(title, '试卷')  # 我的收藏 验证收藏结果
                        if TuserCenterPage().wait_check_page():
                            self.home.click_tab_test_bank()
                            if self.question.wait_check_page('试卷'):
                                ThomePage().click_tab_profile()  # 个人中心
                                RecommendPage().verify_recommend_result(title, '试卷')  # 我的推荐 验证结果

                            if TuserCenterPage().wait_check_page():
                                self.home.click_tab_hw()  # 返回首页

                        self.judge_result_operation(title, van)  # 班级页面 验证结果

            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def assign_paper_operation(self):
        """布置试卷 具体操作 """
        self.detail.assign_button()  # 布置试卷 按钮
        if self.detail.wait_check_assign_list_page():
            print('-----------------布置试卷页面-------------------')
            self.detail.assign_title()
            self.detail.assign_hint()
            name = self.release.van_name()  # 班级名
            count = self.release.choose_count()  # 班级描述信息
            print('------------------------', '\n',
                  '班级列表：')
            for i in range(len(count)):
                print('  ', name[i].text, ' ', count[i].text)
            print('------------------------')

            self.detail.assign_button()  # 布置试卷 按钮
            if not Toast().find_toast('布置学生不能为空'):
                print('★★★ Error- 未弹toast: 布置学生不能为空')
            else:
                print('布置学生不能为空')

            if self.detail.wait_check_assign_list_page():
                name = self.release.van_name()[0].text  # 班级名
                print('------------------------')
                print('选择班级:', name)
                self.release.choose_button()[0].click()  # 班级 单选框

                self.detail.assign_button()  # 布置试卷 按钮
                self.detail.tips_page_info()
                return name

    @teststeps
    def judge_result_operation(self, item, van):
        """验证布置结果 具体操作"""
        if self.home.wait_check_page():  # 页面检查点
            print('------------------验证布置结果------------------')
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                if var == van:
                    name[i].click()  # 进入班级

                    if self.van.wait_check_page(var):  # 页面检查点
                        if self.van.wait_check_list_page():
                            hw = self.van.hw_name()  # 作业名
                            title = self.home.vanclass_name(hw[0].text)
                            if title != item:
                                print('★★★ Error- 布置试卷失败', item, title)
                            else:  # 恢复测试数据
                                print('布置试卷成功')
                                hw[0].click()
                                if self.paper.wait_check_page():  # 页面检查点
                                    self.paper.delete_commit_operation()  # 删除试卷 具体操作
                        elif self.home.wait_check_empty_tips_page():
                            print('★★★ Error-班级动态为空, 布置试卷失败')

                        if self.van.wait_check_page(van):
                            self.home.back_up_button()  # 返回 主界面
                    else:
                        print('未进入班级:', van)
                    break

