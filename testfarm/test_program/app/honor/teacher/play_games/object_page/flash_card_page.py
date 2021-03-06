#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from utils.games_keyboard import Keyboard
from utils.click_bounds import ClickBounds
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class FlashCard(BasePage):
    """闪卡练习"""
    voice_button_value = gv.PACKAGE_ID + "play_voice"
    finish_study_value = "//android.widget.TextView[contains(@text,'完成学习')]"

    def __init__(self):
        self.get = GetAttribute()
        self.key = Keyboard()
        self.sp = SwipeFun()
        self.hw = Homework()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=10):
        """以“title:闪卡练习”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_star")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def judge_img_exist(self, var=3):
        """ 图片是否存在"""
        locator = (By.ID, gv.PACKAGE_ID + "img")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def click_star(self):
        """闪卡练习页面内 标星按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "iv_star") \
            .click()

    @teststep
    def click_voice(self):
        """闪卡练习页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.voice_button_value) \
            .click()

    # 以下为学习模式 特有元素
    @teststep
    def english_study(self):
        """Word"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_english").text
        return word

    @teststep
    def explain_study(self):
        """翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_chinese").text
        return word

    @teststep
    def pattern_switch(self):
        """闪卡练习页面内  全英/英汉模式切换 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "side")\
            .click()
        time.sleep(1)

    # 英汉模式 的例句
    @teststeps
    def wait_check_sentence_page(self, var=10):
        """以“例句”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "sentence")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_explain_page(self, var=10):
        """以“例句解释”的ID为依据"""
        locator = (By.XPATH, gv.PACKAGE_ID + "sentence_explain")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def sentence_study(self):
        """例句"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "sentence").text
        print('例句:', word)

    @teststep
    def sentence_explain_study(self):
        """例句翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "sentence_explain").text
        print('例句解释:', word)

    @teststep
    def sentence_author_study(self):
        """例句 提供老师"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "author").text
        print(word)

    @teststeps
    def click_blank(self):
        """点击空白处"""
        ClickBounds().click_bounds(430, 800)
        print('点击空白处，切换双页面:')
        time.sleep(1)

    # 以下为抄写模式 特有元素
    @teststep
    def word_copy(self):
        """闪卡练习- 抄写模式 内展示的Word"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "english")
        return ele.text

    @teststep
    def english_copy(self):
        """单页面内 答题框填入的Word"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "mine_word")
        return word

    @teststep
    def explain_copy(self):
        """闪卡练习内展示的翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "chinese").text
        return word

    # 以下为闪卡练习 结果页
    @teststeps
    def wait_check_result_page(self, var=10):
        """以“title:答题报告”的ID为依据"""
        locator = (By.XPATH, self.finish_study_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def finish_study(self):
        """完成学习"""
        ele = self.driver \
            .find_element_by_xpath(self.finish_study_value).text
        print(ele)
        return ele

    @teststeps
    def study_sum(self):
        """eg: study_sum:6个内容,0标记★;抄写模式"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "study_sum").text
        print(ele)
        return ele

    @teststep
    def study_again_button(self):
        """再练一遍"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "textView") \
            .click()

    @teststep
    def star_again_button(self):
        """标星内容再练一遍"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_star_en") \
            .click()

    @teststeps
    def wait_check_result_list_page(self, var=10):
        """以“title:答题报告”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_select")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def star_button(self):
        """五星按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_select")
        return ele

    @teststep
    def voice_button(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_voice")[index] \
            .click()

    @teststep
    def result_word(self):
        """展示的Word"""
        ele = self.driver.find_elements_by_id(gv.PACKAGE_ID + "tv_word")
        return ele

    @teststep
    def result_explain(self):
        """展示的  解释"""
        word = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_explain")
        return word

    @teststeps
    def word_study_pattern(self):
        """《闪卡练习 单词学习模式》 游戏过程"""
        if self.wait_check_page():
            if self.hw.wait_check_play_page():
                answer = []   # return值 与结果页内容比对

                rate = self.hw.rate()
                for i in range(int(rate)):
                    if self.hw.wait_check_play_page():
                        print('------------------------------------')
                        self.hw.rate_judge(rate, i)  # 测试当前rate值显示是否正确
                        self.hw.next_button_judge('true')  # 下一题 按钮 状态判断
                        if self.judge_img_exist():
                            print('存在图片')
                            self.sp.swipe_vertical(0.5, 0.8, 0.2)

                        if self.hw.wait_check_play_page():
                            self.voice_operation(i)  # 发音按钮

                            if i in (2, 5):  # 第3、6题  进入全英模式
                                self.pattern_switch()  # 切换到 全英模式
                                print('---切换到 全英模式:')
                                if self.wait_check_sentence_page(5):
                                    self.sentence_study()  # 例句
                                    self.sentence_author_study()  # 例句作者

                                word = self.english_study()  # 单词
                                print('单词:%s' % word)

                                self.pattern_switch()  # 切换到 英汉模式
                            else:
                                if self.wait_check_explain_page(5):
                                    self.sentence_study()  # 例句
                                    self.sentence_explain_study()  # 例句解释
                                    self.sentence_author_study()  # 例句作者

                                word = self.english_study()  # 单词
                                explain = self.explain_study()  # 解释
                                print('单词:%s \n 解释:%s' % (word, explain))

                            answer.append(self.english_study())

                            if i in range(1, 9, 2):  # 点击star按钮
                                self.click_star()
                                # if i == 1:
                                #     self.tips_operation()

                            if i == 3 and i != int(rate) - 1:  # 第四题 滑屏进入下一题
                                self.sp.swipe_horizontal(0.5, 0.9, 0.1)
                            else:
                                if i == int(rate) - 1:  # 最后一题 尝试滑屏进入结果页
                                    self.sp.swipe_horizontal(0.5, 0.9, 0.1)
                                    if self.wait_check_result_page(5):
                                        print('★★★ Error - 滑动页面进入了结果页')

                                self.hw.next_button_operation('true')  # 下一题 按钮 状态判断 加点击
                            time.sleep(2)

                print('=================================================')
                return rate, answer

    @teststeps
    def word_copy_pattern(self):
        """《闪卡练习 单词抄写模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.hw.wait_check_play_page():
                answer = []  # return值 与结果页内容比对
                rate = self.hw.rate()
                for i in range(int(rate)):
                    if self.hw.wait_check_play_page():
                        print('-------------------------------------------')
                        self.hw.rate_judge(rate, i)  # 测试当前rate值显示是否正确
                        if self.judge_img_exist():
                            print('存在图片')
                            self.sp.swipe_horizontal(0.5, 0.9, 0.1)

                        if self.hw.wait_check_play_page():
                            word = self.word_copy()  # 题目  展示的Word
                            explain = self.explain_copy()  # 解释
                            answer.append(word)
                            print("第%s题,单词:%s\n 解释:%s" % (i+1, word, explain))
                            self.voice_operation(i)  # 发音按钮

                            self.english_copy().click()  # 点击输入框，激活小键盘
                            for j in range(len(word)):
                                if word[j] == ' ':
                                    self.click_blank_operation()  # 多次点击空格键 操作
                                else:
                                    if i == 1:  # 单词输入字母错误时
                                        print('---输入错误单词字母：q')
                                        self.key.games_keyboard('q')  # 点击键盘 错误单词字母
                                    else:
                                        if j == 5:
                                            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                                            self.key.games_keyboard(word[j].upper())  # 点击键盘对应 大写字母
                                        else:
                                            if j == 6:
                                                self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                                            self.key.games_keyboard(word[j].lower())  # 点击键盘对应字母

                            self.delete_incorrect_word(i, rate, word)  # 删除错误单词后重新输入
                            if i in range(1, 2, 9):  # 点击star按钮
                                self.click_star()

                    time.sleep(4)
                print('=================================================')
                return rate, answer

    @teststeps
    def sentence_study_pattern(self):
        """《闪卡练习 句子学习模式》 游戏过程"""
        if self.wait_check_page():
            if self.hw.wait_check_play_page():
                answer = []   # return值 与结果页内容比对

                rate = self.hw.rate()
                for i in range(int(rate)):
                    if self.hw.wait_check_play_page():
                        print('------------------------------------')
                        self.hw.rate_judge(rate, i)  # 测试当前rate值显示是否正确
                        self.hw.next_button_judge('true')  # 下一题 按钮 状态判断

                        self.voice_operation(i)  # 发音按钮

                        if i in (0, 3):  # 第3、6题  进入全英模式
                            self.pattern_switch()  # 切换到 全英模式
                            print('---切换到 全英模式:')
                            if self.wait_check_sentence_page(5):
                                self.sentence_study()  # 例句
                                self.sentence_author_study()  # 例句作者

                            word = self.english_study()  # 单词
                            print('单词:%s' % word)

                            self.pattern_switch()  # 切换到 英汉模式
                        else:
                            if self.wait_check_explain_page(5):
                                self.sentence_study()  # 例句
                                self.sentence_explain_study()  # 例句解释
                                self.sentence_author_study()  # 例句作者

                            word = self.english_study()  # 单词
                            explain = self.explain_study()  # 解释
                            print('单词:%s \n 解释:%s' % (word, explain))

                        answer.append(self.english_study())

                        if i in range(0, 3):  # 点击star按钮
                            self.click_star()
                            # if i == 1:
                            #     self.tips_operation()

                        if i == 3 and i != int(rate) - 1:  # 第四题 滑屏进入下一题
                            self.sp.swipe_horizontal(0.5, 0.9, 0.1)
                        else:
                            if i == int(rate) - 1:  # 最后一题 尝试滑屏进入结果页
                                self.sp.swipe_horizontal(0.5, 0.9, 0.1)
                                if self.wait_check_result_page(5):
                                    print('★★★ Error - 滑动页面进入了结果页')

                            self.hw.next_button_operation('true')  # 下一题 按钮 状态判断 加点击
                        time.sleep(2)

                print('=================================================')
                return rate, answer

    @teststeps
    def delete_incorrect_word(self, i, rate, word):
        """单词输入字母错误时,删除后重新输入
        :param i: 小题
        :param rate: 待完成：X
        :param word: 待输入单词
        """
        if i == 1:
            time.sleep(4)
            if self.wait_check_page():
                print('----删除错误单词后重新输入-----')
                self.hw.rate_judge(rate, i)  # 测试当前rate值显示是否正确
                for z in range(len(word)):
                    self.key.games_keyboard('backspace')  # 点击键盘对应 删除按钮

                for k in range(len(word)):
                    self.key.games_keyboard(word[k].lower())  # 点击键盘对应 大写字母

    @teststeps
    def click_blank_operation(self):
        """词组中空格时，多次点击空格键 操作"""
        j = 0
        print('多次点击空格键:')
        while j < 3:
            self.key.games_keyboard('blank')  # 多次点击空格键
            j += 1
        time.sleep(1)

    @teststeps
    def voice_operation(self, i):
        """发音按钮 操作"""
        locator = (By.ID, self.voice_button_value)
        if WaitElement().judge_is_exists(locator):
            if i == 2:  # 第3题
                j = 0
                print('多次点击发音按钮:')
                while j < 4:
                    self.click_voice()  # 多次点击发音按钮
                    j += 1
                time.sleep(1)
            else:
                self.click_voice()  # 点击 发音按钮

    @teststeps
    def result_page_operation(self, answer, content=None):
        """结果页操作
        :param content:
        :param answer: 我的答题结果
        """
        if content is None:
            content = []

        if self.wait_check_result_list_page():  # 结果页检查点
            star = self.star_button()
            word = self.result_word()  # 展示的Word 题目
            explain = self.result_explain()  # 展示的 解释

            if len(star) > 4 and not content:
                content = [word[len(star) - 2].text, explain[len(star) - 2].text]

                self.question_list(len(star)-1, answer, word, explain)  # 详情

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.result_page_operation(answer, content)
            else:
                var = 0
                if content:
                    for k in range(len(star)):
                        if content[0] == word[k].text and content[1] == explain[k].text:
                            var += k + 1
                            break

                self.question_list(len(star), answer, word, explain, var)  # 详情

                SwipeFun().swipe_vertical(0.5, 0.25, 0.95)
        #
        # print('=================================================')

    @teststeps
    def question_list(self, length, answer, word, explain, k=0):
        """结果页 具体操作
        :param k:
        :param explain:
        :param word:
        :param length:  题目数
        :param answer: 我的答题结果
        """
        for i in range(k, length):
            if word[i].text != answer[i]:  # 结果页 展示的word与题目中是否一致
                print('★★★ Error 查看答案页 展示的word与题中不一致', word[i].text, '  ', answer[i])
            else:
                print(word[i].text, '\n', explain[i].text)
            print('-------------------------')

        for index in range(k, length, 3):  # 点击 结果页 发音按钮
            print('点击 结果页 发音按钮: ', index)
            self.voice_button(index)  # 结果页 - 发音按钮
            self.star_button()[index].click()  # 结果页 star 按钮

    @teststeps
    def selected_sum(self):
        """标星的数目统计
        :return 标星的作业数
        """
        if self.wait_check_result_list_page():
            var = self.star_button()  # 结果页star按钮
            ele = []  # 结果页标星的作业数
            for i in range(len(var)):
                if self.get.selected(var[i]) == 'true':
                    ele.append(i)

            if len(ele) == 0:  # 结果页标星的作业数为0，则执行以下操作
                print('结果页标星的作业数为0, 点击star按钮:')
                for y in range(0, len(var), 2):
                    self.star_button()[y].click()  # 结果页 star 按钮

                ele = []  # 结果页标星的作业数
                for k in range(len(var)):
                    if self.get.selected(var[k]) == 'true':
                        ele.append(k)

                self.study_sum()  # 学习情况
                print('----------------')

            print('star按钮数目：', len(var))
            print('标星数：', len(ele))
            return len(ele)
