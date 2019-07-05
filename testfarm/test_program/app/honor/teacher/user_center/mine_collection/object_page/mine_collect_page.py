#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class CollectionPage(BasePage):
    """我的收藏 页面"""
    def __init__(self):
        self.filter = FilterPage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:我的收藏”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的收藏')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“存在 我的收藏列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator)

    @teststep
    def filter_button(self):
        """以“筛选 按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "filter") \
            .click()

    @teststep
    def more_button(self):
        """以“更多 按钮”的class name为依据"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView") \
            .click()

    @teststep
    def label_manage_button(self):
        """以“标签管理 按钮”的class name为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'标签管理')]") \
            .click()

    @teststep
    def the_end(self):
        """以“没有更多了”的text为依据"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'没有更多了')]") \
            .text
        return item

    @teststep
    def question_basket(self):
        """以 右下角“题筐 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_pool") \
            .click()

    @teststep
    def menu_button(self, index):
        """以 条目右侧“菜单按钮”的id为依据"""
        self.driver\
            .find_elements_by_id(gv.PACKAGE_ID + "iv_eg")[index] \
            .click()
        time.sleep(1)

    # 标签管理
    @teststeps
    def wait_check_manage_page(self):
        """以“title:标签管理”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'标签管理')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_manage_list_page(self):
        """以“”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_label_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def label_title(self):
        """label title"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")
        return item

    @teststep
    def label_name(self):
        """以“标签 name”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")
        # for i in range(len(ele)):
        #     print(ele[i].text)
        return ele

    @teststep
    def open_menu(self, ele):
        """标签条目 左键长按"""
        TouchAction(self.driver).long_press(ele).wait(500).release().perform()

    @teststep
    def menu_item(self, index):
        """标签条目 左键长按菜单"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "md_title")[index] \
            .click()

    # 菜单 内容  # 检查点：home_page.py的 wait_check_tips_page()
    @teststep
    def put_to_basket(self):
        """以 菜单- 加入题筐 的text为依据"""
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'加入题筐')]") \
            .click()

    @teststep
    def stick_label(self):
        """以 菜单- 贴标签 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'贴标签')]") \
            .click()

    @teststep
    def recommend_to_school(self):
        """以 菜单- 推荐到学校 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'推荐到学校')]") \
            .click()

    @teststep
    def cancel_collection(self):
        """以 菜单- 取消收藏 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消收藏')]") \
            .click()

    # 贴标签
    @teststeps
    def wait_check_label_page(self):
        """以“title:贴标签”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'贴标签')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def save_button(self):
        """以 贴标签 - 保存按钮 的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "certain") \
            .click()

    @teststep
    def check_box(self, index):
        """以 贴标签 - 单选框 的id为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "cb_checked")[index] \
            .click()

    @teststep
    def add_label(self):
        """以 贴标签 - 创建标签 的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fb_add_label") \
            .click()

    # 筛选
    @teststep
    def question_menu(self):
        """以“题单”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[0]
        return ele

    @teststep
    def click_question_menu(self):
        """以“题单”的text为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[0] \
            .click()

    @teststep
    def game_list(self):
        """以“大题”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[1]
        return ele

    @teststep
    def click_game_list(self):
        """以“大题”的text为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[1] \
            .click()

    @teststep
    def test_paper(self):
        """以“试卷”的text为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[2]
        return ele

    @teststep
    def click_test_paper(self):
        """以“试卷”的text为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_label_name")[2] \
            .click()

    @teststeps
    def filter_all_element(self):
        """页面内所有label元素"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/android.support.v7.widget.RecyclerView"
                                    "/android.widget.LinearLayout"
                                    "/descendant::*/android.widget.TextView")
        return ele

    @teststeps
    def filter_operation(self, var):
        """所有label title+小标签"""
        ele = self.filter_all_element()  # 所有元素

        content = []  # 所有元素
        item = []  # 翻页前最后元素
        for i in range(len(ele)):
            item.append(ele[-1].text)
            content.append(ele[i].text)

        SwipeFun().swipe_vertical(0.5, 0.7, 0.2)
        if self.wait_check_page():
            ele = self.filter_all_element()  # 所有元素

            index = 0
            for i in range(len(ele)):
                if ele[i].text == item[0]:
                    index = i + 1
                    break

            for j in range(index, len(ele)):
                content.append(ele[j].text)

        self.label_content(var, content)  # print所有元素

    @teststeps
    def label_content(self, var, content):
        """筛选 每个标题下的所有label"""
        count = []
        if var == 2:  # 试卷
            for i in range(len(content)):
                if content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '自定义标签':  # 我的收藏/推荐
                    count.append(i)
                    break
        elif var == 3:  # 题单
            for i in range(len(content)):
                if content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '自定义标签':  # 我的收藏/推荐
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                    break
        elif var == 4:  # 大题
            for i in range(len(content)):
                if content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '自定义标签':  # 我的收藏/推荐
                    count.append(i)
                elif content[i] == '活动类型':
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                    break

        count.append(len(content))
        for i in range(len(count)):  # print 所有元素
            if i + 1 == len(count):
                print('---------------------')
                for j in range(count[i], count[-1]):
                    print(content[j])
            else:
                print('---------------------')
                for j in range(count[i], count[i + 1]):
                    print(content[j])
        return count

    @teststeps
    def source_type_selected(self):
        """选中的资源类型"""
        if self.get.selected(self.question_menu()) == 'true':  # 题单
            print('======================选择题单======================')
            self.filter_operation(3)  # 所有label title+小标签
        else:
            if self.get.selected(self.game_list()) == 'true':  # 大题
                print('======================选择大题======================')
                self.filter_operation(4)  # 所有label title+小标签
            else:
                if self.get.selected(self.test_paper()) == 'true':  # 试卷
                    print('======================选择试卷======================')
                    self.filter_operation(2)  # 所有label title+小标签
        print('============================================')

    @teststeps
    def verify_collect_result(self, menu, var='题单'):
        """验证 添加收藏 结果"""
        if TestBankPage().wait_check_page(var):
            ThomePage().click_tab_profile()  # 个人中心
            if TuserCenterPage().wait_check_page():

                TuserCenterPage().click_mine_collection()  # 我的收藏
                if self.wait_check_page():
                    print('---------------验证 -收藏结果------------------')
                    if var == '大题':
                        self.filter_button()  # 筛选按钮
                        if FilterPage().wait_check_page():
                            self.click_game_list()  # 点击大题
                            FilterPage().commit_button()  # 确定按钮
                    elif var == '试卷':
                        self.filter_button()  # 筛选按钮
                        if FilterPage().wait_check_page():
                            self.click_test_paper()  # 点击试卷
                            FilterPage().commit_button()  # 确定按钮

                    if self.wait_check_page():
                        if self.wait_check_list_page():
                            item = TestBankPage().question_name()  # 获取
                            menu1 = item[1][0]
                            if '提分' in menu:
                                menu = menu[:-2]
                            if menu != menu1:
                                print('★★★ Error- 加入收藏失败', menu, menu1)
                            else:
                                print('加入收藏成功')
                                print('----------------')
                                for z in range(len(item[0])):
                                    print(item[1][z])
                                    if self.wait_check_page():
                                        self.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入收藏的题单取消收藏

                                        if ThomePage().wait_check_tips_page():
                                            self.cancel_collection()  # 取消收藏
                                            print('确定取消收藏')
                                            print('------------------')

                    if self.wait_check_page():
                        ThomePage().back_up_button()  # 返回个人中心页面
