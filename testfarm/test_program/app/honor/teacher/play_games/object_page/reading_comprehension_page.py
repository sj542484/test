#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.homework_page import Homework
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from conf.decorator import teststeps, teststep
from conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import ElementBounds
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class ReadComprehension(BasePage):
    """阅读理解"""
    content_value = gv.PACKAGE_ID + "rich_text"  # 文章

    def __init__(self):
        self.get = GetAttribute()
        self.swipe = SwipeFun()
        self.result = ResultPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:阅读理解”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'阅读理解')]")
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
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "dragger")
        return ele

    @teststep
    def question_num(self):
        """题目内容"""
        num = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "question")
        return num

    @teststeps
    def get_first_num(self):
        """获取 当前页面第一个题号"""
        item = self.question_num().text.split(".")[0]
        return item

    @teststeps
    def verify_content_text(self):
        """验证 阅读理解/完形填空的文章 是否存在"""
        locator = (By.ID, self.content_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def article_view(self):
        """文章 元素"""
        ele = self.driver.find_element_by_id(self.content_value)
        return ele

    @teststeps
    def content_desc(self):
        """点击输入框，激活小键盘"""
        content = self.get.description(self.article_view())
        item = content.split(' ')  # y值
        return item[0]

    @teststeps
    def get_result(self, rate):
        """获取 答题结果"""
        answer = {}
        for i in range(int(rate)):
            question = self.question_num().text  # 题目
            if i != 0:
                for step in range(0, 5):
                    if int(self.get_first_num()) == i + 1:  # 正好
                        question = self.question_num().text
                        break
                    elif int(self.get_first_num()) > i + 1:  # 上拉 拉过了
                        self.swipe.swipe_vertical(0.5, 0.7, 0.9)
                        if int(self.get_first_num()) == i + 1:  # 正好
                            question = self.question_num().text
                            break
                        elif int(self.get_first_num()) < i + 1:  # 下拉 拉过了
                            self.swipe.swipe_vertical(0.5, 0.9, 0.8)  # 滑屏

            correct = []
            error = []
            options = self.option_button(question)
            for j in range(len(options[0])):
                print('------')
                var = GetAttribute().description(options[0][j])
                print(var)
                if var == 'right':
                    correct.append(options[1][j].text)  # 获取 答题结果
                elif var == 'error':
                    error.append(options[1][j].text)  # 获取 答题结果

            if correct:
                answer[i].append(correct[0])
            else:
                answer[i].append(error[0])

        print('获取到的答案：', answer)
        return answer

    @teststeps
    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(gv.PACKAGE_ID + "optionlist")
        var = num.size['height']
        return var

    @teststeps
    def option_button(self, var):
        """选项"""
        print(var)
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]"
                                    "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout"
                                    "/android.widget.LinearLayout/android.widget.TextView" % var)

        item = []  # 选项
        content = []  # 选项内容
        for i in range(0, len(ele), 2):
            item.append(ele[i])
            content.append(ele[i+1])
        print('选项个数:', len(item))

        return item, content

    @teststep
    def option_item(self, index):
        """选项 内容"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_item")[index].text
        return ele

    @teststeps
    def reading_operation(self):
        """《阅读理解》 游戏过程
        :return:
        """
        if self.wait_check_page():
            if Homework().wait_check_play_page():
                answer = []  # return 答案
                timestr = []  # 获取每小题的时间

                self.drag_operation()  # 拖拽按钮、Aa判断

                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().commit_button_operation('false')  # 提交 按钮 状态判断 加点击

                    question = self.question_num().text  # 题目
                    if i != 0:
                        for step in range(0, 5):
                            if int(self.get_first_num()) == i+1:  # 正好
                                question = self.question_num().text
                                break
                            elif int(self.get_first_num()) > i+1:  # 上拉 拉过了
                                self.swipe.swipe_vertical(0.5, 0.7, 0.9)
                                if int(self.get_first_num()) == i+1:  # 正好
                                    question = self.question_num().text
                                    break
                                elif int(self.get_first_num()) < i+1:  # 下拉 拉过了
                                    self.swipe.swipe_vertical(0.5, 0.9, 0.8)  # 滑屏

                    options = self.option_button(question)
                    options[0][random.randint(0, len(options[0])) - 1].click()  # 随机点击选项
                    time.sleep(1)
                    for j in range(len(options[0])):
                        if GetAttribute().selected(options[1][j]) == 'true':
                            answer.append(options[1][j].text)  # 获取 答题结果
                            print('我的答案：', options[1][j].text)
                            break

                    if i != int(rate) - 1:
                        self.swipe.swipe_vertical(0.5, 0.9, 0.5)

                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    print('---------------------------')

                Homework().commit_button_operation('true')  # 提交 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                final_time = self.result.get_time(timestr[-1])  # 最后一个小题的时间
                print('=======================================================')
                return rate, answer, final_time

    @teststeps
    def drag_operation(self):
        """拖拽按钮、Aa判断"""
        drag = self.dragger_button()  # 拖动按钮
        loc = ElementBounds().get_element_bounds(drag)  # 获取按钮坐标
        size = self.options_view_size()  # 获取整个选项页面大小
        self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size - 10, 1000)  # 拖拽按钮到最底部，以便测试Aa

        # self.font_operation()  # Aa文字大小切换按钮 状态判断 及 切换操作

        loc = ElementBounds().get_element_bounds(drag)  # 获取按钮坐标
        y = loc[3] - size * 4 / 3
        if loc[3] - size * 4 / 3 < 0:
            y = 0
        self.driver.swipe(loc[2], loc[3], loc[2], y, 1000)  # 向上拖拽

    @teststeps
    def study_again(self):
        """《阅读理解》 错题再练/再练一遍 操作过程"""
        print('====================================================')
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()[0].click()  # 结果页 再练一遍 按钮
            result = self.reading_operation()  # 阅读理解 - 游戏过程
            return result

    @teststeps
    def check_detail_page(self, result, rate):
        """《阅读理解》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('查看答案页面:')
                count = []  # 回答正确题

                answer = self.get_result(rate)  # 获取 答题结果
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
            bounds = self.content_desc()  # 获取y值
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
