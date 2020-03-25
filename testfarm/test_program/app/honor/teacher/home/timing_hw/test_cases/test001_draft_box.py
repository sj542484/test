#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.timing_hw.object_page.draft_page import DraftPage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.timing_hw.test_data.hw_name_data import GetVariable as gv
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.base_page import BasePage
from conf.decorator import setup, testcase, teststeps, teardown
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class DraftBox(unittest.TestCase):
    """草稿箱 - 修改草稿"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.release = ReleasePage()
        cls.get = GetAttribute()
        cls.draft = DraftPage()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)
        cls.login.app_status()  # 判断APP当前状态

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切到apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(DraftBox, self).run(result)

    @testcase
    def test_draft_box_modify(self):
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到vue
        
        self.assertTrue(self.draft.wait_check_page(), self.draft.timing_vue_tips)  # 页面检查点
        self.draft.draft_box_button()  # 草稿箱 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.draft.wait_check_draft_page(), self.draft.draft_tips)  # 页面检查点
        if self.draft.wait_check_empty_tips_page():
            print('草稿箱 暂无数据')
            self.assertTrue(self.draft.wait_check_draft_list_page(), self.draft.draft_list_tips)  # 页面检查点
        else:
            self.assertTrue(self.draft.wait_check_draft_list_page(), self.draft.draft_list_tips)  # 页面检查点
            content = self.draft_box_operation()  # 草稿箱
            self.draft_detail_operation(content)  # 草稿详情页具体操作
            self.judge_draft_operation(content)  # 验证 草稿箱

        self.draft.back_up_button()  # 返回 定时作业
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        self.draft.back_up_button()  # 返回主界面

        # self.judge_result_operation(van)  # 验证 班级 习题列表

    @teststeps
    def draft_box_operation(self):
        """草稿 列表"""
        print('---------------------草稿 列表-------------------')
        draft = self.draft.draft_name()  # 草稿名 元素
        create = self.draft.draft_time()  # 创建时间

        name = []  # 草稿名
        for i in range(len(draft)):
            print(draft[i].text, '\n',
                  create[i].text,)
            print('------------------')
            name.append(draft[i].text)
        return draft, name

    @teststeps
    def draft_detail_operation(self, content):
        """草稿 详情页"""
        content[0][0].click()  # 随机进去一个草稿
        print('------------草稿 %s 详情页:--------------' % content[1][0])
        self.draft.tips_content_commit()  # 温馨提示 页面
        self.vue.switch_app()  # 切回app

        self.assertTrue(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        if name.text != content[1][0][:len(name.text)]:
            print('★★★ Error- 详情页草稿名与草稿箱不一致', name.text, content[1][0])
        modify = gv.DRAFT_MODIFY
        name.send_keys(modify)
        print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

        print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
        self.release.hw_mode_operation()  # 作业模式 操作
        self.release.hw_vanclass_list()  # 班级列表
        self.release.choose_class_operation()  # 选择班级 学生

        self.assertTrue(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        self.release.hw_adjust_order()  # 调整题目顺序

        self.assertTrue(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        # self.release.assign_button()  # 不发布！！！ 因为dev草稿箱只有一个测试数据了
        self.home.back_up_button()
        self.assertTrue(self.draft.wait_check_draft_app_page(), self.draft.draft_tips)  # 页面检查点
        self.vue.switch_h5()

        self.assertTrue(self.draft.wait_check_draft_page(), self.draft.draft_tips)  # 页面检查点
        print('-----------------------------------------')
        print('取消编辑')
        self.draft.back_up_button()  # 返回 定时作业 页面
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        self.draft.back_up_button()  # 返回 主界面

    @teststeps
    def judge_draft_operation(self, content):
        """草稿箱 验证"""
        self.vue.switch_app()  # 切到apk
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)  # 页面检查点
        print('----------------验证布置结果 草稿箱----------------')

        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.draft.wait_check_page(), self.draft.timing_tips)  # 页面检查点
        self.draft.draft_box_button()  # 草稿箱 按钮
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.draft.wait_check_draft_page(), self.draft.draft_tips)  # 页面检查点
        if self.draft.wait_check_draft_list_page():
            name1 = self.draft.draft_name()  # 草稿名
            self.assertEqual(content[1][0], name1[0].text, '★★★ Error- 取消编辑草稿失败')
            print('取消编辑成功')
        elif self.draft.wait_check_empty_tips_page():
            print('取消编辑成功')
