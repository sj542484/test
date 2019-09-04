#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/20 11:49
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testfarm.test_program.app.honor.student.web.object_pages.base import BaseDriverPage
from testfarm.test_program.conf.decorator import teststep


class WebHomePage(BaseDriverPage):
    @teststep
    def wait_check_home_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.ID, 'logo')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_test_class_page(self):
        """测试班级页面检查点 """
        locator = (By.XPATH, '//*[contains(text(),"MVP")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    @teststep
    def wait_check_tips_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-dialog__header')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_delete_tip_page(self):
        time.sleep(2)
        locator = (By.CLASS_NAME, 'el-message-box__content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_class_page(self):
        """单词本页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(), "布置日期")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_blanket_page(self):
        """题筐页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(), "生成试卷")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    @teststep
    def wait_check_assign_homework_page(self):
        """布置试卷/作业页面检查点"""
        time.sleep(2)
        locator = (By.ID, 'homework-student-list-box')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    @teststep
    def click_logo(self):
        """点击在线助教logo"""
        self.driver.find_element_by_id('logo').click()

    @teststep
    def join_blanket(self):
        """加入题筐"""
        self.driver.find_element_by_css_selector('.head-banner .controls .el-button').click()

    @teststep
    def click_select_all(self):
        """全选按钮"""
        self.driver.find_element_by_css_selector('.content .el-checkbox__inner').click()

    @teststep
    def bank_control_btn(self):
        """生成试卷/题单/作业按钮"""
        ele = self.driver.find_elements_by_css_selector('.controls .el-button')
        return ele

    @teststep
    def tip_content(self):
        """提示内容"""
        ele = self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style="display: none;"]) .el-dialog__body')
        return ele.text

    @teststep
    def delete_tip_content(self):
        """删除提示内容"""
        ele = self.driver.find_element_by_css_selector('.el-message-box__message')
        return ele.text

    @teststep
    def click_confirm_delete_btn(self):
        """点击删除提示的确定按钮"""
        self.driver.find_element_by_css_selector('.el-message-box__btns .el-button--primary').click()

    @teststep
    def click_no_more_tip(self):
        """不再提醒"""
        self.driver.find_element_by_css_selector('.el-checkbox__input .el-checkbox__original').click()

    @teststep
    def click_confirm_btn(self):
        self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style="display: none;"]) .dialog-footer .el-button--primary').click()

    @teststep
    def select_test_class(self):
        self.driver.find_element_by_css_selector('.vanclass-list li:last-child .el-checkbox__inner').click()

    @teststep
    def click_more_class(self):
        """更多班级"""
        self.driver.find_element_by_css_selector('.toggle-link').click()

    @teststep
    def click_test_class(self):
        """点击测试班级"""
        self.driver.find_element_by_css_selector('#class-list a:last-child').click()

    @teststep
    def homework_name(self):
        """作业名称"""
        ele = self.driver.find_elements_by_css_selector('.table-list .homework-name')
        return ele

    @teststep
    def homework_tab(self):
        """作业详情tab选项"""
        ele = self.driver.find_elements_by_css_selector('.head-bottom-nav  a')
        return ele

    @teststep
    def delete_btn(self):
        """删除按钮"""
        ele = self.driver.find_element_by_css_selector('.board .controls .icon-cross')
        return ele


    @teststep
    def select_test_class_operate(self):
        """选择测试班级操作"""
        if not self.wait_check_test_class_page():
            self.click_more_class()
            time.sleep(1)
        self.click_test_class()

    @teststep
    def tips_operate(self):
        """提示信息处理"""
        if self.wait_check_tips_page():
            print(self.tip_content(), '\n')
            self.click_confirm_btn()
            time.sleep(2)


    @teststep
    def tip_box_operate(self):
        """删除作业提示处理"""
        if self.wait_check_delete_tip_page():
            print(self.delete_tip_content(), '\n')
            self.click_confirm_delete_btn()
            time.sleep(3)

