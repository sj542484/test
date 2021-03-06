#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from utils.click_bounds import ClickBounds
from utils.wait_element import WaitElement


class UserInfoPage(BasePage):
    """个人信息页面所有控件信息"""
    user_info_tips = '★★★ Error- 未进入个人中心页面'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=15):
        """以title:个人信息 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'个人信息')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def avatar_profile(self):
        """以“头像”的id为依据
            用于判断是否有展示头像，但是具体头像内容不能判定"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "avatar")
        return ele

    @teststep
    def nickname(self):
        """以“昵称”的id为依据
            用于判断昵称修改前后是否相同，默认修改后的昵称与修改前不同"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "nick").text
        return ele

    @teststep
    def school(self):
        """以“学校”的id为依据
            用于判断学校修改前后是否相同，默认修改后与修改前不同"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "school")
        return ele

    @teststep
    def qr_code(self):
        """以“微信二维码”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "qr_code")
        return ele

    @teststep
    def phone(self):
        """以“手机号”的id为依据
            用于判断手机号修改前后是否相同，默认修改后的手机号与修改前不同"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "phone")\
            .text
        return ele

    @teststep
    def click_avatar(self):
        """以“头像”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "avatar")\
            .click()

    @teststep
    def click_nickname(self):
        """以“昵称”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "nick")\
            .click()

    @teststep
    def click_qr_code(self):
        """以“微信二维码”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "qr_code")\
            .click()

    @teststep
    def click_phone_number(self):
        """以“手机号”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "phone")\
            .click()

    @teststep
    def click_password(self):
        """以“密码”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "pwd")\
            .click()

    @teststep
    def click_school(self):
        """以“学校”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "school") \
            .click()

    @teststep
    def input(self):
        """以“修改昵称/用户名/手机号的二级页面中输入框”的class_name为依据"""
        ele = self.driver\
            .find_element_by_class_name('android.widget.EditText')
        return ele

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
    def click_photograph(self):
        """以“拍照”的xpath @index为依据"""
        time.sleep(2)
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'拍照')]")\
            .click()
        print('点击 拍照 按钮')

    @teststep
    def click_album(self):
        """以“从相册选择”的xpath @index为依据"""
        time.sleep(2)
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'从相册选择')]")\
            .click()
        print('点击 从相册选择 按钮')

    @teststep
    def click_block(self):
        """点击页面空白区域"""
        time.sleep(1)
        ClickBounds().click_bounds(540, 300)

    @teststeps
    def back_up(self):
        """从个人信息页 返回主界面"""
        if self.wait_check_page():  # 页面检查点
            ThomePage().back_up_button()  # 返回按钮
            if TuserCenterPage().wait_check_page():  # 页面检查点
                ThomePage().click_tab_hw()

    @teststeps
    def app_account(self, account):
        """判断应用当前 登录账号信息"""
        ThomePage().click_tab_profile()
        if TuserCenterPage().wait_check_page():
            TuserCenterPage().click_avatar_profile()  # 进入 个人信息页面
            if self.wait_check_page():
                phone = self.phone()

                if phone[-4:] == account[-4:]:
                    self.back_up()  # 返回主界面
                    return True
                else:
                    SettingPage().logout()
                    return False
