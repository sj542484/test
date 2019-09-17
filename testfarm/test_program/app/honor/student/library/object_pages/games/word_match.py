# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 10:32
# -------------------------------------------
import time
from math import ceil

from app.honor.student.games.word_match_new import LinkWordNewGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage

from conf.decorator import teststeps, teststep


class LibraryWordMatch(LinkWordNewGame, LibraryPubicPage):

    @teststeps
    def word_match_operate(self, fq, sec_answer):
        """连连看游戏过程"""
        if fq == 2:
            pass
        elif fq == 1:
            timer = []
            tips = []
            index = 0
            total_num = self.rest_bank_num()
            turns = ceil(total_num/5)
            mine_answer = {}
            for i in range(turns):                          # 获取连连看页数 5个单词占一页
                if self.wait_check_word_match_page():
                    english_card = self.get_english_cards()     # 英文序列
                    for en in english_card:
                        word = self.get_word_text_by_img(en)
                        print(word)
                        if word not in tips:
                            tips.append(word)
                        en.click()
                        self.rate_judge(total_num, index)
                        rest_num = self.rest_bank_num()
                        time_str = self.bank_time()
                        hans_card = self.get_not_selected_hans_card()
                        if len(hans_card) != 1:
                            for ch in hans_card:
                                explain = self.get_word_text_by_img(ch)
                                ch.click()
                                if rest_num != 1:
                                    if self.rest_bank_num() == rest_num - 1:
                                        index = index + 1
                                        self.rate_judge(total_num, index)
                                        mine_answer[len(tips)] = word
                                        print('中文：', explain)
                                        print('英文：', word)
                                        print('-'*20, '\n')
                                        timer.append(time_str)
                                        break
                                    else:
                                        en.click()
                        else:
                            explain = self.get_word_text_by_img(hans_card[0])
                            mine_answer[len(tips)] = word
                            print('中文：', explain)
                            print('英文：', word)
                            print('-' * 20, '\n')
                            timer.append(time_str)
                            hans_card[0].click()
                time.sleep(3)
            self.judge_timer(timer)
            time.sleep(2)
            answer = mine_answer if fq == 1 else sec_answer
            print(answer)
            return answer, total_num

