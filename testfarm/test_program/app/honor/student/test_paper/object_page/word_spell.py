import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.test_paper.object_page.answer_page import AnswerPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.utils.games_keyboard import Keyboard


class WordSpell(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_spell_explain_page(self):
        locator = (By.ID, self.id_type() + "tv_explain")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """翻译"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele.text

    @teststep
    def title(self):
        """词汇选择 的单词"""
        ele = self.driver.find_element_by_id(self.id_type() + "tv_head")
        return ele.text

    @teststep
    def finish_word(self):
        """完成的单词"""
        word = self.driver.find_element_by_id(self.id_type() + 'tv_word')
        return word.text

    def play_word_spell_game(self, num, exam_json):
        """单词拼写 """
        exam_json['单词拼写'] = bank_json = {}
        alphas = random.sample(string.ascii_lowercase, 26)
        for i in range(num):
            if self.wait_check_spell_explain_page():
                self.homework.next_button_judge('false')
                explain = self.explain()
                print('解释：', explain)
                length = random.randint(3, 7)

                for j in range(length):
                    Keyboard().games_keyboard(alphas[random.randint(0, len(alphas)-1)])

                word = self.finish_word()
                print('拼写的单词：', word[::2])
                bank_json[explain] = word[::2]
                self.answer.skip_operator(i, num, '单词拼写', self.wait_check_spell_explain_page,
                                          self.judge_tip_status, word)
                print('--------------------------------\n')

    @teststep
    def judge_tip_status(self, word):
        if self.wait_check_spell_explain_page():
            finish_word = self.finish_word()
            if finish_word != word:
                print('★★★ Error-- 题目跳转回来后拼写单词发生改变')
            else:
                print('题目跳转回来后拼写单词未发生改变')


