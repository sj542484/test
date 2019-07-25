#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class AdjustVanOrderPage(BasePage):
    """ 调整班级排序 页面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
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
    def adjust_vanclass_order(self):
        """班级顺序调整 具体操作"""
        if self.wait_check_page():  # 页面检查点
            name = self.vanclass_name()  # 班级名
            num = self.vanclass_no()  # 班号
            print('-----------------班级顺序调整 页面-----------------')

            content = []
            icon = self.drag_icon()  # 拖拽 icon
            if len(num) > 5:
                for i in range(len(num) - 1):
                    print(num[i].text, name[i].text)
                    content.append(num[i].text)
                    content.append(name[i].text)

                self.drag_ele_operation(icon[1], icon[5])  # 向下拖拽
                self.drag_ele_operation(icon[4], icon[1])  # 向上拖拽

                self.judge_hw_adjust(content)  # 验证
            elif 1 < len(num) < 6:
                for i in range(len(num)):
                    print(num[i].text, name[i].text)
                    content.append(num[i].text)
                    content.append(name[i].text)
                self.drag_ele_operation(icon[1], icon[len(num)-1])  # 向下拖拽
                self.drag_ele_operation(icon[len(num)-2], icon[0])  # 向上拖拽

                self.judge_hw_adjust(content)  # 验证
            else:
                print('只有%s个班级' % len(num))

    @teststeps
    def judge_hw_adjust(self, content):
        """验证 调整班级顺序"""
        if self.wait_check_page():  # 页面检查点
            print('---------------验证 调整班级顺序---------------')
            name = self.vanclass_name()  # 班级名
            num = self.vanclass_no()  # 班号

            item = []
            if len(num) > 5:
                for i in range(len(num) - 1):
                    print(num[i].text, name[i].text)
                    item.append(num[i].text)
                    item.append(name[i].text)
            elif 2 < len(num) < 6:
                for i in range(len(num)):
                    print(num[i].text, name[i].text)
                    item.append(num[i].text)
                    item.append(name[i].text)

            count = 0
            for j in range(len(item)):
                if item[j] != content[j]:
                    count += 1

            print('---------------------------')
            if count == 0:
                print('★★★ Error- 调整页面展示, 班级顺序未调整')
            else:
                print('调整页面展示, 调整班级顺序成功')
            print('-----------------------------------------')

    @teststeps
    def drag_ele_operation(self, origin, destination):
        """拖拽元素"""
        TouchAction(self.driver).long_press(origin).move_to(destination).release().perform()
