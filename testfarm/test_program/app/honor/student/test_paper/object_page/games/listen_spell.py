import random
import string
from app.honor.student.games.word_listen_spell import ListenSpellGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard


class ListenSpell(ListenSpellGame):

    def __init__(self):
        self.answer = AnswerPage()

    @teststeps
    def play_listen_spell_game(self, num, exam_json):
        """单词听写 """
        exam_json['单词听写'] = bank_json = {}
        alphas = random.sample(string.ascii_lowercase, 26)
        for i in range(num):
            self.click_voice()
            length = random.randint(3, 6)
            for j in range(length):
                index = random.randint(0, len(alphas)-1)
                Keyboard().games_keyboard(alphas[index])
            finish_word = self.input_word()
            print('听写答案：', finish_word)
            bank_json[i] = finish_word
            self.answer.skip_operator(i, num, '单词听写', self.wait_check_listen_spell_word_page,
                                      self.judge_tip_status, finish_word)

            print('--------------------------------\n')

    @teststep
    def judge_tip_status(self, word):
        finish_word = self.input_word()
        if finish_word != word:
            print('★★★ Error-- 题目跳转回来后拼写单词发生改变')
        else:
            print('题目跳转回来后拼写单词未发生改变')


