#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class FilterPage(BasePage):
    """ 筛选 页面"""
    label_name_value = gv.PACKAGE_ID + "tv_label_name"  # 标签名
    
    def __init__(self):
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”为依据"""
        locator = (By.ID, self.label_name_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def question_menu(self):
        """以“题单”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(self.label_name_value)[2]
        return ele

    @teststep
    def click_question_menu(self):
        """以“题单”的text为依据"""
        self.driver \
            .find_elements_by_id(self.label_name_value)[2] \
            .click()

    @teststep
    def game_list(self):
        """以“大题”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(self.label_name_value)[3]
        return ele

    @teststep
    def click_game_list(self):
        """以“大题”的text为依据"""
        self.driver \
            .find_elements_by_id(self.label_name_value)[3] \
            .click()

    @teststep
    def test_paper(self):
        """以“试卷”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(self.label_name_value)[4]
        return ele

    @teststep
    def click_test_paper(self):
        """以“试卷”的text为依据"""
        self.driver \
            .find_elements_by_id(self.label_name_value)[4]\
            .click()

    @teststep
    def reset_button(self):
        """以“重置按钮”的text为依据"""
        print('点击重置按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_first") \
            .click()

    @teststep
    def commit_button(self):
        """以“确定按钮”的text为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_second") \
            .click()

    @teststep
    def expand_button(self):
        """以“上下拉 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "iv_expand") \
            .click()

    @teststeps
    def label_title(self):
        """以“标签 title”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_title")
        content = []
        for i in range(len(ele)):
            content.append(ele[i].text)
        return content

    @teststep
    def label_name(self):
        """以“标签 name”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(self.label_name_value)
        return ele

    @teststep
    def expand_icon(self):
        """以“收起 icon”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_expand")
        return ele

    @teststeps
    def all_element(self):
        """页面内所有label元素"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/android.support.v7.widget.RecyclerView"
                                    "/android.widget.LinearLayout/"
                                    "descendant::*/android.widget.TextView")
        return ele

    @teststeps
    def filter_all_element(self, var):
        """所有label title+小标签"""
        ele = self.all_element()  # 所有元素

        content = []  # 所有元素
        item = []  # 翻页前最后元素
        for i in range(len(ele)):
            item.append(ele[-1].text)
            content.append(ele[i].text)

        SwipeFun().swipe_vertical(0.5, 0.7, 0.2)
        if self.wait_check_page():
            ele = self.all_element()  # 所有元素

            index = 0
            for i in range(len(ele)):
                if ele[i].text == item[0]:
                    index = i+1
                    break

            for j in range(index, len(ele)):
                content.append(ele[j].text)

        self.label_content(var, content)  # print所有元素

    @teststeps
    def label_content(self, var, content):
        """筛选 每个标题下的所有label"""
        count = []
        if var == 2:  # 试卷
            for i in range(len(content)):
                if content[i] == '题库':
                    count.append(i)
                elif content[i] == '资源类型':
                    count.append(i)
                    break
        elif var == 3:  # 题单
            for i in range(len(content)):
                if content[i] == '题库':
                    count.append(i)
                elif content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                    break
        elif var == 4:  # 大题
            for i in range(len(content)):
                if content[i] == '题库':
                    count.append(i)
                elif content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '活动类型':
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                    break

        count.append(len(content))
        for i in range(len(count)):  # print 所有元素
            if i + 1 == len(count):
                print('---------------------')
                for j in range(count[i], count[-1]):
                    print(content[j])
            else:
                print('---------------------')
                for j in range(count[i], count[i + 1]):
                    print(content[j])
        return count

    @teststeps
    def source_type_selected(self):
        """选中的资源类型"""
        if self.get.selected(self.question_menu()) == 'true':  # 题单
            print('======================选择题单======================')
            self.filter_all_element(3)  # 所有label title+小标签
        else:
            if self.get.selected(self.game_list()) == 'true':  # 大题
                print('======================选择大题======================')
                self.filter_all_element(4)  # 所有label title+小标签
            else:
                if self.get.selected(self.test_paper()) == 'true':  # 试卷
                    print('======================选择试卷======================')
                    self.filter_all_element(2)  # 所有label title+小标签
        print('============================================')
