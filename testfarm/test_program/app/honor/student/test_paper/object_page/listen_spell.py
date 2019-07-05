import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.test_paper.object_page.answer_page import AnswerPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard


class ListenSpell(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_listen_spell_word_page(self):
        locator = (By.ID, self.id_type() + "tv_word")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def finish_word(self):
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

    @teststeps
    def play_listen_spell_game(self, num, exam_json):
        """单词听写 """
        exam_json['单词听写'] = bank_json = {}
        alphas = random.sample(string.ascii_lowercase, 26)
        for i in range(num):
            self.click_voice()
            self.homework.next_button_judge('false')
            length = random.randint(3, 6)
            for j in range(length):
                index = random.randint(0, len(alphas)-1)
                Keyboard().games_keyboard(alphas[index])
            finish_word = self.finish_word()
            print('听写答案：', finish_word)
            bank_json[i] = finish_word
            self.answer.skip_operator(i, num, '单词听写', self.wait_check_listen_spell_word_page,
                                      self.judge_tip_status, finish_word)

            print('--------------------------------\n')

    @teststep
    def judge_tip_status(self, word):
        finish_word = self.finish_word()
        if finish_word != word:
            print('★★★ Error-- 题目跳转回来后拼写单词发生改变')
        else:
            print('题目跳转回来后拼写单词未发生改变')


