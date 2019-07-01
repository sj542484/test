#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/22 10:12
# -----------------------------------------
from app.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf.decorator import teststep


class SpeakingPage(BasePage):

    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_speak_page(self):
        """口语练习等待页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "口语练习")]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_speak_homework_list_page(self):
        """口语作业列表页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_homework_name')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_homework_bank_page(self):
        """作业详情页面检查点"""
        locator = (By.ID, self.id_type() + 'reward')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_bank_list_page(self):
        """作业大题列表页面"""
        locator = (By.ID, self.id_type() + 'tv_testbank_type')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_game_page(self):
        """游戏页面检查点"""
        locator = (By.ID, self.id_type() + 'rate_tv')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_permission_page(self):
        """允许录音提示"""
        locator = (By.ID, 'android:id/title_template')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_microphone_btn_page(self):
        """话筒页面检查点"""
        locator = (By.ID, '{}fab_record'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def select_one_homework(self):
        """选择一个作业"""
        ele = self.driver.find_elements_by_id('{}tv_homework_name'.format(self.id_type()))
        return ele[0]

    @teststep
    def select_one_bank(self):
        """选择一个大题"""
        ele = self.driver.find_elements_by_id('{}tv_testbank_name'.format(self.id_type()))
        return ele[0]

    @teststep
    def microphone_btn(self):
        """话筒按钮"""
        ele = self.driver.find_element_by_id('{}fab_record'.format(self.id_type()))
        return ele

    @teststep
    def allow_btn(self):
        """允许"""
        ele = self.driver.find_element_by_id('android:id/button1')
        return ele
