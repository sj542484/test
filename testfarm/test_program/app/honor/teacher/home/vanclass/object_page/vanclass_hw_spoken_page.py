#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as ge
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext
from utils.wait_element_vue import WaitElement


class VanclassHwPage(BasePage):
    """ 本班作业 页面元素信息"""
    no_data_value = '//div[text()="暂无数据"]'  # 暂无数据
    goto_pool_value = gv.PACKAGE_ID + "tv_topool"  # 去题库

    van_hw_tips = '★★★ Error- 未进入本班作业vue界面'
    van_hw_list_tips = '★★★ Error- 本班作业列表为空'

    def __init__(self):
        self.get = GetAttribute()
        self.wait = WaitElement()
        self.home = ThomePage()
        self.van_detail = VanclassDetailPage()
        self.vue = VueContext()
        self.screen = self.get_window_size()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var):
        """以“title: 班级名称/ 作业名称/本班卷子/口语作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="{}"]'.format(var))
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以完成进度 的id为依据"""
        locator = (By.XPATH, '//div[@class="van-list"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_empty_tips_page(self, var=3):
        """暂无数据"""
        locator = (By.XPATH, self.no_data_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def no_data(self):
        """暂无数据元素"""
        locator = (By.XPATH, self.no_data_value)
        print(self.wait.wait_find_element(locator).text)

    @teststep
    def hw_name(self):
        """作业条目名称"""
        locator = (By.XPATH, '//div[@class="homework-list-content-title-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def hw_create_time(self):
        """创建时间 完成情况"""
        locator = (By.XPATH, '//div[@class="homework-list-content-subtitle-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def remind_button(self):
        """提醒 按钮"""
        locator = (By.XPATH, '//img[@class="homework-list-content-icon-img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def hw_vanclass(self):
        """班级"""
        locator = (By.XPATH, '//div[@class="homework-list-content-icon-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def into_operation(self, title_tip, van_name, var='习题'):
        """进入列表中 指定口语/作业/卷子 具体操作
        :param van_name: 班级名
        :param var: 类型
        :param title_tip: 作业包name
        """
        title = title_tip.format(van_name)
        self.vue.app_web_switch()  # 切到web

        self.my_assert.assertTrue(self.wait_check_page(title), self.van_hw_tips)  # 页面检查点
        if self.wait_check_empty_tips_page():
            self.no_data()
            self.my_assert.assertTrue(self.wait_check_list_page(), self.van_hw_list_tips)  # 页面检查点
        else:
            self.my_assert.assertTrue(self.wait_check_list_page(), self.van_hw_list_tips)  # 页面检查点
            name = self.hw_name()  # 作业name
            count = []
            for i in range(len(name)):
                text = name[i].text
                if self.wait_check_list_page():
                    if self.home.brackets_text_in(text) == var:
                        count.append(i)

            text = None
            if len(count) == 0:
                print('暂无{}作业包'.format(var))
            else:
                index = random.randint(0, len(count) - 1)
                text = name[count[index]].text
                name[count[index]].click()
                self.vue.app_web_switch()  # 切到app 切回web

            return text, title

    @teststeps
    def edit_into_operation(self):
        """进入  有作业的班级"""
        self.my_assert.assertTrue_new(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
        self.my_assert.assertTrue_new(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
        van_name = self.home.item_detail()  # 班号+班级名

        for i in range(len(van_name)):
            self.my_assert.assertTrue_new(self.home.wait_check_list_page(), self.home.van_list_tips)  # 页面加载完成 检查点
            van_name = self.home.item_detail()  # 班号+班级名
            van = self.home.vanclass_name(van_name[i].text)  # 班级名
            if van != ge.VANCLASS:
                van_name[i].click()  # 进入班级

                self.my_assert.assertTrue_new(self.van_detail.wait_check_app_page(van), self.van_detail.van_tips)  # 页面检查点
                self.vue.switch_h5()  # 切到web
                self.my_assert.assertTrue_new(self.van_detail.wait_check_page(van), self.van_detail.van_vue_tips)
                self.van_detail.vanclass_hw()  # 点击进入 本班作业 tab
                title = ge.HW_TITLE.format(van)

                print('本班作业:')
                self.vue.app_web_switch()  # 切到apk 再切回web
                self.my_assert.assertTrue(self.wait_check_page(title), self.van_hw_tips)  # 页面检查点
                if self.wait_check_empty_tips_page():
                    self.back_up_button()  # 返回 答题详情页面
                    self.vue.app_web_switch()  # 切到app 再切换到vue

                    self.my_assert.assertTrue_new(self.van_detail.wait_check_page(van), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
                    self.back_up_button()  # 返回主界面
                    self.vue.switch_app()
                else:
                    self.my_assert.assertTrue(self.wait_check_list_page(), self.van_hw_list_tips)  # 页面检查点
                    print('班级:', van)
                    hw_name = self.random_into_operation()  # 随机进入某个作业 游戏列表
                    if hw_name != 0:
                        print('=====================================')
                        return hw_name, van
                    else:
                        self.back_up_button()  # 返回 答题详情页面
                        self.vue.app_web_switch()  # 切到app 再切换到vue
                        self.my_assert.assertTrue_new(self.van_detail.wait_check_page(van), self.van_detail.van_vue_tips)  # 班级详情 页面检查点
                        self.back_up_button()  # 返回主界面

    @teststeps
    def random_into_operation(self):
        """随机进入列表中 某个口语/作业 具体操作
        """
        hw_name = 0
        hw = self.hw_name()  # 口语/作业 name
        for i in range(len(hw)):
            index = 0
            if len(hw) != 1:
                index = random.randint(0, len(hw)-1)
            hw_name = hw[index].text
            print("口语/作业:", hw_name)
            hw[index].click()  # 进入口语/作业
            break

        if hw_name == 0:
            print('★★★ Error- 没有可测试的口语/作业数据')

        return hw_name

    @teststeps
    def swipe_vertical_web(self, ratio_x, start_y, end_y, steps=1000):
        """
        上/下滑动 x值不变
        :param ratio_x: x坐标系数
        :param start_y: 滑动起点y坐标系数
        :param end_y: 滑动终点y坐标系数
        :param steps: 持续时间ms
        :return: None
        """
        x = int(self.screen[0] * ratio_x)
        y1 = int(self.screen[1] * start_y)
        y2 = int(self.screen[1] * end_y)

        self.driver.swipe(x, y1, x, y2, steps)
