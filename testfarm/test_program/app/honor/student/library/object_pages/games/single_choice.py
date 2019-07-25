# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 9:25
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep


class SingleChoice(BasePage):
    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_single_choice_page(self):
        """单项选择页面检查点"""
        locator = (By.ID, "{}tv_char".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def question(self):
        """题目 """
        ele = self.driver.find_element_by_id("{}question".format(self.id_type()))
        return ele.text

    @teststep
    def opt_char(self):
        """选项字母"""
        ele = self.driver.find_elements_by_id('{}tv_char'.format(self.id_type()))
        return ele

    @teststep
    def opt_text(self):
        """选项文本"""
        ele = self.driver.find_elements_by_id('{}tv_item'.format(self.id_type()))
        return ele

    @teststep
    def right_choice(self):
        """正确选项内容"""
        ele = self.driver.find_element_by_xpath('//*[@content-desc="right"]/following-sibling::android.widget.TextView')
        return ele.text

    @teststep
    def single_choice_operate(self, fq, sec_answer):
        """单项选择做题操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            if self.wait_check_single_choice_page():
                self.common.judge_next_is_true_false('false')
                self.common.rate_judge(total_num, i)
                ques = self.question()
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

                self.common.judge_next_is_true_false('true')
                timer.append(self.common.bank_time())
                self.common.next_btn().click()
        self.common.judge_timer(timer)
        answer = mine_answer if fq == 1 else sec_answer
        return answer, total_num

