# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 16:05
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class RestoreWord(BasePage):
    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_restore_word_explain_page(self):
        """还原单词页面检查点"""
        locator = (By.ID, self.id_type() + "tv_prompt")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele.text

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def word(self):
        """展示的 待还原的单词"""
        word = self.driver.find_elements_by_xpath('//android.widget.TextView['
                                                  '@resource-id="com.vanthink.student.debug:id/tv_word" and @index=0]')
        return word


    @teststep
    def voice(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_sound')
        return ele

    @teststep
    def button_swipe(self, from_x, from_y, to_x, to_y, steps=1000):
        """拖动单词button"""
        self.driver.swipe(from_x, from_y, to_x, to_y, steps)

    @teststep
    def get_element_location(self, ele):
        """获取元素坐标"""
        x = ele.location['x']
        y = ele.location['y']
        return x, y

    @teststeps
    def drag_operate(self, word2, word):
        """拖拽 操作"""
        loc = self.get_element_location(word2)
        y2 = self.get_element_location(word)[1] - 40
        self.button_swipe(loc[0], loc[1], loc[0], y2, 1000)
        time.sleep(1)

    @teststep
    def restore_word_operate(self, fq, sec_answer, half_exit):
        """还原单词错误操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            if self.wait_restore_word_explain_page():
                self.common.rate_judge(total_num, i)
                explain = self.explain()
                print('解释：', explain)
                self.common.judge_next_is_true_false('false')
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
                    self.common.judge_next_is_true_false('true')
                    self.common.next_btn().click()
                    if i != total_num - 1:
                        print('正确答案：', self.word_alpha()[0].text)
                    self.common.next_btn().click()
                else:
                    self.right_restore_word_core(sec_answer[explain])
                    self.common.judge_next_is_true_false('true')
                    print('正确答案：', self.word_alpha()[0].text)

                if i != total_num - 1:
                    timer.append(self.common.bank_time())

                if i == 2:
                    if half_exit:
                        self.click_back_up_button()
                        break
                time.sleep(2)
                print('-' * 20, '\n')
        self.common.judge_timer(timer)
        done_answer = mine_answer if fq == 1 else sec_answer
        return done_answer, total_num


    @teststep
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


