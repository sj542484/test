#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class Homework(BasePage):
    """作业包内 作业列表页面 元素信息"""
    game_name_value = gv.PACKAGE_ID + "test_bank_name"  # 游戏名
    game_type_value = gv.PACKAGE_ID + "type"  # 游戏类型
    game_num_value = gv.PACKAGE_ID + "exercise_num"  # 共X题
    rate_value = gv.PACKAGE_ID + "rate"  # 待完成

    def __init__(self):
        self.wait = WaitElement()
        self.home = ThomePage()
        self.question = TestBankPage()
        self.detail = QuestionDetailPage()

    @teststeps
    def wait_check_page(self):
        """以“作业”的class_name为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_homework_name")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_game_list_page(self, var):
        """以 小游戏的class_name为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, %s)]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def game_mode(self, item):
        """小游戏模式--匹配小括号内游戏模式"""
        m = re.match(".*（(.*)）.*", item)  # title中有一个括号
        if m:
            # print(m.group(1))
            # print('---------------------------------')
            return m.group(1)
        else:
            return None

    @teststep
    def game_name(self, index):
        """以“题目名称”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(self.game_name_value)[index]
        return ele

    @teststep
    def game_num(self, index):
        """题目总数格式：共X题"""
        item = self.driver \
            .find_elements_by_id(self.game_num_value)[index]
        return item

    @teststep
    def game_type(self):
        """以“类型”的id为依据"""
        item = self.driver \
            .find_elements_by_id(self.game_type_value)
        return item

    # 小键盘 右上角的 隐藏按钮
    @teststep
    def hide_button(self):
        """隐藏按钮 的resource-id"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "keyboard_hide") \
            .click()

    # 从结果页返回小游戏list
    @teststeps
    def back_operation(self):
        """从结果页返回小游戏list"""
        if ResultPage().wait_check_result_page():
            self.home.back_up_button()  # 返回 详情界面
            if GamesPage().wait_check_page():
                self.home.back_up_button()  # 返回 题单详情页

    # 公共元素 及操作
    @teststeps
    def commit_button_judge(self, var):
        """‘提交’按钮 状态判断"""
        item = self.commit_button()  # ‘提交’按钮
        value = GetAttribute().enabled(item)

        if value != var:  # 测试 提交 按钮 状态
            print('★★★ 提交按钮 状态Error', value)
        else:
            return True

    @teststep
    def commit_button(self):
        """点击‘提交’按钮"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_commit")
        return item

    @teststeps
    def next_button_judge(self, var):
        """‘下一题’按钮 状态判断"""
        item = self.next_button()  # ‘下一题’按钮
        value = GetAttribute().enabled(item)

        if value != var:  # 测试 下一步 按钮 状态
            print('★★★ 下一步按钮 状态Error', value)
        else:
            return True

    @teststeps
    def next_button(self):
        """点击‘下一题’按钮"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_next")
        return item

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "time").text
        return ele

    @teststep
    def rate(self):
        """获取作业数量 待完成：X"""
        rate = self.driver \
            .find_element_by_id(self.rate_value).text
        return rate

    @teststeps
    def wait_check_play_page(self):
        """以“rate”的ID为依据"""
        locator = (By.ID, self.rate_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def rate_judge(self, rate, i):
        """判断当前小题rate的值是否正确"""
        if int(self.rate()) != int(rate) - i:  # 测试当前rate值显示是否正确
            print('★★★ Rate Error - 当前rate值为%s, 应为%s' % (int(self.rate()), int(rate) - i))

    @teststeps
    def next_button_operation(self, var):
        """下一步按钮 判断 加 点击操作"""
        if self.next_button_judge(var):  # 下一题 按钮 状态判断
            self.next_button().click()  # 点击 下一题 按钮

    @teststeps
    def commit_button_operation(self, var):
        """提交 按钮 判断 加 点击操作"""
        if self.commit_button_judge(var):  # 提交 按钮 状态判断
            self.commit_button().click()  # 点击 提交 按钮

    @teststeps
    def games_operation(self, question, func, game_type):
        """查找进入 题单内 该类型的小游戏
        :param game_type: 需要查找的小游戏类型
        :param question: 题单
        :param func: 具体操作函数game_exit()
        """
        if self.question.wait_check_page():  # 页面检查点
            name = self.question.question_name()
            for i in range(len(name[1])):
                if name[1][i] == question:
                    name[0][i].click()  # 点击进入该作业

                    self.games_count(game_type, func)  # 具体操作函数
                    break

            if self.detail.wait_check_page():  # 检查点
                self.home.back_up_button()  # 返回 题库页面
                if self.question.wait_check_page():  # 检查点
                    self.home.click_tab_hw()  # 返回 主界面

    @teststeps
    def games_count(self, game_type, func, content=None):
        """该类型小游戏的数量
        :param game_type: 游戏类型
        :param func: 具体操作函数game_exit()
        :param content: 已操作的最后一个小游戏
        """
        if content is None:
            content = []

        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                item = self.game_item()  # 获取小游戏条目

                if len(item[1]) > 4 and not content:  # 多于4个
                    content.append(item[1][-2])
                    content.append(item[2][-2])
                    for i in range(len(item[1])-1):
                        if item[1][i] == game_type:
                            func(item[3][i], item[2][i])  # 具体操作

                    if self.detail.wait_check_list_page():
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.3)
                        self.games_count(game_type, func, content)
                else:  # 少于5个
                    var = 0
                    if content:
                        for k in range(len(item[1])):
                            if item[1][k] == content[0] and item[2][k] == content[1]:
                                var = k + 1
                                break

                    for i in range(var, len(item[1])):
                        if item[1][i] == game_type:
                            func(item[3][i], item[2][i])  # 具体操作
        else:
            print('未进入题单详情页')

    @teststeps
    def game_item(self):
        """小游戏条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout"
                                    "/descendant::android.widget.TextView")
        count = []  # 小游戏名称
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:  # 类型
                count.append(i)
        count.append(len(ele))

        content = []  # 页面内所有条目 元素text
        name = []  # 页面内所有条目元素
        num = []  # 共X题
        mold = []  # 游戏类型
        for j in range(len(count) - 1):
            item = []  # 每一个条目的所有元素k
            if count[j + 1] - count[j] in (4, 5, 6):  # 提分/不提分  精
                for k in range(count[j], count[j + 1]):
                    item.append(ele[k].text)
                    if GetAttribute().resource_id(ele[k]) == self.game_num_value:  # 共X题
                        num.append(ele[k])
                    elif GetAttribute().resource_id(ele[k]) == self.game_name_value:  # 题目名称
                        name.append(ele[k].text)
                    elif GetAttribute().resource_id(ele[k]) == self.game_type_value:  # 类型
                        mold.append(ele[k].text)
                    elif ele[k].text == '精':
                        continue

                content.append(item)

        if len(content) != len(mold) != len(name) != len(num):
            print('★★★ Error - 游戏各元素长度不一致', len(content), len(mold), len(name), len(num))

        return content, mold, name, num

    @teststeps
    def now_time(self, times):
        """判断游戏界面 计时功能控件 是否在计时
        :param times:时间列表
        """
        print('判断计时:', times)

        time_list = []
        for i in range(len(times)):
            time_list.append(ResultPage().get_time(times[i]))

        if len(time_list) > 1:
            if any(time_list[i + 1] > time_list[i] for i in range(0, len(time_list) - 1)):
                print('计时功能无误:', time_list)
            else:
                print('★★★ Error - 计时错误:', time_list)
        else:  # 只有一道题
            print('只有一道题，时间为:', time_list[0])
