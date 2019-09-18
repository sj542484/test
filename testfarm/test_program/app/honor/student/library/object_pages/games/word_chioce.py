# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 14:18
# -------------------------------------------
import random
import time

from app.honor.student.games.choice_vocab import VocabChoiceGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from conf.decorator import teststeps


class WordChoice(VocabChoiceGame):
    """词汇选择"""
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def word_choice_operate(self, fq, first_result, half_exit):
        """词汇选择具体操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()  # 获取总题数
        bank_type = 1 if self.wait_check_head_page() else 2      # 区分听音选词和 选单词、选解释
        if fq == 2:                                               # 若为第二次做题，则给sec_answer 赋值
            if bank_type == 1:
                sec_answer = first_result[2]
            else:
                sec_answer = first_result[0]
        else:
            sec_answer = 0

        for i in range(total_num):
            time.sleep(1)
            self.next_btn_judge('false', self.fab_next_btn)  # 判断下一步按钮
            if bank_type == 2:
                self.listen_choice_speak_icon().click()
            elif bank_type == 1:
                print('问题：', self.vocab_question().text)

            if fq == 1:                              # 第一次选择 随机选择一个选项
                random_index = random.randint(0, len(self.vocab_options()) - 1)
                random_choice = self.vocab_options()[random_index]
                selected_opt = random_choice.text
                print('我的答案：', selected_opt)
                random_choice.click()
                if bank_type == 1:
                    mine_answer[self.vocab_question().text] = selected_opt
                else:
                    time.sleep(1)
                    explain = self.vocab_word_explain().text
                    mine_answer[explain] = selected_opt

            else:                              # 第二次(错题再练) 选择正确答案
                if bank_type == 1:
                    answer = sec_answer[self.vocab_question().text]
                else:
                    answer = list(sec_answer.keys())[i]

                print(answer)
                for x in self.vocab_options():
                    if x.text == answer:
                        print('我的答案：', x.text)
                        x.click()
                        break
            if i == 1 and fq == 1:                  # 判断中途是否需要退出
                if half_exit:
                    self.click_back_up_button()
                    break
            if fq == 1:
                print('正确答案：', self.vocab_right_answer())
            print('-'*20, '\n')

            timer.append(self.common.bank_time())    # 添加时间
            self.next_btn_operate('true', self.fab_next_btn)

        self.common.judge_timer(timer)                 # 判断做题时间
        answer = mine_answer if fq == 1 else sec_answer

        print('我的答案：', answer)
        return answer, total_num




