#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import re
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page import Homework
from app.honor.teacher.play_games.object_page import ResultPage
from conf.decorator import teststeps, teststep
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import Element
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class ClozePage(BasePage):
    """完形填空"""
    content_value = gv.PACKAGE_ID + "cl_content"  # 文章

    def __init__(self):
        self.result = ResultPage()
        self.get = GetAttribute()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:完形填空”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'完形填空')]")
        return self.wait.wait_check_element(locator)

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
    def dragger_button(self):
        """拖动按钮"""
        num = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "dragger")
        return num

    @teststeps
    def question(self):
        """题目"""
        num = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "question").text
        return num

    @teststeps
    def option_button(self, var):
        """选项"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]"
                                    "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout"
                                    "/android.widget.LinearLayout/android.widget.TextView" % var)
        item = []  # ABCD
        content = []  # 选项内容
        for i in range(0, len(ele), 2):
            item.append(ele[i])
            content.append(ele[i + 1].text)
        print('选项个数:', len(item))
        return item, content

    @teststeps
    def option_content(self):
        """选项 内容"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_item")
        return ele

    @teststeps
    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(gv.PACKAGE_ID + "option")
        var = num.size
        return var['height']

    @teststeps
    def verify_content_text(self):
        """验证 文章 是否存在"""
        locator = (By.ID, self.content_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def article_content(self):
        """输入框"""
        ele = self.driver \
            .find_element_by_id(self.content_value)
        return ele

    @teststeps
    def get_input_bounds(self):
        """获取 输入框y坐标"""
        content = self.get.description(self.article_content())
        y = content.split(' ')[0]  # 输入框y值
        return y

    @teststeps
    def get_result(self):
        """获取 输入框 的结果"""
        content = self.get.description(self.article_content())
        value = content.split(' ')

        answer = []
        for i in range(2, len(value)):
            if value[i] != '':
                answer.append(value[i])  # 所有输入框值的列表
        return answer

    @teststeps
    def cloze_operation(self):
        """《完形填空》 游戏过程"""
        if self.wait_check_page():
            if Homework().wait_check_play_page():
                self.font_operation()  # Aa文字大小切换按钮 切换 及状态统计
                self.drag_operation()  # 向上拖拽按钮操作

                answer = []  # 选择的答案
                result = []  # 回答正确的题
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operation('false')  # 下一题 按钮 判断加 点击操作

                    if i == 4:
                        self.swipe.swipe_vertical(0.5, 0.5, 0.25, 1000)  # 上滑屏幕

                    num = self.question()  # 题目
                    if int(re.sub("\D", "", num)) == i:  # 如果一次没滑动，再滑一次
                        self.swipe.swipe_horizontal(0.8, 0.9, 0.1, 2000)  # 左滑进入下一题
                        num = self.question()  # 题目
                    print(num)

                    options = self.option_button(num)  # 四个选项
                    options[0][random.randint(0, len(options[0])) - 1].click()  # 随机点击选项
                    time.sleep(1)
                    for j in range(len(options[0])):
                        if self.get.selected(options[0][j]) == 'true':
                            print('选择的答案:', options[1][j])
                            answer.append(options[1][j])
                            break

                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    self.swipe.swipe_horizontal(0.8, 0.9, 0.1, 2000)  # 左滑进入下一题

                    if i == int(rate) - 1:  # 最后一小题：1、测试滑动页面是否可以进入结果页   2、拖拽 拖动按钮
                        if not ResultPage().wait_check_result_page(2):  # 结果页检查点
                            self.drag_operation('down')  # 向下拖拽按钮操作
                        else:
                            print('★★★ Error - 滑动页面进入了结果页')

                    time.sleep(1)
                    content = self.get_result()  # 测试 是否答案已填入文章中
                    print('--------------')
                    if len(content) != len(answer):
                        print('★★★ Error -答案未填入', answer, content)
                    else:
                        if content[-1] != answer[-1]:
                            print('★★★ Error - 填入的答案与选择的答案不一致', answer[-1], content[-1])
                        else:
                            result.append(answer[-1])
                            print('我的答题结果：', answer[-1])
                    print('----------------------------')

                Homework().next_button_operation('true')  # 下一题 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时

                final_time = self.result.get_time(timestr[-1])  # 最后一个小题的时间
                print('===============================================')
                return rate, result, final_time

    @teststeps
    def drag_operation(self, var='up'):
        """拖拽按钮 拖拽操作"""
        drag = self.dragger_button()  # 拖拽 拖动按钮
        loc = Element().get_element_bounds(drag)  # 获取按钮坐标
        size = self.options_view_size()  # 获取整个选项页面大小
        if var == 'up':
            y = loc[3] - size * 4 / 3
            if loc[3] - size * 4 / 3 < 0:
                y = 0
            self.driver.swipe(loc[2], loc[3], loc[2], y, 1000)  # 向上拖拽
        else:
            self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size - 10, 1000)  # 向下拖拽按钮

    @teststeps
    def study_again(self):
        """《完形填空》 错题再练/再练一遍 操作过程"""
        print('===============================================')
        if self.result.wait_check_result_page():  # 结果页检查点
            item = self.result.again_button()  # 结果页 错题再练/再练一遍 按钮
            item[0].click()
            result = self.cloze_operation()  # 完形填空 - 游戏过程
            return item[1], result

    @teststeps
    def check_detail_page(self, result, rate):
        """《完形填空》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('查看答案页面:')
                count = []  # 回答正确题
                answer = self.get_result()  # 获取 答题结果
                for i in range(int(rate)):
                    if answer[i] != result[i]:
                        print('回答错误:', answer[i], result[i])
                    else:
                        print('回答正确:', answer[i])
                        count.append(answer[i])

                if self.result.wait_check_detail_page():  # 页面检查点
                    self.result.back_up_button()  # 返回结果页
                print('==================================================')
                return count

    @teststeps
    def font_operation(self):
        """Aa文字大小切换按钮 状态判断 及 切换操作"""
        y = []
        middle = self.font_middle()  # first
        large = self.font_large()  # second
        great = self.font_great()  # third

        i = j = 0
        while i < 3:
            bounds = self.get_input_bounds()  # 获取输入框y坐标
            print(self.get.checked(middle), self.get.checked(large), self.get.checked(great))

            if self.get.checked(middle) == 'false':
                if self.get.checked(large) == 'false':
                    y.insert(2, bounds)
                    print('当前选中的Aa按钮为第3个:', bounds)
                    j = 3
                else:
                    if self.get.checked(large) == 'true':
                        y.insert(1, bounds)
                        print('当前选中的Aa按钮为第2个:', bounds)
                        j = 2
            else:
                y.insert(0, bounds)
                print('当前选中的Aa按钮为第1个:', bounds)
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
