#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

import ddt

from app.honor.pc_operation.my_resource.test_cases.delete_recommend.delete_recommend import Delete
from app.honor.teacher.home.dynamic_info.test_data.recommend_school_data import tips_data
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.dynamic_info.object_page.recommend_to_scool_page import RecommendSchoolPage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.toast_find import Toast
from utils.vue_context import VueContext


@ddt.ddt
class Homework(unittest.TestCase):
    """习题 更多按钮 -推荐到学校"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.info = DynamicPage()
        cls.user = TuserCenterPage()
        cls.mine_bank = MineTestBankPage()
        cls.filter = FilterPage()
        cls.recommend = RecommendPage()
        cls.rec_school = RecommendSchoolPage()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(Homework, self).run(result)

    @ddt.data(*tips_data)
    @testcase
    def test_001_hw_recommend_school(self, data):
        """推荐到学校"""
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入习题 最近动态页面
            if self.info.wait_check_app_page():  # 页面检查点
                self.vue.switch_h5()  # 切到web

                if self.info.wait_check_page():  # 页面检查点
                    if self.info.wait_check_no_hw_page():
                        print('最近习题动态页面为空')
                        self.info.back_up_button()  # 返回主界面
                        self.assertFalse(self.info.wait_check_no_hw_page(), self.info.dynamic_empty_tips)
                    else:
                        self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                        self.info.into_hw()  # 进入 作业包
                        self.vue.app_web_switch()  # 切到apk 再切回web

                        if self.detail.wait_check_page():
                            game = self.recommend_hw_operation(data)  # 推荐到学校 具体操作

                            if self.detail.wait_check_page():
                                self.info.back_up_button()  # 返回 最近习题动态页面
                                self.vue.app_web_switch()  # 切到apk 再切到web

                                if game:
                                    if self.info.wait_check_page():  # 页面检查点
                                        self.info.back_up_button()  # 返回主界面
                                    self.vue.switch_app()  # 切回app
                                    self.judge_recommend_result(game[0], game[1])  # 验证 推荐到学校 结果

                                    if self.home.wait_check_page():
                                        self.home.click_tab_profile()  # 个人中心 页面
                                        self.rec_school.judge_mine_test_bank_operation(game[0], game[1])
                                        if self.user.wait_check_page():
                                            self.home.click_tab_hw()  # 返回主界面
                                elif data['assert'] == '(C10000)不可重复推荐':
                                    self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
                                    self.info.into_hw()  # 进入 作业包
                                    self.vue.app_web_switch()  # 切到apk 再切回web

                                    if self.detail.wait_check_page():
                                        self.detail.more_button()  # 更多 按钮
                                        if self.detail.wait_check_more_page():
                                            self.detail.more_delete_button()  # 删除 按钮
                                            self.vue.app_web_switch()  # 切到apk 再切回vue

                                            if self.detail.wait_check_tips_page():
                                                self.detail.commit_button()  # 确定按钮
                                                print('确定删除')
                                                self.vue.app_web_switch()  # 切到apk 再切回web
                                                if self.info.wait_check_page():  # 页面检查点
                                                    self.info.back_up_button()  # 返回主界面
                                else:
                                    if self.info.wait_check_page():  # 页面检查点
                                        self.info.back_up_button()  # 返回主界面

                                self.vue.switch_app()  # 切回apk

    @teststeps
    def recommend_hw_operation(self, tips):
        """推荐到学校"""
        if self.detail.wait_check_page():
            self.detail.more_button()  # 更多 按钮
            if self.detail.wait_check_more_page():
                self.detail.more_recommend_button()  # 推荐到学校 按钮

                self.recommend_commit_operation()  # 二次确认 按钮
                self.vue.app_web_switch()  # 切到apk 再切回web
                self.rec_school.choose_school_label_operation(tips['name'])  # 选择 学校标签
                self.my_toast.toast_assert(self.name, Toast().toast_vue_operation(tips['assert']))  # 获取toast
                self.vue.app_web_switch()  # 切到apk 再切回web
                print(tips['name'])
                print('----------------------------')

                if tips['assert'] == '成功推荐到学校':
                    if self.detail.wait_check_page():
                        self.detail.analysis_tab()  # 进入 答题分析 tab页

                        if self.detail.wait_check_hw_list_page():
                            self.info.swipe_vertical_web(0.5, 0.95, 0.1)
                            if self.detail.wait_check_hw_list_page():
                                name = self.detail.game_name()
                                content = [var.text for var in name]
                                print(content)
                                return tips['name'], content  # 游戏 名称
                        elif self.detail.wait_check_empty_tips_page():
                            print('暂无数据')
                else:
                    if self.rec_school.wait_check_page():
                        # self.rec_school.confirm_button()
                        self.rec_school.back_up_button()
                        self.vue.app_web_switch()  # 切到apk 再切回web

    @teststeps
    def judge_recommend_result(self, menu, games):
        """验证 推荐到学校结果 具体操作"""
        print('------------------验证 推荐到学校 结果-----------------')
        print(menu)
        if self.home.wait_check_page():
            self.home.click_tab_profile()  # 个人中心 页面
            if self.user.wait_check_page():

                self.user.click_mine_recommend()  # 我的推荐 按钮
                self.rec_school.verify_recommend_result(menu, games)  # 具体操作
                if self.user.wait_check_page():
                    self.home.click_tab_hw()  # 返回主界面

    @teststeps
    def recommend_commit_operation(self):
        """推荐到本校 具体操作"""
        print('---------推荐到本校---------')
        self.assertTrue(self.detail.wait_check_tips_page(), '★★★ Error- 未进入推荐到本校')
        self.detail.tips_title()
        self.detail.recommend_tips_content()
        self.detail.commit_button()  # 确认按钮
        print('---------------')

    @testcase
    def test_002_delete_hw_recommend_school(self):
        """删除 推荐到学校的"""
        Delete().delete_recommend_operation()  # PC删除推荐题