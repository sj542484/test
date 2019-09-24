#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class HwDetailPage(BasePage):
    """ 答题分析/完成情况 详情页面"""

    more_button_item_value = gv.PACKAGE_ID + "title"  # 更多按钮 -条目元素
    game_type_value = gv.PACKAGE_ID + 'type'  # 小游戏类型

    def __init__(self):
        self.game = GamesPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title: 答题分析”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'答题分析')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def finished_tab(self):
        """完成情况"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'完成情况')]")
        return ele

    @teststep
    def analysis_tab(self):
        """答题分析"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'答题分析')]")
        return ele

    @teststep
    def answer_detail_button(self):
        """答题详情 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "details") \
            .click()

    @teststep
    def more_button(self):
        """更多 按钮"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView")\
            .click()

    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.ID, self.more_button_item_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def edit_delete_button(self, index):
        """编辑& 删除 按钮"""
        self.driver \
            .find_elements_by_id(self.more_button_item_value)[index] \
            .click()

    # 完成情况tab 学生列表
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生完成情况 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "status")
        return self.wait.wait_check_element(locator)

    @teststep
    def st_item(self):
        """学生 条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.RelativeLayout/android.widget.LinearLayout"
                                    "/child::*")

        count = []
        for i in range(0, len(ele), 5):
            if GetAttribute().resource_id(ele[i]) == gv.PACKAGE_ID + 'name':
                count.append(i)
        count.append(len(ele))
        print(count)

        content = []  # 页面内所有学生
        for j in range(len(count) - 1):
            item = []  # 每一个学生
            for k in range(count[j], count[j + 1]):
                if ele[k].text != '':
                    item.append(ele[k].text)
            content.append(item)
        return content

    @teststep
    def st_type(self):
        """基础班/提分版学生"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type")
        return ele

    @teststep
    def st_finish_status(self):
        """学生 完成与否"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "status")
        return ele

    @teststep
    def st_name(self):
        """学生 昵称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def st_icon(self):
        """学生 头像"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "head")
        return ele

    # 答题分析tab 页面
    @teststeps
    def wait_check_hw_list_page(self):
        """以“cup 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_cup")
        return self.wait.wait_check_element(locator)

    @teststep
    def game_item(self):
        """游戏 条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/child::*")

        count = []
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:
                count.append(i)
        count.append(len(ele))

        content = []  # 页面内所有game
        for j in range(len(count)-1):
            item = []  # 每一个game
            for k in range(count[j], count[j+1]):
                if ele[k].text != '':
                    item.append(ele[k].text)
                elif GetAttribute().resource_id(ele[k]) == gv.PACKAGE_ID + 'iv_cup':
                    item.append(ele[k])
            content.append(item)
        return content

    @teststep
    def game_type(self):
        """游戏类型"""
        ele = self.driver \
            .find_elements_by_id(self.game_type_value)
        return ele

    @teststep
    def game_level(self):
        """提分"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "level")
        return ele

    @teststep
    def game_num(self):
        """共x题"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "exercise_num")
        return ele
        
    @teststep
    def game_name(self):
        """游戏 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        return ele

    @teststep
    def average_achievement(self):
        """全班首轮平均成绩x%"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_testbank_status")
        return ele

    @teststep
    def cup_icon(self):
        """奖杯 icon"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_cup")
        return ele

    # 学生个人答题情况页 特有元素
    @teststeps
    def wait_check_per_detail_page(self, var=20):
        """以“最优成绩 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_testbank_status")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def per_game_item(self):
        """个人答题情况页面 -游戏 条目
        :returns:  游戏类型 & 页面内所有game
        """
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/"
                                    "child::*/android.widget.TextView")

        count = []  # 每个游戏条目第一个元素为游戏类型
        var = []  # 游戏类型
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:
                count.append(i)
                var.append(ele[i])
        count.append(len(ele))

        content = []  # 页面内所有game
        for j in range(len(count) - 1):
            item = []  # 每一个game
            for k in range(count[j], count[j + 1]):
                if ele[k].text != '':
                    item.append(ele[k].text)
            content.append(item)
        return var, content

    @teststep
    def optimal_achievement(self):
        """最优成绩-"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_testbank_status")
        return ele

    @teststep
    def first_achievement(self):
        """首次成绩-"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_spend_time")
        return ele

    # 编辑作业 页面
    @teststeps
    def wait_check_edit_page(self):
        """以“title:编辑作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'编辑作业')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def assign_button(self):
        """发布作业 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_first")\
            .click()

    # 删除作业tips 页面
    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'删除作业')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def delete_cancel_operation(self):
        """删除作业 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.edit_delete_button(1)  # 删除按钮

            if self.wait_check_tips_page():
                print('---------删除作业---------')
                ThomePage().tips_title()
                ThomePage().tips_content()
                ThomePage().cancel_button()  # 取消按钮
                print('---------------')
                print('取消删除')
                # ThomePage().commit_button()  # 确定按钮
                # print('确定删除')
            else:
                print('★★★ Error- 无删除提示框')

    @teststeps
    def delete_commit_operation(self):
        """删除作业 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.edit_delete_button(1)  # 删除按钮

            if self.wait_check_tips_page():
                print('---------删除作业---------')
                ThomePage().commit_button().click()  # 确定按钮
                print('确定删除')
