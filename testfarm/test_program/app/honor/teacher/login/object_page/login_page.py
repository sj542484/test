#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_page import BasePage
from utils.screen_shot import ScreenShot
from utils.wait_element import WaitElement


class TloginPage(BasePage):
    """登录界面"""

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=10):
        """以 请输入手机号码 输入框的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "ed_user_nickname")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def input_username(self):
        """以“请输入手机号码”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "ed_user_nickname")
        return ele

    @teststep
    def input_password(self):
        """以“请输入登录密码”的id为依据"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "ed_user_pwd")
        return ele

    @teststep
    def login_button(self):
        """以“登录”Button的ID为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "btn_login") \
            .click()

    @teststep
    def register_button(self):
        """以“注册帐号”的ID为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'register') \
            .click()

    @teststep
    def visible_password(self):
        """以“显示密码”的ID为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'pwd_visible')
        return ele

    @teststep
    def forget_password(self):
        """以“忘记密码？”的ID为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'forget_pwd') \
            .click()

    # 已注册学生账号，未注册老师账号
    @teststeps
    def wait_check_st_page(self, var=20):
        """以title:在线助教 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'在线助教')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def login_operation(self):
        """登录 操作"""
        import os, yaml
        f = open('./testfarm/test_program/conf/user_info.yaml', 'r', encoding='utf8')
        res = f.read()
        res = yaml.full_load(res)
        stu_info = res['userinfo'][self.deviceName]
        user = stu_info['teacher']['teacher']

        pwd = stu_info['pwd']

        self.input_username().send_keys(user)  # 账号输入框
        self.input_password().send_keys(pwd)  # 密码输入框

        self.login_button()  # 登录按钮

    @teststeps
    def app_status(self):
        """判断应用当前状态"""
        if ThomePage().wait_check_page():  # 在主界面
            print('在主界面')
        elif self.wait_check_page():  # 在登录界面
            self.login_operation()  # 登录 操作
        else:
            print('在其他页面,重启app')
            self.close_app()  # 关闭APP
            self.launch_app()  # 重启APP
            if ThomePage().wait_check_page():  # 在主界面
                print('在主界面')
            elif self.wait_check_page():  # 在登录界面
                self.login_operation() # 登录 操作
            else:
                self.screen_shot()  # 截屏

    # 忘记密码
    @teststeps
    def wait_check_forget_page(self):
        """以title:找回密码 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'找回密码')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def input_phone(self):
        """以“请输入手机号码”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "phone")
        return ele

    @teststep
    def input_code(self):
        """以“请输入 验证码”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "code")
        return ele

    @teststep
    def get_code_button(self):
        """以“获取验证码 按钮”的ID为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'count_time')
        return ele

    @teststep
    def next_button(self):
        """以“下一步 按钮”的ID为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'next') \
            .click()

    @teststep
    def back_login_button(self):
        """以“返回登录 按钮”的ID为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'back') \
            .click()

    @teststeps
    def wait_check_reset_page(self):
        """以 再次确认输入框 的resource-id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "pwd_confirm")
        return self.wait.wait_check_element(locator)

    @teststep
    def new_pwd(self):
        """以“请输入 新密码”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "pwd")
        return ele

    @teststep
    def new_pwd_confirm(self):
        """以“再次确认 新密码”的ID为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'pwd_confirm')
        return ele

    @teststep
    def reset_button(self):
        """以“重置 按钮”的ID为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'reset') \
            .click()

    # 注册
    @teststeps
    def wait_check_register_page(self, var=10):
        """以title:老师注册 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'老师注册')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_register_nick_page(self, var=10):
        """以设置昵称 的TEXT为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "nick_name")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def input_nickname(self):
        """以“请设置昵称”的id为依据"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "nick_name")
        return ele

    @teststep
    def launch_app(self):
        """Start on the device the application specified in the desired capabilities.
        """
        self.driver.launch_app()

    @teststep
    def close_app(self):
        """Close on the device the application specified in the desired capabilities.
        """
        self.driver.close_app()

    @teststeps
    def screen_shot(self, name='重启app'):
        """截屏"""
        import os
        import tempfile
        from PIL import Image
        PATH = lambda p: os.path.abspath(p)
        TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

        self.driver.get_screenshot_as_file(TEMP_FILE)
        date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        img_name = name + '_' + date_time + '.png'

        image = Image.open(TEMP_FILE)
        image.save(TEMP_FILE)
        ScreenShot().write_to_file(gv.SCREENSHOT_ROOT, img_name)
        os.path.isfile(gv.SCREENSHOT_ROOT + img_name)
