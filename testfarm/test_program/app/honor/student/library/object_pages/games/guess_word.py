# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 9:58
# -------------------------------------------
import random
import time

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class GuessWord(BasePage):

    def __init__(self):
        self.common = CommonPage()

    """猜词游戏"""
    @teststep
    def keyboard(self):
        """键盘"""
        ele = self.driver.find_element_by_id(self.id_type() + "hm_keyboard")
        return ele

    @teststep
    def key(self):
        ele = self.driver.find_elements_by_xpath('//*[@resource-id="{}hm_keyboard"]/'
                                                 'android.widget.TextView'.format(self.id_type()))
        return ele

    @teststep
    def chinese(self):
        """翻译"""
        ele = self.driver.find_element_by_id(self.id_type() + 'chinese')
        return ele.text

    @teststep
    def english(self):
        """单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'english')
        return ele

    @teststeps
    def play_guess_game_operate(self, fq, sec_answer, half_exit):
        timer = []
        mine_answers = {}
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            self.common.rate_judge(total_num, i)
            explain = self.chinese()
            try:
                if fq == 1:
                    self.error_operate(mine_answers, explain)
                else:
                    self.right_operate(sec_answer[explain].lower())
                timer.append(self.common.bank_time())
                time.sleep(3)

            except:
                self.click_back_up_button()
                break

            if i == 2:
                if half_exit:
                    self.click_back_up_button()
                    break

        self.common.judge_timer(timer)
        done_answer = mine_answers if fq == 1 else sec_answer
        print('我的答案：', done_answer)
        return done_answer, total_num

    @teststep
    def error_operate(self, mine_error_answers, explain):
        wrong, right = [], []
        mine_input = []
        for x in self.key():
            word = self.english().text
            if x.text in mine_input:
                continue
            else:
                mine_input.append(x.text)
                x.click()
                time.sleep(0.5)
                if x.text not in self.english().text:
                    wrong.append(x.text)

                if '_' not in word:
                    right_answer = word[1::2]
                    print('解释：', explain)
                    print('正确答案：', right_answer)
                    print('我输入的：', "".join(mine_input))
                    mine_error_answers[self.chinese()] = "".join(mine_input)

                    if len(wrong) > 6:
                        print('★★★ 单词完整出现时输入错误数大于6')
                    time.sleep(3)

                    break
        print('-'*20, '\n ')

    @teststep
    def right_operate(self, right_answer):
        print('正确答案：', right_answer, '\n')

        for x in right_answer:
            for k in self.key():
                if x == k.text:
                    k.click()
                    break
