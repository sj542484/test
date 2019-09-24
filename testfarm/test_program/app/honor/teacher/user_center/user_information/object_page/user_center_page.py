#!/usr/bin/env python
# encoding:UTF-8
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class TuserCenterPage(BasePage):
    """个人中心 页面"""
    collection_value = gv.PACKAGE_ID + 'star'  # 个人中心页面 我的收藏

    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self, var=10):
        """以“nickname”为依据"""
        locator = (By.ID, self.collection_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def click_avatar_profile(self):
        """以“头像”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'avatar_profile') \
            .click()

    @teststep
    def nickname(self):
        """以“昵称”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'name') \
            .text
        return ele

    @teststep
    def click_mine_collection(self):
        """以“我的收藏”的id为依据"""
        self.driver \
            .find_element_by_id(self.collection_value) \
            .click()

    @teststep
    def click_mine_recommend(self):
        """以“我的推荐”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'recommend') \
            .click()

    @teststep
    def click_mine_bank(self):
        """以“我的题库”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "custom")\
            .click()

    @teststep
    def click_tiny_course(self):
        """以“微课”的class_name为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tiny_course") \
            .click()

    @teststep
    def click_message(self):
        """以“消息”的class_name为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "message") \
            .click()

    @teststep
    def click_setting(self):
        """以“设置”的class_name为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "setting") \
            .click()

    # 筛选
    @teststep
    def filter_button(self):
        """以“筛选 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "filter") \
            .click()

    @teststep
    def question_menu(self):
        """以“题单”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[0]
        return ele

    @teststep
    def click_question_menu(self):
        """以“题单”的text为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[0] \
            .click()

    @teststep
    def game_list(self):
        """以“大题”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[1]
        return ele

    @teststep
    def click_game_list(self):
        """以“大题”的text为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[1] \
            .click()

    @teststep
    def test_paper(self):
        """以“试卷”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[2]
        return ele

    @teststep
    def click_test_paper(self):
        """以“试卷”的text为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[2] \
            .click()

    @teststep
    def label_title(self):
        """label title"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")
        return item

    @teststeps
    def filter_all_element(self):
        """页面内所有label元素"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/android.support.v7.widget.RecyclerView"
                                    "/android.widget.LinearLayout"
                                    "/descendant::*/android.widget.TextView")
        return ele

    @teststeps
    def filter_operation(self, var):
        """所有label title+小标签"""
        ele = self.filter_all_element()  # 所有元素

        content = []  # 所有元素
        item = []  # 翻页前最后元素
        for i in range(len(ele)):
            item.append(ele[-1].text)
            content.append(ele[i].text)

        SwipeFun().swipe_vertical(0.5, 0.7, 0.2)
        if self.wait_check_page():
            ele = self.filter_all_element()  # 所有元素

            index = 0
            for i in range(len(ele)):
                if ele[i].text == item[0]:
                    index = i + 1
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
                if content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '自定义标签':  # 我的收藏/推荐
                    count.append(i)
                    break
        elif var == 3:  # 题单
            for i in range(len(content)):
                if content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '自定义标签':  # 我的收藏/推荐
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                    break
        elif var == 4:  # 大题
            for i in range(len(content)):
                if content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '自定义标签':  # 我的收藏/推荐
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
            self.filter_operation(3)  # 所有label title+小标签
        else:
            if self.get.selected(self.game_list()) == 'true':  # 大题
                print('======================选择大题======================')
                self.filter_operation(4)  # 所有label title+小标签
            else:
                if self.get.selected(self.test_paper()) == 'true':  # 试卷
                    print('======================选择试卷======================')
                    self.filter_operation(2)  # 所有label title+小标签
        print('============================================')


class HelpCenter(BasePage):
    """二级页面：帮助中心页面"""

    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:帮助中心”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'帮助中心')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“VIEW”的CLASS NAME为依据"""
        locator = (By.CLASS_NAME, "android.view.View")
        return self.wait.wait_check_element(locator)

    @teststeps
    def view(self):
        """以“view”的class name为依据"""
        time.sleep(3)
        ele = self.driver\
            .find_elements_by_class_name("android.view.View")

        value = []
        for i in range(len(ele)):
            item = self.get.description(ele[i])
            if (item is not None) and (item not in value):
                value.append(item)
                print(value[i])


class Copyright(BasePage):
    """版权申诉"""
    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:版权申诉”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'版权申诉')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“VIEW”的CLASS NAME为依据"""
        locator = (By.CLASS_NAME, "android.view.View")
        return self.wait.wait_check_element(locator)

    @teststeps
    def content_view(self, value):
        """以“条款内容”的class name为依据"""
        ele = self.driver \
            .find_elements_by_class_name("android.view.View")

        for i in range(len(ele)):
            item = self.get.description(ele[i])
            print(item)
            if (item is not None) and (item not in value):
                value.append(item)
                print(item)
        print('------------------------------------')


class ProtocolPage(BasePage):
    """注册协议"""
    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:注册协议”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'注册协议')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_view_page(self):
        """以“view”的CLASS NAME为依据"""
        locator = (By.CLASS_NAME, "android.webkit.WebView")
        return self.wait.wait_check_element(locator)

    @teststeps
    def content_view(self, value):
        """以“条款内容”的class name为依据"""
        ele = self.driver \
            .find_elements_by_class_name("android.view.View")

        for i in range(len(ele)):
            item = self.get.description(ele[i])
            if (item is not None) and (item not in value):
                value.append(item)
                print(item)
