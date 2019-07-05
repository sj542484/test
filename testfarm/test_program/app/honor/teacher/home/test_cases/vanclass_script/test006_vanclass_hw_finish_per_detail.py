#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re
import time
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.result_detail_page import ResultDetailPage
from testfarm.test_program.app.honor.teacher.home.test_data.hw_detail_data import game_type_operation
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from testfarm.test_program.app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.wait_element import WaitElement


class VanclassHw(unittest.TestCase):
    """本班习题 - 完成情况tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.v_detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.detail = HwDetailPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_hw_per_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VAN_ANALY)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VAN_ANALY):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    if self.v_detail.wait_check_page(gv.HW_ANALY):  # 页面检查点
                        print('本班作业:')
                        if self.v_detail.wait_check_list_page():
                            name = self.v_detail.hw_name()  # 作业name
                            for i in range(len(name)):
                                if name[i].text == gv.HW_ANALY_GAME:
                                    print('###########################################################')
                                    print('作业:', name[i].text)
                                    name[i].click()  # 进入 作业

                                    self.finish_situation_operation()  # 进入 个人答题详情页
                                    break
                        elif self.home.wait_check_empty_tips_page():
                            print('暂无数据')

                        if self.van.wait_check_page(gv.HW_ANALY):  # 本班作业 页面检查点
                            self.home.back_up_button()  # 返回 班级详情页面
                            if self.van.wait_check_page(gv.VAN_ANALY):  # 班级详情 页面检查点
                                self.home.back_up_button()
                    else:
                        print('未进入 习题作业页面')
                        self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        if self.detail.wait_check_page():  # 页面检查点
            analysis = self.detail.finished_tab()  # 完成情况 tab
            if self.get.selected(analysis) is False:
                print('★★★ Error- 未默认在 完成情况 tab页')
            else:
                if self.detail.wait_check_st_list_page():
                    st = self.detail.st_name()  # 学生name
                    for i in range(len(st)):
                        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        if self.detail.wait_check_st_list_page():
                            st = self.detail.st_name()  # 学生name
                            name = st[i].text  # 学生name
                            st[i].click()  # 进入一个学生的答题情况页

                            if self.v_detail.wait_check_page(name):  # 页面检查点
                                print('学生 %s 答题情况：' % name)
                                self.per_answer_detail(['', ''], name)

                                if self.v_detail.wait_check_page(name):  # 页面检查点
                                    self.home.back_up_button()
                                    break
                elif self.home.wait_check_empty_tips_page():
                    print('暂无学生')

                if self.detail.wait_check_page():  # 页面检查点
                    self.home.back_up_button()  # 返回 本班习题 页面
        else:
            print('未进入作业 %s 页面' % gv.HW_ANALY_GAME)
            time.sleep(2)
            self.home.back_up_button()  # 返回 本班习题 页面

    @teststeps
    def per_answer_detail(self, content, st):
        """个人 答题情况详情页"""
        if self.detail.wait_check_per_detail_page():
            if self.detail.wait_check_per_detail_page():
                item = self.detail.per_game_item()  # 游戏条目

                if len(item[1]) > 4 and content[0] == '':
                    content = []
                    var = []  # 游戏name
                    if len(item[-2]) == 4:  # 无提分标志
                        var.append(item[1][-2][2])
                    else:
                        var.append(item[1][-2][3])

                    content.append(var[0])  # 最后一个game的name
                    content.append(item[1][-2][0])  # 最后一个game的type
                    self.game_type_judge_operation(len(item[1])-1, st)  # 小游戏 类型判断 及具体操作

                    if self.detail.wait_check_per_detail_page():
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
                        self.per_answer_detail(content, st)
                else:
                    var = 0
                    for k in range(len(item[1])):
                        title = []
                        if len(item[1][k]) == 4:  # 无提分标志
                            title.append(item[1][k][2])
                        else:
                            title.append(item[1][k][3])

                        if content[0] == title[0] and content[1] == item[1][k][0]:
                            var += k+1
                            break

                    self.game_type_judge_operation(len(item[1]), st, var)  # 小游戏 类型判断 及具体操作

    @teststeps
    def game_type_judge_operation(self, length, st, index=0):
        """小游戏 类型判断 及具体操作"""
        for j in range(index, length):
            if self.v_detail.wait_check_page(st):  # 页面检查点
                title = []
                item = self.detail.per_game_item()  # 游戏条目
                var = item[1][j][-1].split()

                best = re.sub("\D", "", var[1])
                score = re.sub("\D", "", var[-1])
                if len(item[1][j]) == 4:  # 无提分标志
                    title.append(item[1][j][2])
                    count = int(re.sub("\D", "", item[1][j][1]))  # 小题数
                else:
                    title.append(item[1][j][3])
                    count = int(re.sub("\D", "", item[1][j][2]))  # 小题数

                item[0][j].click()  # 点击进入game
                if best != '' and int(best) >= int(score):  # 已做
                    value = game_type_operation(item[1][j][0])
                    if self.result.wait_check_page(title[0]):
                        print(item[1][j][0], title[0])
                        print('=====================答题情况 详情页======================')
                        self.result_detail_operation(value, count, score)

                        if self.result.wait_check_page(title[0]):
                            self.home.back_up_button()
                elif best == score == '':
                    print(item[1][j][0], title[0], ' --该题还未做')
                    # if Toast().find_toast('无需答题报告，答对即可'):
                    #     print('无需答题报告，答对即可')
                    print('---------------------------------')

    @teststeps
    def result_detail_operation(self, index, num, achieve):
        """答题情况 详情页"""
        value = self.result.first_report()  # 首次正答
        self.judge_first_achieve(achieve, value)  # 验证 首次成绩 与首次正答
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
            item = 0
            if index == 14:
                if not WaitElement().judge_is_exists(self.result.voice_value):  # 判断是否存在 发音按钮
                    item = 1

            if len(hint) > 4 and content[0] == '':
                content = [hint[-2].text]

                for j in range(len(hint) - 1):
                    hint = self.result.result_explain()  # 解释
                    print('题目:', self.result.result_answer(j), '\n',
                          "解释:", hint[j].text, '\n',
                          "对错标识:", self.result.result_mine(j))  # 正确word/句子 &解释 &对错标识
                    print('-----------------------------------------------')
                    if item == 0:
                        self.result.result_voice(j)  # 点击 发音按钮

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
                        if item == 0:
                            self.result.result_voice(j)  # 点击发音按钮

    @teststeps
    def judge_first_achieve(self, achieve, report):
        """验证 首次成绩 与首次正答"""
        num = int(re.sub("\D", "", achieve))
        var = report.split('/')
        value = int(re.sub("\D", "", var[0]))

        if num != int(value / int(var[1]) * 100):
            print('★★★ Error- 首次成绩 与首次正答 不匹配:', achieve, report)
