# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/1/26 12:29
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testfarm.test_program.app.honor.student.web.base import BaseDriverPage
from testfarm.test_program.conf.decorator import teststeps, teststep


class LoginWebPage(BaseDriverPage):
    @teststeps
    def wait_check_rocket_page(self):
        """判断是否有小火箭页面"""
        locator = (By.CLASS_NAME, "rocket-box")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def close_page_btn(self):
        """关闭页面"""
        ele = self.driver.find_element_by_class_name('icon-cross')
        return ele

    @teststep
    def username(self):
        """用户名"""
        username = self.driver.find_element_by_xpath('//*[@class="login-form"]/div[1]/input')
        return username

    @teststep
    def password(self):
        """密码"""
        password = self.driver.find_element_by_xpath('//*[@class="login-form"]/div[2]/div/input')
        return password

    @teststep
    def login_btn(self):
        """登录"""
        login_btn = self.driver.find_element_by_xpath('//*[@class="login-form"]/button')
        return login_btn

    @teststep
    def teacher_ele(self):
        ele = self.driver.find_elements_by_class_name('select')
        return ele[1]

    @teststep
    def head_pic_icon(self):
        """头像"""
        ele = self.driver.find_element_by_class_name('name')
        return ele

    @teststep
    def logout_btn(self):
        """退出"""
        ele = self.driver.find_element_by_xpath('//*[@id="user-center"]/div/ul/li[2]/a')
        return ele

    @teststep
    def login_operate(self):
        """登录操作"""
        self.username().click()
        self.username().send_keys('17711110000')
        self.password().send_keys('123456')
        self.login_btn().click()
        time.sleep(2)
        self.teacher_ele().click()
        time.sleep(2)

    # def logout_operate(self):
    #     self.head_pic_icon().click()
    #     time.sleep(1)
    #     self.logout_btn().click()
    #     time.sleep(5)