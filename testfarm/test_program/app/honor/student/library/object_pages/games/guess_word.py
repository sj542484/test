# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 9:58
# -------------------------------------------
import time

from testfarm.test_program.app.honor.student.games.word_guess import GuessWordGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.conf.decorator import teststep, teststeps


class GuessWord(GuessWordGame):

    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def play_guess_game_operate(self, fq, sec_answer):
        """猜词游戏过程"""
        timer = []
        mine_answers = {}

        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            self.common.rate_judge(total_num, i)
            explain = self.word_explain()
            print('解释：', explain)
            count = self.common.rest_bank_num()
            if fq == 1:
                mine_input = []
                if i != total_num - 1:
                    for x in self.keyboard_key():
                        mine_input.append(x.text)
                        x.click()
                        if self.common.rest_bank_num() != count:
                            mine_answers[explain] = ''.join(mine_input)
                            break
                else:
                    for x in self.keyboard_key():
                        mine_input.append(x.text)
                        x.click()
                        if not self.wait_check_guess_word_page():
                            mine_answers[explain] = ''.join(mine_input)
                            break
                print('我的答案:', ''.join(mine_input))

            else:
                self.right_operate(sec_answer[explain].lower())

            if i != total_num - 1:
                timer.append(self.common.bank_time())
            time.sleep(3)
            print('-'*30, '\n')
        self.common.judge_timer(timer)
        done_answer = mine_answers if fq == 1 else sec_answer
        print('我的答案：', done_answer)
        return done_answer, total_num

    @teststep
    def right_operate(self, right_answer):
        print('正确答案：', right_answer, '\n')
        for x in right_answer:
            for k in self.keyboard_key():
                if x == k.text:
                    k.click()
                    break
