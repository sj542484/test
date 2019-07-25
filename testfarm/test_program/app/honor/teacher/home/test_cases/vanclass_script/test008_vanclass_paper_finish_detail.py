#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page import PaperPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class Paper(unittest.TestCase):
    """本班试卷 -完成情况tab 详情 """

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.v_detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.paper = PaperPage()
        cls.detail = PaperDetailPage()
        cls.get = GetAttribute()
        cls.info = DynamicPage()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_analysis_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_PAPER)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_PAPER):  # 页面检查点
                if self.van.wait_check_list_page():

                    self.van.vanclass_paper()  # 进入 本班卷子
                    if self.v_detail.wait_check_page(gv.PAPER_ANALY):  # 页面检查点
                        if WaitElement().judge_is_exists(self.v_detail.goto_pool_value):  # 无卷子时
                            print('暂无卷子，去题库看看吧')
                            # self.detail.goto_paper_pool()  # 点击 去题库 按钮
                        else:  # 有卷子
                            print('本班试卷:')
                            self.finish_situation_operation()  # 完成情况 tab

                        self.home.back_up_button()
                        if self.van.wait_check_page(gv.PAPER_ANALY):  # 本班卷子 页面检查点
                            self.home.back_up_button()
                            if self.van.wait_check_page(gv.VAN_PAPER):  # 班级详情 页面检查点
                                self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        name = self.v_detail.hw_name()  # 试卷name
        progress = self.v_detail.progress()  # 进度
        for i in range(len(name)):
            count =  progress[i].text  # int(re.sub("\D", "", progress[i].text))
            if int(count[3]) != 0:
                var = name[i].text
                name[i].click()  # 进入试卷

                if self.paper.wait_check_page():  # 页面检查点
                    print('###########################################################')
                    print('试卷:', var,'\n',count)
                    self.st_list_statistics()  # 完成情况tab 学生列表

                    break

    @teststeps
    def st_list_statistics(self):
        """完成情况tab 学生列表信息统计"""
        name = self.paper.st_name()  # 学生name
        icon = self.paper.st_icon()  # 学生头像
        status = self.paper.st_score()  # 学生完成与否 todo

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                if self.paper.wait_check_page():
                    status = self.paper.st_score()  # 学生完成与否
                    name = self.paper.st_name()  # 学生name
                    text = name[i].text  # 学生name

                    if status[i].text != '未完成':
                        name[i].click()  # 进入一个学生的答题情况页
                        if self.paper.wait_check_per_detail_page(text):  # 页面检查点
                            if self.paper.wait_check_paper_list_page():
                                print('++++++++++++++++++++++++++++++++++++++++++')
                                print('学生 %s 答题情况:' % text)
                                self.per_answer_detail()  # 答题情况详情页

                            if self.paper.wait_check_per_detail_page(text):  # 页面检查点
                                self.home.back_up_button()
                    elif self.paper.wait_check_page():  # 页面检查点
                        print('学生 %s 还未完成该套试卷' % text)
                print('-------------------------------------------------')
        else:
            print('★★★ Error-已完成/未完成 学生列表信息统计', len(icon), len(name))

    @teststeps
    def per_answer_detail(self):
        """个人 答题情况详情页"""
        if not self.detail.paper_type():
            print('★★★ Error- 试卷详情页的试卷类型')
        print('---------------------试卷详情页---------------------')

        if self.detail.score() in ('100', '120'):
            title = self.detail.score_type()
            score = self.detail.score()  # 分值
            unit = self.detail.score_unit()
            print(title, score, unit)
        else:  # A/B制
            print()

        # 考试时间
        title = self.detail.time_title()
        timestr = self.detail.time_str()
        unit = self.detail.time_unit()
        print(title, timestr, unit)

        # 小题数
        title = self.detail.num_title()
        num = self.detail.game_num()
        unit = self.detail.num_unit()
        print(title, num, unit)

        if self.detail.limit_judge():  # 限制
            print(self.detail.limit_type(), self.detail.limit_hand(), self.detail.limit_unit())
        else:
            print(self.detail.limit_type(), self.detail.limit_hand())

        print('----------------')
        self.detail.game_list_tile()
        mode = self.paper.game_title()
        score = self.paper.game_score()
        info = self.paper.game_desc()

        item = []
        for i in range(len(info)):
            item.append(mode[i])
            print(' ', mode[i].text, info[i].text, '    ', score[i + 1].text)
        print('----------------------------------')

        return item
