#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.hw_analysis_tab_answer_game_detail_page import *
from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.test_data.hw_detail_data import game_type_operation
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.vue_context import VueContext


class VanclassHw(unittest.TestCase):
    """本班习题 - 答题分析tab 详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.van_detail = VanclassDetailPage()
        cls.v_hw = VanclassHwPage()
        cls.hw_detail = HwDetailPage()
        cls.game_detail = VanclassGameDetailPage()


        cls.get = GetAttribute()
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
    def test_vanclass_hw_answer_analysis(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)

        self.van_detail.vanclass_hw()  # 点击 本班作业 tab
        title = gv.HW_TITLE.format(gv.VANCLASS)
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        if self.v_hw.wait_check_empty_tips_page():
            self.v_hw.no_data()  # 暂无数据
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
        else:
            print('本班作业:')
            self.hw_list_operation()  # 具体操作

        self.assertTrue(self.v_hw.wait_check_page(title), self.v_hw.van_hw_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切回vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
        self.v_hw.back_up_button()  # 返回主界面

    @teststeps
    def hw_list_operation(self):
        """作业列表"""
        self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
        name = self.v_hw.hw_name()  # 作业name
        count = []
        for i in range(4, len(name)):
            self.assertTrue(self.v_hw.wait_check_list_page(), self.v_hw.van_hw_list_tips)  # 页面检查点
            text = name[i].text
            if self.home.brackets_text_in(text) == '习题':
                count.append(i)
                print('#########################################################################')
                name[i].click()  # 进入作业

                self.vue.app_web_switch()  # 切到apk 再切到vue
                self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)  # 页面检查点
                self.hw_detail.analysis_tab()  # 进入 答题分析 tab页

                status = self.hw_detail.wait_check_empty_tips_page()
                if status:
                    print('暂无数据')
                    self.v_hw.back_up_button()  # 返回
                    self.vue.app_web_switch()  # 切到apk 再切到vue
                    if self.v_hw.wait_check_page():
                        self.v_hw.back_up_button()  # 返回
                        self.vue.app_web_switch()  # 切到apk 再切到vue

                        if self.van_detail.wait_check_page():  # 页面检查点
                            self.v_hw.back_up_button()  # 返回 主界面
                            self.vue.switch_app()  # 切回apk
                    self.assertFalse(status, '暂无数据')
                else:
                    self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
                    self.answer_detail_operation()  # 具体操作

                self.assertTrue(self.hw_detail.wait_check_page(), self.hw_detail.hw_detail_tips)
                self.v_hw.back_up_button()  # 返回 本班作业 作业列表
                self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertFalse(len(count)==0, '暂无测试数据')

    @teststeps
    def answer_detail_operation(self):
        """答题情况 详情页"""
        mode = self.hw_detail.game_type()  # 游戏类型
        name = self.hw_detail.game_name()  # 游戏名称

        for j in range(len(name)):
            self.assertTrue(self.hw_detail.wait_check_hw_list_page(), self.hw_detail.hw_list_tips)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(mode[j].text, '\n', name[j].text)
            value = game_type_operation(mode[j].text)
            game = name[j].text

            if value in (1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 18):
                mode[j].click()  # 点击game
                self.vue.app_web_switch()  # 切到apk 再切到vue

                self.game_detail_operation(value, game)  # 游戏详情页
            elif value in (21, 22, 23):  # 口语看读/背诵/跟读
                print('口语')  # todo
                mode[j].click()  # 点击game
                self.vue.app_web_switch()  # 切到apk 再切到vue

                self.v_hw.back_up_button()   # 返回  游戏列表
            elif value == 24:
                mode[j].click()  # 点击game
                self.vue.app_web_switch()  # 切到apk 再切到vue

                self.v_hw.back_up_button()   # 返回  游戏列表
            else:  # 10单词听写/11单词拼写/12猜词游戏/13词汇选择/14闪卡练习/16连连看/17微课/19连词成句/20还原单词
                mode[j].click()  # 点击game
                if value == 17:  # 微课
                    tips = '无需答题报告'
                else:
                    tips = TipsData().no_report
                MyToast().toast_assert(self.name, Toast().toast_vue_operation(tips))  # 获取toast

            self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def game_detail_operation(self, index, game_name):
        """游戏详情页"""
        content = []
        self.assertTrue(self.game_detail.wait_check_page(game_name), self.game_detail.detail_tips)  # 页面检查点
        print('=======================游戏详情页=======================')

        if index == 1:  # 听后选择
            self.game_detail.listen_choose_operation(content)  # 具体操作
        elif index == 2:  # 单项选择
            self.game_detail.single_choose_operation(content)  # 具体操作
        elif index == 3:  # 强化炼句
            self.game_detail.strength_sentence_operation(content)  # 具体操作
        elif index == 4:  # 听音连句
            self.game_detail.listen_ergodic_list(content)  # 具体操作
        elif index == 5:  # 句型转换
            self.game_detail.sentence_trans_ergodic_list(content)  # 具体操作
        elif index == 6:  # 阅读理解
            self.game_detail.reading_article_list_operation(content)  # 具体操作
        elif index == 7:  # 完形填空
            self.game_detail.cloze_test_list_operation(content)  # 具体操作
        elif index == 8:  # 补全文章
            self.game_detail.complete_article_operation(content)  # 具体操作
        elif index == 9:  # 选词填空
            self.game_detail.choose_vocabulary_block(content)  # 具体操作
        elif index == 15:  # 听音选图
            self.game_detail.picture_list_operation(content)  # 具体操作
        elif index == 18:  # 磨耳朵
            self.game_detail.ears_ergodic_list(content)  # 具体操作
        elif index == 24:  # 单词跟读
            print('单词跟读')
            # self.game_detail.word_reading_operation()  # 具体操作

        self.assertTrue(self.game_detail.wait_check_page(game_name), self.game_detail.detail_tips)  # 页面检查点
        self.v_hw.back_up_button()  # 返回

        print('=========================================================')
