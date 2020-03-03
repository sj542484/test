#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class VanMemberPage(BasePage):
    """ 班级成员 详情页面"""
    no_st_info_value = gv.PACKAGE_ID + "no_result"  # 没有匹配到学生
    search_input_value = gv.PACKAGE_ID + "input"  # 搜索输入框 元素

    game_type_value = gv.PACKAGE_ID + 'type'  # 小游戏类型  详情页
    member_tips = '★★★ Error- 未进入班级成员页'
    member_list_tips = '★★★ Error- 班级成员页无成员'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var):
        """以“title: 班级名称/ 作业名称/本班卷子/口语作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_st_list_page(self, var=10):
        """以“学生头像”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "head")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def open_menu(self, ele):
        """学生条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(1000).release().perform()

    @teststep
    def menu_item(self, index):
        """学生条目 左键长按菜单"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "md_title")[index] \
            .click()

    # 分组
    @teststeps
    def group_judge(self):
        """判断是否有小组"""
        locator = (By.ID, gv.PACKAGE_ID + "group_name")
        return self.wait.judge_is_exists(locator)

    @teststeps
    def group_hint(self):
        """小组列表(长按可进行更多操作)"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "hint")[0].text
        print(item)

    @teststeps
    def group_icon(self):
        """小组icon"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "hint")
        return item

    @teststeps
    def group_name(self):
        """小组名"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "group_name")
        return item

    @teststep
    def st_count(self):
        """学生 人数"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "group_num")
        return ele

    # 学生列表
    @teststeps
    def st_hint(self):
        """3人/2人 “提分版” /0人已购买(长按可进行更多操作)"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "hint")
        print(item[-1].text)

    @teststep
    def st_icon(self):
        """学生icon"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "head")
        return item

    @teststep
    def st_remark(self):
        """学生 备注名"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "title")
        return item

    @teststep
    def st_phone(self):
        """学生phone"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "sub_title")
        return item

    @teststep
    def st_tags(self):
        """学生 tags"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tags")
        return item

    @teststep
    def st_vip_expired(self):
        """学生 会员到期信息"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "vip_expired")
        return item

    @teststep
    def open_menu(self, ele):
        """学生条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(1000).release().perform()

    @teststep
    def menu_item(self, index):
        """学生条目 左键长按菜单"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "md_title")[index] \
            .click()

    @teststep
    def search_button(self):
        """搜索 button"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "search") \
            .click()

    @teststep
    def add_group_button(self):
        """以“创建小组 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "create_group") \
            .click()

    # 搜索界面
    @teststeps
    def wait_check_search_page(self):
        """以“搜索 输入框 元素”为依据"""
        locator = (By.ID, self.search_input_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def search_input(self):
        """搜索 输入框"""
        ele = self.driver \
            .find_element_by_id(self.search_input_value)
        return ele

    @teststep
    def input_clear_button(self):
        """清除 搜索信息button"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "input_clear") \
            .click()

    @teststep
    def wait_check_empty_page(self, var=10):
        """没有匹配到学生"""
        locator = (By.ID, self.no_st_info_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def no_st_info(self):
        """没有匹配到学生"""
        ele = self.driver \
            .find_element_by_id(self.no_st_info_value)
        print(ele.text)

    # 小组 详情页面
    @teststep
    def add_st_button(self):
        """加 学生button"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "add_student")\
            .click()

    # 添加学生页面
    @teststep
    def choose_button(self):
        """单选框"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "choose")
        return ele

    @teststep
    def confirm_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "confirm") \
            .click()

    @teststeps
    def judge_phone_digit(self, var):
        """验证 手机号格式 中间4位不显示成*  -- 根据校长端设置！！！"""
        if not self.is_digit(var):
            print('★★★ Error- 不为数字：', var)

    # 学生个人答题情况页 特有元素
    @teststeps
    def wait_check_per_detail_page(self, var=20):
        """以“最优成绩 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_testbank_status")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def per_game_item(self):
        """个人答题情况页面 -游戏 条目
        :returns:  游戏类型 & 页面内所有game
        """
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/"
                                    "child::*/android.widget.TextView")

        count = []  # 每个游戏条目第一个元素为游戏类型
        var = []  # 游戏类型
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:
                count.append(i)
                var.append(ele[i])
        count.append(len(ele))

        content = []  # 页面内所有game
        for j in range(len(count) - 1):
            item = [ele[k].text for k in range(count[j], count[j + 1]) if ele[k].text != '']  # 每一个game
            content.append(item)
        return var, content

    @teststep
    def game_type(self):
        """游戏类型"""
        ele = self.driver \
            .find_elements_by_id(self.game_type_value)
        return ele

    @teststep
    def game_name(self):
        """游戏 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        return ele

    @teststep
    def optimal_achievement(self):
        """最优成绩-"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_testbank_status")
        return ele

    @teststep
    def first_achievement(self):
        """首次成绩-"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_spend_time")
        return ele

    @teststeps
    def judge_phone(self, phone):
        """验证 手机号格式 （中间4位显示成*）-- 根据校长端设置！！！"""
        var = phone[:3] + phone[7:]

        if not self.is_digit(var):
            print('★★★ Error- 其他部分不为数字：', phone)
        if phone[3:7] != '****':
            print('★★★ Error- 中间4位未显示成*：', phone)

    @teststeps
    def is_digit(self, var):
        """ 判断 是否为数字"""
        try:
            var = int(var)
            return isinstance(var, int)
        except ValueError:
            return False
