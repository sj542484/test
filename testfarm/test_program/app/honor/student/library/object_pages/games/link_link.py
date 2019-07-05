# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 10:32
# -------------------------------------------
import re
import time
from math import ceil

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class LinkLink(BasePage):
    def __init__(self):
        self.common = CommonPage()

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
        pattern = re.compile(r'^[A-Za-z/\-. ]+$')
        if pattern.match(word) is not None:
            return True
        else:
            return False

    @teststep
    def get_word_cards(self):
        cards = self.text_view()
        return cards[4:]

    @teststep
    def get_english_cards(self):
        """获取英文卡片"""
        en_cards = [x for x in self.get_word_cards()  if self.is_word(x.text)]
        return en_cards

    @teststep
    def get_not_selected_hans_card(self):
        """获取中文未被选择的卡片"""
        ch_cards =[x for x in self.get_word_cards() if not self.is_word(x.text) and GetAttribute().selected(x) == 'false']
        return ch_cards

    @teststeps
    def word_match_operate(self, fq, sec_answer, half_exit):
        """连连看游戏过程"""
        timer = []
        index = 0
        total_num = self.common.rest_bank_num()
        mine_answer = {}
        flag = False
        for i in range(ceil(total_num/5)):                          # 获取连连看页数 5个单词占一页
            if flag:
                break

            if self.wait_check_word_match_img():
                english_card = self.get_english_cards()     # 英文序列
                for en in english_card:
                    if index == 2:
                        if half_exit:
                            flag = True
                            self.click_back_up_button()
                            break

                    en.click()
                    self.common.rate_judge(total_num, index)
                    rest_num = self.common.rest_bank_num()
                    time_str = self.common.bank_time()
                    hans_card = self.get_not_selected_hans_card()
                    if len(hans_card) != 1:
                        for ch in hans_card:
                            ch.click()
                            if rest_num != 1:
                                if self.common.rest_bank_num() == rest_num - 1:
                                    index = index + 1
                                    self.common.rate_judge(total_num, index)
                                    mine_answer[ch.text] = en.text
                                    print('中文：', ch.text)
                                    print('英文：', en.text)
                                    print('-'*20, '\n')
                                    timer.append(time_str)
                                    break
                                else:
                                    en.click()
                    else:
                        mine_answer[hans_card[0].text] = en.text
                        print('中文：', hans_card[0].text)
                        print('英文：', en.text)
                        print('-' * 20, '\n')
                        timer.append(time_str)
                        hans_card[0].click()
        self.common.judge_timer(timer)
        time.sleep(2)
        answer = mine_answer if fq == 1 else sec_answer
        return answer, total_num


