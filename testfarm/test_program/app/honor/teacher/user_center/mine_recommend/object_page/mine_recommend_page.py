#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class RecommendPage(BasePage):
    """我的推荐 页面"""
    def __init__(self):
        self.filter = FilterPage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:我的推荐”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的推荐')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“存在 我的推荐列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator)

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
            .find_elements_by_class_name("android.widget.ImageView") \
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
    def back_up_button(self):
        """以“返回按钮”的class name为依据"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageButton") \
            .click()

    @teststep
    def menu_button(self, index):
        """以 条目右侧“菜单按钮”的id为依据"""
        self.driver\
            .find_elements_by_id(gv.PACKAGE_ID + "iv_eg")[index] \
            .click()

    # 标签管理
    @teststeps
    def wait_check_manage_page(self):
        """以“title:老师测试版”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "fb_add_label")
        return self.wait.wait_check_element(locator)

    # 菜单 内容
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

    @teststep
    def click_negative_button(self):
        """以“取消按钮”的id为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消')]") \
            .click()

    @teststep
    def click_positive_button(self):
        """以“确认按钮”的id为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'确定')]") \
            .click()

    @teststep
    def positive_button(self):
        """以“确认按钮”的id为依据"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'确定')]")
        value = ele.get_attribute('enabled')
        return value

    @teststep
    def expand_icon(self):
        """以“收起 icon”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_expand")
        return ele

    # 本校标签
    @teststeps
    def wait_check_school_label_page(self):
        """以“title:学校标签”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学校标签')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_label_list_page(self):
        """以“存在 标签列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "label_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def check_button(self):
        """以“单选 按钮”的class name为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "check")
        return ele

    @teststep
    def commit_button(self):
        """确定 按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "confirm")
        return ele

    @teststeps
    def verify_recommend_result(self, menu, var='题单'):
        """验证 添加推荐 结果"""
        if TuserCenterPage().wait_check_page():
            TuserCenterPage().click_mine_recommend()  # 我的推荐
            if self.wait_check_page():
                print('----------------验证 -推荐结果-----------------')
                FilterPage().all_element()
                if var == '大题':
                    TuserCenterPage().filter_button()  # 筛选按钮
                    if FilterPage().wait_check_page():
                        TuserCenterPage().click_game_list()  # 点击大题
                        FilterPage().commit_button()  # 确定按钮
                elif var == '试卷':
                    TuserCenterPage().filter_button()  # 筛选按钮
                    if FilterPage().wait_check_page():
                        TuserCenterPage().click_test_paper()  # 点击试卷
                        FilterPage().commit_button()  # 确定按钮

                if self.wait_check_page():
                    if self.wait_check_list_page():
                        item = TestBankPage().question_name()  # 获取
                        menu1 = item[1][0]
                        if '提分' in menu:
                            menu = menu[:-2]
                        if menu != menu1:
                            print('★★★ Error- 加入推荐失败', menu, menu1)
                        else:
                            print('加入推荐成功')
                            for z in range(len(item[0])):
                                print(item[1][z])
                                if self.wait_check_list_page():
                                    self.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入推荐的题单取消
                                    ThomePage().tips_commit()  # 温馨提示 -- 确定
                                    print('确定删除')
                if self.wait_check_page():
                    ThomePage().back_up_button()  # 返回 个人中心
