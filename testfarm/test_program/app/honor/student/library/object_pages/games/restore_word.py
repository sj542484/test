# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 16:05
# -------------------------------------------
import time
from app.honor.student.games.word_restore import RestoreWordGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from conf.decorator import teststeps


class RestoreWord(RestoreWordGame):
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def restore_word_operate(self, fq, sec_answer):
        """还原单词错误操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            if self.wait_restore_word_explain_page():
                self.common.rate_judge(total_num, i)
                explain = self.word_explain().text
                print('解释：', explain)
                self.next_btn_judge('false', self.fab_commit_btn)
                word_alpha = self.word_alpha()
                word = []
                for char in word_alpha:
                    word.append(char.text)
                print('还原前单词：', ''.join(word))
                if fq == 1:
                    self.drag_operate(word_alpha[0], word_alpha[-1])
                    finish_word = [x.text for x in self.word_alpha()]
                    print('还原后单词：', ''.join(finish_word))
                    mine_answer[explain] = ''.join(finish_word)
                    self.next_btn_operate('true', self.fab_commit_btn)
                    if i != total_num - 1:
                        print('正确答案：', self.word_alpha()[0].text)
                    self.fab_next_btn().click()
                else:
                    self.right_restore_word_core(sec_answer[explain])
                    self.next_btn_operate('true', self.fab_next_btn)

                if i != total_num - 1:
                    timer.append(self.common.bank_time())
                time.sleep(2)
                print('-' * 20, '\n')
        self.common.judge_timer(timer)
        done_answer = mine_answer if fq == 1 else sec_answer
        return done_answer, total_num


    @teststeps
    def right_restore_word_core(self, english):
        """还原单词主要步骤"""
        index = 0
        count = 0
        sort_word = ''
        while True:
            alphas = self.word()
            for x in range(count, len(alphas)):
                alpha_len = len(alphas[x].text)
                if index + alpha_len >= len(english) - 1:
                    english += ' ' * alpha_len
                word_part = ''.join([english[x] for x in range(index, index + alpha_len)])

                if alphas[x].text == word_part.strip():
                    if count != x:
                        self.drag_operate(alphas[x], alphas[count])
                        sort_word = ''.join([k.text for k in self.word()])
                    index += alpha_len
                    count += 1
                    break
            if english.strip() == sort_word:
                print('还原后单词', sort_word)
                break


