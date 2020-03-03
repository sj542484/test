#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.test_data.word_dictation_data import dictation_operation
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute
from utils.judge_character_type import JudgeType
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class WordDictation(BasePage):
    """单词听写"""
    word_value = gv.PACKAGE_ID + "word"  # 查看答案

    def __init__(self):
        self.result = ResultPage()
        self.key = Keyboard()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:单词听写”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词听写')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "play_voice") \
            .click()

    @teststeps
    def word(self):
        """展示的Word  点击喇叭听写单词"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_word").text
        word = ele.replace(' ', '')  # 删除空格
        return word

    # 下一步 按钮之后 答案页展示的答案
    @teststeps
    def mine_answer(self):
        """展示的Word """
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_word").text
        word = ele.replace(' ', '')  # 删除空格
        return word

    @teststep
    def question(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_explain").text
        return word

    @teststeps
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_answer").text
        print('正确答案：', word)
        return word

    @teststep
    def correct_judge(self):
        """判断 答案是否展示"""
        try:
            self.driver.find_element_by_id(gv.PACKAGE_ID + "tv_answer")
            return True
        except:
            return False

    # 以下为答案详情页面元素
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, self.word_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "audio")[index] \
            .click()

    @teststep
    def result_answer(self):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(self.word_value)
        return ele

    @teststep
    def result_explain(self):
        """解释"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "explain")
        return ele

    @teststep
    def result_mine(self):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "result")
        return ele

    @teststeps
    def word_dictation(self):
        """《单词听写》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                questions = []
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断 加点击

                    self.word()  # 灰字文案：点击喇叭听写单词
                    self.click_voice()  # 点击喇叭

                    word = dictation_operation(i)  # 数据字典
                    if JudgeType().is_alphabet(word):  # 解释内容为word
                        for j in range(len(word)):
                            self.keyboard_operation(j, word[j])  # 点击键盘 具体操作

                    answer.append(self.word())  # 我的答案
                    Homework().commit_button().click()  # 提交 按钮点击

                    self.result_operation(answer, questions, i, timestr, self.mine_answer())  # 下一步按钮后的答案页面 测试
                    Homework().next_button_operation('true')  # 下一题 按钮 状态判断 加点击
                    print('--------------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==============================================')
                return rate, answer, questions

    @teststeps
    def keyboard_operation(self, j, value):
        """点击键盘 具体操作"""
        if j == 4:
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.key.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.key.games_keyboard(value)  # 点击键盘对应字母
        Homework().commit_button_judge('true')  # 提交 按钮 状态判断

    @teststeps
    def result_operation(self, answer, questions, i, timestr, mine):
        """下一步按钮后的答案页面"""
        # mine 为 答案页面展示的 我的答题结果
        time.sleep(2)
        result = answer[len(answer) - 1]
        print('我的答案:', result)
        print('我的答题结果：', mine)
        if self.correct_judge():  # 展示的答案元素存在说明回答错误
            correct = self.correct()  # 正确答案
            if mine.lower() != result.lower():  # 展示的答题结果与我填入的答案不一致
                print('★★★ Error - 展示的答题结果:%s 与我填入的答案:%s 不一致' % (mine, result))

            for k in range(len(correct)):  # 测试 答案判断是否正确
                if result[k] not in correct:
                    break
        else:  # 回答正确
            questions.append(result)
            if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                print('★★★ Error - 展示的答题结果 与我填入的不一致:', mine, result)

        if i == 1:  # 第2题
            j = 0
            print('多次点击发音按钮:')
            while j < 4:
                print(j)
                self.click_voice()  # 多次点击发音按钮
                j += 1
            time.sleep(1)
        else:
            self.click_voice()  # 点击 发音按钮
        timestr.append(Homework().time())  # 统计每小题的计时控件time信息

    @teststeps
    def result_detail_page(self, answer):
        """《单词听写》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('查看答案:')
                self.answer_explain(answer)
                self.result.back_up_button()  # 返回结果页
                time.sleep(2)
            print('==============================================')

    @teststeps
    def answer_explain(self, result, content=None):
        """答案/解释类型
        :param result:答题结果
        :param content: 翻页
        """
        if content is None:
            content = []

        if self.wait_check_detail_page():
            hint = self.result_answer()  # 解释
            if len(hint) > 4 and not content:
                self.ergodic_list(result, len(hint) - 1)

                content = [hint[-2].text]
                if self.wait_check_detail_page():
                    SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                    self.answer_explain(result, content)
            else:
                var = 0
                if content:
                    for k in range(len(hint)):
                        if content[0] == hint[k].text:
                            var += k + 1
                            break

                self.ergodic_list(result, len(hint), var)

    @teststeps
    def ergodic_list(self, result, length, var=0):
        """遍历列表
        :param result:答题结果
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        explain = self.result_explain()  # 解释
        answer = self.result_answer()  # 答案
        mine = self.result_mine()  # 对错标识

        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            word = answer[i].text
            print('解释:', explain[i].text)  # 解释
            print('单词:', word)  # 正确word
            mode = GetAttribute().selected(mine[i])
            print(mode)
            if mode == 'true':
                if word != result[i].lower():
                    print('★★★ Error - 与答题结果不一致', answer[i].text, result[i])
            self.result_voice(i)  # 点击发音按钮
            print('-----------------------------------------')

    @teststeps
    def study_again(self):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()
            result = self.word_dictation()  # 游戏过程
            return item[1], result
