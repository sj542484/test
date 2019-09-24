#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time

from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class SearchPage(BasePage):
    """题库 搜索页面"""
    question_value = gv.PACKAGE_ID + "test_bank_name"  # 题单名
    question_type_value = gv.PACKAGE_ID + "type"  # 题单类型
    num_value = gv.PACKAGE_ID + "exercise_num"  # 共X题
    drop_down_value = gv.PACKAGE_ID + "title"  # 下拉菜单

    lock_value = gv.PACKAGE_ID + "lock"  # 锁input_clear_button


    def __init__(self):
        self.sp = SwipeFun()
        self.home = ThomePage()
        self.wait = WaitElement()

    # 搜索框
    @teststeps
    def wait_check_game_type_page(self):
        """以“大题类型”为依据"""
        locator = (By.ID, self.question_type_value)
        return self.wait.wait_check_element(locator, 3)

    # 搜索页面
    @teststeps
    def wait_check_search_page(self):
        """以“搜索 按钮”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "search")
        return self.wait.wait_check_element(locator, 3)

    @teststep
    def drop_down_button(self):
        """以“下拉 按钮”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "choose_menu")
        # print('选定的搜索条件：', ele.text)
        return ele

    @teststep
    def search_criteria_menu(self):
        """以“下拉 菜单”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(self.drop_down_value)
        return ele

    @teststeps
    def judge_search_menu(self):
        """判断 下拉 菜单"""
        locator = (By.ID, self.drop_down_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def input_clear_button(self):
        """以“清空 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "input_clear") \
            .click()

    @teststep
    def search_button(self):
        """以“搜索 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "search") \
            .click()

    @teststep
    def search_icon(self):
        """以“历史搜索词 的icon”的class name为依据"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.ImageView")
        return ele

    @teststep
    def history_word(self):
        """以“历史搜索词”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "text")
        return ele

    @teststep
    def delete_button(self, index):
        """以“删除 按钮”的id为依据"""
        print('点击删除按钮')
        time.sleep(1)
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "delete")[index] \
            .click()

    @teststeps
    def choose_condition(self, var):
        """搜索条件  判断"""
        if var[0].text != '资源' or var[1].text != '上传者':
            for i in range(len(var)):
                print('★★★ Error -', var[i].text)
            print('-------------------')

    @teststeps
    def get_history_search_word(self, item=None, content=None):
        """获取历史搜索词
        :param item:历史搜索词元素
        :param content:历史搜索词
        """
        if item is None:
            item = []
        if content is None:
            content = []

        name = self.history_word()  # 历史搜索词

        if len(name) > 9 and not content:  # 有9个以上历史搜索词时
            content = []
            for i in range(len(name) - 1):  # # 最后一个容易出现信息展示不全
                item.append(name[i])
                content.append(name[i].text)

            self.sp.swipe_vertical(0.5, 0.85, 0.1)
            return self.get_history_search_word(item, content)
        else:  # <10 & 翻页
            var = 0
            if content:
                for k in range(len(name)):  # 判断翻页后，页面中是否存在已操作过的搜索词
                    if content[-1] == name[k].text:
                        var += k + 1
                        break

            for j in range(var, len(name)):
                item.append(name[j])
                content.append(name[j].text)

            return content, item
