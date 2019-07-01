# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/2 8:28
# -------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.data_action import DataAction
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep


class UserCenterPage(BasePage):
    @teststep
    def wait_check_user_center_page(self):
        """以“设置”业务的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_buy_page(self):
        """购买页面检查点"""
        locator = (By.ID, self.id_type() + "goToCustomerService")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def nickname(self):
        """昵称"""
        ele = self.driver.find_element_by_id(self.id_type() + 'name')
        return ele.text

    @teststep
    def school_name(self):
        """学校名称"""
        ele = self.driver.find_element_by_id(self.id_type() + 'school_name')
        return ele.text

    @teststep
    def purchase(self):
        """购买"""
        ele = self.driver.find_element_by_id(self.id_type() + 'study_card')
        return ele

    @teststep
    def phone(self):
        """学生的手机号"""
        ele = self.driver.find_element_by_id(self.id_type() + 'phone')
        return ele.text

    @teststep
    def get_user_info(self):
        """:return 学生id、学校名称、学校id、昵称"""
        HomePage().click_tab_profile()
        if self.wait_check_user_center_page():
            self.purchase().click()
            if self.wait_check_buy_page():
                phone = self.phone()
                stu_id = DataAction().find_student_id(phone)[0][0]
                HomePage().click_back_up_button()
                if self.wait_check_user_center_page():
                    school_name = self.school_name()
                    school_id = self.mysql.find_school_id(school_name)[0][0]
                    nickname = self.nickname()
                    HomePage().click_tab_hw()
                    return stu_id, school_name, school_id, nickname
