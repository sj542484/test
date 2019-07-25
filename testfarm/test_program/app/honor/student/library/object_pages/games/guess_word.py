# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 9:58
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class GuessWord(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_guess_word_page(self):
        """"""
        locator = (By.ID, 'level')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x:x.find_element(*locator))
            return True
        except:
            return False

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
    def play_guess_game_operate(self, fq, sec_answer):
        """猜词游戏过程"""
        timer = []
        mine_answers = {}

        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            self.common.rate_judge(total_num, i)
            explain = self.chinese()
            print('解释：', explain)
            count = self.common.rest_bank_num()
            if fq == 1:
                mine_input = []
                if i != total_num - 1:
                    for x in self.key():
                        mine_input.append(x.text)
                        x.click()
                        if self.common.rest_bank_num() != count:
                            mine_answers[explain] = ''.join(mine_input)
                            break
                else:
                    for x in self.key():
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
            for k in self.key():
                if x == k.text:
                    k.click()
                    break
