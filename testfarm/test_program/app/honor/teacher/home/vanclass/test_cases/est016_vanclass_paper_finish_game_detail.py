#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest
import re

from app.honor.teacher.home.vanclass.object_page.vanclass_paper_finish_detail_page import PaperDetailPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.paper_detail_data import game_type_operation
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.object_page.paper_finish_tab_student_answer_result_detail_page import PaperResultDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class VanclassPaper(unittest.TestCase):
    """本班试卷 -完成情况tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.van_paper = VanclassPaperPage()
        cls.van_detail = VanclassDetailPage()
        cls.report = PaperReportPage()
        cls.paper = PaperDetailPage()
        cls.result = PaperResultDetailPage()

        cls.get = GetAttribute()
        cls.my_toast = MyToast()
        cls.vue = VueContext()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassPaper, self).run(result)
        
    @testcase
    def test_vanclass_paper_game_detail(self):
        self.login.app_status()  # 判断APP当前状态

        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到web
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)
        
        self.van_detail.vanclass_paper()  # 进入 本班卷子
        self.vue.app_web_switch()  # 切到apk 再切回web
        title = gv.PAPER_TITLE.format(gv.VANCLASS)

        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        if self.van_paper.wait_check_empty_tips_page():  # 无卷子时
            self.van_paper.no_data()  # 暂无数据
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)  # 页面检查点
        else:
            print('本班试卷:')
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)  # 页面检查点
            name = self.van_paper.hw_name()  # 试卷name
            progress = self.van_paper.progress()  # 进度
            count = []
            for i in range(len(name)):
                create = progress[i].text
                pro = int(re.sub("\D", "", create.split()[-1])[0])
                var = name[i].text
    
                if pro != 0 and '试卷' in self.home.brackets_text_in(var):
                    count.append(i)
                    name[i].click()  # 进入试卷
                    self.vue.app_web_switch()  # 切到apk 再切到vue
                    print('###########################################################')
                    print('试卷:', var, '\n', create)
                    self.finish_situation_operation()  # 具体操作
    
                    if self.report.wait_check_st_list_page():
                        self.van_paper.back_up_button()  # 返回 试卷列表
                    
            if self.report.wait_check_page():  # 页面检查点
                self.van_paper.back_up_button()

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)  # 页面检查点
        print('---------------------完成情况tab---------------------')
        if self.report.wait_check_empty_tips_page():
            self.assertTrue(self.report.wait_check_empty_tips_page(), '暂无数据')
            print('暂无数据')
        else:
            self.assertTrue(self.report.wait_check_st_list_page(), self.report.st_list_tips)
            status = self.report.st_score()  # 学生完成与否
            for i in range(len(status)):
                self.assertTrue(self.report.wait_check_st_list_page(), self.report.st_list_tips)
                name = self.report.st_name()  # 学生name
                status = self.report.st_score()  # 学生完成与否
                if status[i].text == '未完成':
                    print('-------------------------------------------')
                    print('学生 %s 还未完成该试卷' % name[i].text)
                else:
                    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    text = name[i].text
                    name[i].click()  # 进入学生的答题情况页

                    if self.van_paper.wait_check_page(text):  # 页面检查点
                        print('学生 %s 答题情况:' % text)
                        self.per_answer_detail(text)  # 试卷 详情页

                        if self.van_paper.wait_check_page(text):
                            self.van_detail.back_up_button()  # 返回 试卷列表

    @teststeps
    def per_answer_detail(self, title):
        """个人 答题情况详情页"""
        self.assertTrue(self.paper.wait_check_page(title), self.paper.paper_tips)  # 页面检查点
        self.assertTrue(self.paper.wait_check_list_page(), self.paper.paper_list_tips)
        mode = self.report.game_title()
        score = self.report.game_score()
        info = self.report.game_desc()

        for i in range(len(info)):
            game = mode[i].text
            print(game, info[i].text, '    ', score[i].text)
            mode[i].click()

            self.paper_detail_operation(game)  # 个人 答题情况 游戏详情页

    @teststeps
    def paper_detail_operation(self, st):
        """个人 答题情况 游戏详情页"""
        self.assertTrue(self.result.wait_check_page(), self.result.result_tips)  # 页面检查点
        item = self.result.per_game_item()[1]  # 游戏条目

        for j in range(len(item)):
            print('=================================================================')
            self.assertTrue(self.result.wait_check_page(st), self.result.result_tips)  # 页面检查点
            mode = self.result.game_mode(item[1][j][-2])
            var = item[1][j][-1].split()  # '最优成绩100% 首轮成绩100%'
            best = re.sub("\D", "", var[0])
            score = re.sub("\D", "", var[-1])

            if best != '' and int(best) >= int(score):  # 已做
                value = game_type_operation(item[1][j][0])
                print(item[1][j][0], value)
                print('--------------------答题情况 详情页---------------------')

                if value == 17:  # 微课
                    item[0][j].click()  # 点击进入game
                    MyToast().toast_assert(self.name, Toast().toast_vue_operation(TipsData().no_report))  # 获取toast
                elif value == 24:  # 单词跟读
                    item[0][j].click()  # 点击进入game
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    self.result.word_reading_operation(score)
                elif value in (21, 22, 23):  # 口语
                    print('口语')  #
                    item[0][j].click()  # 点击进入game
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    self.v_hw.back_up_button()   # 返回  游戏列表
                elif value == 14:  # 闪卡练习
                    print(mode)
                    item[0][j].click()  # 点击进入game
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    content = []
                    if mode == '句子学习':
                        self.result.flash_sentence_operation(content, score)
                    elif mode in ('单词学习', '单词抄写'):
                        self.result.flash_card_list_operation(content, score)
                elif value == 16:  # 连连看
                    item[0][j].click()  # 点击进入game
                    self.vue.app_web_switch()  # 切到apk 再切回vue

                    content = []
                    print(mode)
                    if mode == '文字模式':
                        if self.result.wait_check_list_page():
                            self.result.report_score_compare(score)  # 验证 首次成绩 与首次正答

                        self.result.list_operation(content)
                    elif mode == '图文模式':  # 图文模式
                        self.result.match_img_operation(content, score)
                elif value == 18:  # 磨耳朵
                    item[0][j].click()  # 点击进入game
                    self.vue.app_web_switch()  # 切到apk 再切回vue
                    self.result.ears_ergodic_list()
                else:
                    item[0][j].click()  # 点击进入game
                    self.vue.app_web_switch()  # 切到apk 再切回vue
                    self.result.hw_detail_operation(value, score)
            elif best == score == '':
                print(item[1][j][0], ' --该题还未做')

            self.vue.app_web_switch()  # 切到apk 再切回vue

    @teststeps
    def per_game_list(self, st):
        """个人 game答题情况页 列表"""
        self.assertTrue(self.result.wait_check_page(st), self.result.st_detail_tips)  # 页面检查点
        name = self.result.game_name()  # 游戏name
        mode = self.result.game_type()  # 类型
        status = self.result.optimal_first_achievement()  # 游戏完成情况

        for i in range(len(status)-1):
            print(mode[i].text, name[i].text, status[i].text)
