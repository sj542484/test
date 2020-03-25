#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from utils.click_bounds import ClickBounds
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import ElementBounds
from utils.wait_element import WaitElement


class BankedCloze(BasePage):
    """选词填空"""
    prompt_value = gv.PACKAGE_ID + "prompt"  # 提示词
    prompt_locator = (By.ID, prompt_value)  # 提示词locator
    tb_content_value = gv.PACKAGE_ID + "rich_text"  # 文章

    def __init__(self):
        self.bounds = ClickBounds()
        self.result = ResultPage()
        self.get = GetAttribute()
        self.key = Keyboard()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=10):
        """以“title:选词填空”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选词填空')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def font_middle(self):
        """第一个Aa"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "font_middle")
        return ele

    @teststep
    def font_large(self):
        """第二个Aa"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "font_large")
        return ele

    @teststep
    def font_great(self):
        """第三个Aa"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "font_great")
        return ele

    @teststep
    def prompt(self):
        """提示词"""
        self.driver \
            .find_element_by_id(self.prompt_value).click()

    @teststep
    def prompt_tips(self):
        """提示词 弹框"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "md_root")
        return ele

    @teststep
    def prompt_content(self):
        """提示词内容"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.ScrollView/android.widget.TextView").text
        return ele

    @teststep
    def click_blank(self):
        """点击页面 提示词弹框 以外空白处，弹框消失"""
        ele = self.prompt_tips()
        loc = ElementBounds().get_element_bounds(ele)
        x = loc[4] - 200
        y = loc[5] + 100
        print(x, y)
        self.driver.tap([(x, y)])

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID,  gv.PACKAGE_ID + "tv_answer")
        return self.wait.wait_check_element(locator)

    @teststeps
    def verify_content_text(self):
        """验证 阅读理解/完形填空的文章 是否存在"""
        locator = (By.ID, self.tb_content_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def content_value(self):
        """获取整个 外框元素"""
        ele = self.driver\
            .find_element_by_id(self.tb_content_value)
        return ele

    @teststeps
    def content_desc(self):
        """点击输入框，激活小键盘"""
        content = self.get.description(self.content_value())
        item = content.split(' ')  # y值
        return item[0]

    @teststeps
    def get_answer(self):
        """获取 答题结果"""
        var = self.get.description(self.content_value())
        content = ' '.join(var.split())  # 删除字符串中的连续空格只保留一个
        value = content[6:].split(' ')  # answer

        answer = []
        for i in range(len(value)):
            if value[i] != '':
                answer.append(value[i])   # 所有输入框值的列表
        print('答题结果：', answer)

        return answer

    @teststeps
    def get_result(self):
        """获取 答题结果"""
        var = self.get.description(self.content_value())
        content = '  '.join(var.split('  '))  # 删除字符串中的连续空格只保留一个
        value = content[6:].split('  ')  # answer

        answer = []
        result = []  # 答题结果
        for i in range(len(value)):
            if value[i] != '':
                if "(" in value[i]:
                    del result[-1]
                    result.append(value[i][1:-1].lower())  # 答错的题
                else:
                    result.append(value[i].lower())
                    answer.append(value[i].lower())  # 正确答案

        return answer, result

    @teststeps
    def banked_cloze_operation(self, word_list):
        """《选词填空》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if Homework().wait_check_play_page():
                timestr = []
                self.font_operation()  # Aa文字大小切换按钮 切换 及状态统计

                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 状态判断 加点击

                    if i != 0:
                        self.key.games_keyboard('enter')  # 点击回车键 激活输入框 或者进入下一题

                    if len(word_list) > i:  # 提示词足够
                        word = word_list[i]  # 提示词 单词
                    else:  # 提示词过少 或者 无提示词
                        word = 'qwe'
                    print('word:', word)

                    for y in range(len(word)):
                        if y == 4:
                            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                            self.key.games_keyboard(word[y].upper())  # 点击键盘对应 大写字母
                            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                        else:
                            self.key.games_keyboard(word[y])  # 点击键盘对应字母
                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                print('-----------------------------------')

                answer = self.get_answer()  # 获取 答题结果
                Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时

                final_time = self.result.get_time(timestr[-1])  # 最后一个小题的时间
                print('==================================================')
                return rate, answer, final_time

    @teststeps
    def check_detail_page(self, result, rate):
        """查看答案页面
        :param result:答题结果
        :param rate:题目数
        """
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮

            if self.result.wait_check_detail_page():  # 页面检查点
                print('查看答案页面:')
                count = []  # 回答正确题
                answer = self.get_result()  # 获取 答题结果

                for i in range(int(rate)):
                    if result[i].lower() not in answer[1]:
                        print('★★★ Error - 答题结果错误:', answer[1], result[i])

                print('---------答题情况--------')
                for i in range(int(rate)):
                    if result[i].lower() != answer[0][i].lower():
                        print('回答错误:', answer[0], result[i])
                    else:
                        print('回答正确:', result[i])
                        count.append(result[i])

                if self.result.wait_check_detail_page():  # 页面检查点
                    self.result.back_up_button()  # 返回结果页
                print('==================================================')
                return count

    @teststeps
    def study_again(self, word):
        """《选词填空》 错题再练/再练一遍 操作过程
        :param word:提示词
        :return item[1]: 错题再练/再练一遍 按钮text 用于结果页 准确率判断
        :return  result: 答题过程的返回值
        """
        print('==================================================')
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()
            result = self.banked_cloze_operation(word)  # 选词填空 - 游戏过程
            return item[1], result

    @teststeps
    def font_operation(self):
        """Aa文字大小切换按钮 状态判断 及 切换操作"""
        y = []
        middle = self.font_middle()  # first
        large = self.font_large()  # second
        great = self.font_great()  # third

        i = j = 0
        while i < 3:
            bounds = self.content_desc()  # 获取输入框坐标
            print(self.get.checked(middle), self.get.checked(large), self.get.checked(great))

            if self.get.checked(middle) == 'false':
                if self.get.checked(large) == 'false':
                    y.insert(2, bounds)
                    print('当前选中的Aa按钮为第3个：', bounds)
                    j = 3
                else:
                    if self.get.checked(large) == 'true':
                        y.insert(1, bounds)
                        print('当前选中的Aa按钮为第2个：', bounds)
                        j = 2
            else:
                y.insert(0, bounds)
                print('当前选中的Aa按钮为第1个：', bounds)
                j = 1

            if j == 1:
                large.click()
            elif j == 2:
                great.click()
            else:
                middle.click()
            i += 1
            print('--------------------------------------------')
            time.sleep(2)

        if not float(y[2]) > float(y[1]) > float(y[0]):
            print('★★★ Error - Aa文字大小切换按钮:', y)
        print('==============================================')
