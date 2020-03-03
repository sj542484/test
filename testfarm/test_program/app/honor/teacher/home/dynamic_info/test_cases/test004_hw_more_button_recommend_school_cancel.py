#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.pc_operation.my_resource.test_cases.delete_recommend.delete_recommend import Delete
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


class Homework(unittest.TestCase):
    """习题 更多按钮 -推荐到学校/取消"""

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

    @testcase
    def test_001_hw_more_cancel(self):
        """更多按钮 - 取消"""
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.hw_icon()  # 进入习题 最近动态页面

        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点

        if self.info.wait_check_no_hw_page():
            print('最近习题动态页面为空')
            self.info.back_up_button()
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        else:
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            self.info.into_hw()  # 进入 作业包
            self.vue.app_web_switch()  # 切到apk 再切回web

            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
            self.detail.more_button()  # 更多 按钮
            self.assertTrue(self.detail.wait_check_more_page(), self.detail.more_tips)
            self.detail.more_cancel_button()  # 取消按钮
            print('更多按钮 - 取消')

            self.vue.app_web_switch()  # 切到apk 再切回web
            if self.detail.wait_check_page():  # 页面检查点
                self.info.back_up_button()  # 返回 最近动态页面

                self.vue.app_web_switch()  # 切到apk 再切回web
                if self.info.wait_check_page():  # 页面检查点
                    self.info.back_up_button()  # 返回主界面
                    self.vue.switch_app()  # 切回apk

    @testcase
    def test_002_hw_recommend_school(self):
        """推荐到学校"""
        self.login.app_status_no_check()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.hw_icon()  # 进入习题 最近动态页面
        self.assertTrue(self.info.wait_check_app_page(), self.info.dynamic_tips)  # 页面检查点

        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点

        if self.info.wait_check_no_hw_page():
            print('最近习题动态页面为空')
            self.info.back_up_button()
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
        else:
            self.assertTrue(self.info.wait_check_list_page(), self.info.dynamic_list_tips)
            self.info.into_hw()  # 进入 作业包
            self.vue.app_web_switch()  # 切到apk 再切回web

            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
            game = self.recommend_hw_operation()  # 推荐到学校 具体操作

            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
            self.info.back_up_button()  # 返回 最近习题动态页面
            self.vue.app_web_switch()  # 切到apk 再切到web
            self.assertTrue(self.info.wait_check_page(), self.info.dynamic_vue_tips)  # 页面检查点
            self.info.back_up_button()  # 返回主界面

            if game:
                self.vue.switch_app()  # 切回app
                self.judge_recommend_result(game[0], game[1])  # 验证 推荐到学校 结果
                self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
                self.home.click_tab_profile()  # 个人中心 页面
                self.rec_school.judge_mine_test_bank_operation(game[0], game[1])
                if self.user.wait_check_page():
                    self.home.click_tab_hw()  # 返回主界面

            self.vue.switch_app()  # 切回apk

            Delete().delete_recommend_operation()  # PC删除推荐题

            self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
            self.login.reset_app()

    @teststeps
    def recommend_hw_operation(self):
        """推荐到学校"""
        self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
        self.detail.more_button()  # 更多 按钮
        self.assertTrue(self.detail.wait_check_more_page(), self.detail.more_tips)
        self.detail.more_recommend_button()  # 推荐到学校 按钮
        self.recommend_commit_operation()  # 二次确认 按钮

        self.vue.app_web_switch()  # 切到apk 再切回web
        menu_name = self.rec_school.choose_school_label_operation()[0]  # 选择 学校标签
        self.my_toast.toast_assert(self.name, Toast().toast_vue_operation('成功推荐到学校'))  # 获取toast

        self.vue.app_web_switch()  # 切到apk 再切回web
        if self.detail.wait_check_page(5):
            print(menu_name)
            print('推荐到学校成功')
            print('----------------------------')
            self.assertTrue(self.detail.wait_check_page(), self.detail.hw_detail_tips)
            self.detail.analysis_tab().click()  # 进入 答题分析 tab页

            if self.detail.wait_check_hw_list_page():
                self.info.swipe_vertical_web(0.5, 0.95, 0.1)
                if self.detail.wait_check_hw_list_page():
                    name = self.detail.game_name()
                    content = [var.text for var in name]
                    print(content)
                    return menu_name, content  # 游戏 名称
            elif self.detail.wait_check_empty_tips_page():
                print('暂无数据')
        elif self.rec_school.wait_check_page():
            print('推荐到学校失败')
            # self.rec_school.confirm_button()
            self.my_toast.toast_assert(self.name, Toast().toast_vue_operation('推荐到学校失败'))  # 获取toast
            self.rec_school.back_up_button()
            self.vue.app_web_switch()  # 切到apk 再切回web

    @teststeps
    def judge_recommend_result(self, menu, games):
        """验证 推荐到学校结果 具体操作"""
        print('------------------验证 推荐到学校 结果-----------------')
        print(menu)
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.click_tab_profile()  # 个人中心 页面
        self.assertTrue(self.user.wait_check_page(), self.home.home_tips)

        self.user.click_mine_recommend()  # 我的推荐 按钮
        self.rec_school.verify_recommend_result(menu, games)  # 具体操作
        if self.user.wait_check_page():
            self.home.click_tab_hw()  # 返回主界面
        else:
            print('未进入 个人中心 页面')

    @teststeps
    def recommend_commit_operation(self):
        """推荐到本校 具体操作"""
        print('---------推荐到本校---------')
        self.assertTrue(self.detail.wait_check_tips_page(), '★★★ Error- 未进入推荐到本校')
        self.detail.tips_title()
        self.detail.recommend_tips_content()
        self.detail.commit_button()  # 确认按钮
        print('---------------')
