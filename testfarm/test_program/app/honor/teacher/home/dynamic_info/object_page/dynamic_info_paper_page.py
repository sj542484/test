#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_paper_page import VanclassPaperPage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as ge
from conf.decorator_vue import teststep, teststeps
from conf.base_page import BasePage
from utils.assert_package import MyAssert
from utils.wait_element_vue import WaitElement


class DynamicPaperPage(BasePage):
    """app主页面- 试卷动态信息页面 元素信息"""
    dynamic_tips = '★★★ Error- 未进入近期卷子界面'
    dynamic_vue_tips = '★★★ Error- 未进入近期卷子vue界面'
    dynamic_list_tips = '★★★ Error- 近期卷子列表未加载成功'
    dynamic_empty_tips = '★★★ Error- 近期卷子列表为空'

    def __init__(self):
        self.home = ThomePage()
        self.wait = WaitElement()
        self.paper = VanclassPaperPage()
        self.screen = self.get_window_size()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_app_page(self):
        """以“title:近期作业”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="卷子"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self):
        """以“title:近期卷子作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="卷子"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以 完成情况 为依据"""
        locator = (By.XPATH, "//div[@id='homework-list']")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_no_hw_page(self, var=10):
        """删除所有作业后， 无最近作业提示检查点 以提示text作为依据"""
        locator = (By.XPATH, "//div[text()='学生练得不够?给学生布置个作业吧!']")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//img[@class="vt-page-left-img-Android"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def help_button(self):
        """ 提示 按钮"""
        locator = (By.XPATH, '//i[@class="nav-right-icon van-icon van-icon-question-o"]')
        self.wait \
            .wait_find_element(locator).click()

    # 列表 元素
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
    def hw_name(self):
        """作业条目名称"""
        locator = (By.XPATH, '//div[@class="homework-list-content-title-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def hw_vanclass(self):
        """班级"""
        locator = (By.XPATH, '//div[@class="homework-list-content-icon-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def hw_status(self):
        """完成情况"""
        locator = (By.XPATH, '//div[@class="homework-list-content-subtitle-text"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def help_operation(self):
        """ 右上角 提示按钮"""
        self.help_button()  # 右上角 提示按钮
        self.tips_content_commit()

    # 温馨提示 页面
    @teststeps
    def wait_check_tips_page(self, var=3):
        """以“温馨提示”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__header" and text()="温馨提示"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.XPATH, '//div[text()="温馨提示"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title van-dialog__message--left"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def commit_button(self):
        """确认 按钮"""
        locator = (By.XPATH, '//span[text()="确认"]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def into_hw(self):
        """进入作业/卷子/口语列表中的该作业/卷子/口语
        """
        # var = self.home.brackets_text_out(var)
        self.my_assert.assertTrue_new(self.wait_check_page(), self.dynamic_tips)  # 页面检查点
        self.my_assert.assertFalse(self.wait_check_no_hw_page(), self.dynamic_list_tips)  # 页面检查点

        hw = self.hw_name()  # 作业条目
        van = self.hw_vanclass()  # 班级名

        count = 0
        van_name = []
        name = []
        for i in range(len(hw)):
            if van[i].text != ge.VANCLASS:  # 班级 （近期作业中 不能进行编辑的）
                print("进入作业/试卷:", hw[i].text)
                name.append(hw[i].text)
                van_name.append(van[i].text)
                van[i].click()  # 进入作业
                count += 1
                break

        if count == 0:
            print('★★★ Error- 没有可测试的数据')
        else:
            return name[0], van_name[0]

    @teststeps
    def hw_list_operation(self):
        """获取 近期试卷列表
        """
        name = self.hw_name()
        create = self.hw_create_time()
        status = self.hw_status()
        van = self.hw_vanclass()  # 班级

        for i in range(len(name)):
            print(name[i].text, '\n',
                  create[i].text, '  ', van[i].text, '  ', status[i].text)
            print('----------------------')

    @teststep
    def delete_recent_hw_operation(self):
        """清空最近习题作业列表"""
        while True:
            self.my_assert.assertTrue_new(self.wait_check_page(), self.dynamic_tips)  # 页面检查点

            self.swipe_vertical_web(0.5, 0.2, 0.9)
            if self.wait_check_no_hw_page():
                print('作业已清空完毕')
                ThomePage().back_up_button()
                break
            else:
                van_class = self.hw_vanclass()  # 班级
                for i in range(len(van_class)):
                    if self.wait_check_page():
                        name = self.hw_name()  # 作业名称
                        date = self.hw_create_time()  # 创建时间
                        status = self.hw_status()  # 完成情况
                        print(name[0].text, date[0].text, status[0].text, van_class[0].text)
                        name[0].click()

                        if self.paper.wait_check_page():
                            self.paper.delete_commit_operation()  # 删除作业 具体操作
            print('-' * 20)

    @teststeps
    def tips_content_commit(self, var=5):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page(var):  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.commit_button()  # 确定按钮
            print('--------------------------')

    @teststeps
    def tips_commit(self):
        """温馨提示 -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.commit_button()  # 确定按钮

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
