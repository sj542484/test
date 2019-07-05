#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.wait_element import WaitElement


class VideoPage(BasePage):
    """视频"""
    shoot_video_value = gv.PACKAGE_ID + 'video'  # 拍摄按钮
    time_value = gv.PACKAGE_ID + 'time'  # 拍摄时长
    delete_button_value = gv.PACKAGE_ID + 'delete'  # 删除按钮

    permission_title_value = "com.android.packageinstaller:id/permission_message"  # 权限问询 title

    video_item_value = 'com.android.documentsui:id/mz_text_container'  # 视频条目

    def __init__(self):
        self.wait = WaitElement()

    # 权限询问页面
    @teststeps
    def wait_check_permission_page(self, var=3):
        """ 权限title的id为依据"""
        locator = (By.ID, self.permission_title_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def permission_title(self):
        """权限title"""
        ele = self.driver \
            .find_element_by_id(self.permission_title_value).text
        print(ele)

    @teststeps
    def allow_button(self):
        """允许 按钮"""
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'允许')]") \
            .click()

    @teststeps
    def permission_allow(self):
        """ 拍照权限"""
        if self.wait_check_permission_page():
            self.permission_title()  # 权限title
            self.allow_button()  # 允许 按钮
            print('-----------')

    # 拍摄
    @teststeps
    def wait_check_shoot_page(self):
        """拍摄视频 的为依据"""
        locator = (By.ID, self.shoot_video_value)
        return self.wait.wait_check_element(locator)

    # 第一页面
    @teststeps
    def shoot_button(self):
        """'拍摄'按钮"""
        print('点击拍摄按钮')
        self.driver \
            .find_element_by_id(self.shoot_video_value) \
            .click()

    @teststeps
    def rotate_button(self):
        """切换前后摄像头"""
        print('点击切换前后摄像头')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "rotate") \
            .click()

    # 第二页面
    @teststeps
    def wait_check_suspend_page(self, var=10):
        """暂停拍摄按钮 为依据"""
        locator = (By.ID, self.time_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def suspend_button(self):
        """'暂停'按钮"""
        print('点击暂停按钮')
        self.driver \
            .find_element_by_id(self.shoot_video_value) \
            .click()

    # 第三页面
    @teststeps
    def wait_check_done_page(self, var=10):
        """时间 为依据"""
        locator = (By.ID, self.delete_button_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def shoot_time(self):
        """拍摄时长"""
        ele = self.driver \
            .find_element_by_id(self.time_value).text
        return ele

    @teststeps
    def delete_button(self):
        """'删除'按钮"""
        print('点击删除按钮')
        self.driver \
            .find_element_by_id(self.delete_button_value) \
            .click()

    @teststeps
    def done_button(self):
        """完成按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "done") \
            .click()

    # 本地视频 有视频/无视频
    @teststeps
    def wait_check_local_page(self, var=10):
        """title:最近 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'最近')]")
        return self.wait.wait_check_element(locator, var)

    # 本地视频 有视频 进入视频列表
    @teststeps
    def wait_check_local_list_page(self, var=10):
        """视频条目列表 为依据"""
        locator = (By.ID, self.video_item_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def click_video_item(self, index):
        """点击 视频 条目"""
        self.driver \
            .find_elements_by_id(self.video_item_value)[index].click()

    @teststeps
    def video_item(self):
        """视频信息"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.RelativeLayout/descendant::*")

        content = []
        value = []
        for i in range(len(ele)):
            if ele.text != '':
                value.append(ele.text)
            if GetAttribute().resource_id(ele[i]) == 'com.android.documentsui:id/mz_icon_container':
                content.append(value)
                continue

        return content
