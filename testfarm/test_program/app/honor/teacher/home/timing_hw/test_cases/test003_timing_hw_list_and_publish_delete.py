#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.timing_hw.object_page.draft_page import DraftPage
from app.honor.teacher.home.timing_hw.test_data.tips_data import TipsData
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.decorator import testcase, teststeps, teardown, setupclass
from conf.base_page import BasePage
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.vue_context import VueContext


class TimingHw(unittest.TestCase):
    """定时作业列表 及删除/发布"""

    @classmethod
    @setupclass
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.draft = DraftPage()
        cls.release = ReleasePage()

        cls.get = GetAttribute()
        cls.van_detail = VanclassDetailPage()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切到app
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(TimingHw, self).run(result)

    @testcase
    def test_001_timing_hw_list(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        print("1.验证：切换班级/时间tab\n"
              "==================================================================")

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        if self.draft.wait_check_empty_tips_page():
            print('暂无 定时作业')
            self.draft.back_up_button()  # 返回主界面
            self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
        else:
            self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
            self.timing_list_operation()  # 获取目前 定时作业数

            if self.draft.wait_check_page():  # 页面检查点
                self.draft.back_up_button()  # 返回主界面

    @teststeps
    def timing_list_operation(self):
        """定时作业 列表 具体操作"""
        self.draft.all_vanclass()  # 点击 班级
        self.assertTrue(self.draft.wait_check_tab_page(), self.draft.van_choose_tips)
        vanclass = self.draft.van_check_text()  # 班级元素
        print('------------------所有班级-----------------')
        for i in range(len(vanclass)):
            print(vanclass[i].text)

        var = 0  # 为节省运行时间，只 切换班级3次
        for k in range(len(vanclass)):
            self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
            vanclass = self.draft.van_check_text()  # 班级元素
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            van = vanclass[k].text  # 班级名
            vanclass[k].click()  # 选择班级
            var += 1
            print('班级:', van)

            self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
            self.draft.all_time()  # 发布时间元素
            self.assertTrue(self.draft.wait_check_tab_page(), self.draft.van_choose_tips)
            spend = self.draft.date_check_text()  # 时间元素
            for j in range(len(spend)):
                title = spend[j].text  # 发布时间
                spend[j].click()  # 选择时间
                print('--------------%s---------------' % title)

                if self.draft.wait_check_empty_tips_page():
                    print('暂无 定时作业')
                else:
                    self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
                    name = self.draft.draft_name()
                    create = self.draft.draft_time()
                    for i in range(len(create)):
                        print(name[i].text, '\n',
                              create[i].text)
                        print('-------------------')

                if j != len(spend) - 1:
                    self.draft.all_time()  # 发布时间元素
                    self.assertTrue(self.draft.wait_check_tab_page(), self.draft.van_choose_tips)
                    spend = self.draft.date_check_text()  # 时间元素

            if var != 2:
                self.draft.all_vanclass()  # 点击 班级
                self.assertTrue(self.draft.wait_check_tab_page(), self.draft.van_choose_tips)
                vanclass = self.draft.van_check_text()  # 班级元素
            else:
                break

    @testcase
    def test_002_timing_hw_publish(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        print("1.验证：长按菜单 发布 \n"
              "==================================================================")
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到vue

        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        if self.draft.wait_check_empty_tips_page():
            print('暂无 定时作业')
            self.draft.back_up_button()  # 返回主界面
            self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
        else:
            self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
            self.draft.more_button()[0].click()  #
            if self.draft.wait_check_more_page():
                self.draft.more_edit_button()  # 发布
                print('点击菜单 编辑/发布作业')
                self.vue.switch_app()  # 切到app

                self.assertTrue(HwDetailPage().wait_check_edit_page(), HwDetailPage().edit_tips)
                self.assertTrue(self.release.wait_check_release_list_page(), HwDetailPage().edit_list_tips)
                print('-------------------编辑作业页面-------------------')
                choose = 0  # 发布班级
                name = self.release.hw_name_edit().text  # 名称
                print(name)
                delete_time_button = self.release.delete_time_button()
                for i in range(len(delete_time_button)):
                    delete_time_button[i].click()  # 删除上一次设定的时间

                self.assertTrue(self.release.wait_check_release_list_page(), HwDetailPage().edit_list_tips)
                SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                self.assertTrue(self.release.wait_check_release_list_page(), HwDetailPage().edit_list_tips)
                button = self.release.choose_button()  # 单选框
                van = self.release.van_name()  # 班级 元素
                for i in range(len(button)):
                    if GetAttribute().selected(button[i]) == 'true':
                        choose = van[i].text
                        break

                print('布置到的班级:', choose)
                self.assertTrue(self.release.wait_check_release_list_page(), HwDetailPage().edit_list_tips)
                self.release.assign_button()  # 点击 发布作业 按钮

                if Toast().find_toast(TipsData().hw_success):  # 布置成功
                    print(TipsData().hw_success)
                else:  # 与当天布置的作业有重名
                    self.assertTrue(self.release.wait_check_release_list_page(), HwDetailPage().edit_list_tips)
                    self.release.assign_button()  # 点击 发布作业 按钮
                    if Toast().find_toast(TipsData().hw_only_daily):  # 获取toast
                        print(TipsData().hw_only_daily)
                        name = self.release.republish_operation()  # 重新命名布置

                self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
                self.home.timing_button()  # 定时作业 按钮
                self.judge_result_operation({name: choose}, '发布定时作业')  # 定时作业列表

                if self.draft.wait_check_page():  # 页面检查点
                    self.draft.back_up_button()
                    self.vue.switch_app()

                self.van_detail.judge_vanclass_result_operation(choose, name)  # 班级中 验证布置结果

    @testcase
    def test_003_timing_hw_delete(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        print("1.验证：删除 \n"
              "==================================================================")
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.timing_button()  # 定时作业 按钮
        self.assertTrue(self.draft.wait_check_app_page(), self.draft.timing_tips)
        self.vue.switch_h5()  # 切到vue

        hw = self.draft.timing_hw_delete()  # 删除
        if hw:  # 删除 成功
            self.draft.swipe_vertical_web(0.5, 0.3, 0.9)  # 删除成功后不会重新请求列表，需手动下拉刷新
            self.judge_result_operation(hw)

        if self.draft.wait_check_page():  # 页面检查点
            self.draft.back_up_button()  # 返回主界面

    @teststeps
    def judge_result_operation(self, hw, modify='删除'):
        """验证 删除/发布结果
        :param modify: 删除/发布
        :param hw:删除/发布的作业
        """
        self.vue.app_web_switch()  # 切到app, 切到vue
        print('-----------------------验证 {} 结果---------------------'.format(modify))
        self.assertTrue(self.draft.wait_check_page(), self.draft.back_timing_tips)  # 页面检查点
        if self.draft.wait_check_empty_tips_page():
            print('{}成功'.format(modify))
        else:
            self.assertTrue(self.draft.wait_check_hw_list_page, self.draft.timing_tips)
            name = self.draft.draft_name()  # 名称
            publish_time = self.draft.draft_time()  # 发布时间

            count = []
            for i in range(len(name)):  # 验证发布是否成功
                print(name[i].text, publish_time[i].text)
                for key in hw:
                    print(key, hw[key])
                    if name[i].text == key and publish_time[i].text == hw[key]:
                        count.append(i)
                print('-----------------------------')

            self.assertTrue(len(count) == 0, '★★★ Error -{}失败'.format(modify))
            print('{}成功'.format(modify))
