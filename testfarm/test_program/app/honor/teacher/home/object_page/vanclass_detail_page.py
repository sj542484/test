#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class VanclassDetailPage(BasePage):
    """ 班级详情页 修改、查询页面元素信息"""
    goto_pool_value = gv.PACKAGE_ID + "tv_topool"  # 去题库
    st_icon_value = gv.PACKAGE_ID + "head"  # 学生头像
    st_order_value = gv.PACKAGE_ID + "tv_order"  # 序号

    def __init__(self):
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststep
    def judge_van_modify(self):
        """班级名称 修改验证"""
        ele = self.driver \
            .find_element_by_class_name("android.widget.TextView").text
        return ele

    # 本班作业
    @teststeps
    def wait_check_page(self, var):
        """以“title: 班级名称/ 作业名称/本班卷子/口语作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以完成进度 的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "status")
        return self.wait.wait_check_element(locator)

    @teststep
    def best_tab(self):
        """最优成绩 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'最优成绩')]")
        return ele

    @teststep
    def first_tab(self):
        """首次成绩 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'首次成绩')]")
        return ele

    # 最优成绩 tab
    @teststeps
    def wait_check_achievement_list_page(self):
        """以“列表中 序号”为依据"""
        locator = (By.ID, self.st_order_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def answer_detail_button(self):
        """答题详情 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "details") \
            .click()

    @teststep
    def end_tips(self):
        """没有更多了"""
        try:
            self.driver.find_element_by_id(gv.PACKAGE_ID + "end")
            return True
        except Exception:
            return False

    @teststep
    def hw_name(self):
        """作业name"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def progress(self):
        """完成进度 - 已完成x/x"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "status")
        return ele

    @teststep
    def create_time(self):
        """作业创建时间"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "date")
        return ele

    @teststep
    def remind(self):
        """提醒 按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "remind")
        return ele

    @teststep
    def vanclass_name(self):
        """班级名"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "class_name")
        return ele

    @teststep
    def spend_time(self):
        """用时"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_spend_time")
        return ele

    @teststep
    def accuracy(self):
        """正答率"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_accurency")
        return ele

    # 本班卷子
    @teststep
    def goto_paper_pool(self):
        """无试卷时 --去题库按钮"""
        self.driver \
            .find_elements_by_id(self.goto_pool_value).click()

    @teststep
    def first_item(self):
        """第一个元素 index = 1"""
        ele = self.driver.find_elements_by_xpath("//android.widget.TextView")[1]
        if GetAttribute().resource_id(ele) == gv.PACKAGE_ID + 'name':
            return True
        else:
            return False

    # 积分排行榜
    @teststeps
    def wait_check_score_page(self):
        """以“title:积分排行榜”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'积分排行榜')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_tab_list_page(self):
        """以“积分/星星排行榜”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_student_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def this_week_tab(self):
        """本周 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'本周')]")
        return ele

    @teststep
    def last_week_tab(self):
        """上周"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'上周')]")
        return ele

    @teststep
    def this_month_tab(self):
        """本月 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'本月')]")
        return ele

    @teststep
    def all_tab(self):
        """全部"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'全部')]")
        return ele

    @teststep
    def st_order(self):
        """排序"""
        ele = self.driver \
            .find_elements_by_id(self.st_order_value)
        return ele

    @teststep
    def st_icon(self):
        """头像"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_student_icon")
        return ele

    @teststep
    def st_name(self):
        """学生 昵称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_student_name")
        return ele

    @teststep
    def num(self):
        """积分/星星数目"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_nums")
        return ele

    # 星星排行榜
    @teststeps
    def wait_check_star_page(self):
        """以“title:星星排行榜”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'星星排行榜')]")
        return self.wait.wait_check_element(locator)

    # 入班申请
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生头像”为依据"""
        locator = (By.ID, self.st_icon_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def icon(self):
        """头像"""
        ele = self.driver \
            .find_elements_by_id(self.st_icon_value)
        return ele

    @teststep
    def st_nick(self):
        """学生 昵称"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "title")
        return item

    @teststep
    def st_remark(self):
        """学生 备注名"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "sub_title")
        return item

    @teststep
    def agree_button(self):
        """同意 按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "agree")
        return ele

    @teststep
    def open_menu(self, ele):
        """学生条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(500).release().perform()

    @teststep
    def menu_item(self, index):
        """学生条目 左键长按菜单"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "md_title")[index] \
            .click()

    @teststeps
    def button_enabled_judge(self, length, button, size, max=10):
        """按钮enabled状态 与 字符数
        :param length:展示的字符数
        :param button:按钮
        :param size:实际输入的字符数
        """
        if 0 < length <= max:
            if length != int(size):
                print('★★★ Error- 字符数展示有误', length, size)
            else:
                if self.get.enabled(button) == 'false':
                    print('★★★ Error- 确定按钮不可点击')
        elif length == 0:
            if length != int(size):
                print('★★★ Error- 字符数展示有误', length, size)
            else:
                if self.get.enabled(button) == 'true':
                    print('★★★ Error- 确定按钮未置灰可点击')
        elif length > max:
            if length != int(size):
                print('★★★ Error- 字符数展示有误', length, size)
            else:
                if self.get.enabled(button) == 'true':
                    print('★★★ Error- 确定按钮未置灰可点击')
        return self.get.enabled(button)

    @teststep
    def into_operation(self, var, check):
        """进入列表中 某个口语/作业/卷子 具体操作
        :param var:作业包name
        :param check: 页面检查点
        """
        while True:
            name = self.hw_name()  # 口语作业包 name
            if len(name) == 10:
                count = len(name) - 1
            else:
                count = len(name)

            index = []
            for i in range(count):
                if name[i].text == var:
                    index.append(i)
                    break
            if len(index) == 1:
                name[index[0]].click()  # 进入作业
                break
            else:
                if self.wait_check_page(check):  # 页面检查点
                    SwipeFun().swipe_vertical(0.5, 0.75, 0.25)
