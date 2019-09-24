#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class SettingPage(BasePage):
    """设置页面"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:设置”的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def help_center(self):
        """以“帮助中心”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "help") \
            .click()

    @teststep
    def help_center(self):
        """以“帮助中心”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "help")\
            .click()

    @teststep
    def copyright_complaints(self):
        """以“版权申诉”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "right") \
            .click()

    @teststep
    def regist_protocol(self):
        """以“注册协议”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "protocol") \
            .click()

    @teststep
    def version_check(self):
        """以“版本号”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "version_check") \
            .click()

    @teststep
    def version(self):
        """以“版本号”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "version") \
            .click()

    @teststep
    def logout_button(self):
        """以“退出登录按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "logout") \
            .click()

    @teststep
    def back_up_button(self):
        """以“返回按钮”的id为依据"""
        self.driver\
            .find_element_by_class_name("android.widget.ImageButton") \
            .click()

    @teststep
    def logout_operation(self):
        """退出登录"""
        ThomePage().click_tab_profile()    # 进入首页后点击‘个人中心’按钮
        if TuserCenterPage().wait_check_page():  # 页面检查点
            TuserCenterPage().click_setting()  # 进入设置页面

            if self.wait_check_page():  # 页面检查点
                self.logout_button()  # 退出登录按钮
                ThomePage().tips_content_commit()  # 退出登录提示框
                if not TloginPage().wait_check_page():
                    print(' 退出登录失败 ')
