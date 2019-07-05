#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import re

from selenium.webdriver.common.by import By
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.homework_detail_page import HwDetailPage

from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class DynamicPage(BasePage):
    """app主页面- 各动态信息页面 元素信息"""
    hw_name_value = gv.PACKAGE_ID + 'name'  # 作业条目名称
    remind_button_value = gv.PACKAGE_ID + 'remind'  # 作业条目 提醒按钮

    def __init__(self):
        self.home = ThomePage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var):
        """以xpath为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以xpath为依据"""
        locator = (By.ID,gv.PACKAGE_ID + "status")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_spoken_page(self):
        """以“title:近期口语作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'近期口语作业')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_hw_page(self):
        """以“title:近期习题作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'近期习题作业')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_paper_page(self):
        """以“title:近期卷子作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'近期卷子作业')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_no_hw_page(self, var=10):
        """删除所有作业后， 无最近作业提示检查点 以提示text作为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学生练得不够?给学生布置个作业吧!')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def help_button(self):
        """ 提示 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "question") \
            .click()

    # 列表 元素
    @teststeps
    def hw_item(self):
        """作业包 条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/android.widget.RelativeLayout/"
                                    "child::*")

        count = []
        for i in range(0, len(ele), 5):
            if GetAttribute().resource_id(ele[i]) == self.hw_name_value:
                count.append(i)
        count.append(len(ele))

        content = []  # 页面内所有条目 元素text
        element = []  # 页面内所有条目元素
        remind = []  # 提醒按钮
        for j in range(len(count) - 1):
            item = []  # 每一个条目的所有元素
            var = []  # 各条目
            if count[j + 1] - count[j] == 5:
                for k in range(count[j], count[j + 1]):
                    if ele[k].text != '':
                        item.append(ele[k].text)
                        var.append(ele[k])
                    else:
                        if GetAttribute().resource_id(ele[k]) == self.remind_button_value:
                            remind.append(ele[k])

                content.append(item)
                element.append(var)

        print(content)
        return element, content, remind

    @teststep
    def hw_name(self):
        """作业条目名称"""
        ele = self.driver\
            .find_elements_by_id(self.hw_name_value)
        return ele

    @teststep
    def hw_create_time(self):
        """创建时间"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "date")
        return ele

    @teststep
    def hw_status(self):
        """完成情况"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "status")

        return ele

    @teststep
    def remind_button(self):
        """提醒 按钮"""
        ele = self.driver \
            .find_elements_by_id(self.remind_button_value)
        return ele

    @teststep
    def hw_vanclass(self):
        """班级"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "class_name")
        return ele

    @teststeps
    def help_operation(self):
        """ 右上角 提示按钮"""
        self.help_button()  # 右上角 提示按钮
        ThomePage().tips_content_commit()

    @teststeps
    def into_hw(self, title, finish=0):
        """进入作业/卷子/口语列表中的该作业/卷子/口语"""
        if self.wait_check_page(title):
            item = self.hw_item()  # 作业条目
            length = len(item[0])
            if len(item[0]) > 7:
                length = len(item[0]) - 1

            count = 0
            if finish != 0:
                for i in range(length):
                    var = re.findall(r'\d+(?#\D)', item[1][i][3])[0]
                    if var != 0:
                        count += i
                        break
            else:
                for i in range(length):
                    var = re.findall(r'\d+(?#\D)', item[1][i][3])[0]
                    if var == 0:
                        count += i
                        break

            if count != 0:
                item[0][count][0].click()  # 进入作业
                print(title, item[1][count][0])
                return item[1][count][0]
            else:
                if self.wait_check_page(title):
                    SwipeFun().swipe_vertical(0.5, 0.75, 0.25)
                    self.into_hw(title, finish)  # 进入

    @teststeps
    def hw_list_operation(self, index=0):
        """获取作业/试卷/口语列表 及 页面内最后一个name"""
        item = self.hw_item()  # 作业条目
        for i in range(index, len(item[1])):
            print(item[1][i][0], '\n',
                  item[1][i][1], '  ', item[1][i][2], '  ', item[1][i][3])
            print('----------------------')
        last = item[1][-1]  # 最后一个作业

        return last

    @teststeps
    def swipe_operation(self, k):
        """滑屏 操作"""
        print('----------------------近期作业列表----------------------')
        var = self.hw_list_operation(k)  # 获取列表信息
        SwipeFun().swipe_vertical(0.5, 0.75, 0.25)
        item = self.hw_item()  # 作业条目
        if len(item[1]) > 9:
            last = item[1][-1]  # 最后一个作业
            if var in item[1] and last != var:   # 滑动了# todo 列表中可能有多个相同作业/卷子/口语名
                # print('滑动后到底部')
                for i in range(len(item[1]), 0):
                    if item[1][i] == var:
                        self.swipe_operation(i+1)
                        break
        else:
            last = item[1][-1]  # 最后一个作业
            # print('滑动后未到底部')
            if var in item[1] and last != var:  # 未滑够一页
                # print('未滑够一页')
                for i in range(len(item[1]), 0):
                    if item[1][i] == var[0]:
                        self.swipe_operation(i+1)
                        break

    @teststep
    def delete_recent_hw_operation(self):
        """清空最近习题作业列表"""
        while True:
            if self.wait_check_page():
                SwipeFun().swipe_vertical(0.5, 0.2, 0.9)
                if self.wait_check_no_hw_page():
                    print('作业已清空完毕')
                    ThomePage().back_up_button()
                    break
                else:
                    vanclass = self.hw_vanclass()  # 班级
                    for i in range(len(vanclass)):
                        if self.wait_check_page():
                            name = self.hw_name()  # 作业名称
                            date = self.hw_create_time()  # 创建时间
                            status = self.hw_status()  # 完成情况
                            print(name[0].text, date[0].text, status[0].text, vanclass[0].text)
                            name[0].click()
                            if HwDetailPage().wait_check_page():
                                HwDetailPage().delete_commit_operation()  # 删除作业 具体操作
            print('-' * 20)
