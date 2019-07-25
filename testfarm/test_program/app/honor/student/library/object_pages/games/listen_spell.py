# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 13:48
# -------------------------------------------
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard


class ListenSpell(BasePage):
    """单词听写"""
    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_listen_spell_word_page(self):
        locator = (By.ID, self.id_type() + "tv_word")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def input_word(self):
        """完成的单词"""
        word = self.driver.find_element_by_id(self.id_type() + 'tv_word')
        finish_word = word.text.replace(' ', '')
        return finish_word

    @teststep
    def click_voice(self):
        """声音按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'play_voice')\
            .click()

    @teststep
    def explain(self):
        """翻译"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele.text

    @teststep
    def answer_word(self):
        """答案单词 """
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return ele.text

    @teststeps
    def listen_spell_operate(self, fq, sec_answer):
        """单词听写具体操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()  # 获取总题数

        for i in range(total_num):
            if self.wait_check_listen_spell_word_page():
                self.common.judge_next_is_true_false('false')
                if self.input_word() != '点击喇叭听写单词':
                    print('★★★ 默写单词栏默认不为空！')
                if fq == 1:
                    random_length = random.randint(3, 5)  # 创建随机字母
                    random_string = ''.join(random.sample(string.ascii_letters, random_length))
                    for j in range(len(random_string)):  # 输入随机字母
                        Keyboard().games_keyboard(random_string[j])
                else:
                    right_answer = list(sec_answer.values())[i]
                    for j in range(len(right_answer)):  # 输入正确答案
                        Keyboard().games_keyboard(right_answer[j])

                self.common.judge_next_is_true_false('true')
                self.common.next_btn().click()
                finish_word = self.input_word()
                print('解释：', self.explain())
                print('我的答案：', finish_word)
                mine_answer[self.explain()] = finish_word
                if fq == 1:
                    print('正确答案：', self.answer_word())
                else:
                    print('正确答案：', finish_word)
                self.click_voice()
                timer.append(self.common.bank_time())
                print('-'*20, '\n')

                self.common.next_btn().click()
        self.common.judge_timer(timer)
        bank_answer = mine_answer if fq == 1 else sec_answer
        return bank_answer, total_num
