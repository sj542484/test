# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/29 11:29
# -------------------------------------------
import random
import re
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard


class WordSpell(BasePage):
    """单词拼写"""
    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_spell_explain_page(self):
        """单词拼写页面检查点"""
        locator = (By.ID, self.id_type() + "tv_explain")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_hint_word_page(self):
        """提示字母页面检查点"""
        locator = (By.ID, self.id_type() + "tv_word")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_hint_page(self):
        """默写模式页面检查点"""
        locator = (By.ID, self.id_type() + "hint")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_answer_page(self):
        """提示字母页面检查点"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """翻译"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele.text

    @teststep
    def hint_btn(self):
        """提示按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'hint')
        return ele

    @teststep
    def spell_word(self):
        """完成的单词"""
        word = self.driver.find_element_by_id(self.id_type() + 'tv_word')
        return word.text.replace(' ', '')

    @teststep
    def answer_word(self):
        """答案单词 """
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return ele.text

    @teststeps
    def spell_word_operate(self, fq, sec_answer):
        """单词拼写具体步骤"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()        # 获取总题数
        for i in range(total_num):
            if self.wait_check_spell_explain_page():
                self.common.judge_next_is_true_false('false')        # 判断下一题按钮状态
                self.common.rate_judge(total_num, i)                 # 校验剩余题数
                explain = self.explain()
                print('解释：', explain)

                if self.wait_check_hint_word_page():
                    wait_spell_word = self.spell_word()[1:-1]
                    print('待填单词：', wait_spell_word)
                    if fq == 1:
                        print(len(re.findall(r'_', wait_spell_word)))
                        for x in range(len(re.findall(r'_', wait_spell_word))):
                            random_str = random.choice(string.ascii_lowercase)
                            Keyboard().games_keyboard(random_str)
                    else:
                        right_answer = list(sec_answer[explain])
                        for x in list(wait_spell_word.replace('_', '')):
                            right_answer.remove(x)
                        for y in right_answer:
                            Keyboard().games_keyboard(y)

                    self.common.next_btn().click()
                    mine_answer[explain] = self.spell_word()[1::2]
                    print('我的答案：', self.spell_word()[1::2])
                else:
                    if self.wait_check_hint_word_page():                # 校验点击提示或输入前, 是否出现单词
                        if self.spell_word() != '':
                            print('★★★ 未点击提示或未输入字符出现默写单词')
                    self.hint_btn().click()

                    if not self.wait_check_hint_word_page():          # 校验是否有提示字母
                        print('★★★ 未发现首字母提示！')

                    self.common.judge_next_is_true_false('true')      # 判断下一题按钮状态
                    if fq == 1:
                        random_length = random.randint(3, 5)              # 创建随机字母
                        random_string = ''.join(random.sample(string.ascii_letters, random_length))
                        mine_answer[explain] = random_string
                        for j in range(len(random_string)):              # 输入随机字母
                            Keyboard().games_keyboard(random_string[j])
                    else:
                        Keyboard().games_keyboard('backspace')
                        right_answer = sec_answer[explain]
                        for j in range(len(right_answer)):
                            Keyboard().games_keyboard(right_answer[j])

                    self.common.next_btn().click()
                    print('我的答案：', self.spell_word())

                if fq == 1:
                    if self.wait_check_answer_page():
                        print('正确答案：', self.answer_word())
                else:
                    print('正确答案：', sec_answer[explain])
                timer.append(self.common.bank_time())

                self.common.next_btn().click()
                print('-'*20, '\n')

        self.common.judge_timer(timer)           # 时间校验
        bank_answer = mine_answer if fq == 1 else sec_answer
        return bank_answer, total_num




