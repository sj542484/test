#!/usr/bin/env python
# encoding:UTF-8
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.play_games.object_page.result_page import ResultPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.raise_exception import MyError
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class Homework(BasePage):
    """作业包内 作业列表页面 元素信息"""
    def __init__(self):
        self.detail = QuestionDetailPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“作业”的class_name为依据"""
        locator = (By.ID, gv.PACKAGE_ID+ "tv_homework_name")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_game_list_page(self, var):
        """以 小游戏的class_name为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, %s)]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def game_mode(self, index):
        """小游戏模式--匹配小括号内游戏模式"""
        item = self.game_name(index).text
        m = re.match(".*\（(.*)\）.*", item)  # title中有一个括号
        print(m.group(1))
        return m.group(1)

    @teststeps
    def tv_game_mode(self, index):
        """小游戏模式--匹配小括号内游戏模式"""
        item = self.game_name(index).text
        m = re.match(".*\（(.*)\）.*\（", item)  # 有两个括号，匹配第二个
        print(m.group(1))
        return m.group(1)

    @teststep
    def game_name(self,index):
        """以“题目名称”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID+ "test_bank_name")[index]
        return ele

    @teststep
    def num(self, index):
        """题目总数格式：共X题"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "exercise_num")[index]
        return item

    @teststep
    def game_type(self):
        """以“类型”的id为依据"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID+ "type")
        return item

    # 小键盘 右上角的 隐藏按钮
    @teststep
    def hide_button(self):
        """隐藏按钮 的resource-id"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "keyboard_hide")\
            .click()

    # 从结果页返回小游戏list
    @teststeps
    def back_operation(self):
        """从结果页返回小游戏list"""
        if ResultPage().wait_check_result_page():
            ThomePage().back_up_button()  # 返回小游戏界面
            if GamesPage().wait_check_page():
                ThomePage().back_up_button()  # 返回 题单详情页

    # 公共元素 及操作
    @teststep
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

    @teststep
    def next_button_judge(self, var):
        """‘下一题’按钮 状态判断"""
        item = self.next_button()  # ‘下一题’按钮
        value = GetAttribute().enabled(item)

        if value != var:  # 测试 下一步 按钮 状态
            print('★★★ 下一步按钮 状态Error', value)
        else:
            return True

    @teststep
    def next_button(self):
        """点击‘下一题’按钮"""
        time.sleep(1)
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
        rate = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "rate").text
        return rate

    @teststeps
    def wait_check_play_page(self):
        """以“rate”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "rate")
        return self.wait.wait_check_element(locator)

    @teststeps
    def rate_judge(self, rate, i):
        """判断当前小题rate的值是否正确"""
        time.sleep(1)
        if int(self.rate()) != int(rate) - i:   # 测试当前rate值显示是否正确
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
    def games_count(self, game_type, count, content=None):
        """该类型小游戏的数量
        :param game_type:游戏类型
        :param content: 已操作的最后一个小游戏
        :param count:  # 小游戏数目
        """
        if content == None:
            content = []
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                print('game_type:', game_type)
                mody = self.game_type()  # 获取小游戏类型

                if len(mody) > 6 and not content:  # 多于8个
                    content.append(mody[-2].text)
                    for i in range(len(mody)):
                        if mody[i].text == game_type:
                            count.append(i)
                    print('小游戏：', count)

                    SwipeFun().swipe_vertical(0.5, 0.9, 0.3)
                    self.games_count(game_type, count, content)
                else:  # 少于6个 todo
                    var = 0
                    if content:
                        for k in range(len(mody) - 1, 0, -1):
                            if mody[k].text == content[0]:
                                var = k + 1
                                break

                    for i in range(var, len(mody)):
                        if mody[i].text == game_type:
                            count.append(i)
                    print('小游戏：', count)
                    print('---------------')

    @teststeps
    def now_time(self, ele):
        """判断游戏界面 计时功能控件 是否在计时"""
        time.sleep(1)
        print('判断计时:', ele)
        time_list = []
        for i in range(len(ele)):
            time_list.append(ResultPage().get_time(ele[i]))
        if len(time_list) > 1:
            if any(time_list[i + 1] > time_list[i] for i in range(0, len(time_list) - 1)):
                print('计时功能无误:', time_list)
                return True
            else:
                print('★★★ Error - 计时错误:', time_list)
                MyError(self.driver).my_error(any(time_list[i + 1] <= time_list[i] for i in range(0, len(time_list) - 1)))
        else:  # 只有一道题
            print('只有一道题，时间为:', time_list[0])
            return True
