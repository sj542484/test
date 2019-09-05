# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 13:48
# -------------------------------------------
import random
import string
from testfarm.test_program.app.honor.student.games.word_listen_spell import ListenSpellGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.conf.decorator import teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard


class ListenSpell(ListenSpellGame):
    """单词听写"""
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def listen_spell_operate(self, fq, sec_answer):
        """单词听写具体操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()  # 获取总题数

        for i in range(total_num):
            if self.wait_check_listen_spell_word_page():
                self.next_btn_judge('false', self.fab_commit_btn)
                if self.input_word() != '点喇听单':
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

                self.next_btn_operate('true', self.fab_commit_btn)
                finish_word = self.input_word()
                print('解释：', self.word_explain().text)
                print('我的答案：', finish_word)
                mine_answer[self.word_explain().text] = finish_word
                if fq == 1:
                    print('正确答案：', self.input_word())
                else:
                    print('正确答案：', finish_word)
                self.click_voice()
                timer.append(self.common.bank_time())
                print('-'*20, '\n')

                self.fab_next_btn().click()
        self.common.judge_timer(timer)
        bank_answer = mine_answer if fq == 1 else sec_answer
        return bank_answer, total_num
