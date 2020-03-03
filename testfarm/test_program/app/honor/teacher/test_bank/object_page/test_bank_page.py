#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.test_bank_search_page import SearchPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class TestBankPage(BasePage):
    """题库 页面"""
    question_value = gv.PACKAGE_ID + "test_bank_name"  # 题单名
    question_type_value = gv.PACKAGE_ID + "type"  # 题单类型
    num_value = gv.PACKAGE_ID + "exercise_num"  # 共X题
    drop_down_value = gv.PACKAGE_ID + "title"  # 下拉菜单

    lock_value = gv.PACKAGE_ID + "lock"  # 锁

    question_tips = '★★★ Error- 未进入题库页面'
    back_question_tips = '★★★ Error- 未返回题库页面'
    filter_game_tips = '★★★ Error- 未进入筛选大题页面'

    @teststeps
    def __init__(self):
        self.sp = SwipeFun()
        self.home = ThomePage()
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var='题单', index=10):
        """以“搜索框中灰字:搜索”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator, index)

    @teststep
    def search_input(self):
        """以“输入框”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "input")
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def question_basket(self):
        """以 题筐 按钮的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "fab_pool")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def filter_button(self):
        """以“筛选 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "filter")
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_check_game_type_page(self):
        """以“大题类型”为依据"""
        locator = (By.ID, self.question_type_value)
        return self.wait.wait_check_element(locator, 3)

    # 题单
    @teststep
    def question_name(self):
        """以“题目名称”的id为依据"""
        locator = (By.ID, self.question_value)
        ele = self.wait\
            .wait_find_elements(locator)
        content = [x.text for x in ele]
        return ele, content

    @teststep
    def question_type(self, index):
        """以“类型”的id为依据"""
        locator = (By.ID, self.question_type_value)
        return self.wait.wait_find_elements(locator)[index].text

    @teststep
    def question_perfect(self, index):
        """以 加“精”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "perfect")
        return self.wait.wait_find_elements(locator)[index]

    @teststep
    def question_num(self, index):
        """以“数量”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "exercise_num")
        return self.wait.wait_find_elements(locator)[index].text

    @teststep
    def question_author(self):
        """以“作者”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_find_elements(locator)

    @teststeps
    def question_item(self):
        """题单条目"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id, %s)]"
                             "/parent::android.widget.LinearLayout"
                             "/descendant::*" % self.question_value)
        ele = self.wait.wait_find_elements(locator)

        count = []  # 题目名称
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.question_type_value:  # 类型
                count.append(i)
        count.append(len(ele)-1)

        content = []  # 页面内所有条目 元素text
        name = []  # 页面内所有条目元素
        num = []  # 共X题
        lock = []  # 锁定icon

        for j in range(len(count) - 1):
            item = []  # 每一个条目的所有元素k
            if count[j + 1] - count[j] in (4, 5, 6):
                for k in range(count[j], count[j + 1]):
                    item.append(ele[k].text)
                    if GetAttribute().resource_id(ele[k]) == self.num_value:  # 共X题
                        num.append(ele[k])
                    elif GetAttribute().resource_id(ele[k]) == self.question_value:  # 题目名称
                        name.append(ele[k].text)
                    elif GetAttribute().resource_id(ele[k]) == self.lock_value:  # # 锁定icon 元素
                        lock.append(k)

                content.append(item)
        return name, content, num, lock

    # 大题
    @teststep
    def question_level(self, index):
        """以“题目等级”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "level")
        return self.wait.wait_find_elements(locator)[index]

    @teststep
    def question_lock(self):
        """以“题目是否锁定”的id为依据"""
        locator = (By.ID, self.lock_value)
        return self.wait\
            .wait_find_element(locator).text

    @teststep
    def judge_question_lock(self):
        """判断页面内是否存在 lock 标识"""
        locator = (By.ID, self.lock_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def judge_into_tab_question(self, title='题单'):
        """从首页进入题库tab"""
        self.home.click_tab_test_bank()  # 进入首页后 点击 题库tab
        if not self.wait_check_page(title):  # 页面检查点
            print('进入首页后 点击 题库tab，没加载出题单，重新进入')
            self.home.click_tab_hw()
            self.home.click_tab_test_bank()  # 进入首页后 点击 题库tab
            print('----------------')

    @teststeps
    def search_operation(self, search='autotest_', title='题单'):
        """查找 小游戏"""
        self.judge_into_tab_question(title)  # 进入首页后 点击 题库tab
        self.my_assert.assertEqual(self.wait_check_page(title), True, self.question_tips)

        name = self.question_name()  # 题单name
        if search not in name[1][0]:
            self.search_input().click()  # 点击 搜索框

            self.my_assert.assertEqual(self.wait_check_page('资源'), True, '★★★ Error- 未进入题库搜索页面')
            box = self.search_input()  # 搜索框
            box.send_keys(search)  # 输入搜索内容
            SearchPage().search_button()  # 搜索按钮

            self.my_assert.assertEqual(self.wait_check_page(title), True, self.back_question_tips)
            k = 0
            while k < 10:  # 最多下拉10次,跳出循环 (因为其他脚本的操作可能会向上滑屏，导致搜索结果不能展示在页面中)
                self.sp.swipe_vertical(0.5, 0.2, 0.85)  # 滑屏一次
                self.my_assert.assertEqual(self.wait_check_page(title), True, self.question_tips)
                name = self.question_name()  # 题单name
                if search not in name[1][0]:
                    k += 1
                else:  # 跳出循环
                    self.sp.swipe_vertical(0.5, 0.2, 0.85)  # 滑屏一次
                    break
        else:
            print('无需搜索, 有 %s 小游戏' % search)

    @teststeps
    def clear_search_operation(self):
        """清除 搜索框内容"""
        if self.wait_check_page():  # 恢复测试数据
            print('-------清除 搜索框内容------')
            self.search_input().click()  # 搜索框
            if self.wait_check_page('资源'):
                SearchPage().input_clear_button()  # 清空 按钮

                if self.wait_check_page('资源'):
                    SearchPage().search_button()  # 点击搜索按钮
            else:
                print('!!!未进入题库搜索页面')
