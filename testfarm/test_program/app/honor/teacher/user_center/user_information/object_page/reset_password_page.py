#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.utils.wait_element import WaitElement


class PwdReset(BasePage):
    """修改密码页面所有控件信息"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:重置密码”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'重置密码')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def pwd_origin(self):
        """以“原始密码”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "pwd_origin")
        return ele

    @teststep
    def pwd_new(self):
        """以“新密码”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "pwd_new")
        return ele

    @teststep
    def pwd_confirm(self):
        """以“新密码二次确认”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "pwd_confirm")
        return ele

    @teststep
    def visible_pwd(self):
        """以“显示密码”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "pwd_visible")\
            .click()

    @teststep
    def confirm_button(self):
        """以“完成按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "pwd_complete")\
            .click()

    @teststep
    def pwd_tips(self):
        """以“密码组成提示”的xpath @text为依据"""
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'密码由6-20位英文字母或数字组成')]")
