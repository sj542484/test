#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.dynamic_info.object_page.recommend_to_scool_page import RecommendSchoolPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.dynamic_info.test_data.draft_data import GetVariable as ge
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassHw(unittest.TestCase):
    """习题 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.hw_detail = HwDetailPage()
        cls.van_detail = VanclassDetailPage()
        cls.v_hw = VanclassHwPage()
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
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassHw, self).run(result)

    @testcase
    def test_001_hw_more_button_cancel_and_delete(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        var = self.v_hw.edit_into_operation()  # 进入 班级 作业

        title = gv.HW_TITLE.format(var[1])
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.hw_detail.delete_cancel_operation()  # 删除 具体操作

        print('==========================================')
        self.vue.app_web_switch()  # 切到apk 再切回web
        if self.hw_detail.wait_check_page():  # 页面检查点
            self.hw_detail.more_button()  # 更多 按钮
            if self.hw_detail.wait_check_more_page():
                self.hw_detail.more_cancel_button()  # 取消按钮
                print('更多按钮 - 取消')
        else:
            print('★★★ Error- 未进入作业包')

        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)
        self.v_hw.back_up_button()  # 返回
        self.vue.app_web_switch()  # 切到apk 再切回vue

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切回vue

        self.assertTrue(self.van_detail.wait_check_page(var[1]), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
        self.van_detail.back_up_button()  # 返回主界面

    @testcase
    def test_002_hw_more_button_edit(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        var = self.v_hw.edit_into_operation()  # 进入 班级 作业
        # title = gv.HW_TITLE.format(var[1])

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.hw_detail.delete_cancel_operation()  # 删除 具体操作

        self.vue.app_web_switch()  # 切到apk 再切回web
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.hw_detail.more_button()  # 更多 按钮
        if self.hw_detail.wait_check_more_page():
            self.hw_detail.more_edit_button()  # 编辑按钮
            van = self.edit_hw_operation()  # 编辑 具体操作

            self.judge_result(van)  # 保存编辑,取消删除时，验证 结果

    @teststeps
    def edit_hw_operation(self):
        """编辑作业 详情页"""
        self.vue.switch_app()  # 切到apk
        self.home.tips_content_commit()  # 温馨提示 页面

        self.assertTrue(self.hw_detail.wait_check_edit_page(), self.hw_detail.edit_tips)
        self.assertTrue(self.release.wait_check_release_list_page(), self.hw_detail.edit_list_tips)

        print('-------------------编辑作业 详情页-------------------')
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        var = gv.HW_TEST
        name.send_keys(var)  # 修改name
        print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

        print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
        self.release.hw_mode_operation()  # 作业模式 操作
        self.release.hw_vanclass_list()  # 班级列表
        choose = self.release.choose_class_operation()  # 选择班级 学生

        if self.release.wait_check_release_page():  # 页面检查点
            self.release.hw_adjust_order()  # 调整题目顺序

            if self.release.wait_check_release_page():  # 页面检查点
                self.hw_detail.assign_button()  # 发布作业 按钮

                if Toast().find_toast(TipsData().hw_success):  # 获取toast信息
                    print(TipsData().hw_success)
                elif not self.home.wait_check_page(5):  # 发布不成功，验证 达标模式不能包含口语题
                    print('-------验证 达标模式不能包含口语题-------')
                    self.hw_detail.assign_button()  # 发布作业 按钮
                    self.home.tips_content_commit()  # 达标模式不能包含口语题

                    self.release.hw_mode_operation('free')  # 作业模式 操作
                    self.hw_detail.assign_button()  # 发布作业 按钮
                    Toast().toast_operation(TipsData().hw_success)  # 获取toast信息

        return var, choose

    @teststeps
    def judge_result(self, vanclass):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():  # 页面检查点
            self.v_hw.swipe_vertical_web(0.5, 0.2, 0.8)

        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入习题 最近动态页面

            self.vue.switch_h5()  # 切到web
            if self.info.wait_check_page():  # 页面检查点
                if self.info.wait_check_list_page():
                    print('--------------验证 编辑/取消删除 结果--------------')
                    name = self.info.hw_name()  # 作业name
                    van = self.info.hw_vanclass()  # 班级
                    if name[0].text == vanclass[0]:
                        if van[0].text != vanclass[1][0]:
                            print('★★★ Error- 作业编辑不成功', van[0].text, vanclass[1][0])
                        else:  # 编辑保存成功, 恢复测试数据
                            print('编辑保存成功')
                            self.delete_commit_operation(name[0], vanclass)  # 删除 具体操作
                    else:
                        print('★★★ Error- 取消删除失败')
                elif self.info.wait_check_no_hw_page():
                    print('★★★ Error- 取消删除失败')
                self.vue.app_web_switch()  # 切到apk 再切回vue

                self.info.back_up_button()  # 返回主界面
                if self.home.wait_check_page():  # 页面检查点
                    self.vue.switch_h5()  # 切到web

    @teststeps
    def delete_commit_operation(self, hw, vanclass):
        """删除作业 具体操作"""
        print('---------------------删除作业---------------------')
        hw.click()
        self.vue.app_web_switch()  # 切到apk 再切回vue

        if self.hw_detail.wait_check_page():
            self.hw_detail.more_button()  # 更多 按钮
            self.vue.app_web_switch()  # 切到apk 再切回vue
            if self.hw_detail.wait_check_more_page():
                self.hw_detail.more_delete_button()  # 删除按钮
                self.vue.app_web_switch()  # 切到apk 再切回vue

                if self.hw_detail.wait_check_tips_page():
                    self.hw_detail.commit_button()  # 确定按钮
                    print('确定删除')
                    self.vue.app_web_switch()  # 切到apk 再切回web

                    if self.info.wait_check_page():  # 页面检查点
                        self.v_hw.swipe_vertical_web(0.5, 0.2, 0.8)
                        if self.info.wait_check_list_page():
                            print('--------------验证 删除 结果--------------')
                            name = self.info.hw_name()  # 作业name
                            van = self.info.hw_vanclass()  # 班级
                            if name[0].text == vanclass[0]:
                                if van[0].text == vanclass[1][0]:
                                    print('★★★ Error- 作业删除不成功', van[0].text, vanclass[1][0])

                                    if self.info.wait_check_list_page():
                                        self.info.back_up_button()  # 返回主界面
                                        self.vue.switch_app()  # 切到apk
                                else:  # 删除成功
                                    print('删除成功')
                            else:
                                print('删除成功')
                        elif self.info.wait_check_no_hw_page():
                            print('删除成功')

    @testcase
    def test_003_hw_more_button_delete(self):
        self.login.app_status()  # 判断APP当前状态

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        var = self.v_hw.edit_into_operation()[0]  # 进入 班级 作业

        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        name = self.recommend_hw_operation()  # 推荐到学校 具体操作

        self.vue.app_web_switch()  # 切到apk 再切回web
        if self.hw_detail.wait_check_page():  # 页面检查点
            self.info.back_up_button()

            self.vue.app_web_switch()  # 切到apk 再切回web
            if self.info.wait_check_page():  # 页面检查点
                self.info.back_up_button()  # 返回主界面

                if name:
                    self.judge_recommend_result(var, name)  # 验证 推荐到学校 结果
                    self.rec_school.judge_mine_test_bank_operation(var, name)
                    if self.user.wait_check_page():
                        self.home.click_tab_hw()

    @teststeps
    def recommend_hw_operation(self):
        """推荐到学校"""
        self.hw_detail.more_button()  # 更多 按钮
        if self.hw_detail.wait_check_more_page():
            self.hw_detail.more_recommend_button()  # 推荐到学校 按钮
            self.recommend_commit_operation()  # 二次确认 按钮

            self.vue.app_web_switch()  # 切到apk 再切回web
            self.rec_school.choose_school_label_operation(ge.RECOMMEND)  # 选择 学校标签

            self.vue.app_web_switch()  # 切到apk 再切回web
            if self.hw_detail.wait_check_page(5):
                print('推荐到学校成功')
                # self.hw_detail.toast_operation('成功推荐到学校')  # 获取toast
                if self.hw_detail.wait_check_page():  # 页面检查点
                    self.hw_detail.analysis_tab()  # 进入 答题分析 tab页

                    if self.hw_detail.wait_check_hw_list_page():
                        name = self.hw_detail.game_name()
                        content = [var.text for var in name]
                        return content  # 游戏 名称
                    elif self.hw_detail.wait_check_empty_tips_page():
                        print('暂无数据')
                else:
                    print('★★★ Error- 未返回详情页')
            elif self.rec_school.wait_check_page():
                print('推荐到学校失败')
                # self.rec_school.confirm_button()
                Toast().toast_vue_operation('推荐到学校失败')  # 获取toast
                self.rec_school.back_up_button()
                self.vue.app_web_switch()  # 切到apk 再切回web

    @teststeps
    def judge_recommend_result(self, menu, games):
        """验证 推荐到学校结果 具体操作"""
        print('------------------验证 推荐到学校 结果-----------------')
        print(menu)
        self.vue.switch_app()  # 切回app
        if self.home.wait_check_page():
            self.home.click_tab_profile()  # 个人中心 页面

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_recommend()  # 我的推荐 按钮
                self.rec_school.verify_recommend_result(menu, games)  # 具体操作
                if self.user.wait_check_page():
                    self.home.click_tab_hw()  # 返回主界面
            else:
                print('未进入 个人中心 页面')

    @teststeps
    def recommend_commit_operation(self):
        """推荐到本校 具体操作"""
        if self.hw_detail.wait_check_tips_page():
            print('---------推荐到本校---------')
            self.hw_detail.tips_title()
            self.hw_detail.recommend_tips_content()
            self.hw_detail.commit_button()  # 确认按钮
            print('---------------')
