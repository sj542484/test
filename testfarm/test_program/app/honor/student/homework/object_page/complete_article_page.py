#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from conf.decorator import teststeps, teststep
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class CompleteArticle(BasePage):
    """补全文章"""
    def __init__(self):
        self.result = ResultPage()
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:补全文章”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'补全文章')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_play_page(self):
        """以“rate”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,'{}rate)]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def rate(self):
        """获取作业数量"""
        rate = self.driver \
            .find_element_by_id(self.id_type() + "rate").text
        return rate

    @teststep
    def font_middle(self):
        """第一个Aa"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "font_middle")

        return ele

    @teststep
    def font_large(self):
        """第二个Aa"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "font_large")
        return ele

    @teststep
    def font_great(self):
        """第三个Aa"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "font_great")
        return ele

    @teststep
    def dragger_button(self):
        """拖动按钮"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "dragger")
        return ele

    @teststep
    def option_button(self):
        """选项ABCD"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + 'tv_char')
        return ele

    @teststep
    def option_content(self, index):
        """选项 内容"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + 'tv_item')[index].text
        print('选项内容:', ele)
        return ele

    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(self.id_type() + "option")
        var = num.size
        return var['height']

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststep
    def input_text(self):
        """输入框"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "ss_view")
        return ele

    @teststeps
    def get_input_bounds(self):
        """获取 输入框坐标"""
        ele = self.input_text()  # 输入框
        content = self.get.get_description(ele)
        item_x = re.match(".*\[(.*)\].*\[", content)  # x值
        item_y = re.match(".*\[(.*)\].*", content)  # y值
        x = item_x.group(1).split(',')  # 所有输入框y值的列表
        y = item_y.group(1).split(',')  # 所有输入框x值的列表
        return x, y

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}tb_content)']".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def get_result(self):
        """获取 输入框 的结果"""
        ele = self.input_text()  # 输入框
        content = self.get.get_description(ele)
        value = re.match("\\[(.+?)\\]", content)  # answer
        answer = value.group(1).split(',')  # 所有输入框值的列表
        return answer

    @teststeps
    def complete_article_operate(self):
        """《补全文章》 游戏过程"""
        if self.wait_check_page():
            if self.wait_check_play_page():
                content = []
                timestr = []  # 获取每小题的时间

                self.font_operate()  # Aa文字大小切换按钮 切换 及状态统计

                drag = self.dragger_button()  # 拖拽 拖动按钮
                loc = self.get_element_bounds(drag)  # 获取按钮坐标
                size = self.options_view_size()  # 获取整个选项页面大小
                self.driver.swipe(loc[2], loc[3], loc[2], loc[3] - size, 1000)  # 向上拖拽

                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    options = self.option_button()  # 选项ABCD
                    if len(options) < i+1:
                        options = self.option_button()  # 选项ABCD
                        self.screen_swipe_up(0.5, 0.9, 0.6, 1000)  # 滑屏

                    text = [options[i].text]
                    options[i].click()  # 依次点击选项

                    content.append(self.get_result()[i])  # 测试 是否答案已填入文章中
                    time.sleep(1)
                    if content[i] == ' ':
                        print('❌❌❌ Error - 答案未填入文章中')
                    else:
                        print('第%s题:' % (i+1))
                        print(text, content[i])
                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    print('-------------------------')

                    if i == int(rate) - 1:
                        drag = self.dragger_button()  # 拖拽 拖动按钮
                        loc = self.get_element_bounds(drag)  # 获取按钮坐标
                        size = self.options_view_size()  # 获取整个选项页面大小
                        self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size - 10, 1000)  # 向下拖拽按钮

                Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('============================================')
                return rate

    @teststeps
    def result_detail_page(self):
        """查看答案页面"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():  # 页面检查点
                if self.wait_check_detail_page():
                    print('查看答案页面:')
                    item = self.get_result()
                    print("正确答案:", item)
                    self.result.back_up_button()  # 返回结果页

    @teststeps
    def font_operate(self):
        """Aa文字大小切换按钮 状态判断 及 切换操作"""
        x = []
        y = []
        middle = self.font_middle()  # first
        large = self.font_large()  # second
        great = self.font_great()  # third

        i = 0
        j = 0
        while i < 3:
            bounds = self.get_input_bounds()  # 获取输入框坐标
            print(self.get.get_checked(middle), self.get.get_checked(large), self.get.get_checked(great))

            if self.get.get_checked(middle) == 'false':
                if self.get.get_checked(large) == 'false':
                    x.insert(2, bounds[0][0])
                    y.insert(2, bounds[1][0])
                    print('当前选中的Aa按钮为第3个:', bounds[0][0], bounds[1][0])
                    j = 3
                else:
                    if self.get.get_checked(large) == 'true':
                        x.insert(1, bounds[0][0])
                        y.insert(1, bounds[1][0])
                        print('当前选中的Aa按钮为第2个:', bounds[0][0], bounds[1][0])
                        j = 2
            else:
                x.insert(0, bounds[0][0])
                y.insert(0, bounds[1][0])
                print('当前选中的Aa按钮为第1个:', bounds[0][0], bounds[1][0])
                j = 1

            if j == 1:
                large.click()
            elif j == 2:
                great.click()
            elif j == 3:
                middle.click()
            i += 1
            print('--------------------------------------------')
            time.sleep(2)

        if not float(y[2]) > float(y[1]) > float(y[0]):
            print('❌❌❌ Error - Aa文字大小切换按钮:', y)
        print('==============================================')
