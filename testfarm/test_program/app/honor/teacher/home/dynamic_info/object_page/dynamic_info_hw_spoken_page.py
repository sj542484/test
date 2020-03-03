#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable as ge
from utils.assert_package import MyAssert
from utils.vue_context import VueContext
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.wait_element_vue import WaitElement
# 首页口语/习题 班级口语/习题和下方作业列表 ,其中除用户指南 作业编辑 再次发布跳转到原生 , 其余全是网页


class DynamicPage(BasePage):
    """app主页面- 各动态信息页面 元素信息"""
    hw_item_value = "//div[@id='homework-list']"  # 作业条目

    dynamic_tips = '★★★ Error- 未进入习题作业界面'
    dynamic_vue_tips = '★★★ Error- 未进入近期习题作业vue界面'
    dynamic_list_tips = '★★★ Error- 近期习题作业列表为空'

    def __init__(self):
        self.home = ThomePage()
        self.wait = WaitElement()
        self.screen = self.get_window_size()
        self.vue = VueContext()

    @teststeps
    def wait_check_app_page(self):
        """以“title:近期作业”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="口语/习题"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self):
        """以“title:近期作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="口语/习题"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以 完成情况 为依据"""
        locator = (By.XPATH, self.hw_item_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_no_hw_page(self, var=5):
        """删除所有作业后， 无最近作业提示检查点 以提示text作为依据"""
        locator = (By.XPATH, "//div[@text='学生练得不够?给学生布置个作业吧!']")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//img[@class="vt-page-left-img-Android"]')
        self.wait\
            .wait_find_element(locator).click()

    @teststep
    def help_button(self):
        """ 提示 按钮"""
        locator = (By.XPATH, '//i[@class="nav-right-icon van-icon van-icon-question-o"]')
        self.wait\
            .wait_find_element(locator).click()

    # 列表 元素
    @teststeps
    def hw_items(self):
        """作业包 条目"""
        locator = (By.XPATH, self.hw_item_value)
        return self.wait.wait_find_elements(locator)

    # @teststeps
    # def hw_items_info(self):
    #     """作业包 条目信息"""
    #     content = []  # 页面内所有条目 元素text
    #     elements = []  # 页面内所有条目元素
    #     remind = []  # 提醒按钮
    #
    #     ele = self.hw_items()  # 作业包 条目
    #     for i in range(len(ele)):
    #         item = []  # 每一个条目的所有元素text
    #         element = []  # 每一个条目的所有元素
    #         descendant = ele[i].find_elements_by_xpath('.//descendant::div')
    #
    #         for j in range(len(descendant)):
    #             var = descendant[j].text
    #             if var not in ('', '  '):
    #                 if GetAttribute().class_name(descendant[j]) == 'android.widget.Image':  # 提醒按钮
    #                     remind.append(descendant[j + 1])
    #                 elif GetAttribute().class_name(descendant[j]) == 'homework-list-content-subtitle-text':
    #                     item.append(var)
    #                     element.append(descendant[j])
    #
    #         content.append(item/)
    #         elements.append(element)
    #
    #     return elements, content, remind

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
        locator = (By.XPATH, '//span[@text()="确认"]/parent::button')
        return self.wait.wait_find_element(locator)

    @teststeps
    def into_hw(self):
        """进入作业/口语列表中的该作业/口语
        """
        count = 0
        van_name = []
        name = []
        if self.wait_check_list_page():
            hw = self.hw_name()  # 作业名
            van = self.hw_vanclass()  # 班级名

            for i in range(len(hw)):
                print('-----------------')
                if (van[i].text != ge.VANCLASS) and ('spoken assign' not in hw[i].text):  # 班级 （近期作业中 不能进行编辑的）
                    print("进入作业:", hw[i].text, van[i].text)
                    name.append(hw[i].text)
                    van_name.append(van[i].text)
                    van[i].click()  # 进入作业
                    count += 1
                    break
        elif self.wait_check_no_hw_page():
            print('暂无数据')

        if count == 0:
            print('★★★ Error- 没有可测试的数据')
        else:
            return name[0], van_name[0]

    @teststeps
    def hw_list_operation(self, content=None):
        """近期作业 列表"""
        MyAssert().assertTrue_new(self.wait_check_list_page(), self.dynamic_list_tips)
        if content is None:
            content = []

        name = self.hw_name()  # 作业条目
        create = self.hw_create_time()  # 创建时间
        if len(name) > 6 and not content:
            self.hw_list(name, create, len(name)-1)  # 获取作业/试卷/口语列表
            content = [name[-2], create[-2]]

            self.swipe_vertical_web(0.5, 0.85, 0.1)
            self.hw_list_operation(content)  # 最后一个作业的name
        else:
            var = 0
            length = len(name)
            if content:
                for k in range(len(name)):
                    if content[0] == name[k] and content[1] == create[k]:
                        var = k + 1
                        break

                if var == 0:
                    var = 1
                if len(name) > 8:
                    length = 8

            self.hw_list(name, create, length, var)  # 获取作业/试卷/口语列表
            print('---------------------------------------------------')

    @teststeps
    def hw_list(self, hw, create, length, index=0):
        """获取作业/试卷/口语列表
        """
        van = self.hw_vanclass()  # 班级名
        remind = self.remind_button()  # 提醒按钮
        if len(hw) != len(remind) or len(create) != len(van):
            print('★★★ Error- 题目各元素个数不等', len(hw), len(remind), len(create), len(van))

        for i in range(index, length):
            print(hw[i].text, '\n',
                  create[i].text, '  ', van[i].text)
            print('----------------------')

    @teststeps
    def judge_dynamic_result_operation(self, assign):
        """近期动态 验证布置结果 具体操作
        :param assign:名称
        """
        if self.home.wait_check_page():  # 页面检查点
            print('------------------验证 近期动态 布置结果------------------')
            self.home.hw_icon()  # 作业icon
            MyAssert().assertTrue_new(self.wait_check_app_page(), self.dynamic_tips)
            self.vue.switch_h5()
            MyAssert().assertTrue_new(self.wait_check_page(), self.dynamic_vue_tips)
            if self.wait_check_no_hw_page():
                print('★★★ Error- 暂无近期作业，布置作业失败')
            else:
                MyAssert().assertTrue_new(self.wait_check_list_page(), self.dynamic_list_tips)
                name = self.hw_name()  # 条目名称
                var = self.hw_vanclass()  # 班级名
                create = self.hw_create_time()

                for i in range(len(name)):
                    vanclass = var[i].text
                    title = name[i].text
                    count = 0
                    for key in assign:
                        if vanclass == assign[key] and title == key and create[i].text == time.strftime('%Y%m%d'):
                            count = 1
                            print('有重名作业', assign, title)
                            break

                    if count == 0:
                        print('★★★ Error- 无重名作业')
                    else:
                        break

            MyAssert().assertTrue_new(self.wait_check_page(), self.dynamic_vue_tips)
            self.back_up_button()  # 返回 主界面
            self.vue.switch_app()

    @teststeps
    def delete_recent_hw_operation(self):
        """清空最近习题作业列表"""
        while True:
            MyAssert().assertTrue_new(self.wait_check_page(), self.dynamic_vue_tips)
            self.swipe_vertical_web(0.5, 0.2, 0.9)
            if self.wait_check_no_hw_page():
                print('作业已清空完毕')
                self.home.back_up_button()
                break
            else:
                MyAssert().assertTrue_new(self.wait_check_list_page(), self.dynamic_list_tips)
                van_class = self.hw_vanclass()  # 班级
                for i in range(len(van_class)):
                    MyAssert().assertTrue_new(self.wait_check_page(), self.dynamic_vue_tips)
                    name = self.hw_name()  # 作业名称
                    create = self.hw_create_time()  # 创建时间 完成情况
                    print(name[0].text, create[0].text, van_class[0].text)
                    name[0].click()
                    if HwDetailPage().wait_check_page():
                        HwDetailPage().delete_commit_operation()  # 删除作业 具体操作
        print('-' * 20)

    @teststeps
    def tips_content_commit(self, var=5):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page(var):  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.commit_button().click()  # 确定按钮
            print('--------------------------')

    @teststeps
    def tips_commit(self):
        """温馨提示 -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.commit_button().click()  # 确定按钮

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

    @teststeps
    def current_activity(self):
        """首页口语/习题 班级口语/习题和下方作业列表 ,其中除用户指南 作业编辑 再次发布跳转到原生 , 其余全是网页"""
        self.driver.background_app(2)
        print('ACTIVITY:',self.driver.current_context)

