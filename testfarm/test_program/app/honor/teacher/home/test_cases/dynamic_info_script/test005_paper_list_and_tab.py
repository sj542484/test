#!/usr/bin/env python
import unittest

from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page import PaperPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.test_data import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Paper(unittest.TestCase):
    """卷子列表 & 答卷分析/完成情况tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.info = DynamicPage()
        cls.paper = PaperPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_list_tab(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_list_page():  # 页面加载完成 检查点
                self.home.paper_icon()  # 进入卷子 最近动态页面

                if self.info.wait_check_paper_page():  # 页面检查点
                    if self.info.wait_check_list_page():
                        self.info.help_operation()  # 右上角 提示按钮

                        self.info.swipe_operation()  # 列表
                        self.info.into_hw(gv.PAPER_TITLE)  # 进入 作业包

                        if self.paper.wait_check_page():  # 页面检查点
                            self.finish_situation_operation()  # 完成情况 tab
                            self.answer_analysis_operation()  # 答卷分析 tab

                            if self.paper.wait_check_page():  # 页面检查点
                                self.home.back_up_button()  # 返回 卷子动态页面
                                if self.info.wait_check_paper_page():  # 页面检查点
                                    pass
                    else:
                        print('最近卷子动态页面为空')
                    self.home.back_up_button()  # 返回 主界面
            else:
                print('暂无班级')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        complete = self.paper.finished_tab()  # 完成情况 tab
        if self.get.selected(complete) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('-------------------完成情况tab-------------------')
            if self.paper.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况 学生列表
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def answer_analysis_operation(self):
        """答卷分析tab 具体操作"""
        if self.paper.wait_check_page():  # 页面检查点
            analysis = self.paper.analysis_tab()  # 答卷分析 tab
            if self.get.selected(analysis) is True:
                print('★★★ Error- 默认在 答卷分析 tab页')
            else:
                analysis.click()  # 进入 答卷分析 tab页
                if self.get.selected(analysis) is False:
                    print('★★★ Error- 进入 答卷分析 tab页')
                else:
                    print('-------------------答卷分析tab-------------------')
                    if self.paper.wait_check_paper_list_page():
                        self.answer_analysis_detail()  # 答卷分析页 list
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, content=None):
        """答卷分析 详情页"""
        if content is None:
            content = []

        mode = self.paper.game_type()  # 游戏类型
        name = self.paper.game_name()  # 游戏name
        average = self.paper.van_average_achievement()  # 全班平均得分x分; 总分x分

        if len(mode) > 4 and not content:
            content = []
            for j in range(len(mode) - 1):
                print(mode[j].text, name[j].text, '\n',
                      average[j].text)
                print('----------------------')

            content.append(name[len(mode) - 2].text)  # 最后一个game的name
            content.append(mode[-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content)
        else:
            mode = self.paper.game_type()  # 游戏类型
            name = self.paper.game_name()  # 游戏name
            average = self.paper.van_average_achievement()  # 全班平均得分x分; 总分x分

            var = 0
            if content:
                if content[0] != name[-1].text and content[1] != mode[-1].text:
                    for k in range(len(name)):
                        if content[0] == name[k].text and content[1] == mode[k].text:
                            var += k
                            break

            for j in range(var, len(name)):
                print(mode[j].text, name[j].text, '\n',
                      ' ', average[j].text)
                print('----------------------')

    @teststeps
    def st_list_statistics(self):
        """已完成/未完成 学生列表信息统计"""
        name = self.paper.st_name()  # 学生name
        icon = self.paper.st_icon()  # 学生头像
        status = self.paper.st_score()  # 学生完成与否 todo

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

        else:
            print('★★★ Error-已完成/未完成 学生列表信息统计', len(icon), len(name))
