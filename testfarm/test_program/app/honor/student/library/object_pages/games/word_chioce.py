# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 14:18
# -------------------------------------------
import random
import re
import time

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.games.link_link import LibraryLinkLink
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class WordChoice(BasePage):
    """词汇选择"""
    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_title_page(self):
        """判断是否有题目"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_head")
            return True
        except:
            return False

    @teststep
    def question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_head')
        return ele.text

    @teststep
    def options(self):
        """选项"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'option')
        return ele

    @teststep
    def voice(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_sound')
        return ele

    @teststep
    def right_answer(self):
        """正确答案"""
        return [x.text for x in self.options() if x.get_attribute('contentDescription') == 'true'][0]

    @teststep
    def word_explain(self):
        """听音选词的单词解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'explain')
        return ele.text

    @teststeps
    def word_choice_operate(self, fq, first_result, half_exit):
        """词汇选择具体操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()  # 获取总题数
        bank_type = 1 if self.wait_check_title_page() else 2      # 区分听音选词和 选单词、选解释
        if fq == 2:                                               # 若为第二次做题，则给sec_answer 赋值
            sec_answer = first_result[2] if bank_type == 1 else first_result[0]
        else:
            sec_answer = 0

        for i in range(total_num):
            self.common.judge_next_is_true_false('false')  # 判断下一步按钮
            try:
                self.voice().click()           # 点击音频 (选单词模式没有声音按钮)
            except:
                pass

            if bank_type == 1:
                print('问题：', self.question())

            if fq == 1:                              # 第一次选择 随机选择一个选项
                random_index = random.randint(0, len(self.options()) - 1)
                random_choice = self.options()[random_index]
                selected_opt = random_choice.text
                print('我的答案：', selected_opt)
                random_choice.click()
                if self.wait_check_title_page():
                    mine_answer[self.question()] = selected_opt
                else:
                    mine_answer[self.word_explain()] = selected_opt

            else:                              # 第二次(错题再练) 选择正确答案
                if bank_type == 1:
                    answer = sec_answer[self.question()]
                else:
                    answer = list(sec_answer.values())[i]

                for x in self.options():
                    if x.text == answer:
                        x.click()
                        print('我的答案：', x.text)
                        break
            self.common.judge_next_is_true_false('true')
            if i == 1 and fq == 1:                  # 判断中途是否需要退出
                if half_exit:
                    self.click_back_up_button()
                    break

            print('正确答案：', self.right_answer())
            print('-'*20, '\n')
            timer.append(self.common.bank_time())    # 添加时间
            self.common.next_btn().click()
        self.common.judge_timer(timer)                 # 判断做题时间
        answer = mine_answer if fq == 1 else sec_answer

        print('我的答案：', answer)
        return answer, total_num




