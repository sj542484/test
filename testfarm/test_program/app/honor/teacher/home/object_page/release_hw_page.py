#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.utils.get_element_bounds import Element
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.utils.wait_element import WaitElement


class ReleasePage(BasePage):
    """ 发布作业 页面"""

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
    def wait_check_release_list_page(self):
        """以“”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "class_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def hw_title(self):
        """作业名称"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "hw_title").text
        return item

    @teststep
    def hw_name_edit(self):
        """作业名称 编辑框"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "hw_name")
        return item

    @teststep
    def hw_list(self):
        """题目列表"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'题目列表')]").text
        return item

    @teststep
    def hw_list_tips(self):
        """题目列表 -调整题目顺序"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'调整题目顺序')]").text
        return item

    @teststep
    def adjust_order_button(self):
        """进入 题目顺序调整 页面"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "bank") \
            .click()

    @teststep
    def hw_mode_title(self):
        """作业模式"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "hw_mode_title").text
        print(item)
        return item

    @teststep
    def hw_mode_free(self):
        """作业模式 - 自由模式"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "free")
        return item

    @teststep
    def hw_mode_reach(self):
        """作业模式 - 达标模式"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "reach")
        return item

    @teststep
    def hw_mode_tips(self):
        """达标 提示"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").text
        return item

    # 定时作业
    @teststep
    def timing_check_box(self):
        """定时勾选框"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "is_need_time")
        return ele

    @teststep
    def timing_title(self):
        """title:指定时间"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'指定时间')]").text
        print(item)

    @teststep
    def timing_show(self):
        """指定时间 展示text"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "send_time")
        return item

    @teststep
    def help_button(self):
        """指定时间 展示text"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "time_question").click()

    # 选择时间
    @teststeps
    def wait_check_time_list_page(self):
        """以“确定 按钮”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "confirm")
        return self.wait.wait_check_element(locator)

    @teststep
    def number_input(self):
        """选择 时间"""
        ele = self.driver \
            .find_elements_by_id("android:id/numberpicker_input")
        return ele

    @teststep
    def get_assign_date(self, index=2):
        """调整发布时间"""
        ele = self.number_input()  # 获取当前展示的时间
        loc = Element().get_element_bounds(ele[index])
        self.driver.swipe(loc[2], loc[3], loc[2], loc[3]-200, 1000)  # 调整发布时间

        if self.wait_check_time_list_page():
            item = self.number_input()  # 获取当前展示的时间
            content = []
            for i in range(len(item)):
                content.append(item[i].text)

            if int(content[1]) < 10:
                content[1] = '0' + content[1]

            return content

    @teststep
    def cancel_button(self):
        """取消按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "cancel") \
            .click()

    # 班级列表
    @teststep
    def publish_hw(self):
        """发布作业 title"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'发布作业')]").text
        print(item)

    @teststep
    def choose_button(self):
        """班级 单选框"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "choose")
        return ele

    @teststep
    def van_name(self):
        """班级 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "class_name")
        return ele

    @teststep
    def choose_count(self):
        """班级 描述"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "choose_count")
        return ele

    @teststep
    def assign_button(self):
        """发布作业 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_first") \
            .click()

    def swipe_operation(self, content):
        """获取整个班级列表"""

    # 班级页面 学生list
    @teststeps
    def wait_check_st_list_page(self, var=20):
        """以“学生头像”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "head")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def st_title(self):
        """学生title"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "title")
        return item

    @teststep
    def st_phone(self):
        """学生title"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "sub_title")
        return item

    @teststep
    def st_tag(self):
        """"""
        ele = self.driver.find_elements_by_id(gv.PACKAGE_ID + 'tags')
        return ele

    # 调整题目顺序
    @teststeps
    def wait_check_adjust_page(self):
        """以“title:题目列表”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题目列表')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def confirm_button(self):
        """确定按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "confirm").click()

    @teststep
    def game_type(self):
        """游戏类型"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type")
        return ele

    @teststep
    def game_name(self):
        """游戏 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        return ele

    @teststep
    def drag_icon(self):
        """拖拽 icon"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_drag_icon")
        return ele

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
            print('------------------------------------------', '\n',
                  '温馨提示 页面:')
            self.home.tips_title()
            self.home.tips_content()
            self.home.never_notify()  # 不再提醒
            self.home.cancel_button()  # 取消按钮

            self.assign_button()  # 发布作业 按钮
            time.sleep(1)
            self.home.commit_button()  # 确定按钮

    @teststeps
    def hw_mode_operation(self, var='reach'):
        """发布作业 - 作业模式"""
        self.hw_mode_title()  # 作业模式

        free = self.hw_mode_free()  # 自由模式
        reach = self.hw_mode_reach()  # 达标模式
        print('  ', free.text, reach.text, self.hw_mode_tips())
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
        loc = Element().get_element_location(button[-1])  # 获取当前页面中最后一个单选框坐标
        self.driver.swipe(loc[0], loc[1], loc[0], 100, 1000)

        van = self.van_name()  # 班级 元素
        button = self.choose_button()  # 单选 按钮
        count = self.choose_count()  # 班级描述

        vanclass = []  # 班级名
        if len(button) != len(van):
            print('★★★ Error- 单选框的个数与班级个数不同', len(button), len(van))
        else:
            for i in range(len(count)):
                print('-------')
                print(van[i].text, '\n', count[i].text)
                vanclass.append(van[i].text)

        # loc1 = self.get_element_location(button[0])  # 获取当前页面中最后一个单选框坐标
        # self.driver.swipe(loc1[0], loc1[1], loc1[0], loc[1], 1000)
        return van, vanclass

    @teststeps
    def choose_class_operation(self):
        """选择班级 学生"""
        if self.wait_check_release_list_page():
            print('----------------------------')
            button = self.choose_button()  # 单选框
            van = self.van_name()  # 班级 元素

            cancel = 0
            count = 0
            for i in range(len(button)):
                if GetAttribute().selected(button[i]) == 'true':
                    cancel = van[i].text
                    count = i
                    print('取消选择班级:', cancel)
                    button[i].click()  # 取消选择 一个班
                    break

            choose = 0
            for k in range(len(button)):
                if GetAttribute().selected(button[k]) == 'false' and k != count:
                    print('所选择的班级:', van[k].text)
                    choose = van[k].text
                    button[k].click()  # 选择 一个班
                    van[k].click()  # 进入该班级

                    if self.wait_check_vanclass_page(choose):
                        if self.wait_check_st_list_page():
                            st = self.st_title()  # 学生
                            phone = self.st_phone()  # 手机号
                            for i in range(len(phone)):
                                print('  ', st[i].text, phone[i].text)
                            print('------------------')

                            if len(phone)>1:
                                button = self.choose_button()
                                print('  取消选择学生:', phone[0].text)
                                button[0].click()  # 取消选择一个学生

                                self.confirm_button()  # 确定按钮
                            elif len(phone) == 1:
                                self.confirm_button()  # 确定按钮
                                if  Toast().find_toast('还未选择学生！'):
                                    print('还未选择学生！')
                                    button[0].click()  # 选择一个学生

                                self.confirm_button()  # 确定按钮
                        elif self.home.wait_check_empty_tips_page():
                            print('  本班级 暂无学生')
                            self.home.back_up_button()  # 返回 编辑 页面

                        print('-----------------------------')
                    break

            if self.wait_check_release_list_page():
                SwipeFun().swipe_vertical(0.5, 0.2, 0.9)

            return choose, cancel

    @teststeps
    def hw_adjust_order(self):
        """发布作业 - 调整题目顺序"""
        print('---------------调整题目顺序-------------')
        self.adjust_order_button()  # 调整题目顺序 按钮
        self.home.tips_content_commit()  # 提示框

        if self.wait_check_adjust_page():  # 页面检查点
            mode = self.game_type()  # 游戏类型
            name = self.game_name()  # 游戏name

            content = []
            icon = self.drag_icon()  # 拖拽 icon
            if len(mode) > 5:  # 多于5个
                for i in range(len(mode) - 1):
                    print(mode[i].text, name[i].text)
                    content.append(mode[i].text)
                    content.append(name[i].text)
                self.drag_ele_operation(icon[1], icon[5])  # 向下拖拽
                time.sleep(2)
                self.drag_ele_operation(icon[4], icon[1])  # 向上拖拽

                self.judge_hw_adjust(content)  # 判断 调整题目顺序
            elif 2 < len(mode) < 6:
                for i in range(len(mode)):
                    print(mode[i].text, name[i].text)
                    content.append(mode[i].text)
                    content.append(name[i].text)
                self.drag_ele_operation(icon[0], icon[len(mode) - 1])  # 向下拖拽
                time.sleep(2)
                self.drag_ele_operation(icon[len(mode) - 2], icon[0])  # 向上拖拽

                self.judge_hw_adjust(content)  # 判断 调整题目顺序
            else:  # 1个
                print('只有%s道大题' % len(mode))

        print('----------------------------------------------------')
        self.confirm_button()  # 确定按钮

    @teststeps
    def judge_hw_adjust(self, var):
        """判断 调整题目顺序"""
        print('---------------验证 调整题目顺序---------------')
        mode = self.game_type()  # 游戏类型
        name = self.game_name()  # 游戏name

        content = []
        if len(mode) > 5:
            for i in range(len(mode) - 1):
                content.append(mode[i].text)
                content.append(name[i].text)
        elif 2 < len(mode) < 6:
            for i in range(len(mode)):
                content.append(mode[i].text)
                content.append(name[i].text)
        else:
            for i in range(len(mode)):
                content.append(mode[i].text)
                content.append(name[i].text)

        count = 0
        for j in range(len(content)):
            if content[j] != var[j]:
                count += 1

        if count == 0:
            print('★★★ Error- 题目顺序未调整', '\n',
                  '----------------------------')

    @teststeps
    def drag_ele_operation(self, origin, destination):
        """拖拽元素"""
        orig_x = origin.location['x']
        orig_y = origin.location['y']
        dest_x = destination.location['x']
        dest_y = destination.location['y']+50

        TouchAction(self.driver).long_press(x=orig_x, y=orig_y)\
            .move_to(x=dest_x, y=dest_y).release().perform()
