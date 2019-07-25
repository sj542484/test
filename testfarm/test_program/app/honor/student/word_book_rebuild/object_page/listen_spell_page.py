#!/usr/bin/env python
# code:UTF-8
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.utils.games_keyboard import Keyboard


class ListenSpellWordPage(BasePage):
    """单词听写"""
    def __init__(self):
        self.homework = Homework()
        self.key = Keyboard()

    @teststep
    def wait_check_word_dictation_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "点击喇叭听写单词")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_answer_word_page(self):
        """判断 答案是否展示"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def input_word(self):
        """展示的Word  点击喇叭听写单词"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        word = ele[::2]
        return word

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def question(self):
        """展示的翻译"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        print('解释：%s'%explain)
        return explain

    @teststep
    def correct(self):
        """展示的答案"""
        correct_word = self.driver \
            .find_element_by_id(self.id_type() + "tv_answer").text
        print("正确答案：%s" % correct_word)
        return correct_word

    @teststep
    def explain(self):
        """解释"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain")
        return ele
    
    @teststeps
    def listen_spell_operate(self, bank_count, new_explain_words):
        """《单词听写》 游戏过程"""
        print('\n单词听写模式(新词)\n')

        answer_word = []
        for x in range(bank_count*2):
            self.homework.next_button_operate('false')  # 下一题 按钮 判断加 点击操作
            self.click_voice()  # 点击播放按钮
            if not answer_word:    # 数组为空，说明上一题已回答正确，本题需随机填入字母以获取正确答案
                self.key.games_keyboard(random.choice(string.ascii_lowercase))  # 随机输入一个小写字母
                mine_input = self.input_word()  # 输入的答案
                self.homework.next_button_operate('true')
                if self.wait_check_answer_word_page():  # 判断正确答案是否存在
                    correct_ans = self.correct()  # 获取正确答案
                    answer_word.append(correct_ans)
                    explain = self.explain()
                    explain_id = explain.get_attribute('contentDescription')
                    if explain_id in new_explain_words:
                        print('★★★ 此单词为新释义，不应出现单词听写游戏')
                    print('解释：', explain.text)
                    print('我输入的答案：', mine_input)
                    print('正确答案为:', correct_ans)
                else:
                    print("★★★ Error - 未显示正确答案")

            else:   # 数组长度为1，说明已获取正确答案，直接输入正确答案即可
                for alpha in list(answer_word[0]):
                    self.key.games_keyboard(alpha.upper())   # 输入单词的大写字母

                print('我输入的单词：', answer_word[0].upper())
                self.homework.next_button_operate('true')      # 提交 判断加 点击操作
                if self.input_word() != answer_word[0].lower():
                    print('★★★ 输入单词大写后，点击确定，单词未变为小写字母')

                if self.wait_check_answer_word_page():  # 判断正确答案是否出现
                    print("★★★ Error -听写正确却显示正确答案")
                explain = self.explain()
                explain_id = explain.get_attribute('contentDescription')
                if explain_id in new_explain_words:
                    print('★★★ 此单词为新释义，不应出现单词听写游戏')
                print('解释：', explain.text)
                print('回答正确！')
                answer_word.clear()

            self.homework.next_button_operate('true')  # 下一题
            print('-'*30, '\n')



