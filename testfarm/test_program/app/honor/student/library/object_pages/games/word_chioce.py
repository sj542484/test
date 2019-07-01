# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 14:18
# -------------------------------------------
import random

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.basepage import BasePage
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
        ele = self.driver.find_element_by_accessibility_id('true')
        return ele.text

    @teststeps
    def word_choice_operate(self, fq, sec_answer, half_exit):
        """词汇选择具体操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()  # 获取总题数
        for i in range(total_num):
            if self.wait_check_title_page():
                self.common.judge_next_is_true_false('false')       # 判断下一步按钮
                self.voice().click()                               # 点击音频
                question = self.question()                         # 选项问题
                print('问题：', self.question())
                if fq == 1:                              # 第一次选择 随机选择一个选项
                    random_index = random.randint(0, len(self.options()) - 1)
                    random_choice = self.options()[random_index]
                    selected_opt = random_choice.text
                    print('我的答案：', selected_opt)
                    mine_answer[question] = selected_opt
                    random_choice.click()
                else:                              # 第二次(错题再练) 选择正确答案
                    answer = sec_answer[question]
                    for x in self.options():
                        if x.text == answer:
                            x.click()
                            break
                self.common.judge_next_is_true_false('true')

                if i == 2:                  # 判断中途是否需要退出
                    if half_exit and fq == 1:
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




