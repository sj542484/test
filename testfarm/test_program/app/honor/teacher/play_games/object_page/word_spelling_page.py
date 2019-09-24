#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.test_data.word_spelling_data import word_spelling_operation
from utils.get_attribute import GetAttribute
from utils.games_keyboard import Keyboard
from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.judge_character_type import JudgeType
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class WordSpelling(BasePage):
    """单词拼写"""
    word_value = gv.PACKAGE_ID + "tv_word"  # 单词
    correct_value = gv.PACKAGE_ID + "word"  # 提交 按钮之后 答案页展示的答案

    def __init__(self):
        self.result = ResultPage()
        self.get = GetAttribute()
        self.key = Keyboard()
        self.wait = WaitElement()

    # 以下为 共有元素
    @teststeps
    def wait_check_page(self):
        """以“title:单词拼写”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词拼写')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "play_voice").click()

    @teststeps
    def question_word(self):
        """展示的Word"""
        ele = self.driver \
            .find_element_by_id(self.word_value).text
        return ele

    @teststeps
    def exist_words(self):
        """未缺失的字母"""
        ele = self.question_word()
        word = ele[1::2]
        print('word：', word)
        return word

    @teststep
    def explain(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_explain").text
        return word

    @teststep
    def finish_word(self):
        """完成答题 之后 展示的Word 前后含额外字符：aa"""
        word = self.question_word()
        return word[1::2]

    # 默写模式 特有元素
    @teststeps
    def dictation_word(self):
        """展示的Word"""
        ele = self.question_word()
        value = ele[::2]
        return value

    @teststeps
    def judge_dictation_word(self):
        """判断是否展示Word"""
        locator = (By.ID, self.word_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def under_line(self):
        """展示的横线"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "underline")
        return ele

    @teststep
    def hint_button(self):
        """提示按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "hint")
        return ele

    # 提交 按钮之后 答案页展示的答案
    @teststep
    def mine_answer(self):
        """展示的Word  前后含额外字符:aa"""
        word = self.driver \
            .find_element_by_id(self.word_value).text
        return word[1::2]

    @teststep
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(self.correct_value).text
        return word

    # 默写模式 答案页特有元素
    @teststep
    def dictation_finish_word(self):
        """完成答题 之后 展示的Word  前后不含额外字符:aa"""
        word = self.question_word()
        return word[::2]

    @teststep
    def dictation_mine_answer(self):
        """展示的Word  前后不含额外字符:aa"""
        word = self.question_word()
        return word[::2]

    # 以下为答案详情页面元素
    @teststeps
    def wait_check_correct_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, self.correct_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "audio")[index] \
            .click()

    @teststep
    def result_item(self):
        """题目条目"""
        ele = self.driver \
            .find_elements_by_class_name("android.view.ViewGroup")
        return ele

    @teststep
    def result_answer(self):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(self.correct_value)
        return ele

    @teststep
    def result_explain(self):
        """解释"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "explain")
        return ele

    @teststep
    def result_remove(self):
        """去除"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "remove")
        return ele

    @teststep
    def result_mine(self):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "result")
        return ele

    @teststeps
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        if tpe == '默写模式':
            answer = self.dictation_pattern()
        elif tpe == '自定义':
            answer = self.custom_pattern()
        else:  # 随机模式
            answer = self.random_pattern()
        return answer

    @teststeps
    def random_pattern(self):
        """《单词拼写 随机模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                var = []  # 随机消除的字母
                answer = []   # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间

                rate = Homework().rate()
                for i in range(int(rate)):
                    mine = []  # 我的答案
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交按钮 判断加 点击操作

                    explain = self.explain()  # 解释
                    word = self.exist_words()  # 未缺失的字母
                    value = word_spelling_operation(explain)  # 数据字典

                    item = word.replace('_', '')
                    if JudgeType().is_alphabet(item):  # 未缺失的内容为字母
                        if value != word:  # 随机消除的字母消除了
                            for j in range(len(value)):
                                if value[j] != word[j]:
                                    print('缺失的字母：', value[j])
                                    var.append(j)
                                    self.keyboard_operation(j, value[j])  # 点击键盘 具体操作

                    mine.append(self.finish_word())  # 我的答案
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断加 点击操作

                    self.result_operation(mine, i, self.mine_answer(), timestr, answer)  # 答案页面 测试

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==================================================')
                return rate, answer, var

    @teststeps
    def custom_pattern(self):
        """《单词拼写 自定义模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    mine = []  # 我的答案
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断加 点击操作

                    explain = self.explain()  # 解释
                    word = self.exist_words()  # 未缺失的字母
                    value = word_spelling_operation(explain)  # 数据字典

                    item = word.replace('_', '')
                    if JudgeType().is_alphabet(item):  # 未缺失的内容为字母
                        if len(word) != 0:
                            if value != word:  # 自定义消除的字母消除了
                                for j in range(len(value)):
                                    if value[j] != word[j]:
                                        print('缺失的字母：', value[j])
                                        self.keyboard_operation(j, value[j])  # 点击键盘 具体操作
                            else:
                                print('★★★ Error - 自定义消除的字母未消除', word)
                                for j in range(0, len(value)-1):
                                    if value[j] != word[j]:
                                        print('★★★ Error - 未自定义消除的字母%s也消除了' % value[j])

                    mine.append(self.finish_word())  # 我的答案
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击

                    self.result_operation(mine, i, self.mine_answer(), timestr, answer)  # 答案页面 测试

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==================================================')
                return rate, answer

    @teststeps
    def dictation_pattern(self):
        """《单词拼写 默写模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    mine = []  # 我的答案
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断 加点击

                    explain = self.explain()  # 解释
                    value = word_spelling_operation(explain)  # 数据字典

                    if self.judge_dictation_word():  # 默写模式 - 字母未全部消除
                        print('★★★ Error - 单词拼写 默写模式 - 字母未全部消除')

                    if i in range(2, 5, 2):
                        hint = self.hint_button()  # 提示按钮
                        if self.get.enabled(hint) == 'true':
                            hint.click()  # 点击 提示按钮
                            if self.get.enabled(hint) != 'false':
                                print('★★★ Error - 点击后提示按钮enabled属性为:', self.get.enabled(hint))

                            if self.judge_dictation_word():  # 出现首字母提示
                                word = self.dictation_word()
                                if len(word) == 1 and word == value[0]:
                                    print('点击提示出现首字母提示', word)
                                else:
                                    print('★★★ Error - 点击提示未出现首字母提示')
                        else:
                            print('★★★ Error - 提示按钮enabled属性为:', self.get.enabled(hint))

                    for j in range(len(value)):
                        self.keyboard_operation(j, value[j])  # 点击键盘 具体操作

                    mine.append(self.dictation_finish_word())  # 我的答案
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击

                    self.result_operation(mine, i, self.dictation_mine_answer(), timestr, answer)  # 答案页面 测试

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==================================================')
                return rate, answer

    @teststeps
    def keyboard_operation(self, j, value):
        """点击键盘 具体操作
        :param j: 索引值
        :param value: 单词
        """
        if j == 4:
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.key.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.key.games_keyboard(value)  # 点击键盘对应字母

    @teststeps
    def result_operation(self, content, i, mine, timestr, answer):
        """点击提交按钮后的答案页面
        :param content：我的答案
        :param i: 第X小题
        :param mine: 为 答案页面展示的 我的答题结果
        :param timestr:统计时间
        :param answer: 作对的题
        """
        print('----------------------')
        result = content[- 1]
        print('我的答案:', result)
        print('我的答题结果:', mine)

        if self.wait_check_correct_page():  # 展示的答案元素存在说明回答错误
            correct = self.correct()  # 正确答案
            print('解释:', self.explain())
            if len(mine) <= len(correct):  # 输入少于或等于单词字母数的字符
                if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('★★★ Error - 字符数少于或等于时:', mine.lower(), result.lower())
            else:  # 输入过多的字符
                if correct + mine[len(correct):].lower() != correct + result[
                                                                      len(correct):].lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('★★★ Error - 字符输入过多时:', correct + mine[len(correct):].lower(),
                          correct + result[len(correct):].lower())

            for k in range(len(correct)):  # 测试 答案判断是否正确
                if result == correct:
                    print('★★★ Error - 答案判断错误', result, correct)
                    break
        else:  # 回答正确
            if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                print('★★★ Error - 展示的答题结果 与我填入的不一致:', mine.lower(), result.lower())
            else:
                answer.append(mine[0])  # 做对的题目

        self.click_voice_operation(i)  # 点击发音按钮 操作

        timestr.append(Homework().time())  # 统计每小题的计时控件time信息
        Homework().next_button_operation('true')  # 下一题 按钮 状态判断 加点击
        print('---------------------------------')

    @teststeps
    def click_voice_operation(self, i):
        """点击发音按钮 操作
        :param i: 第X小题
        """
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
        print('--------')

    @teststeps
    def result_detail_page(self):
        """查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            print('查看答案:')
            self.swipe_operation()
            self.result.back_up_button()  # 返回结果页
            print('==============================================')

    @teststeps
    def swipe_operation(self, content=None):
        """查看答案 - 点击听力按钮
        :param content: 翻页
        """
        if self.result.wait_check_detail_page():
            if content is None:
                content = []

            ques = self.result_answer()
            if len(ques) > 4 and not content:
                self.ergodic_list(len(ques) - 1)
                content = [ques[-2].text]

                SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                self.swipe_operation(content)
            else:
                var = 0
                if content:
                    for k in range(len(ques)):
                        if content[0] == ques[k].text:
                            var += k + 1
                            break

                self.ergodic_list(len(ques), var)

    @teststeps
    def ergodic_list(self, length, var=1):
        """遍历列表
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        explain = self.result_explain()  # 解释
        answer = self.result_answer()  # 答案
        remove = self.result_remove()  # 去除
        mine = self.result_mine()  # 对错标识

        content = []  # 答对的小题数
        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            print('单词:', answer[i].text)  # 正确word
            print('解释:', explain[i].text)  # 解释
            print(remove[i].text)  # 去除
            mode = GetAttribute().selected(mine[i])
            print('对错标识:', mode)

            if mode == 'true':
                content.append(i)

            print('-----------------------------------------')
            self.result_voice(i)  # 点击发音按钮

    @teststeps
    def study_again(self, tpe):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()

            result = self.diff_type(tpe)  # 不同模式 对应不同的游戏过程
            return item[1], result
