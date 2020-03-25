#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class TuserCenterPage(BasePage):
    """个人中心 页面"""
    collection_value = gv.PACKAGE_ID + 'star'  # 个人中心页面 我的收藏
    label_name_value = gv.PACKAGE_ID + "tv_label_name"  # 标签名

    user_center_tips = '★★★ Error- 未进入个人中心页面'

    def __init__(self):
        self.wait = WaitElement()
        self.get = GetAttribute()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var=10):
        """以“nickname”为依据"""
        locator = (By.ID, self.collection_value)
        ele = self.wait.wait_check_element(locator, var)
        self.my_assert.assertTrue(ele, self.user_center_tips)
        return ele

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
    @teststeps
    def wait_check_filter_page(self):
        """以“”为依据"""
        locator = (By.ID, self.label_name_value)
        return self.wait.wait_check_element(locator)

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
            .find_elements_by_id(self.label_name_value)[0]
        return ele

    @teststep
    def click_question_menu(self):
        """以“题单”的text为依据"""
        self.driver \
            .find_elements_by_id(self.label_name_value)[0] \
            .click()

    @teststep
    def game_list(self):
        """以“大题”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(self.label_name_value)[1]
        return ele

    @teststep
    def click_game_list(self):
        """以“大题”的text为依据"""
        self.driver \
            .find_elements_by_id(self.label_name_value)[1] \
            .click()

    @teststep
    def test_paper(self):
        """以“试卷”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(self.label_name_value)[2]
        return ele

    @teststep
    def click_test_paper(self):
        """以“试卷”的text为依据"""
        self.driver \
            .find_elements_by_id(self.label_name_value)[2] \
            .click()

    @teststep
    def label_title(self):
        """label title"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_title")
        return item

    @teststep
    def label_names(self):
        """label_name"""
        item = self.driver \
            .find_elements_by_id(self.label_name_value)
        return item

    @teststeps
    def all_element(self):
        """页面内所有label title+小标签 元素"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout"
                                    "/android.support.v7.widget.RecyclerView[contains(@resource-id, '{}')]"
                                    "/descendant::android.widget.TextView".format(gv.PACKAGE_ID + 'rv'))

        return ele

    @teststeps
    def filter_operation(self, count, element, var=0):
        """所有label title+小标签"""
        for i in range(var, len(element)):
            if self.get.resource_id(element[i]) == gv.PACKAGE_ID + 'tv_title':
                count.append(element[i].text)
                print('------------------')
                print(element[i].text)
            else:
                print(' ', element[i].text)

    @teststeps
    def judge_label_title(self, label_mode, content):
        """判断标签 类型及个数
            筛选标签展示规则：资源类型
            自定义标签：个人自定义标签
            系统标签：有带系统标签的推荐内容，则展示
        """
        print(content)
        if label_mode == '试卷':  # 试卷
            if content[0] != '资源类型' or content[1] != '自定义标签':  # 我的收藏/题库
                print('★★★ Error- 标签类型有误', content)
        elif label_mode == '题单':  # 题单
            if content[0] == '资源类型' and content[1] == '自定义标签':  # 我的收藏/题库
                if len(content) == 3 and content[2] != '系统标签':
                    print('★★★ Error- 标签个数 {}，类型有误'.format(len(content)), content)
            else:
                print('★★★ Error- 标签类型有误', content)
        elif label_mode == '大题':  # 大题
            if content[0] == '资源类型' and content[1] == '自定义标签' and content[2] == '活动类型':  # 我的收藏/题库
                if len(content) == 4 and content[3] != '系统标签':
                    print('★★★ Error- 标签个数 {}，类型有误'.format(len(content)), content)
            else:
                print('★★★ Error- 标签类型有误', content)

    @teststeps
    def source_type_selected(self):
        """选中的资源类型
        题单：3/2； 大题：4/3； 试卷：2
        筛选标签展示规则：我的题库/我的收藏
            自定义标签：自己的自定义标签
            系统标签：有带系统标签的内容，则展示
        """
        global mode
        if self.get.selected(self.question_menu()) == 'true':  # 题单
            print('======================选择 题单======================')
            mode = '题单'
        elif self.get.selected(self.game_list()) == 'true':  # 大题
            print('======================选择 大题======================')
            mode = '大题'
        elif self.get.selected(self.test_paper()) == 'true':  # 试卷
            print('======================选择 试卷======================')
            mode = '试卷'

        if self.wait_check_filter_page():
            ele = self.all_element()  # 所有label title+小标签
            count = []  # 标签数
            last = ele[-1].text  # 翻页
            self.filter_operation(count, ele)  # 统计

            SwipeFun().swipe_vertical(0.5, 0.7, 0.2)  # 翻页
            if self.wait_check_page():
                ele = self.all_element()  # 所有label title+小标签
                if ele[-1].text != last:
                    var = 0
                    for k in range(len(ele) - 1, 0):
                        if last == ele[k].text:
                            var = k + 1
                            break

                    self.filter_operation(count, ele, var)  # 统计
            return mode, count
        print('============================================')
