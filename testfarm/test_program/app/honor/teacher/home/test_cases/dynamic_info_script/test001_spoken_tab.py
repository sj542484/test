#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.dynamic_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class Spoken(unittest.TestCase):
    """口语 完成情况&答题分析 tab"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.speak = SpokenDetailPage()
        cls.info = DynamicPage()
        cls.get = GetAttribute()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_spoken_tab(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_list_page():  # 页面加载完成 检查点
                self.home.spoken_icon()  # 进入口语 最近动态页面

                if self.info.wait_check_spoken_page():  # 页面检查点
                    if self.info.wait_check_list_page():
                        self.info.help_operation()  # 右上角 提示按钮

                        self.info.swipe_operation(0)  # 作业包 列表
                        self.info.into_hw(gv.SPOKEN_TITLE)  # 进入 作业包

                        if self.speak.wait_check_page():  # 页面检查点
                            if self.speak.wait_check_st_list_page():
                                self.finish_situation_operation()  # 完成情况 tab
                                self.answer_analysis_operation()  # 答题分析 tab

                            if self.speak.wait_check_page():  # 页面检查点
                                self.home.back_up_button()  # 返回 口语list 页面
                                if self.info.wait_check_spoken_page():  # 页面检查点
                                    pass
                    else:
                        print('最近口语动态页面为空')

                    self.home.back_up_button()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        analysis = self.detail.finished_tab()  # 完成情况 tab
        if self.get.selected(analysis) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('====================完成情况tab====================')
            if self.speak.wait_check_st_list_page():
                self.st_list_statistics(['', ''])  # 完成情况tab 列表信息
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def st_list_statistics(self, content):
        """完成情况 tab页信息"""
        name = self.detail.st_name()  # 学生name
        status = self.detail.st_finish_status()  # 学生完成与否

        if len(name) > 7 and content[0] == '':
            content = []
            for i in range(len(name)-1):
                print('学生:', name[i].text, ' ', status[i].text)  # 打印所有学生信息

            content.append(name[-2].text)  # 最后一个game的name
            content.append(status[len(name)-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.st_list_statistics(content)

            return content
        else:
            var = 0
            for k in range(len(name)):
                if content[0] == name[k].text and content[1] == status[k].text:
                    var += k
                    break

            for j in range(var, len(name)):
                print('学生:', name[j].text, ' ', status[j].text)  # 打印所有学生信息

    @teststeps
    def answer_analysis_operation(self):
        """答题分析tab 具体操作"""
        if self.detail.wait_check_page():  # 页面检查点
            analysis = self.detail.analysis_tab()  # 答题分析 tab
            if self.get.selected(analysis) is True:
                print('★★★ Error- 默认在 答题分析 tab页')
            else:
                analysis.click()  # 进入 答题分析 tab页
                if self.get.selected(analysis) is False:
                    print('★★★ Error- 进入 答题分析 tab页')
                else:
                    print('====================答题分析tab====================')
                    if self.speak.wait_check_spoken_list_page():
                        self.answer_analysis_detail(['', ''])  # 答题分析tab 列表信息
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def answer_analysis_detail(self, content):
        """答题分析 tab页信息"""
        mode = self.detail.game_type()  # 游戏类型
        name = self.detail.game_name()  # 游戏name
        average = self.detail.average_achievement()  # 本班完成率

        if len(mode) > 5 and content[0] == '':
            content = []
            for j in range(len(mode) - 1):
                print(mode[j].text, name[j].text, average[j].text)

            content.append(name[len(mode)-2].text)  # 最后一个game的name
            content.append(mode[-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_analysis_detail(content)

            return content
        else:
            var = 0
            for k in range(len(mode)):
                if content[0] == name[k].text and content[1] == mode[k].text:
                    var += k
                    break

            for j in range(var, len(mode)):
                print(mode[j].text, name[j].text, average[j].text)
