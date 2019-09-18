# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 10:59
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.listen_everyday.object_page.game_link_sentence import LinkWordSentencePage
from app.honor.student.listen_everyday.object_page.game_listen_choice import ListenChoicePage
from app.honor.student.listen_everyday.object_page.game_select_image import ListenSelectImagePage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.listen_everyday.object_page.listen_result_page import ListenResultPage
from app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast


class ListenGamePage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.listen = ListenHomePage()

    @teststep
    def wait_check_gaming_page(self):
        """以游戏界面计时的id作为根据"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"待完成:")]')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_image_page(self):
        """听音选图 -- 以题号的id作为根据"""
        locator = (By.ID, self.id_type() + 'num')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_rich_page(self):
        locator = (By.ID, self.id_type() + 'rich_text')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_next_button_page(self):
        """以下一步按钮的id作为根据"""
        locator = (By.ID, self.id_type() + 'fab_commit')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_next_submit_page(self):
        """以下一步按钮的id作为根据"""
        locator = (By.ID, self.id_type() + 'fab_submit')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_right_answer(self):
        locator = (By.ID, self.id_type() + 'tv_right')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_button_page(self):
        locator = (By.ID, self.id_type() + 'clear')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_red_hint_page(self):
        locator = (By.ID, self.id_type() + 'tv_hint')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_choice_question_page(self):
        locator = (By.ID, self.id_type() + 'question')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def game_num(self):
        """游戏剩余个数"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rate')
        return ele

    @teststep
    def game_use_time(self):
        """游戏使用时间"""
        ele = self.driver.find_element_by_id(self.id_type() + 'time')
        return ele

    @teststep
    def images(self):
        """图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + "img")
        return ele

    @teststep
    def question(self):
        """题目"""
        ele = self.driver.find_element_by_id(self.id_type() + "sentence")
        return ele

    @teststep
    def question_index(self):
        """题号"""
        ele = self.driver.find_element_by_id(self.id_type() + "num")
        return ele

    # 听音连句
    @teststep
    def need_input_word(self):
        """需要填补的空格"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rich')
        word_num = len(ele.text.split(' '))
        return word_num

    @teststep
    def finish_word(self):
        """填补后的单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rich')
        return ele

    @teststep
    def clear_button(self):
        """清除按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'clear')
        return ele

    @teststep
    def audio_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'play_voice')
        return ele

    @teststep
    def split_sentence_word(self):
        """候选单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + "text")
        word_list = [i for i in ele if i.text != '']
        return word_list

    @teststep
    def correct_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_right')
        return ele

    @teststep
    def red_hint(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_hint')
        return ele

    @teststep
    def play_voice(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_audio')
        return ele

    @teststep
    def choice_question(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'question')
        return ele

    @teststep
    def choice_char(self, question):
        ele = self.driver.\
                find_elements_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/following-sibling::'
                                       'android.widget.LinearLayout/android.widget.LinearLayout/'
                                       'android.widget.LinearLayout/android.widget.TextView[contains(@resource-id,'
                                       '"{1}tv_char")]'.format(question, self.id_type()))
        return ele

    @teststep
    def choice_item(self, question):
        ele = self.driver.\
            find_elements_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/following-sibling::'
                                   'android.widget.LinearLayout/android.widget.LinearLayout/'
                                   'android.widget.LinearLayout/android.widget.TextView[contains(@resource-id,'
                                   '"{1}tv_item")]'.format(question, self.id_type()))

        return ele

    @teststep
    def text_views(self):
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        text_list = [x for x in ele if x.text != '' or x.text is not None]
        return text_list

    @teststep
    def last_text(self):
        all_text = self.text_views()
        return all_text[-1].get_attribute('resourceId')

    @teststep
    def next_button(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_submit')
        return ele

    @teststep
    def play_listen_game_process(self):
        bank_info = 0
        if self.wait_check_image_page():
            """听音选图"""
            bank_info = ListenSelectImagePage().play_listen_select_image_game()

        elif self.wait_check_rich_page():
            """听音连句"""
            bank_info = LinkWordSentencePage().play_link_word_to_sentence_game()

        elif self.wait_check_red_hint_page():
            """听后选择"""
            bank_info = ListenChoicePage().play_listen_choice_game()

        ListenResultPage().result_page_operate(bank_info)
        self.home.click_back_up_button()
        if ListenResultPage().wait_check_result_page():
            self.home.click_back_up_button()
        

