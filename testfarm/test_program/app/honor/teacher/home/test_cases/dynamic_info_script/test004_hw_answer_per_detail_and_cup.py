#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re

from testfarm.test_program.app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.test_data.dynamic_data import GetVariable as gv
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class Homework(unittest.TestCase):
    """习题 - 完成情况tab 详情 &cup"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.v_detail = VanclassDetailPage()
        cls.get = GetAttribute()
        cls.info = DynamicPage()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_hw_per_detail_and_cup(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_list_page():  # 页面加载完成 检查点
                self.home.hw_icon()  # 进入习题 最近动态页面

                if self.info.wait_check_hw_page():  # 页面检查点
                    if self.info.wait_check_list_page():
                        self.info.into_hw(gv.HW_TITLE)  # 进入 作业包

                        if self.detail.wait_check_page():  # 页面检查点
                            self.finish_situation_operation()  # 完成情况 tab
                            self.answer_analysis_operation()  # 答题分析 tab

                            if self.detail.wait_check_page():  # 页面检查点
                                self.home.back_up_button()  # 返回
                                if self.info.wait_check_hw_page():  # 页面检查点
                                    pass
                    else:
                        print('最近习题动态页面为空')

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
            print('-------------------------完成情况tab-------------------------')
            if self.detail.wait_check_st_list_page():
                self.st_list_statistics()  # 完成情况tab 学生
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

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
                    print('-------------------------答题分析tab-------------------------')
                    if self.detail.wait_check_hw_list_page():
                        self.answer_analysis_detail([''])  # 答题分析 列表
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')

    @teststeps
    def st_list_statistics(self):
        """完成情况tab 学生信息"""
        name = self.detail.st_name()  # 学生name
        icon = self.detail.st_icon()  # 学生头像
        status = self.detail.st_finish_status()  # 学生完成与否
        # arrow = self.detail.arrow_button()  # 转至按钮

        if len(name) == len(icon) == len(status):
            for i in range(len(name)):
                if self.detail.wait_check_page():  # 页面检查点
                    status = self.detail.st_finish_status()  # 学生完成与否
                    name = self.detail.st_name()  # 学生name
                    text = name[i].text
                    if status[i].text == '未完成':
                        print('学生 %s 未完成该作业' % text)
                    else:
                        name[i].click()  # 进入一个学生的答题情况页
                        if self.v_detail.wait_check_page(text):  # 页面检查点
                            print('学生 %s 答题情况:' % text)
                            self.per_answer_detail(['', ''])  # 答题情况详情页 展示不全 滑屏

                            if self.v_detail.wait_check_page(text):  # 页面检查点
                                self.home.back_up_button()

                    print('-----------------------------------------')
        else:
            print('★★★ Error-完成情况tab 列表信息统计', len(icon), len(name))

    @teststeps
    def per_answer_detail(self, content):
        """个人 答题情况详情页"""
        mode = self.detail.game_type()  # 游戏类型
        name = self.detail.game_name()  # 游戏name
        num = self.detail.game_num()  # 游戏 小题数
        optimal = self.detail.optimal_achievement()  # 最优成绩

        if len(optimal) > 4 and content[0] == '':
            content = []
            for j in range(len(optimal) - 1):
                print(mode[j].text, num[j].text, '\n',
                      name[j].text, '\n',
                      optimal[j].text)
                print('--------------------')

            content.append(name[len(optimal)-2].text)  # 最后一个game的name
            content.append(mode[-2].text)  # 最后一个game的type
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.per_answer_detail(content)
        else:
            global var
            mode = self.detail.game_type()  # 游戏类型
            name = self.detail.game_name()  # 游戏name
            num = self.detail.game_num()  # 游戏 小题数
            optimal = self.detail.optimal_achievement()  # 最优成绩

            if content[0] != '':
                if content[0] != name[-1].text and content[1] != mode[-1].text:
                    for k in range(len(name)):
                        if content[0] == name[k].text and content[1] == mode[k].text:
                            var += k + 1
                            break
                    for j in range(var, len(name)):
                        print(mode[j].text, num[j].text, '\n',
                              name[j].text, '\n',
                              optimal[j].text)
                        print('--------------------')
            else:
                for j in range(var, len(name)):
                    print(mode[j].text, num[j].text, '\n',
                          name[j].text, '\n',
                              optimal[j].text)
                    print('--------------------')

    @teststeps
    def answer_analysis_detail(self, content):
        """答题分析 详情页"""
        item = self.detail.game_item()  # 游戏 条目

        if len(item) > 4 and content[0] == '':
            content = [item[-2][2]]
            self.cup_operation(item, len(item)-1)  # 进入cup页面 及具体操作

            if self.detail.wait_check_hw_list_page():
                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.answer_analysis_detail(content)
        else:
            var = 0
            for k in range(len(item)):
                if content[0] in item[k]:
                    var += k+1
                    break

            self.cup_operation(item, len(item), var)  # 进入cup页面 及具体操作

    @teststeps
    def cup_operation(self, item, length, index=0):
        """进入cup页面 及具体操作"""
        for i in range(index, length):
            var = []
            if self.detail.wait_check_page():  # 页面检查点
                if len(item[i]) == 4:  # 无提分标志
                    print(item[i][0], '\n', item[i][1], '\n', item[i][2])
                    num = int(re.sub("\D", "", item[i][2]))  # 提取 全班首轮平均成绩
                    var.append(item[i][1])
                else:
                    print(item[i][0], item[i][1], '\n', item[i][2], '\n', item[i][3])
                    num = int(re.sub("\D", "", item[i][3]))  # 提取 全班首轮平均成绩
                    var.append(item[i][2])

                if num != 0:
                    item[i][-1].click()  # 点击奖杯 icon

                    if self.info.wait_check_page(var[0]):  # 作业 页面检查点
                        self.best_accuracy()  # 奖杯页面 最优成绩tab
                        self.first_accuracy()  # 奖杯页面 首次成绩tab

                        if self.v_detail.wait_check_achievement_list_page():  # 作业 页面检查点
                            self.home.back_up_button()
                print('-----------------------------------------')

    @teststeps
    def best_accuracy(self):
        """单个题目 答题详情 操作"""
        all_hw = self.v_detail.best_tab()  # 最优成绩 tab
        if self.get.selected(all_hw) is False:
            print('★★★ Error- 未默认在 最优成绩页面')
        else:
            print('--------最优成绩tab--------')
            if self.v_detail.wait_check_achievement_list_page():
                self.accuracy_detail([''])
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def first_accuracy(self):
        """首次成绩tab 具体操作"""
        incomplete = self.v_detail.first_tab()  # 首次成绩 tab
        if self.get.selected(incomplete) is True:
            print('★★★ Error- 默认在 首次成绩 tab页')
        else:
            incomplete.click()  # 进入 首次成绩 tab页
            if self.get.selected(incomplete) is False:
                print('★★★ Error- 进入 首次成绩 tab页')
            else:
                print('--------首次成绩tab--------')
                if self.v_detail.wait_check_achievement_list_page():
                    self.accuracy_detail([''])
                elif self.home.wait_check_empty_tips_page():
                    print('暂无数据')

    @teststeps
    def accuracy_detail(self, content):
        """首次成绩/最优成绩 详情"""
        order = self.v_detail.st_order()  # 编号
        icon = self.v_detail.st_icon()  # 头像
        name = self.v_detail.st_name()  # 昵称
        accuracy = self.v_detail.accuracy()  # 正答率
        spend = self.v_detail.spend_time()  # 用时

        if len(order) > 5:
            content = []
            for j in range(len(order) - 1):
                print(order[j].text, name[j].text, accuracy[j].text, spend[j].text)

            content.append(name[len(order) - 2].text)  # 最后一个game的name
            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.accuracy_detail(content)
        else:
            var = 0
            for k in range(len(icon)):
                if content[0] == name[k].text:
                    var += k
                    break

            for j in range(var, len(icon)):
                print(order[j].text, name[j].text, accuracy[j].text, spend[j].text)
