# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/2/16 13:52
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testfarm.test_program.app.honor.student.web.base import BaseDriverPage
from testfarm.test_program.app.honor.student.web.driver import Driver
from testfarm.test_program.app.honor.student.web.login_page import LoginWebPage
from testfarm.test_program.conf.decorator import teststep, teststeps


class ResignExamPage(BaseDriverPage):

    def wait_check_home_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="小学资源推荐"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
     
    def wait_check_mine_item_pool_page(self):
        """我的题库页面检查点"""
        time.sleep(3)
        locator = (By.XPATH, '//*[text()="我的"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_exam_tab_page(self):
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="卷子名称"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_mine_exam_page(self):
        """我的试卷页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="我的自创"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_exam_detail_page(self):
        """试卷详情页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="开始答卷"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_delete_tip_page(self):
        """删除作业提示页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"删除试卷不可恢复")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_publish_tip_page(self):
        """删除作业提示页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"试卷为【提分版】功能")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
     
    def wait_check_assign_page(self):
        """布置试卷页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"考试信息")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
     
    def logo(self):
        """logo"""
        ele = self.driver.find_element_by_id('logo')
        return ele

    def mine_item_pool(self):
        """我的题库"""
        ele = self.driver.find_element_by_xpath('//*[@id="side-bar"]/div[2]/div/a[1]')
        return ele

    def exam_label(self):
        """试卷"""
        ele = self.driver.find_element_by_xpath('//*[@id="page-head"]/div[1]/div/div[2]/div[1]/div[1]/a[3]')
        return ele
     
    def mine_label(self):
        """我的"""
        ele = self.driver.find_element_by_xpath('//*[@id="page-head"]/div[2]/div/a[2]')
        return ele
     
    def exam_list(self):
        """试卷列表"""
        ele = self.driver.find_elements_by_xpath('//*[@id="page-content"]/div/div[2]/table/tbody/tr')
        return ele

    def exam_name(self, ele):
        """试卷名称"""
        name = ele.find_element_by_xpath('./td[1]/div/span')
        return name

    def delete_btn(self):
        """删除试卷"""
        ele = self.driver.find_element_by_xpath('//*[text()="删除试卷"]')
        return ele
    
    def publish_confirm_btn(self):
        """发布试卷确定按钮"""
        ele = self.driver.find_element_by_xpath('//*[text()="确 定"]')
        return ele

    def delete_confirm_btn(self):
        """删除提示信息确定按钮"""
        ele = self.driver.find_element_by_xpath('//*[@class="el-button el-button--default el-button--primary "]')
        return ele
 
    def assign_exam_btn(self):
        """布置试卷"""
        ele = self.driver.find_element_by_xpath('//*[text()="布置试卷"]')
        return ele

    def student_card(self):
        """学生列表"""
        ele = self.driver.find_elements_by_class_name('student-card')
        return ele

    def publish_btn(self):
        """发布试卷按钮"""
        ele = self.driver.find_element_by_xpath('//*[@id="bodyer"]/div/div[1]/div/div/div/div[1]/button')
        return ele

    def enter_to_mine_exam_page(self):
        if self.wait_check_home_page():
            self.mine_item_pool().click()
            if self.wait_check_mine_item_pool_page():
                self.mine_label().click()
                time.sleep(2)
                self.exam_label().click()
                time.sleep(2)

    def delete_exams(self):
        while True:
            if len(self.exam_list()) == 4:
                break
            else:
                exam_name = self.exam_name(self.exam_list()[0])
                print("删除试卷：", exam_name.text)
                exam_name.click()
                if self.wait_check_exam_detail_page():
                    self.delete_btn().click()
                    if self.wait_check_delete_tip_page():
                        self.delete_confirm_btn().click()
                        time.sleep(3)

    def assign_exams(self, index):
        self.exam_name(self.exam_list()[index]).click()
        if self.wait_check_exam_detail_page():
            self.assign_exam_btn().click()
            if self.wait_check_assign_page():
                self.student_card()[0].click()   # 选择第一个学生
                self.publish_btn().click()
                if self.wait_check_publish_tip_page():
                    self.publish_confirm_btn().click()
        index = index - 1
        return index

    def reassign_exam_operate(self):
        LoginWebPage().login_operate()
        if self.wait_check_home_page():
            self.enter_to_mine_exam_page()
            self.delete_exams()
            self.logo().click()
            time.sleep(3)

            if self.wait_check_home_page():
                index = -1
                for i in range(4):
                    self.enter_to_mine_exam_page()
                    index = self.assign_exams(index)







