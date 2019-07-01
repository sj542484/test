#!/usr/bin/env python
# code:UTF-8
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.student.homework.object_page.homework_page import Homework
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard


class WordDictation(BasePage):
    """单词听写"""
    def __init__(self):
        self.homework = Homework()
        self.key = Keyboard()

    @teststep
    def word(self):
        """展示的Word  点击喇叭听写单词"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        word = ele[::2]
        print('我的答案：%s' % word)
        return word

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice") \
            .click()

    # 下一步 按钮之后 答案页展示的答案
    @teststep
    def mine_answer(self):
        """展示的Word """
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        mine_ans = ele[::2]
        print("提交结果：%s" % mine_ans)
        return mine_ans

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
    def correct_judge(self):
        """判断 答案是否展示"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def result_explain(self):
        """解释"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return ele
    
    @teststeps
    def word_dictation(self, i, answer):
        """《单词听写》 游戏过程"""
        if i == 0:
            print('\n单词听写模式(新词)\n')

        self.homework.next_button_operate('false')  # 下一题 按钮 判断加 点击操作
        self.click_voice()  # 点击播放按钮

        if answer[0] == '':    # 数组为0，说明上一题已回答正确，本题需随机填入字母以获取正确答案
            alpha_list = [chr(i) for i in range(65, 91)]  # 生成小写字母表
            self.keyboard_operate(i, alpha_list[random.randint(0, 25)])  # 随机输入一个字母
            self.homework.next_button_operate('true')  # 提交 判断加 点击操作
            self.word()  # 输入的答案
            mine_ans = self.mine_answer()  # 提交后的答案
            if self.correct_judge():  # 判断正确答案是否存在
                correct_ans = self.correct()  # 获取正确答案
                self.result_explain()   # 解释
                if mine_ans != correct_ans:
                    answer[0] = correct_ans
                    print('答案不正确,正确答案为:', correct_ans)
            else:
                print("★★★ Error - 未显示正确答案")

        else:   # 数组长度为1，说明已获取正确答案，直接输入正确答案即可
            for j in range(0, len(answer[0])):
                self.keyboard_operate(j, answer[0][j])   #
            self.homework.next_button_operate('true')  # 提交 判断加 点击操作
            self.word()  # 填入的答案
            self.mine_answer()  # 提交后的答案
            if self.correct_judge():  # 判断正确答案是否出现
                print("★★★ Error -听写正确却显示正确答案")
            else:
                self.result_explain()  # 解释
                print('回答正确！')
                print('----------------------------------')

            answer[0] = ''

        self.homework.next_button_operate('true')  # 下一题

    @teststeps
    def keyboard_operate(self, j, value):
        """点击键盘 具体操作"""
        if j == 4:
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.key.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.key.games_keyboard(value)  # 点击键盘对应字母
