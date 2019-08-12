import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class WordMatch(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()

    @teststep
    def wait_check_word_match_img(self):
        locator = (By.ID, '{}mg_1'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def text_view(self):
        """class 为TextView的元素"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def is_word(self, word):
        """判断 是否为字母"""
        pattern = re.compile(r'^[A-Za-z\-. ]+$')
        if pattern.match(word) is not None:
            return True
        else:
            return False

    @teststep
    def get_no_selected_cards(self):
        time.sleep(2)
        cards = [x for x in self.text_view() if x.get_attribute("selected") == 'false']
        return cards[2:]

    @teststeps
    def play_word_match_game(self, num, exam_json):
        """连连看 """
        exam_json['连连看'] = {}
        tips = []
        while True:
            no_selected_cards = self.get_no_selected_cards()
            hans_card = [x for x in no_selected_cards if not self.is_word(x.text)]
            english_card = [x for x in no_selected_cards if self.is_word(x.text)]

            for ch in hans_card:
                for en in english_card:
                    ch.click()
                    en.click()
                    time.sleep(0.8)
                    if len(self.get_no_selected_cards()) < len(no_selected_cards):
                        tips.append(ch)
                        print('英文：', en.text)
                        print('中文：', ch.text)
                        break
                break

            self.answer.skip_operator(len(tips)-1, num, '连连看', self.wait_check_word_match_img,
                                      self.judge_tip_status, tips[-1], next_page=1)
            if len(tips) == num:
                break

    @teststep
    def judge_tip_status(self, ele):
        if ele.get_attribute('selected') == 'true':
            print('题目跳转后选中状态未发生改变')
        else:
            print("★★★ 题目跳转后选中状态发生改变!")



