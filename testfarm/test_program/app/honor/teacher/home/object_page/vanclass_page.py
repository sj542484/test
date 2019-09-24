#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class VanclassPage(BasePage):
    """ 班级 页面"""
    tab_locator = (By.ID, gv.PACKAGE_ID + "notice")  # 各tab
    tab_icon_locator = (By.ID, gv.PACKAGE_ID + "type_text")  # 各tab icon
    
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var, index=10):
        """以“title: 班级名称”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def wait_check_list_page(self):
        """以“菜单title 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "type_text")
        return self.wait.wait_check_element(locator)

    # 菜单
    @teststep
    def vanclass_hw(self):
        """本班作业"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[0] \
            .click()

    @teststep
    def vanclass_paper(self):
        """本班卷子"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[1] \
            .click()

    @teststep
    def word_book(self):
        """单词本"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[2] \
            .click()

    @teststep
    def daily_listen(self):
        """每日一听"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[3] \
            .click()

    @teststep
    def score_ranking(self):
        """积分排行榜"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[4] \
            .click()

    @teststep
    def star_ranking(self):
        """星星排行榜"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[5] \
            .click()

    @teststep
    def vanclass_member(self):
        """班级成员"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[6] \
            .click()

    @teststep
    def invite_st_button(self):
        """以“邀请学生 按钮”的id为依据"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[7] \
            .click()

    @teststep
    def vanclass_application(self):
        """入班申请"""
        self.wait. \
            wait_find_elements(self.tab_icon_locator)[8] \
            .click()

    @teststep
    def more_button(self):
        """更多 按钮"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView")\
            .click()

    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除作业”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "title")
        return self.wait.wait_check_element(locator)

    @teststep
    def modify_name(self, index):
        """班级/学校名称 修改"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "title")[index]\
            .click()

    # 列表
    @teststep
    def hint_text(self):
        """最近2周动态（可点击查看）"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "hint_text") \
            .text
        print(item)

    @teststep
    def hint_button(self):
        """帮助 按钮"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "hint") \
            .text
        print(item)

    @teststep
    def hw_name(self):
        """作业name"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def create_time(self):
        """作业创建时间"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "date")
        return ele

    # 分享界面
    @teststeps
    def wait_check_share_tips_page(self):
        """以“title”为依据"""
        locator = (By.ID, "android:id/alertTitle")
        return self.wait.wait_check_element(locator)

    @teststep
    def share_title(self):
        """分享title"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_title").text
        print(item)
        return item

    @teststep
    def share_content(self):
        """分享 内容"""
        item = self.driver \
            .find_elements_by_id("android:id/text1")
        return item
