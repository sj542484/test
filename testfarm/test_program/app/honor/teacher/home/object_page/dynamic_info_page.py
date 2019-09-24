#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as ge
from testfarm.test_program.conf.base_page import BasePage
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class DynamicPage(BasePage):
    """app主页面- 各动态信息页面 元素信息"""
    hw_name_value = gv.PACKAGE_ID + 'name'  # 作业条目名称
    remind_button_value = gv.PACKAGE_ID + 'remind'  # 作业条目 提醒按钮

    def __init__(self):
        self.home = ThomePage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var):
        """以 xpath为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以 完成情况 为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "status")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_hw_page(self):
        """以“title:近期作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'{}')]".format(ge.DY_HW_TITLE))
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_paper_page(self):
        """以“title:近期卷子作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'{}')]".format(ge.DY_PAPER_TITLE))
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
        for i in range(len(ele)):

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
    def into_hw(self, title, var, vanclass):
        """进入作业/卷子/口语列表中的该作业/卷子/口语
        :param title:  近期卷子/口语/习题作业
        :param var: 作业/试卷 （近期作业中 不能进行编辑的）
        :param vanclass: 班级 （近期作业中 不能进行编辑的）
        """
        # var = self.home.brackets_text_out(var)
        if self.wait_check_page(title):
            hw = self.hw_item()  # 作业条目
            van = self.hw_vanclass()  # 班级名

            count = 0
            for i in range(len(hw)):
                name = hw[1][i][0]

                if name not in var or (name == var and van[i].text != vanclass):
                    print("进入作业/试卷:", hw[1][i])
                    hw[0][i][0].click()  # 进入作业
                    count = name
                    break

            if count == 0:
                print('★★★ Error- 没有可测试的数据')
            else:
                return count

    @teststeps
    def hw_list_operation(self, content=None):
        """近期作业 列表"""
        if self.wait_check_list_page():
            if content is None:
                content = []

            item = self.hw_item()  # 作业条目
            if len(item[1]) > 6 and not content:
                self.hw_list(item[1], len(item[1])-1)  # 获取作业/试卷/口语列表
            else:
                var = 0
                if content:
                    for k in range(len(item[1])):
                        if content[0] == item[1][k][0]:
                            var = k + 1
                            break

                if (not content) or (var != 0):
                    self.hw_list(item[1], len(item[1]), var)  # 获取作业/试卷/口语列表

    @teststeps
    def hw_list(self, item, length, index=0):
        """获取作业/试卷/口语列表
        """
        for i in range(index, length):
            print(item[i][0], '\n',
                  item[i][1], '  ', item[i][2], '  ', item[i][3])
            print('----------------------')

        content = [item[-1]]  # 最后一个作业的name
        SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
        self.hw_list_operation(content)

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
