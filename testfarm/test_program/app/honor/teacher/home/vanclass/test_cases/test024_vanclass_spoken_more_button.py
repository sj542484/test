#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.dynamic_info.object_page.dynamic_info_hw_spoken_page import DynamicPage
from app.honor.teacher.home.dynamic_info.object_page.spoken_finish_tab_detail_page import SpokenFinishDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassSpoken(unittest.TestCase):
    """口语作业 更多按钮 -编辑/删除"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.hw_detail = HwDetailPage()
        cls.speak = SpokenFinishDetailPage()
        cls.van = VanclassPage()
        cls.v_hw = VanclassHwPage()
        cls.release = ReleasePage()
        cls.info = DynamicPage()
        cls.vue = VueContext()

        cls.my_toast = MyToast()
        cls.vue = VueContext()
    
        BasePage().set_assert(cls.ass)
    
    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况
    
    def run(self, result=None):
        self.ass_result = result
        super(VanclassSpoken, self).run(result)

    @testcase
    def test_spoken_more_button(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
    
        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)
        self.van.vanclass_hw()  # 点击 本班作业 tab
        name = self.v_hw.into_operation(gv.HW_TITLE, gv.VANCLASS, '口语')
    
        self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
        self.assertTrue(self.hw_detail.wait_check_st_list_page(), self.hw_detail.st_list_tips)
        print("题单:", name[0])
        self.hw_detail.delete_cancel_operation()  # 取消删除 具体操作
    
        self.vue.app_web_switch()  # 切到apk 再切到vue
        if self.hw_detail.wait_check_page():  # 页面检查点
            self.hw_detail.more_button()  # 更多 按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue
            
            if self.hw_detail.wait_check_more_page():
                self.hw_detail.more_edit_button()  # 编辑按钮
                van = self.edit_hw_operation()  # 编辑 具体操作
    
                self.judge_result(van)  # 保存编辑,取消删除时，验证结果；成功则进行删除操作

    @teststeps
    def edit_hw_operation(self):
        """编辑作业 详情页"""
        self.vue.switch_app()  # 切到apk
        self.home.tips_content_commit(5)  # 温馨提示 页面

        if self.hw_detail.wait_check_edit_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                print('-------------------编辑作业 详情页-------------------')
                name = self.release.hw_name_edit()  # 作业名称 编辑框
                var = gv.SPOKEN_EDIT
                name.send_keys(var)  # 修改name
                print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

                print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
                self.release.hw_mode_operation('free')  # 作业模式 操作
                self.release.hw_vanclass_list()  # 班级列表
                choose = self.release.choose_class_operation()  # 选择班级 学生

                if self.release.wait_check_release_page():  # 页面检查点
                    self.release.hw_adjust_order()  # 调整题目顺序

                    if self.release.wait_check_release_page():  # 页面检查点
                        self.hw_detail.assign_button()  # 发布作业 按钮
                        Toast().toast_operation(TipsData().hw_success)  # 获取toast信息

                        return var, choose

    @teststeps
    def judge_result(self, vanclass):
        """验证 编辑/删除 结果"""
        if self.home.wait_check_page():  # 页面检查点
            SwipeFun().swipe_vertical(0.5, 0.2, 0.8)

        if self.home.wait_check_page():  # 页面检查点
            self.home.hw_icon()  # 进入作业 最近动态页面

            if self.info.wait_check_app_page():
                self.vue.switch_h5()
                if self.info.wait_check_page():  # 页面检查点
                    if self.info.wait_check_list_page():
                        print('--------------验证 编辑/取消删除 结果--------------')
                        name = self.info.hw_name()  # 作业name
                        van = self.info.hw_vanclass()  # 班级
                        if name[0].text == vanclass[0]:
                            if van[0].text != vanclass[1][0]:
                                print('★★★ Error- 作业编辑不成功', van[0].text, vanclass[1][0])

                                if self.info.wait_check_list_page():
                                    self.info.back_up_button()  # 返回主界面
                            else:  # 编辑保存成功, 执行删除操作
                                print('编辑保存成功')
                                self.delete_commit_operation(name[0], vanclass)  # 删除 具体操作
                        else:
                            print('★★★ Error- 取消删除失败')
                    elif self.v_hw.wait_check_empty_tips_page():
                        print('★★★ Error- 取消删除失败')

    @teststeps
    def delete_commit_operation(self, hw, vanclass):
        """删除作业 具体操作"""
        print('---------------------删除作业---------------------')
        hw.click()
        self.vue.app_web_switch()  # 切到apk 再切到vue
        if self.hw_detail.wait_check_page():
            self.hw_detail.more_button()  # 更多 按钮
            self.vue.app_web_switch()  # 切到apk 再切到vue
            
            if self.hw_detail.wait_check_more_page():
                self.hw_detail.more_delete_button()  # 删除按钮
                self.vue.app_web_switch()  # 切到apk 再切到vue

                if self.hw_detail.wait_check_tips_page():
                    self.hw_detail.commit_button()  # 确定按钮
                    print('确定删除')

                    self.vue.app_web_switch()  # 切到apk 再切到vue
                    if self.info.wait_check_page():  # 页面检查点
                        self.v_hw.swipe_vertical_web(0.5, 0.2, 0.8)
                        if self.info.wait_check_list_page():
                            print('--------------验证 删除 结果--------------')
                            name = self.info.hw_name()  # 作业name
                            van = self.info.hw_vanclass()  # 班级
                            if name[0].text == vanclass[0]:
                                if van[0].text == vanclass[1][0]:
                                    print('★★★ Error- 作业删除不成功', van[0].text, vanclass[1][0])
                                else:  # 删除成功
                                    print('删除成功')
                            else:
                                print('删除成功')
                        elif self.v_hw.wait_check_empty_tips_page():
                            print('删除成功')

                        if self.info.wait_check_list_page():
                            self.info.back_up_button()  # 返回主界面

    @teststeps
    def edit_into_operation(self):
        """进入  有作业的班级"""
        if self.home.wait_check_list_page():
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            if self.home.wait_check_list_page():
                van_name = self.home.item_detail()  # 班号+班级名

                for i in range(len(van_name)):
                    van = self.home.vanclass_name(van_name[i].text)  # 班级名
                    if van == gv.VANCLASS:
                        van_name[i].click()  # 进入班级

                        self.vue.switch_h5()  # 切到vue
                        if self.van.wait_check_page(van):  # 页面检查点
                            if self.van.wait_check_list_page():  # 加载完成
                                self.van.vanclass_hw()  # 点击进入 本班作业 tab
                                title = gv.HW_TITLE.format(van)

                                if self.van.wait_check_app_page(title):
                                    print('本班作业')
                                    self.vue.app_web_switch()  # 切到apk 再切到vue
                                    if self.v_hw.wait_check_page(title):  # 页面检查点
                                        if self.v_hw.wait_check_list_page():
                                            print('班级:', van)
                                            hw_name = self.into_hw_operation()  # 随机进入某个作业 游戏列表
                                            if hw_name != 0:
                                                print('=====================================')
                                                return hw_name, van
                                            else:
                                                self.v_hw.back_up_button()  # 返回 答题详情页面
                                                self.vue.app_web_switch()  # 切到apk 再切到vue
                                                
                                                if self.van.wait_check_page(van):  # 班级详情 页面检查点
                                                    self.van.back_up_button()  # 返回主界面
                                        else:
                                            self.v_hw.back_up_button()  # 返回 答题详情页面
                                            self.vue.app_web_switch()  # 切到apk 再切到vue
                                            if self.van.wait_check_page(van):  # 班级详情 页面检查点
                                                self.van.back_up_button()  # 返回主界面
                                    else:
                                        print('未进入本班作业', title)
                                else:
                                    print('未进入班级页面', van)
                        break

    @teststeps
    def into_hw_operation(self):
        """进入列表中 口语作业 具体操作
        """
        hw_name = []
        hw = self.v_hw.hw_name()  # 口语/作业 name
        for i in range(len(hw)):
            if '口语作业(测试)' in hw[i].text:
                hw_name.append(hw[i].text)
                print("作业:", hw_name)
                hw[i].click()  # 进入口语作业
                self.vue.app_web_switch()  # 切到apk 再切到vue
                break

        if len(hw_name) == 0:
            print('★★★ Error- 没有可测试的数据')
        else:
            return hw_name[0]
