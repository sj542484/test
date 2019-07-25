# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/2/13 13:27
# -------------------------------------------
from selenium import webdriver

from testfarm.test_program.app.honor.student.web.object_pages.base import BaseDriverPage


class Driver:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('http://dev.vanthink.cn/accounts#/login')

    def set_driver(self):
        base = BaseDriverPage()
        base.set_driver(self.driver)

    def quit_web(self):
        self.driver.quit()


