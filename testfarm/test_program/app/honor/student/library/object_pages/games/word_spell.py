# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 11:29
# -------------------------------------------
import random
import re
import string
from testfarm.test_program.app.honor.student.games.word_spell import SpellWordGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.conf.decorator import teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard


class WordSpell(SpellWordGame):
    """单词拼写"""
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def spell_word_operate(self, fq, sec_answer):
        """单词拼写具体步骤"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()        # 获取总题数
        for i in range(total_num):
            self.next_btn_judge('false', self.fab_commit_btn)  # 判断下一题按钮状态
            self.common.rate_judge(total_num, i)  # 校验剩余题数
            explain = self.word_explain().text
            print('解释：', explain)
            if self.wait_check_tv_word_or_random_page():
                wait_spell_word = self.spell_word()[1::2]
                print('待填单词：', wait_spell_word)
                input_count = len(re.findall(r'_', wait_spell_word))

                if fq == 1:
                    for x in range(input_count):
                        random_str = random.choice(string.ascii_lowercase)
                        Keyboard().games_keyboard(random_str)
                else:
                    right_answer = list(sec_answer[explain])
                    print('正确答案：', right_answer)
                    print('页面字符：', wait_spell_word.replace('_', ''))
                    for x in list(wait_spell_word.replace('_', '')):
                        right_answer.remove(x)
                    for y in right_answer:
                        Keyboard().games_keyboard(y)

                self.next_btn_operate('true', self.fab_commit_btn)  # 判断下一题按钮状态
                finish_answer = self.spell_word()[1::2]
                mine_answer[explain] = finish_answer
                print('我的答案：', finish_answer)
            else:
                if self.wait_check_hint_word_page():                # 校验点击提示或输入前, 是否出现单词
                    print('★★★ 未点击提示或未输入字符出现默写单词')
                self.hint_btn().click()
                if not self.wait_check_hint_word_page():          # 校验是否有提示字母
                    print('★★★ 未发现首字母提示！')

                self.next_btn_judge('true', self.fab_commit_btn)  # 判断下一题按钮状态
                if fq == 1:
                    random_length = random.randint(3, 5)              # 创建随机字母
                    random_string = ''.join(random.sample(string.ascii_letters, random_length))
                    mine_answer[explain] = random_string
                    for j in range(len(random_string)):              # 输入随机字母
                        Keyboard().games_keyboard(random_string[j])
                else:
                    Keyboard().games_keyboard('backspace')
                    right_answer = sec_answer[explain]
                    for j in range(len(right_answer)):
                        Keyboard().games_keyboard(right_answer[j])

                self.next_btn_operate('true', self.fab_commit_btn)  # 判断下一题按钮状态
                print('我的答案：', self.spell_word()[1::2])

            if fq == 1:
                if self.wait_check_right_answer_page():
                    print('正确答案：', self.right_answer_word())
            else:
                print('正确答案：', sec_answer[explain])
            timer.append(self.common.bank_time())

            self.fab_next_btn().click()
            print('-'*20, '\n')

        self.common.judge_timer(timer)           # 时间校验
        bank_answer = mine_answer if fq == 1 else sec_answer
        return bank_answer, total_num




