import random
import re
import string
from app.honor.student.games.word_spell import SpellWordGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep
from utils.games_keyboard import Keyboard


class WordSpell(SpellWordGame):

    def __init__(self):
        self.answer = AnswerPage()


    def play_word_spell_game(self, num, exam_json):
        """单词拼写 """
        exam_json['单词拼写'] = bank_json = {}
        alphas = random.sample(string.ascii_lowercase, 26)
        for i in range(num):
            if self.wait_check_normal_spell_page():
                explain = self.word_explain()
                print('解释：', explain)
                length = random.randint(3, 5)
                for j in range(length):
                    Keyboard().games_keyboard(alphas[random.randint(0, len(alphas)-1)])

                word = self.spell_word()[::2]
                print('拼写的单词：', word)
                bank_json[explain] = word
                self.answer.skip_operator(i, num, '单词拼写', self.wait_check_normal_spell_page,
                                          self.judge_tip_status, word)
            elif self.wait_check_tv_word_or_random_page():
                explain = self.word_explain()
                print('解释：', explain)

                input_count = len(re.findall(r'_', self.spell_word()))
                for x in range(input_count):
                    Keyboard().games_keyboard(random.choice(string.ascii_lowercase))
                word = self.spell_word()[1::2]
                print('拼写的单词：', word)
                bank_json[explain] = word
                self.answer.skip_operator(i, num, '单词拼写', self.wait_check_tv_word_or_random_page,
                                          self.judge_tip_status, word)
                print('--------------------------------\n')

    @teststep
    def judge_tip_status(self, word):
        if self.wait_check_normal_spell_page() or self.wait_check_tv_word_or_random_page():
            finish_word = self.spell_word()[::2]
            if finish_word != word:
                print('★★★ Error-- 题目跳转回来后拼写单词发生改变')
            else:
                print('题目跳转回来后拼写单词未发生改变')


