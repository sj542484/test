#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.play_games.test_data.matching_exercise_data import match_operation
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.judge_character_type import JudgeType
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class MatchingExercises(BasePage):
    """连连看"""
    word_value = gv.PACKAGE_ID + "word"  # 查看答案页面

    def __init__(self):
        self.result = ResultPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:连连看”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'连连看')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def item(self):
        """题数"""
        ele = self.driver \
            .find_elements_by_class_name('android.widget.ImageView')
        return ele

    @teststep
    def word_explain(self):
        """展示的Word"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")[4:]

        word = []  # 单词list
        explain = []  # 解释list

        for i in range(len(ele)):
            if JudgeType().is_alphabet(ele[i].text[0]):  # 如果是字母
                word.append(ele[i])
            else:  # 如果是汉字
                explain.append(ele[i])

        return word, explain

    @teststeps
    def word_img(self):
        """图文模式 - 展示的Word & img"""
        view = self.driver.find_elements_by_xpath('//android.view.ViewGroup')
        ele = self.driver \
            .find_elements_by_xpath("//android.view.ViewGroup/android.widget.TextView")
        word = []
        word_text = []  # 单词list
        img = []
        for i in range(1, len(ele)):  # 去掉页面title
            if ele[i].text != '':  # word
                word.append(view[i])
                word_text.append(ele[i].text)
            else:  # 图片
                img.append(view[i])

        return word, img, word_text

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
    def result_img(self):
        """图片"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "img")
        return ele

    @teststep
    def result_word(self):
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
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        if tpe == '图文模式':
            result = self.match_exercise_picture()
            return result
        else:
            result = self.match_exercise_word()
            return result

    @teststeps
    def match_exercise_word(self):
        """《连连看 文字模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = {}  # 答题结果
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()

                count = int(len(self.item()) // 2)
                if int(rate) % count == 0:
                    page = int(int(rate) / count)
                else:
                    page = int(int(rate) / count) + 1
                print('页数:', page)

                for j in range(page):  # 然后在不同页面做对应的题目
                    print('===========================================')
                    print('第%s页：' % (j+1))
                    var = j * count  # 每页5个单词

                    ele = self.word_explain()
                    word = ele[0]  # 单词list
                    explain = ele[1]  # 解释list

                    for k in range(len(word)):  # 具体操作
                        print('---------------------------------')
                        Homework().rate_judge(rate, k + var)  # 测试当前rate值显示是否正确

                        print('word:', word[k].text)
                        value = match_operation(word[k].text)  # 数据字典
                        word[k].click()  # 点击单词

                        for z in range(len(explain)):
                            if explain[z].text == value:
                                timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                                answer[word[k].text] = explain[z].text
                                explain[z].click()  # 点击对应解释
                                print('解释:', explain[z].text)

                                if j == 0 and k == 0:  # 测试 配对成功后，不可再次点击
                                    word[k].click()
                                break

                    time.sleep(1)
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('======================================================')
                return rate, answer

    @teststeps
    def match_exercise_picture(self):
        """《连连看 图文模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                answer = {}  # 答题结果
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()

                count = len(self.item())//2
                if int(rate) % count == 0:
                    page = int(int(rate) / count)
                else:
                    page = int(int(rate) / count) + 1
                print('页数:', page)

                for i in range(page):  # 然后在不同页面做对应的题目
                    print('===========================================')
                    print('第%s页：' % (i + 1))
                    var = i * count # 每页4个单词

                    ele = self.word_img()  # ele[0]：word; ele[1]：图片
                    word = ele[0]  # word元素
                    img = ele[1]  # 图片元素
                    for k in range(len(word)):  # 具体操作
                        print('---------------------------------')
                        time.sleep(1)  # 等待rate值改变
                        Homework().rate_judge(rate, k + var)  # 验证 当前rate值显示是否正确

                        print('word:', ele[2][k])
                        for z in range(len(img)):
                            word[k].click()  # 点击单词

                            value = GetAttribute().enabled(img[z])
                            if value == 'true':
                                img[z].click()  # 点击对应 图片
                                time.sleep(1)

                                if z != len(img)-1:
                                    value = GetAttribute().enabled(img[z])
                                    if value == 'false':  # 判断是否选对(false代表选对)
                                        # if k != 0:  # 验证 点击已匹配成功的button
                                        #     del img[z]
                                        break

                        timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    time.sleep(3)  # 等待切换页面

                print('==============================================')
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('======================================================')
                return rate, answer

    @teststeps
    def result_detail_page(self, mode):
        """《连连看》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('==============================================')
                print('查看答案:')
                content = []
                if mode == "图文模式":
                    self.get_list(self.img_ergodic_list, content)
                elif mode == '文字模式':
                    self.get_list(self.explain_ergodic_list, content)

                if self.wait_check_detail_page():
                    self.result.back_up_button()  # 返回结果页
            else:
                print('★★★ Error - 未进入查看答案页面')

    @teststeps
    def get_list(self, func, content=None):
        """单个content值
        :param func: 遍历列表
        :param content: 用于滑屏翻页
        """
        if self.wait_check_detail_page():
            if content is None:
                content = []

            count = []
            word = self.result_word()  # 循环
            if len(word) > 8 and not content:
                content = [word[-2].text]
                func(count, len(word) - 1)  # 遍历

                if self.wait_check_detail_page():
                    SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                    self.get_list(func, content)
            else:
                var = 0
                if content:
                    for k in range(len(word)):
                        if content[0] == word[k].text:
                            var += k + 1
                            break

                func(count, len(word), var)  # 遍历

    @teststeps
    def explain_ergodic_list(self, content, length, var=0, item=1):
        """文本模式 - 遍历整个列表
        :param content: 对错标识为true的索引值
        :param length:
        :param var:
        :param item:1表示有发音按钮
        """
        explain = self.result_explain()  # 解释
        word = self.result_word()  # word
        mine = self.result_mine()  # 对错标识

        if len(explain) < 7:
            if len(explain) != len(word):
                print('★★★ Error - word和解释数量不一致', len(explain), len(word))

        for i in range(var, length):
            print('-----------------------------------')
            print('解释:', explain[i].text)  # 解释
            print('单词:', word[i].text)  # 正确word

            mode = GetAttribute().selected(mine[i])
            if mode != 'true':
                print('★★★ Error - 对错标识', mode)
            else:
                print('对错标识: true')
                content.append(i)

            if item == 1:
                print('点击发音按钮')
            self.result_voice(i)  # 点击发音按钮

    @teststeps
    def img_ergodic_list(self, content, length, var=0, item=1):
        """图文模式 - 遍历整个列表"""
        img = self.result_img()  # 图片
        word = self.result_word()  # 答案
        mine = self.result_mine()  # 对错标识

        if len(img) != len(word):
            print('★★★ Error - word和图片数量不一致', len(img), len(word))
        for i in range(var, length):
            print('-----------------------------------')
            print('单词:', word[i].text)  # 正确word
            mode = GetAttribute().selected(mine[i])
            if mode != 'true':
                print('★★★ Error - 对错标识', mode)
            else:
                content.append(i)
                print('对错标识: true')

            if item == 1:
                print('点击发音按钮')
            self.result_voice(i)  # 点击发音按钮

    @teststeps
    def study_again(self, game_type):
        """再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            print('==============================================')
            self.result.again_button()[0].click()  # 结果页 再练一遍 按钮

            result = self.diff_type(game_type)  # 不同模式小游戏的 游戏过程
            return result
