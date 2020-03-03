#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.assert_package import MyAssert, MyToast
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import ElementBounds
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class ReleasePage(BasePage):
    """ 发布作业 页面"""
    add_time_locator = (By.ID, gv.PACKAGE_ID + "add_time")  # 设定时间 按钮

    release_tips = '★★★ Error- 未进入发布界面'
    release_list_tips = '★★★ Error- 发布界面未加载成功'
    choose_time_tips = '★★★ Error- 未进入选择时间界面'

    def __init__(self):
        self.home = ThomePage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_release_page(self):
        """以“title:发布作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'发布作业')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_release_list_page(self, var=15):
        """以“”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "class_name")
        return self.wait.wait_check_list_element(locator, var)

    @teststep
    def hw_title(self):
        """作业名称"""
        locator = (By.ID, gv.PACKAGE_ID + "hw_title")
        item = self.wait\
            .wait_find_element(locator).text
        return item

    @teststep
    def hw_name_edit(self):
        """作业名称 编辑框"""
        locator = (By.ID, gv.PACKAGE_ID + "hw_name")
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def hw_list(self):
        """题目列表"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题目列表')]")
        return self.wait \
            .wait_find_element(locator).text

    @teststep
    def hw_list_tips(self):
        """题目列表 -调整题目顺序"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'调整题目顺序')]")
        return self.wait \
            .wait_find_element(locator).text

    @teststep
    def adjust_order_button(self):
        """进入 题目顺序调整 页面"""
        locator = (By.ID, gv.PACKAGE_ID + "bank")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def hw_mode_title(self):
        """作业模式"""
        locator = (By.ID, gv.PACKAGE_ID + "hw_mode_title")
        ele = self.wait \
            .wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def hw_mode_free(self):
        """作业模式 - 自由模式"""
        locator = (By.ID, gv.PACKAGE_ID + "free")
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def hw_mode_reach(self):
        """作业模式 - 达标模式"""
        locator = (By.ID, gv.PACKAGE_ID + "reach")
        return self.wait \
            .wait_find_element(locator)

    @teststep
    def hw_mode_tips(self):
        """达标 提示"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@index,2)]")
        return self.wait \
            .wait_find_element(locator).text

    # 定时作业
    @teststeps
    def timing_show(self):
        """时间展示元素"""
        locator = (By.ID, gv.PACKAGE_ID + "send_time")
        return self.wait\
            .wait_find_elements(locator)

    @teststep
    def add_time_button(self):
        """设定时间 按钮"""
        self.wait \
            .wait_find_element(self.add_time_locator).click()

    @teststep
    def judge_not_add_time_button(self):
        """判断 没有 设定时间 按钮"""
        return self.wait\
            .judge_is_exists(self.add_time_locator)

    @teststep
    def delete_time_button(self):
        """ '删除时间 按钮 """
        locator = (By.ID, gv.PACKAGE_ID + "delete_time")
        return self.wait.wait_find_elements(locator)

    @teststep
    def hint_help_button(self):
        """ '定时作业tips' + 按钮 ？"""
        locator = (By.ID, gv.PACKAGE_ID + "send_time_hint")
        self.wait \
            .wait_find_element(locator).click()

    # 选择时间
    @teststeps
    def wait_check_time_list_page(self):
        """以“确定 按钮”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "confirm")
        return self.wait.wait_check_element(locator)

    @teststep
    def number_input(self):
        """选择 时间 eg:'09月26日 周四', '17', '42'  三个元素"""
        locator = (By.ID, "android:id/numberpicker_input")
        return self.wait.wait_find_elements(locator)

    @teststep
    def cancel_button(self):
        """取消按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "cancel")
        self.wait.wait_find_element(locator) \
            .click()

    # 班级列表
    @teststep
    def publish_hw(self):
        """发布作业 title"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'发布作业')]")
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def choose_button(self):
        """班级 单选框"""
        locator = (By.ID, gv.PACKAGE_ID + "choose")
        return self.wait.wait_find_elements(locator)

    @teststep
    def van_name(self):
        """班级 名称"""
        locator = (By.ID, gv.PACKAGE_ID + "class_name")
        return self.wait.wait_find_elements(locator)

    @teststep
    def choose_count(self):
        """班级 描述"""
        locator = (By.ID, gv.PACKAGE_ID + "choose_count")
        return self.wait.wait_find_elements(locator)

    @teststep
    def assign_button(self):
        """发布作业 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "action_first")
        self.wait.wait_find_element(locator).click()

    # 班级页面 学生list
    @teststeps
    def wait_check_st_list_page(self, var=20):
        """以“学生头像”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "head")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def st_title(self):
        """学生title"""
        locator = (By.ID, gv.PACKAGE_ID + "title")
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_phone(self):
        """学生title"""
        locator = (By.ID, gv.PACKAGE_ID + "sub_title")
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_tag(self):
        """"""
        locator = (By.ID, gv.PACKAGE_ID + "tags")
        return self.wait.wait_find_elements(locator)

    # 调整题目顺序
    @teststeps
    def wait_check_adjust_page(self):
        """以“title:题目列表”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题目列表')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def confirm_button(self):
        """确定按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "confirm")
        self.wait.wait_find_element(locator).click()

    @teststep
    def game_type(self):
        """游戏类型"""
        locator = (By.ID, gv.PACKAGE_ID + "type")
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_name(self):
        """游戏 名称"""
        locator = (By.ID, gv.PACKAGE_ID + "test_bank_name")
        return self.wait.wait_find_elements(locator)

    @teststep
    def drag_icon(self):
        """拖拽 icon"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_drag_icon")
        return self.wait.wait_find_elements(locator)

    # 班级 学生列表
    @teststeps
    def wait_check_vanclass_page(self, var):
        """以“title:班级名称”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def tips_page_info(self):
        """温馨提示 页面信息  -- 有 不再提醒 元素"""
        if self.home.wait_check_tips_page():
            print('------------------------------------------')
            self.home.tips_title()
            self.home.tips_content()
            self.home.never_notify()  # 不再提醒
            self.cancel_button()  # 取消按钮

            MyAssert().assertTrue_new(self.wait_check_release_list_page(), '★★★ Error- 编辑/发布页未加载成功')
            self.assign_button()  # 发布作业 按钮
            if self.home.wait_check_tips_page():
                self.home.commit_button().click()  # 确定按钮

    @teststeps
    def hw_mode_operation(self, var='reach'):
        """发布作业 - 作业模式"""
        self.hw_mode_title()  # 作业模式

        free = self.hw_mode_free()  # 自由模式
        reach = self.hw_mode_reach()  # 达标模式
        reach_tips = self.hw_mode_tips()
        if all([free.text == '自由模式', reach.text == '达标模式', reach_tips == '(默认达标标准为80%)']):
            print('  ', free.text, reach.text, reach_tips)
        else:
            print('★★★ Error- 作业模式展示有误', free.text, reach.text, reach_tips)

        if self.get.checked(free) is False:
            print('★★★ Error- 默认选择的作业模式有误')
        else:
            if var == 'reach':
                reach.click()  # 选择达标模式
                if self.get.checked(reach) is False:
                    print('★★★ Error- 作业模式 checked属性有误')
            else:
                free.click()  # 选择达标模式
                if self.get.checked(free) is False:
                    print('★★★ Error- 作业模式 checked属性有误')
        print('----------------------------')

        return free, reach

    @teststeps
    def hw_vanclass_list(self):
        """发布作业 - 班级列表"""
        self.publish_hw()  # 打印元素 发布作业到

        button = self.choose_button()  # 班级单选框
        loc = ElementBounds().get_element_location(button[-1])  # 获取当前页面中最后一个单选框坐标
        self.driver.swipe(loc[0], loc[1], loc[0], 100, 1000)

        van = self.van_name()  # 班级 元素
        button = self.choose_button()  # 单选 按钮
        count = self.choose_count()  # 班级描述

        vanclass = []  # 班级名
        if len(button) != len(van):
            print('★★★ Error- 单选框的个数与班级个数不同', len(button), len(van))
        else:
            print('班级列表')
            vanclass.append(van[i].text for i in range(len(count)))

        return van, vanclass

    @teststeps
    def choose_class_operation(self):
        """选择班级 学生"""
        MyAssert().assertTrue_new(self.wait_check_release_list_page(), '★★★ Error- 编辑/发布页未加载成功')
        print('----------------------------')
        button = self.choose_button()  # 单选框
        van = self.van_name()  # 班级 元素

        cancel = 0
        index = 0
        for i in range(len(button)):
            if GetAttribute().selected(button[i]) == 'true':
                cancel = van[i].text
                index = i
                print('取消选择班级:', cancel)
                button[i].click()  # 取消选择 一个班
                print('-----------')
                break

        choose = 0
        count = 0
        for k in range(len(button)):
            if all([GetAttribute().selected(button[k]) == 'false',
                    k != index, van[k].text != GetVariable().VANCLASS]):
                count += 1
                print('所选择的班级:', van[k].text)
                choose = van[k].text
                button[k].click()  # 选择 一个班
                van[k].click()  # 进入该班级

                if self.home.wait_check_empty_tips_page():
                    print('  本班级 暂无学生')
                    self.home.back_up_button()  # 返回 编辑 页面
                elif self.wait_check_vanclass_page(choose):
                    if self.wait_check_st_list_page():
                        st = self.st_title()  # 学生
                        phone = self.st_phone()  # 手机号
                        for i in range(len(phone)):
                            print('  ', st[i].text, phone[i].text)
                        print('------------------')

                        print('  取消选择学生:', phone[0].text)
                        self.choose_button()[0].click()  # 取消选择一个学生

                        if self.wait_check_st_list_page():
                            if len(phone) == 1:
                                self.confirm_button()  # 确定按钮
                                Toast().toast_operation('还未选择学生!')
                                self.choose_button()[0].click()  # 选择一个学生

                        if self.wait_check_st_list_page():
                            self.confirm_button()  # 确定按钮

                print('-----------------------------')
                break

        if count == 0:
            print('暂无可选择班级')

        if self.wait_check_release_list_page():
            SwipeFun().swipe_vertical(0.5, 0.2, 0.9)

        return choose, cancel

    @teststeps
    def hw_adjust_order(self):
        """发布作业 - 调整题目顺序"""
        print('---------------调整题目顺序-------------')
        self.adjust_order_button()  # 调整题目顺序 按钮
        self.home.tips_content_commit()  # 提示框

        MyAssert().assertTrue_new(self.wait_check_adjust_page(), '★★★ Error- 未进入 调整题目顺序界面')
        mode = self.game_type()  # 游戏类型
        name = self.game_name()  # 游戏name

        content = []
        icon = self.drag_icon()  # 拖拽 icon
        if len(mode) > 5:  # 多于5个
            self.game_list_drop(name, mode, icon, len(mode)-1, content)  # 游戏列表
        elif 2 < len(mode) < 6:
            self.game_list_drop(name, mode, icon, len(mode), content)  # 游戏列表
        else:  # 1个
            print('只有%s道大题' % len(mode))

        if content:
            self.judge_hw_adjust(content)  # 判断 调整题目顺序

        print('----------------------------------------------------')
        self.confirm_button()  # 确定按钮

    @teststeps
    def game_list_drop(self, name, mode, icon, length, content):
        """调整题目页面 游戏列表"""
        for i in range(length):
            print(mode[i].text, name[i].text)
            content.append(mode[i].text)
            content.append(name[i].text)

        self.drag_ele_operation(icon[0], icon[-2])  # 向下拖拽
        MyAssert().assertTrue_new(self.wait_check_adjust_page(), '★★★ Error- 未进入 调整题目顺序界面')
        icon = self.drag_icon()  # 拖拽 icon
        self.drag_ele_operation(icon[-1], icon[1], 'up')  # 向上拖拽

    @teststeps
    def judge_hw_adjust(self, var):
        """判断 调整题目顺序"""
        print('---------------验证 调整题目顺序---------------')
        mode = self.game_type()  # 游戏类型
        name = self.game_name()  # 游戏name

        content = []
        length = (len(mode)-1 if len(mode) > 5 else len(mode))

        for i in range(length):
            content.append(mode[i].text)
            content.append(name[i].text)

        count = 0
        for j in range(len(content)):
            if content[j] != var[j]:
                count += 1

        print('★★★ Error- 题目顺序未调整\n{}'.format('-'*15) if count == 0
              else '题目顺序已调整')

    @teststeps
    def drag_ele_operation(self, origin, destination, dire='down'):
        """拖拽元素
        :param dire: 拖拽方向
        :param origin: 起始
        :param destination: 目标"""
        dest_x = destination.location['x']
        dest_y = (destination.location['y']+50 if dire == 'down' else destination.location['y']-50)

        TouchAction(self.driver).long_press(origin)\
            .move_to(x=dest_x, y=dest_y).release().perform()

    @teststeps
    def get_assign_date(self, index=2, direction='up'):
        """调整发布时间"""
        ele = self.number_input()  # 获取当前展示的时间  3个可调元素
        loc = ElementBounds().get_element_bounds(ele[index])
        y_loc = (loc[3] + 20 if direction == 'down' else loc[3] - 20)

        while True:
            self.driver.swipe(loc[2], loc[3], loc[2], y_loc, 1000)  # 调整发布时间
            if index == 0:
                break
            else:
                index -= 1

        MyAssert().assertTrue_new(self.wait_check_time_list_page(), self.choose_time_tips)
        item = self.number_input()  # 获取当前展示的时间
        date = []  # 时间列表 length=3
        for i in range(len(item)):
            if i == 0:
                z = item[i].text.split('月')
                month = re.sub('\D', '', z[0])
                day = re.sub('\D', '', z[1])
                date.extend([month, day])
            else:
                var = item[i].text
                if len(item[i].text) == 1:
                    var = '0' + item[i].text
                date.append(var)
        return date

    @teststeps
    def republish_operation(self):
        """与当天布置的作业有重名"""
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        SwipeFun().swipe_vertical(0.5, 0.2, 0.9)
        MyAssert().assertTrue_new(self.wait_check_release_list_page(), '★★★ Error- 编辑作业 详情页未加载成功')

        title = '定时作业发布' + str(random.randint(1000, 9999))
        self.hw_name_edit().send_keys(title)  # name
        self.assign_button()  # 点击 发布作业 按钮
        MyToast().toast_assert(self.name, Toast().toast_operation(TipsData().hw_success))

        return title
