#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from utils.assert_package import MyAssert
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class THomeVanclassPage(BasePage):
    """app主页面 班级相关元素信息"""
    vanclass_locator = (By.ID, gv.PACKAGE_ID + "class_info")  # 班级条目

    van_list_tips = '★★★ Error- 无班级'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_list_page(self):
        """以“有无班级”为依据"""
        return self.wait.wait_check_element(self.vanclass_locator)

    @teststep
    def wait_check_empty_tips_page(self, var=3):
        """暂时没有数据"""
        locator = (By.ID, gv.PACKAGE_ID + "load_empty")
        return self.wait.wait_check_element(locator, var)

    # 班级列表
    @teststep
    def item_detail(self):
        """首页 条目名称  班号+班级名"""
        return self.wait\
            .wait_find_elements(self.vanclass_locator)

    @teststep
    def vanclass_name(self, var):
        """班级名"""
        value = re.sub(r'\[.*?\]', '', var)
        return value

    @teststeps
    def vanclass_no(self, var):
        """班号"""
        m = re.match(r".*\[(.*)\].*", var)  # title中有一个中括号
        value = re.findall(r'\d+(?#\D)', m.group(1))
        return value[0]

    @teststep
    def st_count(self):
        """学生人数"""
        locator = (By.ID, gv.PACKAGE_ID + "student_num")
        return self.wait \
            .wait_find_elements(locator)

    @teststep
    def unread_point(self):
        """未读 小红点"""
        locator = (By.ID, gv.PACKAGE_ID + "unread")
        return self.wait \
            .wait_find_elements(locator)

    # 调整班级排序 页面
    @teststeps
    def wait_check_adjust_page(self):
        """以“title:班级列表”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'班级列表')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def confirm_button(self):
        """确定按钮"""
        self.driver \
            .find_element_by_id("confirm") \
            .click()

    @teststep
    def vanclass_name(self):
        """班级名"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "class_name")
        return ele

    @teststep
    def vanclass_no(self):
        """班号"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "class_no")
        return ele

    @teststep
    def drag_icon(self):
        """拖拽 icon"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_drag_icon")
        return ele

    @teststeps
    def drag_ele_operation(self, origin, target):
        """拖拽元素"""
        TouchAction(self.driver).long_press(origin).move_to(target).release().perform()

    @teststeps
    def vanclass_order(self):
        """班级 列表"""
        van = []
        self.list_swipe_operation(van)  # 已有班级数 统计

        print('--------------------------------------')
        content = []
        for i in range(len(van)):
            for j in range(len(van[i])):
                content.append(van[i][j])

        print(content)
        return content

    @teststeps
    def list_swipe_operation(self, content):
        """班级列表 滑屏 操作"""
        var = self.vanclass_statistic_operation(content)  # 获取 班级列表信息
        SwipeFun().swipe_vertical(0.5, 0.75, 0.25)

        self.my_assert.assertTrue(self.wait_check_list_page(), self.van_list_tips)  # 页面加载完成 检查点
        title = []
        item = self.item_detail()  # 班级条目
        for i in range(len(item)):
            name = self.vanclass_name(item[i].text)  # name
            title.append(name)
        last = item[-1].text  # 最后一个班级的title

        index = []
        if len(title) != 10:  # 到底部
            if var in title:  # todo 列表中可能有多个相同
                if last != var:  # 滑动了
                    # print('滑动后到底部')
                    for i in range(len(title)):
                        if title[i] == var:
                            index.append(i + 1)
                            break
                else:
                    # print('到底了')
                    index.append(len(title))

                self.vanclass_statistic_operation(content, index[0])  # 获取 班级列表信息
        else:
            # print('滑动后未到底部')
            if var in title:  # 未滑够一页
                # print('未滑够一页')
                for i in range(len(title)):
                    if title[i] == var:
                        index.append(i + 1)
                        break
            else:
                index.append(0)

            return self.vanclass_statistic_operation(content, index[0])  # 获取 班级列表信息

    @teststeps
    def vanclass_statistic_operation(self, content, index=0):
        """获取班级列表 及 页面内最后一个name"""
        self.my_assert.assertTrue(self.wait_check_list_page(), self.van_list_tips)  # 页面加载完成 检查点

        name = self.item_detail()  # 班号+班级名
        count = self.st_count()  # 学生人数

        if len(name) != len(count):  # 滑屏后
            length = min(len(name), len(count))
        else:
            length = len(count)

        for i in range(index, length):
            num = self.vanclass_no(name[i].text)  # 班号
            van = self.vanclass_name(name[i].text)  # 班级名
            content[van] = count[i].text
        last = self.vanclass_name(name[-1].text)  # 最后一个作业的title

        return last
