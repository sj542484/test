# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 10:32
# -------------------------------------------
import time
from math import ceil
from testfarm.test_program.app.honor.student.games.word_match import LinkWordGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage

from testfarm.test_program.conf.decorator import teststeps


class LibraryWordMatch(LinkWordGame):
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def word_match_operate(self, fq, sec_answer):
        """连连看游戏过程"""
        timer = []
        index = 0
        total_num = self.common.rest_bank_num()
        mine_answer = {}
        for i in range(ceil(total_num/5)):                          # 获取连连看页数 5个单词占一页
            if self.wait_check_word_match_page():
                english_card = self.get_english_cards()     # 英文序列
                for en in english_card:
                    en.click()
                    self.common.rate_judge(total_num, index)
                    rest_num = self.common.rest_bank_num()
                    time_str = self.common.bank_time()
                    hans_card = self.get_not_selected_hans_card()
                    if len(hans_card) != 1:
                        for ch in hans_card:
                            ch.click()
                            if rest_num != 1:
                                if self.common.rest_bank_num() == rest_num - 1:
                                    index = index + 1
                                    self.common.rate_judge(total_num, index)
                                    mine_answer[ch.text] = en.text
                                    print('中文：', ch.text)
                                    print('英文：', en.text)
                                    print('-'*20, '\n')
                                    timer.append(time_str)
                                    break
                                else:
                                    en.click()
                    else:
                        mine_answer[hans_card[0].text] = en.text
                        print('中文：', hans_card[0].text)
                        print('英文：', en.text)
                        print('-' * 20, '\n')
                        timer.append(time_str)
                        hans_card[0].click()
        self.common.judge_timer(timer)
        time.sleep(2)
        answer = mine_answer if fq == 1 else sec_answer
        return answer, total_num


