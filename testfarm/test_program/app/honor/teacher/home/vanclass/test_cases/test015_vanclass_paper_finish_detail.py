#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_finish_detail_page import PaperDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.assert_package import MyToast
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext


class VanclassPaper(unittest.TestCase):
    """本班试卷 -完成情况tab 详情 """

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
        cls.get = GetAttribute()
        cls.vue = VueContext()
        cls.my_toast = MyToast()

        BasePage().set_assert(cls.ass)

    @teardown
    def tearDown(self):
        self.vue.switch_app()  # 切回apk
        self.login.tearDown(self.ass, self.my_toast, self.ass_result)  # 统计错误情况

    def run(self, result=None):
        self.ass_result = result
        super(VanclassPaper, self).run(result)

    @testcase
    def test_paper_analysis_detail(self):
        self.login.app_status()  # 判断APP当前状态
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.assertTrue(self.home.wait_check_page(), self.home.home_tips)
        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页

        self.assertTrue(self.van_detail.wait_check_app_page(gv.VANCLASS), self.van_detail.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)
        self.van_detail.vanclass_paper()  # 进入 本班卷子
        self.vue.app_web_switch()  # 切到apk 再切到vue

        title = gv.PAPER_TITLE.format(gv.VANCLASS)
        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        if self.van_paper.wait_check_empty_tips_page():
            self.assertFalse(self.van_paper.wait_check_empty_tips_page(), '★★★ Error-班级试卷为空, {}')
        else:
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)
            print('本班试卷:')
            self.finish_situation_operation()  # 完成情况 tab

        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        self.van_paper.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van_detail.wait_check_page(gv.VANCLASS), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
        self.van_detail.back_up_button()  # 返回主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
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
                self.st_list_statistics()  # 完成情况tab 学生列表
                break

        self.assertFalse(len(count)==0, '暂无试卷或者暂无学生完成该试卷')

    @teststeps
    def st_list_statistics(self):
        """完成情况tab 学生列表信息统计"""
        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        name = self.report.st_name()  # 学生name

        for i in range(len(name)):
            self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
            status = self.report.st_score()  # 学生完成与否
            name = self.report.st_name()  # 学生name
            text = name[i].text  # 学生name

            if status[i].text != '未完成':
                print('++++++++++++++++++++++++++++++++++++++++++')
                print('学生 %s 答题情况:' % text)
                name[i].click()  # 进入一个学生的答题情况页
                self.vue.app_web_switch()  # 切到apk 再切到vue

                self.per_answer_detail(text)  # 答题情况详情页

                self.assertTrue(self.report.wait_check_per_detail_page(text), self.report.paper_detail_tips)  # 页面检查点
                self.van_paper.back_up_button()  # 返回 完成情况 页面
                self.vue.app_web_switch()  # 切到apk 再切到vue
            elif self.report.wait_check_page():  # 页面检查点
                print('学生 %s 还未完成该套试卷' % text)
            print('-------------------------------------------------')

        self.assertTrue(self.report.wait_check_page(), self.report.paper_detail_tips)
        self.van_paper.back_up_button()  # 返回 本班试卷
        self.vue.app_web_switch()  # 切到apk 再切到vue

    @teststeps
    def per_answer_detail(self, title):
        """个人 答题情况详情页"""
        self.assertTrue(self.paper.wait_check_page(title), self.paper.paper_tips)  # 页面检查点
        self.assertTrue(self.paper.wait_check_list_page(), self.paper.paper_list_tips)
        if not self.paper.paper_type():
            print('★★★ Error- 试卷详情页的试卷类型')
        print('---------------------试卷详情页---------------------')

        mode = self.paper.score_type()
        if re.sub('\D', '', mode[0]) in ('100', '120'):
            print('分数制')
        else:  # A/B制
            print('A/B制')
        print(mode)
        print(self.paper.test_time())  # 考试时间
        print(self.paper.games_num())  # 小题数
        print(self.paper.limit_type())  # 限制/不限制交卷

        print('----------------')
        self.paper.game_list_title()
        mode = self.report.game_title()
        score = self.report.game_score()
        info = self.report.game_desc()

        item = []
        for i in range(len(info)):
            item.append(mode[i])
            print(' ', mode[i].text, info[i].text, '    ', score[i].text)
        print('----------------------------------')

        return item
