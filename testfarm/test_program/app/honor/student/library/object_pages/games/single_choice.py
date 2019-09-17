# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 9:25
# -------------------------------------------
import random
import time
from app.honor.student.games.choice_single import SingleChoiceGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from conf.decorator import teststep


class SingleChoice(SingleChoiceGame):
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststep
    def single_choice_operate(self, fq, sec_answer):
        """单项选择做题操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            if self.wait_check_single_choice_page():
                self.next_btn_judge('false', self.fab_next_btn)
                self.common.rate_judge(total_num, i)
                ques = self.question()[0].text
                print('问题：', ques)

                opt_char = self.opt_char()
                opt_text = self.opt_text()
                for j in range(len(opt_char)):
                    print(opt_char[j].text, '  ', opt_text[j].text)
                if fq == 1:
                    select_index = random.randint(0, len(opt_char) - 1)
                    select_choice = opt_text[select_index].text
                    opt_text[select_index].click()
                    time.sleep(1)
                    print('选择选项：', select_choice)
                    print('正确选项：', self.right_choice())
                    mine_answer[i+1] = select_choice
                else:
                    for x, opt in enumerate(opt_text):
                        if opt.text == sec_answer[i+1]:
                            self.opt_char()[x].click()
                            break
                    print('选择正确选项：', sec_answer[i+1])

                print('-'*20, '\n')
                timer.append(self.common.bank_time())
                self.next_btn_operate('true', self.fab_next_btn)
        self.common.judge_timer(timer)
        answer = mine_answer if fq == 1 else sec_answer
        return answer, total_num

