#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.pc_operation.tools.wait_element import WaitElement
from conf.base_config import GetVariable
from conf.decorator_pc import teststeps
from conf.base_page import BasePage


class LoginPage(BasePage):
    """登录页面"""
    identify_locator = (By.XPATH, '//h2[@class="identity" and text()="选择身份"]')
    teacher_value = '//span[contains(text(),"在编教师")]'

    def __init__(self, driver):
        self.wait = WaitElement(driver)
        self.driver = driver

    @teststeps
    def wait_check_page(self, index=10):
        """以 login-form元素 的xpath为依据"""
        locator = (By.CSS_SELECTOR, "div[class='login-form']")
        return self.wait.wait_check_element(locator, index)

    @teststeps
    def header_notice(self):
        """提示信息"""
        ele = self.driver \
            .find_element_by_xpath('//div[@class="header-notice"]')
        return ele

    @teststeps
    def download_button(self):
        """顶部 右上角 'APP 下载' """
        locator = (By.XPATH, '//span[text()="APP 下载"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def top_register_button(self):
        """顶部 右上角 '注册' """
        locator = (By.XPATH, '//span[text()="注册"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def top_login_button(self):
        """顶部 右上角 '登录' """
        locator = (By.XPATH, '//span[text()="登录"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def login_title(self):
        """登录 title"""
        locator = (By.XPATH, '//h2[@class="login" and text()="用户登录"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def input_username(self):
        """账号"""
        locator = (By.XPATH, '//input[@type="text"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def input_password(self):
        """账号/密码  # 是否显示密码会影响元素type值"""
        locator = (By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/div/div[2]/div/input')
        return self.wait.wait_find_element(locator)

    @teststeps
    def login_button(self):
        """登录按钮"""
        locator = (By.XPATH, '//button[text()="登录"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def visible_password(self):
        """显示密码"""
        locator = (By.XPATH, '//div[@class="el-input el-input-group"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def login_check_button(self):
        """保持登录状态 勾选框"""
        locator = (By.XPATH, '//span[@class="el-checkbox__inner"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def keep_login_status(self):
        """wording: 保持登录状态"""
        locator = (By.XPATH, '//span[text()="保持登录状态"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def forget_password(self):
        """忘记密码?"""
        locator = (By.LINK_TEXT, '忘记密码?')
        self.wait.wait_find_element(locator).click()

    # 身份选择
    @teststeps
    def identity_title(self, var=5):
        """登录 title"""
        return self.wait.wait_check_element(self.identify_locator, var)

    @teststeps
    def teacher_identity(self):
        """老师身份"""
        locator = (By.XPATH, '//span[contains(text(),"自由教师")]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def judge_teacher(self, var=5):
        """老师身份"""
        locator = (By.XPATH, self.teacher_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def school_teacher_identity(self):
        """老师身份"""
        locator = (By.XPATH, self.teacher_value)
        self.wait.wait_find_element(locator).click()

    @teststeps
    def student_identity(self):
        """学生身份"""
        locator = (By.XPATH, '//span[text()="学生"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def back_login_button(self):
        """返回上一步 按钮"""
        locator = (By.XPATH, '//a[text()="< 返回上一步"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def wait_identity_not(self):
        """等待 元素：选择身份title 消失"""
        return self.wait.wait_until_not_element(self.identify_locator, 5)

    @teststeps
    def wechat_before_hint(self):
        """遇到问题了？请联系"""
        locator = (By.XPATH, '//div[@class="wechat-service"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def wechat_service(self):
        """微信客服"""
        locator = (By.XPATH, '//div[@class="wechat-service"]/span[text()="微信客服"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def wechat_service_time(self):
        """客服值班时间：8:30-22:30（全年无休）"""
        locator = (By.XPATH, '//div[@class="service-time"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def login_operation(self):
        """登录操作"""
        user_info = self.get_user_info()
        user = user_info['teacher']['teacher']
        pwd = user_info['pwd']

        self.input_username().send_keys(user)
        self.input_password().send_keys(pwd)
        self.login_button()  # 登录 按钮

        if self.identity_title():
            print('------选择身份------')
            if self.judge_teacher():
                self.school_teacher_identity()
            else:
                self.teacher_identity()  # 老师
            self.wait_identity_not()  # 等待登录界面消失，进入主界面

    @teststeps
    def login_account(self, user, password):
        """登录操作"""
        phone = self.input_username()
        phone.clear()
        phone.send_keys(user)  # 输入手机号

        pwd = self.input_password()
        pwd.clear()
        pwd.send_keys(password)  # 输入密码
