#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.test_data.strength_sentence_data import strength_sentence_operation
from utils.click_bounds import ClickBounds
from utils.games_keyboard import Keyboard
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.get_attribute import GetAttribute
from utils.judge_character_type import JudgeType
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class StrengthenSentencePage(BasePage):
    """强化炼句"""
    def __init__(self):
        self.bounds = ClickBounds()
        self.result = ResultPage()
        self.key = Keyboard()
        self.get = GetAttribute()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    # 以下为 共有元素
    @teststeps
    def wait_check_page(self):
        """以“title:强化炼句”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'强化炼句')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def content_value(self):
        """获取整个 外框元素"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID  + "rich_text")
        return ele

    @teststeps
    def content_desc(self):
        """点击输入框，激活小键盘"""
        content = self.get.description(self.content_value())
        item = content.split(' ')  # y值
        return item[0]

    @teststeps
    def get_result(self):
        """获取 填入的答案"""
        var = self.get.description(self.content_value())
        content = re.match(".* ## (.*)", var).group(1)
        answer = content.split('  ')  # answer
        return answer

    @teststeps
    def sentence(self):
        """展示的句子"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID  + "rich_text").text
        return word

    @teststep
    def explain(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID  + "explain").text
        return word

    # 每小题回答完，下一步按钮后展示答案的页面
    @teststeps
    def wait_check_correct_page(self):
        """展示的答案title:正确答案 的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID  + "correct_title")
        return self.wait.wait_check_element(locator)

    @teststeps
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(gv.PACKAGE_ID  + "correct").text
        ele = word[:-1]  # 去掉最后的标点符号
        return ele

    # 查看答案页面
    @teststeps
    def result_question(self):
        """展示的题目"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "tv_hint")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        return word

    @teststeps
    def result_answer(self):
        """展示的 正确答案"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "tv_answer")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        return word

    @teststep
    def result_mine_state(self, index):
        """我的答案对错标识 selected属性"""
        word = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID  + "iv_mine")[index].get_attribute('selected')
        return word

    @teststeps
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        if tpe == '默写模式':
            answer = self.dictation_pattern()
        elif tpe == '自定义模式':
            answer = self.custom_pattern()
        elif tpe == '简单模式':
            answer = self.easy_pattern()
        else:  # 复杂模式
            answer = self.random_pattern()
        return answer

    @teststeps
    def random_pattern(self):
        """《强化炼句 复杂模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断加 点击操作

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断加 点击操作 ,进入答案页面

                    self.correct_judge(value, i)  # 判断答题是否正确
                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operation('true')  # 下一题 按钮 状态判断加 点击操作
                    print('-------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('=======================================')
                return rate, answer

    @teststeps
    def custom_pattern(self):
        """《强化炼句 自定义模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断加 点击操作

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断加 点击操作 ,进入答案页面
                    if self.wait_check_correct_page():
                        result = self.correct_judge(value, i)  # 判断答题是否正确
                        answer.append(result[0])

                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    Homework().next_button_operation('true')  # 下一题 按钮 状态判断 点击
                    print('-------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('=======================================')
                return rate, answer

    @teststeps
    def easy_pattern(self):
        """《强化炼句 简单模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断加 点击操作

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断加 点击操作 ,进入答案页面

                    result = self.correct_judge(value, i)  # 判断答题是否正确
                    answer.append(result[0])
                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operation('true')  # 下一题 按钮 状态判断 点击
                    print('-------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('=======================================')
                return rate, answer

    @teststeps
    def dictation_pattern(self):
        """《强化炼句 默写模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 判断加 点击操作

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().commit_button_operation('true')  # 提交 按钮 状态判断加 点击操作 ,进入答案页面

                    result = self.correct_judge(value, i)  # 判断答题是否正确
                    answer.append(result[0])
                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operation('true')  # 下一题 按钮 状态判断 点击
                    print('-----------------------------')
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('=======================================')
                return rate, answer

    @teststeps
    def input_text(self):
        """激活输入框 并 输入内容"""
        explain = self.explain()  # 解释的内容
        sentence = self.sentence().split(' ')  # 句子
        value = strength_sentence_operation(explain)  # 数据字典
        print('--------------')
        print('题目:', self.sentence())

        words = value.split(' ')  # 将句子分割成单词
        word = []
        for i in range(len(words)):
            if (JudgeType().is_alphabet(words[i])) and (words[i] not in sentence):
                word.append(words[i])

        for j in range(len(word)):
            if j !=0:
                self.key.games_keyboard('enter')  # 点击键盘 下一步按钮

            for z in range(len(word[j])):
                if j == len(word)-1:
                    if word[j][z] in ['.', '?', '!']:  # 去掉最后的标点符号
                        break
                if z == 4 and z != len(word[j])-1:
                    self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                    self.key.games_keyboard(word[j][z].upper())  # 点击键盘对应 大写字母
                    self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                else:
                    if j == 2 and word[j][z] == "'":
                        self.key.games_keyboard(',')  # 第二小题  点击键盘 逗号
                    else:
                        self.key.games_keyboard(word[j][z])  # 点击键盘对应字母
        return value

    @teststeps
    def correct_judge(self, value, i):
        """每小题回答完，下一步按钮后展示答案的页面"""
        if self.wait_check_correct_page():  # 展示的答案title元素是否存在
            result = self.get_result()  # content-desc的值
            answer = self.sentence()  # 展示的本人的答案

            for j in range(len(result)):
                for k in range(len(answer)):
                    if answer[k] == '{':
                        if len(answer) != 2:
                            if k == 0:  # 展示的本人的答案 result[j]
                                answer = result[j].strip() + answer[k + 2:]
                            elif k + 1 == len(answer) - 1:
                                if ' ' not in result[j]:
                                    answer = answer[:k - 1] + ' ' + result[j]
                                else:
                                    answer = answer[:k - 1] + result[j]
                            else:
                                if ' ' not in result[j]:
                                    answer = answer[:k - 1] + ' ' + result[j] + answer[k + 2:]
                                else:
                                    answer = answer[:k - 1] + result[j] + answer[k + 2:]
                            break

            if answer[len(answer)-1] == ' ':
                answer = answer[:-1]
            correct = self.correct()  # 展示的正确答案
            print('我的答案：', answer)
            if correct == value:  # 测试展示的答案是否正确
                if answer == correct:
                    print('回答正确')
                else:
                    print('回答错误')
            return answer, i

    @teststeps
    def check_detail_page(self, i, answer):
        """查看答案页面"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('结果页 - 查看答案 按钮：')
                if int(i) <= 16:
                    self.result_operation(answer)
                else:
                    item = self.result_question()
                    if int(i) % len(item) == 0:
                        page = int(int(i) / len(item))
                    else:
                        page = int(int(i) / len(item)) + 1
                    print('页数:', page)
                    for j in range(page):
                        last_one = self.result_operation(answer)  # 滑动前页面内最后一个小题- 做题结果
                        self.swipe.swipe_vertical(0.5, 0.75, 0.35, 1000)
                        item_2 = self.result_question()  # 滑动后页面内的题目 的数量
                        if item_2[len(item_2) - 1].text == last_one:
                            print('到底啦', last_one)
                            self.result.back_up_button()
                            break
                        elif item_2[len(item_2) - 1].text == answer[len(answer) - 1]:
                            # 滑动后到底，因为普通情况下最多只有两页，滑动一次即可到底
                            print('滑动后到底', last_one)
                            k = []
                            for i in range(len(item_2) - 1, -1, -1):  # 倒序
                                if item_2[i].text == last_one:
                                    k.append(i + 1)
                                    break
                            self.result_operation(answer, k[0])
                            break
                        else:
                            continue
                    self.swipe.swipe_vertical(0.5, 0.75, 0.35, 1000)
                time.sleep(2)
            self.result.back_up_button()

    @teststeps
    def result_operation(self, var, index=0):
        """查看答案页面 -- 展示的解释内容验证"""
        explain = self.result_question()  # 题目
        answer = self.result_answer()  # 正确答案
        print(answer, var)
        for i in range(index, len(explain)):
            count = []
            value = strength_sentence_operation(explain[i]).split(' ')
            if answer[i] == var[i]:  # 测试结果页 我的答案展示是否正确
                if answer[i] == value:  # 测试 正确答案
                    for j in range(len(var)):  # 我的答案 与 正确答案 比较
                        if var[j] != value[j]:  # 答案不正确 count+1
                            count.append(j)
                            if self.result_mine_state() != 'false':
                                print('★★★ Error - 我的答案:%s 与 正确答案:%s 对错标识:%s' % (var[j], value[j], 'true'))
                        else:
                            if self.result_mine_state() != 'true':
                                print('★★★ Error - 我的答案:%s 与 正确答案:%s 对错标识:%s' % (var[j], value[j], 'false'))
                        break
                else:
                    print('★★★ Error - 正确答案:', answer[i], value)
            print('------------------------------------')
        return var[1][len(var[1]) - 1]

    @teststeps
    def study_again(self, tpe):
        """错题再练/再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练 按钮
            item[0].click()
            result = self.diff_type(tpe)  # 强化炼句 - 游戏过程

            return item[1], result[0], result[1]