#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_page import VanclassPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.vue_context import VueContext
from utils.wait_element_vue import WaitElement


class VanclassPaperPage(BasePage):
    """ 班级详情页 修改、查询页面元素信息"""
    no_data_value = '//div[text()="暂无数据"]'  # 暂无数据

    paper_tips = '★★★ Error- 未进入本班卷子vue界面'
    paper_list_tips = '★★★ Error- 本班卷子列表为空'

    more_tips = '★★★ Error- 未进入更多按钮详情'
    more_delete_tips = '★★★ Error- 未弹出试卷删除二次确认弹框'

    edit_tips = '★★★ Error- 未进入编辑试卷 详情页'
    edit_list_tips = '★★★ Error- 编辑试卷 详情页未加载成功'

    def __init__(self):
        self.get = GetAttribute()
        self.wait = WaitElement()
        self.home = ThomePage()
        self.van = VanclassPage()
        self.my_assert = MyAssert()
        self.vue = VueContext()
        self.screen = self.get_window_size()

    @teststeps
    def wait_check_page(self, var):
        """以“title: 班级本班卷子”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以完成进度 的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "status")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_empty_tips_page(self, var=3):
        """暂无口语/作业/试卷，去题库看看吧"""
        locator = (By.XPATH, self.no_data_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def no_data(self):
        """暂无数据元素"""
        locator = (By.XPATH, self.no_data_value)
        ele = self.wait.wait_find_element(locator)
        print(ele.text)

    @teststep
    def hw_name(self):
        """试卷name"""
        locator = (By.XPATH, '//div[@class="homework-list-content-title-text"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def progress(self):
        """完成进度 - 已完成x/x"""
        locator = (By.XPATH, '//div[@class="homework-list-content-subtitle-text"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def vanclass_name(self):
        """班级名"""
        locator = (By.XPATH, '//div[@class="homework-list-content-icon-text"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait.wait_find_element(locator).click()
    
    @teststep
    def more_button(self):
        """更多 按钮"""
        locator = (By.XPATH, '//i[@class="nav-right-icon van-icon van-icon-ellipsis"]')
        self.wait \
            .wait_find_element(locator).click()
    
    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.XPATH, '//div[@class="van-popup van-popup--round van-popup--bottom van-action-sheet"]')
        return self.wait.wait_check_element(locator)
    
    @teststep
    def more_edit_button(self):
        """编辑 按钮"""
        locator = (By.XPATH, '//span[text()="编辑"]')
        self.wait \
            .wait_find_element(locator).click()
    
    @teststep
    def more_delete_button(self):
        """删除 按钮"""
        locator = (By.XPATH, '//span[text()="删除"]')
        self.wait \
            .wait_find_element(locator).click()
    
    @teststeps
    def more_cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//div[@class="van-action-sheet__cancel"]')
        self.wait \
            .wait_find_element(locator).click()


    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__confirm van-hairline--left"]')
        self.wait \
            .wait_find_element(locator).click()

    # 删除作业tips 页面
    @teststeps
    def delete_commit_operation(self):
        """删除试卷 具体操作"""
        self.more_button()  # 更多 按钮
        self.my_assert.assertEqual(self.wait_check_more_page(), True, self.more_tips)

        self.more_delete_button()  # 删除按钮
        self.vue.app_web_switch()  # 切到apk 再切回web
        self.my_assert.assertEqual(self.wait_check_tips_page(), True, self.more_delete_tips)
        print('--删除试卷--')
        self.commit_button()  # 确定按钮
        print('确定删除')
        self.vue.app_web_switch()

    @teststeps
    def delete_cancel_operation(self):
        """删除试卷 具体操作"""
        self.more_button()  # 更多 按钮
        self.my_assert.assertEqual(self.wait_check_more_page(), True, self.more_tips)

        self.more_delete_button()  # 删除按钮
        self.vue.app_web_switch()  # 切到apk 再切回web
        self.my_assert.assertEqual(self.wait_check_tips_page(), True, self.more_delete_tips)
        print('---------删除试卷---------')
        self.tips_title()
        self.tips_content()
        self.cancel_button()  # 取消按钮
        self.vue.app_web_switch()  # 切到apk 再切回web

        print('---------------')
        print('取消删除')

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
