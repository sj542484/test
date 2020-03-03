#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import unittest

from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.dynamic_info.object_page.paper_detail_page import PaperReportPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
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
        cls.van = VanclassPage()
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

        self.assertTrue(self.van.wait_check_app_page(gv.VANCLASS), self.van.van_tips)  # 页面检查点
        self.vue.switch_h5()  # 切到vue
        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)
        self.van.vanclass_paper()  # 进入 本班卷子
        self.vue.app_web_switch()  # 切到apk 再切回web

        title = gv.PAPER_TITLE.format(gv.VANCLASS)
        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        if self.van_paper.wait_check_empty_tips_page():
            self.assertFalse(self.van_paper.wait_check_empty_tips_page(), '★★★ Error-班级试卷为空, {}')
        else:
            self.assertTrue(self.van_paper.wait_check_list_page(), self.van_paper.paper_list_tips)
            print('本班试卷:')
            self.finish_situation_operation()  # 完成情况 tab

        self.van.back_up_button()
        self.vue.app_web_switch()  # 切到apk 再切到vue
        self.assertTrue(self.van_paper.wait_check_page(title), self.van_paper.paper_tips)  # 页面检查点
        self.van_paper.back_up_button()  # 返回 班级详情页面
        self.vue.app_web_switch()  # 切到apk 再切到vue

        self.assertTrue(self.van.wait_check_page(gv.VANCLASS), self.van.van_vue_tips)  # 班级详情 页面检查点
        self.van.back_up_button()  # 返回主界面

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        name = self.van_paper.hw_name()  # 试卷name
        progress = self.van_paper.progress()  # 进度
        count = 0
        for i in range(len(name)):
            pro = progress[i].text  # int(re.sub("\D", "", progress[i].text))
            var = name[i].text
            if int(pro[3]) != 0 and self.home.brackets_text_in(var) == '试卷':
                count += 1
                name[i].click()  # 进入试卷
                print('###########################################################')
                print('试卷:', var, '\n', pro)
                if self.report.wait_check_page():  # 页面检查点
                    self.st_list_statistics()  # 完成情况tab 学生列表
                break

        if count == 0:
            print('暂无试卷或者暂无学生完成该试卷')


    @teststeps
    def st_list_statistics(self):
        """完成情况tab 学生列表信息统计"""
        name = self.report.st_name()  # 学生name
        icon = self.report.st_icon()  # 学生头像
        status = self.report.st_score()  # 学生完成与否

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                if self.report.wait_check_page():
                    status = self.report.st_score()  # 学生完成与否
                    name = self.report.st_name()  # 学生name
                    text = name[i].text  # 学生name

                    if status[i].text != '未完成':
                        name[i].click()  # 进入一个学生的答题情况页
                        if self.report.wait_check_per_detail_page(text):  # 页面检查点
                            if self.report.wait_check_paper_list_page():
                                print('++++++++++++++++++++++++++++++++++++++++++')
                                print('学生 %s 答题情况:' % text)
                                self.per_answer_detail()  # 答题情况详情页

                            if self.report.wait_check_per_detail_page(text):  # 页面检查点
                                self.home.back_up_button()
                    elif self.report.wait_check_page():  # 页面检查点
                        print('学生 %s 还未完成该套试卷' % text)
                print('-------------------------------------------------')
        else:
            print('★★★ Error-已完成/未完成 学生列表信息统计', len(icon), len(name))

    @teststeps
    def per_answer_detail(self):
        """个人 答题情况详情页"""
        if not self.paper.paper_type():
            print('★★★ Error- 试卷详情页的试卷类型')
        print('---------------------试卷详情页---------------------')

        if self.paper.score() in ('100', '120'):
            title = self.paper.score_type()
            score = self.paper.score()  # 分值
            unit = self.paper.score_unit()
            print(title, score, unit)
        else:  # A/B制
            print('A/B制')

        # 考试时间
        title = self.paper.time_title()
        timestr = self.paper.time_str()
        unit = self.paper.time_unit()
        print(title, timestr, unit)

        # 小题数
        title = self.paper.num_title()
        num = self.paper.game_num()
        unit = self.paper.num_unit()
        print(title, num, unit)

        if self.paper.limit_judge():  # 限制
            print(self.paper.limit_type(), self.paper.limit_hand(), self.paper.limit_unit())
        else:
            print(self.paper.limit_type(), self.paper.limit_hand())

        print('----------------')
        self.paper.game_list_title()
        mode = self.report.game_title()
        score = self.report.game_score()
        info = self.report.game_desc()

        item = []
        for i in range(len(info)):
            item.append(mode[i])
            print(' ', mode[i].text, info[i].text, '    ', score[i + 1].text)
        print('----------------------------------')

        return item
