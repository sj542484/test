# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/12 14:50
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testfarm.test_program.app.honor.student.web.base import BaseDriverPage
from testfarm.test_program.app.honor.student.web.login_page import LoginWebPage



class AssignWord(BaseDriverPage):

    def wait_check_home_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.ID, 'class-list')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_wordbook_page(self):
        """单词本页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="单词量排行"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_label_select_page(self):
        """检查是否还有下一级标签"""
        time.sleep(1)
        locator = (By.CLASS_NAME, 'label-select')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_assign_tip_page(self):
        """布置单词提示页面检查点"""
        time.sleep(1)
        locator = (By.XPATH, '//*[text()="提示"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_class_page(self):
        locator = (By.XPATH, "//*[text()=' 邀请学生']")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_word_page(self):
        time.sleep(2)
        locator = (By.XPATH, "//*[text()='选择单词 ']")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def class_list(self):
        """班级列表"""
        ele = self.driver.find_elements_by_xpath('//*[@class="move"]')
        return ele

    def wordbook_tab(self):
        """单词本"""
        ele = self.driver.find_element_by_xpath('//*[text()="单词本"]')
        return ele

    def assign_word_btn(self):
        """布置单词按钮"""
        ele = self.driver.find_element_by_xpath('//*[@class="controls-bar"]/button[1]')
        return ele

    def first_label(self, index):  # 48, 46, 28
        """复习1 标签"""
        ele = self.driver.find_element_by_xpath('//*[@class="label-list"]/a[{}]'.format(index))
        return ele

    def next_label(self):
        """下一级标签"""
        ele = self.driver.find_element_by_xpath('//*[@class="label-list"]/a[1]')
        return ele

    def vanclass_student(self):
        ele = self.driver.find_element_by_class_name('student-card')
        return ele

    def assign_now_btn(self):
        """立即布置按钮"""
        ele = self.driver.find_element_by_xpath('//*[@class="controls-bar"]/button')
        return ele

    def assign_confirm_btn(self):
        """确定按钮"""
        ele = self.driver.find_element_by_xpath('//*[@id="page-content"]/div[5]/div/div[3]/div/button[2]')
        return ele


    def assign_wordbook_operate(self):
        LoginWebPage().login_operate()
        # self.page_source_web()
        if self.wait_check_home_page():
            self.class_list()[0].click()
            if self.wait_check_class_page():
                self.wordbook_tab().click()
                word_label_index = [21, 48, 46]
                for x in word_label_index:
                    if self.wait_check_wordbook_page():
                        self.assign_word_btn().click()
                        if self.wait_check_word_page():
                            self.vanclass_student().click()
                            self.first_label(x).click()
                            time.sleep(1)
                            while self.wait_check_label_select_page():
                                self.next_label().click()
                                time.sleep(0.5)

                            self.assign_now_btn().click()
                            if self.wait_check_assign_tip_page():
                                self.assign_confirm_btn().click()
                                time.sleep(2)









