#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.result_detail_page import ResultDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.paper_detail_data import game_type_operation
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.paper_detail_page import PaperPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.wait_element import WaitElement


class VanclassPaper(unittest.TestCase):
    """本班试卷 -完成情况tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.paper = PaperPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_paper_game_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_PAPER)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_PAPER):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_paper()  # 进入 本班卷子
                    if self.detail.wait_check_page(gv.PAPER_ANALY):  # 页面检查点
                        if WaitElement().judge_is_exists(self.detail.goto_pool_value):  # 无卷子时
                            print('暂无卷子，去题库看看吧')
                            # self.detail.goto_paper_pool()  # 点击 去题库 按钮
                        elif self.detail.wait_check_list_page():  # 有卷子
                            print('本班试卷:')
                            name = self.detail.hw_name()  # 试卷name
                            progress = self.detail.progress()  # 进度
                            for i in range(len(name)):
                                count = progress[i].text  # int(re.sub("\D", "", progress[i].text))
                                if int(count[3]) != 0:
                                    var = name[i].text
                                    name[i].click()  # 进入试卷

                                    if self.paper.wait_check_page():  # 页面检查点
                                        print('###########################################################')
                                        print('试卷:', var, '\n', count)
                                        self.finish_situation_operation()  # 具体操作
                                        if self.paper.wait_check_page():  # 页面检查点
                                            self.home.back_up_button()
                                    break
                    else:
                        print('未进入 本班试卷页面')
                    if self.van.wait_check_page(gv.PAPER_ANALY):  # 本班卷子 页面检查点
                        self.home.back_up_button()  # 返回 班级页面
            else:
                print('未进入班级:', gv.VAN_PAPER)
            if self.van.wait_check_page(gv.VAN_PAPER):  # 班级 页面检查点
                self.home.back_up_button()  # 返回 主界面
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
            print('---------------------完成情况tab---------------------')
            if self.paper.wait_check_st_list_page():
                status = self.paper.st_score()  # 学生完成与否

                for i in range(len(status)):
                    if self.paper.wait_check_st_list_page():
                        name = self.paper.st_name()  # 学生name
                        status = self.paper.st_score()  # 学生完成与否
                        if status[i].text == '未完成':
                            print('-------------------------------------------')
                            print('学生 %s 还未完成该试卷' % name[i].text)
                        else:
                            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            text = name[i].text
                            name[i].click()  # 进入一个学生的答题情况页

                            if self.detail.wait_check_page(text):  # 页面检查点
                                print('学生 %s 答题情况:' % text)
                                self.paper_detail_operation(text, ['', ''])  # 试卷 详情页

                                if self.paper.wait_check_paper_list_page():
                                    self.home.back_up_button()  # 返回 tab页
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def paper_detail_operation(self, st, content):
        """答题具体信息 页面"""
        if self.paper.wait_check_paper_list_page():
            mode = self.paper.game_title()  # 游戏类型 元素
            info = self.paper.game_desc()  # 共x题 xx分

            if len(info) > 4 and content[0] == '':
                content = [mode[len(info)-2].text, info[-2].text]

                self.result_detail_operation(0, len(info)-1, st)  # 答题详情页

                if self.detail.wait_check_page(st):  # 页面检查点
                    SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                    self.paper_detail_operation(st, content)

                return content
            else:
                var = 0
                for k in range(len(mode)):
                    if content[0] == mode[k].text and content[1] == info[k].text:
                        var += k
                        break

                self.result_detail_operation(var, len(info), st)  # 答题详情页

    @teststeps
    def result_detail_operation(self, var, length, st):
        """答题 详情页"""
        for i in range(var, length):
            if self.detail.wait_check_page(st):  # 页面检查点
                if self.paper.wait_check_paper_list_page():
                    mode = self.paper.game_title()  # 游戏类型 元素
                    # score = self.paper.game_score()  # 得分
                    info = self.paper.game_desc()[i].text  # 共x题 xx分

                    if self.detail.wait_check_page(st):  # 页面检查点
                        count = int(re.sub("\D", "", info.split(' ')[0]))  # 小题数

                        text = mode[i].text.split(' ')[0]  # # 游戏类型
                        print(text)
                        value = game_type_operation(text)
                        mode[i].click()  # 进入游戏 详情页

                        if self.paper.wait_check_per_detail_page(text):
                            if self.paper.wait_check_per_answer_page():
                                self.game_detail_operation(value, count)

                                if self.paper.wait_check_per_detail_page(text):
                                    self.home.back_up_button()  # 返回 答题详情页

    @teststeps
    def game_detail_operation(self, index, num):
        """游戏 详情页"""
        self.result.first_report()  # 首次正答
        print('-------------------------')
        if index == 2:  # 有选项
            self.result.swipe_operation(num)  # 单选题滑屏及具体操作
        else:  # 答案+解释
            self.answer_explain_type([''], index)

        print('==========================================================')

    @teststeps
    def answer_explain_type(self, content, index):
        """答案/解释类型"""
        if self.result.wait_check_answer_list_page():
            hint = self.result.result_explain()  # 解释

            if len(hint) > 8 and content[0] == '':
                content = [hint[-2].text]

                for j in range(len(hint) - 1):
                    hint = self.result.result_explain()  # 解释
                    print('题目:', self.result.result_answer(j), '\n',
                          "解释:", hint[j].text, '\n',
                          "对错标识:", self.result.result_mine(j))  # 正确word/句子 &解释 &对错标识
                    print('-----------------------------------------------')

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.answer_explain_type(content, index)

                return content
            else:
                if content[0] != hint[-1].text:
                    var = 0
                    for k in range(len(hint)):
                        if content[0] == hint[k].text:
                            var += k + 1
                            break

                    for j in range(var, len(hint)):
                        hint = self.result.result_explain()  # 解释
                        print('题目:', self.result.result_answer(j), '\n',
                              "解释:", hint[j].text, '\n',
                              "对错标识:", self.result.result_mine(j))  # 正确word/句子 &解释 &对错标识

                        print('-----------------------------------------')
