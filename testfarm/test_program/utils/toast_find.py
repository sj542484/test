#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.conf.base_page import BasePage


class Toast (BasePage):
    @teststep
    def find_toast_by_xpath(self, text):
        """is toast exist, return True or False"""
        try:
            toast = (By.XPATH, ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(toast))
            return True
        except Exception:
            return False

    @teststep
    def find_toast_by_content(self,content):
        """is toast exist, return True or False"""
        try:
            toast = (By.ACCESSIBILITY_ID, content)
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(toast))
            return True
        except Exception:
            return False
