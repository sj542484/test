# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/14 13:40
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast


class LevelPage(BasePage):
    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_listening_level_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"听力等级")]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_level_page(self, level_name):
        """最后一个等级页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"{}")]'.format(level_name))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def wait_start_button(self, back_name):
        try:
            self.start_button(back_name)
            return True
        except:
            return False

    @teststep
    def back_name(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'back_name')
        return ele

    @teststep
    def play_voice_button(self, back_name):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/'
                                                'following-sibling::android.widget.LinearLayout/'
                                                'android.widget.ImageView'.format(back_name))
        return ele

    @teststep
    def level_name(self, back_name):
        ele = self.driver.find_elements_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling'
                                                 '::android.widget.LinearLayout/android.widget.TextView'
                                                 .format(back_name))
        return ele

    @teststep
    def start_button(self, back_name):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling'
                                                '::android.widget.TextView'.format(back_name))
        return ele


    @teststeps
    def level_page_ele_operate(self):
        level_info = {}
        index = 0
        while True:
            back_name = self.back_name()
            back_num = range(0, len(back_name)-1) if index == 0 else range(1, len(back_name))
            for i in back_num:
                level_info[back_name[i].text] = [y.text for y in self.level_name(back_name[i].text)]

            if self.wait_check_level_page('10级B'):
                self.start_button('10B').click()
                break
            else:
                self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)
                index = index + 1

        while not self.wait_check_level_page('2级A'):
            self.home.screen_swipe_up(0.5, 0.3, 0.9, 1000)

        print('级别类型:')
        for level in level_info:
            print(level_info[level])
            time.sleep(2)
            if self.wait_start_button(level):
                if self.start_button(level).text != '练习中...':
                    self.level_name_toast_judge(level)
                else:
                    if Toast().find_toast('该等级尚未开放哦'):
                        print('该等级尚未开放哦，先选择其他等级练习吧！')
                    else:
                        print('★★★ 未发现Toast')
            else:
                self.home.screen_swipe_up(0.5, 0.9, 0.3, 1500)
                self.level_name_toast_judge(level)
        self.home.click_back_up_button()

    @teststep
    def level_name_toast_judge(self, level):
        self.play_voice_button(level).click()
        self.start_button(level).click()
        if Toast().find_toast('听力等级设置成功'):
            print('听力等级设置成功')
            if self.start_button(level).text != '练习中...':
                print('★★★ Error-- 点击开始后文字未发生改变')
        else:
            print('★★★ 未发现Toast')

        print('-' * 30, '\n')



