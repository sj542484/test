#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.play_games.object_page.homework_page import Homework
from testfarm.test_program.app.honor.teacher.play_games.object_page.result_page import ResultPage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.get_element_bounds import Element
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class CompleteArticle(BasePage):
    """补全文章"""
    def __init__(self):
        self.result = ResultPage()
        self.get = GetAttribute()
        self.hw = Homework()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:补全文章”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'补全文章')]")
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
    def option_button(self):
        """选项ABCD"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + 'tv_char')
        return ele

    @teststep
    def option_content(self, index):
        """选项 内容"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + 'tv_item')[index].text
        print('选项内容:', ele)
        return ele

    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(gv.PACKAGE_ID + "option")
        var = num.size
        return var['height']

    @teststep
    def input_text(self):
        """输入框"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "rich_text")
        return ele

    @teststeps
    def get_input_bounds(self):
        """获取 输入框坐标"""
        content = self.get.description(self.input_text())
        item = content.split(' ')  # y值
        return item[0]

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tb_content")
        return self.wait.wait_check_element(locator)

    @teststeps
    def get_result(self):
        """获取 输入框 的结果"""
        var = self.get.description(self.input_text())
        content = re.match(".* ## (.*)",var).group(1)
        answer = content.split('  ')  # answer
        return answer

    @teststeps
    def complete_article_operation(self):
        """《补全文章》 游戏过程"""
        if self.wait_check_page():
            content = []
            timestr = []  # 获取每小题的时间

            self.swipe.swipe_vertical(0.5, 0.2, 0.45)  # 滑屏 (由于补全文章 是直接定位到第一个空）
            self.font_operation()  # Aa文字大小切换按钮 切换 及状态统计

            self.drag_operation()  # 向上拖拽按钮操作

            rate = self.hw.rate()
            for i in range(int(rate)):
                self.hw.rate_judge(rate, i)  # 测试当前rate值显示是否正确
                self.hw.next_button_operation('false')  # 下一题 按钮 判断加 点击操作

                options = self.option_button()  # 选项ABCD
                if len(options) < i+1:
                    options = self.option_button()  # 选项ABCD
                    self.swipe.swipe_vertical(0.5, 0.9, 0.6)  # 滑屏

                item = [options[i].text]
                options[i].click()  # 依次点击选项

                content.append(self.get_result()[i])  # 测试 是否答案已填入文章中
                time.sleep(1)
                if content[i] == ' ':
                    print('★★★ Error - 答案未填入文章中')
                else:
                    print('第%s题:' % (i+1))
                    print(item, content[i])
                timestr.append(self.hw.time())  # 统计每小题的计时控件time信息
                print('-------------------------')

                if i == int(rate) - 1:
                    self.drag_operation('down')  # 向下拖拽按钮操作

            self.hw.next_button_operation('true')  # 下一题 按钮 状态判断 加点击
            final_time = ResultPage().get_time(timestr[len(timestr) - 1])  # 最后一个小题的时间
            self.hw.now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
            print('============================================')
            return rate, final_time

    @teststeps
    def drag_operation(self, var='up'):
        """拖拽按钮 拖拽操作"""
        drag = self.dragger_button()  # 拖拽 拖动按钮
        loc = Element().get_element_bounds(drag)  # 获取按钮坐标
        size = self.options_view_size()  # 获取整个选项页面大小
        if var == 'up':
            self.driver.swipe(loc[2], loc[3], loc[2], loc[3] - size, 1000)  # 向上拖拽
        else:
            self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size - 10, 1000)  # 向下拖拽按钮

    @teststeps
    def result_detail_page(self):
        """查看答案页面"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():  # 页面检查点
                if self.wait_check_detail_page():
                    item = self.get_result()
                    print("正确答案:", item)
                    self.result.back_up_button()  # 返回结果页

    @teststeps
    def font_operation(self):
        """Aa文字大小切换按钮 状态判断 及 切换操作"""
        self.swipe.swipe_vertical(0.5, 0.2, 0.45)  # 滑屏 (由于补全文章 是直接定位到第一个空）
        if self.hw.wait_check_play_page():
            y = []
            middle = self.font_middle()  # first
            large = self.font_large()  # second
            great = self.font_great()  # third

            i = j = 0
            while i < 3:
                bounds = self.get_input_bounds()  # 获取输入框坐标
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
