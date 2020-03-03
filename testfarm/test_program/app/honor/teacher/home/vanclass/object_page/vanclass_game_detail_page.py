#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
from selenium.webdriver.common.by import By

from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.click_bounds import ClickBounds
from utils.get_element_bounds import ElementBounds
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class VanclassGameDetailPage(BasePage):
    """ 作业详情 页面"""
    game_title_value = gv.PACKAGE_ID + "title"  # 游戏名
    drop_down_menu_value = gv.PACKAGE_ID + "report_content"  # 下拉菜单 内容
    content_value = gv.PACKAGE_ID + "content"  # 阅读理解/完形填空 文章元素
    hint_word_value = gv.PACKAGE_ID + "hint"  # 选词填空的提示词
    char_value = gv.PACKAGE_ID + "tv_char"  # 选项 ABCD
    voice_button_value = gv.PACKAGE_ID + "iv_play"  # 听音选择 播音按钮

    game_tips = '★★★ Error- 未进入作业详情vue界面'
    game_list_tips = '★★★ Error- 作业详情页作业列表为空'

    def __init__(self):
        self.game = GamesPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=20):
        """以“title:详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'详情')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self, var=20):
        """以“游戏title”为依据"""
        locator = (By.ID, self.game_title_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def game_title(self):
        """游戏title"""
        item = self.driver \
            .find_element_by_id(self.game_title_value)
        print(item.text)
        return item.text

    @teststep
    def game_info(self):
        """游戏 具体信息"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "info") \
            .text
        return item

    @teststeps
    def game_num(self):
        """获取游戏数量"""
        ele = self.game_info().split()

        if len(ele) == 2:
            num = re.sub("\D", "", ele[0])  # 共5题    2018-02-28
        else:
            num = re.sub("\D", "", ele[1])  # 自定义模式    共8题    2018-02-28
        return int(num)

    @teststeps
    def teacher_nickname(self):
        """老师昵称"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "name") \
            .text
        print(item)
        print('--------------------')
        return item

    @teststep
    def sentence(self):
        """句子"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_answer")
        return item

    @teststep
    def hint(self):
        """句子- 解释"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_hint")
        return item

    # 单选
    @teststeps
    def verify_voice_button(self):
        """验证 听音选择的 播音按钮 是否存在"""
        locator = (By.ID, self.voice_button_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def play_button(self):
        """听音选择的 播音按钮"""
        self.driver \
            .find_element_by_id(self.voice_button_value) \
            .click()

    # 选词填空
    @teststeps
    def verify_hint_word(self):
        """验证 选词填空的wording: 提示词 是否存在"""
        locator = (By.ID, self.hint_word_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def hint_word(self):
        """wording: 提示词"""
        item = self.driver \
            .find_element_by_id(self.hint_word_value).text
        print(item)

    @teststep
    def prompt_word(self):
        """提示的单词"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "prompt").text
        print(item)
        print('-----------------------------------')

    # 补全文章
    @teststep
    def option_char(self):
        """选项 ABCD"""
        item = self.driver \
            .find_elements_by_id(self.char_value)
        return item

    @teststep
    def option_item(self):
        """选项 内容"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_item")
        return item

    @teststep
    def drop_down_button(self, var):
        """正确选项后答对率 下拉按钮"""
        loc = ElementBounds().get_element_bounds(var)
        self.driver.tap([(loc[2], loc[5] - 10)])

    @teststeps
    def verify_drop_down_content(self, var=5):
        """验证 正确选项后答对率 下拉菜单 是否存在"""
        locator = (By.ID, self.drop_down_menu_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def drop_down_content(self):
        """x% 下拉菜单 内容"""
        item = self.driver \
            .find_element_by_id(self.drop_down_menu_value).text
        print('答题错误详情：', item)
        return item

    @teststeps
    def click_block(self):
        """点击 空白处"""
        ClickBounds().click_bounds(540, 200)

    @teststeps
    def verify_content_text(self):
        """验证 阅读理解/补全文章的文章 是否存在"""
        locator = (By.ID, self.content_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def article_content(self):
        """阅读理解/补全文章的文章"""
        item = self.driver \
            .find_element_by_id(self.content_value).text
        print(item)
        print('-----------------------------------')

    @teststeps
    def swipe_operation(self, swipe_num):
        """滑屏 获取所有题目内容"""
        ques_last_index = 0

        for i in range(swipe_num):
            if ques_last_index < swipe_num:
                ques_first_index = self.game.get_num()  # 当前页面中第一题 题号

                if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                    for step in range(0, 10):
                        SwipeFun().swipe_vertical(0.5, 0.5, 0.62)
                        if self.game.get_num() == ques_last_index + 1:  # 正好
                            break
                        elif self.game.get_num() < ques_last_index + 1:  # 下拉拉过了
                            SwipeFun().swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                            if self.game.get_num() == ques_last_index + 1:  # 正好
                                break

                last_one = self.game.get_last_element()  # 页面最后一个元素
                quesnum = self.game.single_question()  # 题目

                if self.game.question_judge(last_one):  # 判断最后一项是否为题目
                    for j in range(len(quesnum) - 1):
                        current_index = self.game.get_num(j)  # 当前页面中题号

                        if current_index > ques_last_index:
                            print('-----------------------------')
                            print(quesnum[j].text)
                            self.drop_down_operation(j)  # 选项内容及下拉按钮是否可点击
                            ques_last_index = self.game.get_num(j)  # 当前页面中 做过的最后一题 题号
                else:  # 判断最后一题是否为选项
                    for k in range(len(quesnum)):
                        if k < len(quesnum) - 1:  # 前面的题目照常点击
                            current_index = self.game.get_num(k)  # 当前页面中题号

                            if current_index > ques_last_index:
                                print('-----------------------------')
                                print(quesnum[k].text)
                                self.drop_down_operation(k)  # 选项内容及下拉按钮是否可点击

                                ques_last_index = self.game.get_num(k)  # 当前页面中 做过的最后一题 题号
                        elif k == len(quesnum) - 1:  # 最后一个题目上滑一部分再进行选择
                            SwipeFun().swipe_vertical(0.5, 0.8, 0.55)
                            quesnum = self.game.single_question()  # 题目
                            for z in range(len(quesnum)):
                                current_index = self.game.get_num(z)  # 当前页面中题号

                                if current_index > ques_last_index:
                                    print('-----------------------------')
                                    print(quesnum[z].text)
                                    self.drop_down_operation(z)  # 选项内容及下拉按钮是否可点击
                                    ques_last_index = self.game.get_num(z)  # 当前页面中 做过的最后一题 题号
                                    break

                if i != swipe_num - 1:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
            else:
                break

    @teststeps
    def rm_bracket(self, var):
        """ 去掉括号及其中的内容"""
        st = []
        ret = []
        for x in var:
            if x == '(':
                st.append(x)
            elif x == ')':
                st.pop()
            else:
                if len(st) == 0:
                    ret.append(x)  # 没有'('
        return ''.join(ret)

    @teststeps
    def drop_down_operation(self, k):
        """下拉按钮"""
        options = self.game.option_button()  # 选项
        print('选项:', options[0][k])
        rate = re.sub("\D", "", options[2][k].split()[-1])  # 准确率

        if rate == '' and options[2][k].split()[-1] == '未作答':
            print('该题还没有学生完成')
        else:
            if int(rate) < 100:
                self.drop_down_button(options[1][k])
                if self.verify_drop_down_content():
                    content = self.drop_down_content()
                    self.click_block()

                    item = self.rm_bracket(content)  # 去掉括号及其中的内容
                    var = item.split('\n')  # 以'\n'分割字符串

                    for i in range(0, len(var) - 1, 2):  # len()-1是为了去掉最后一个换行符分割出的空元素
                        if var[i] not in options[0][k]:
                            print('★★★ Error -下拉菜单内容不是本题选项', options[0][k], var[i])
            elif int(rate) == 100:
                print('该题正确率100%')
            else:
                print('★★★ Error -该题正确率', rate)
