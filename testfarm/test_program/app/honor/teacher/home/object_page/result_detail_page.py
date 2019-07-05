#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class ResultDetailPage(BasePage):
    """结果 详情页"""
    result_answer_value = gv.PACKAGE_ID + "tv_answer"  # 单词
    voice_value = gv.PACKAGE_ID + "iv_speak"  # 发音按钮
    char_value = gv.PACKAGE_ID + "tv_char"  # 选项元素 ABCD
    question_value = gv.PACKAGE_ID + "tv_question"  # 题目

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var):
        """以“title: 小游戏名”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_answer_list_page(self):
        """以“答案 元素”的ID为依据"""
        locator = (By.ID, self.result_answer_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def first_report(self):
        """首次正答率"""
        item = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "first_report").text
        print(item)
        return item

    @teststep
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(self.voice_value)[index] \
            .click()

    @teststep
    def result_answer(self, index):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(self.result_answer_value)[index].text
        return ele

    @teststep
    def result_explain(self):
        """解释"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_hint")
        return ele

    @teststep
    def result_mine(self, index):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_mine")[index]
        value = GetAttribute().selected(ele)
        return value

    # 单选
    @teststeps
    def wait_check_option_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.ID, )
        return self.wait.wait_check_element(locator)

    @teststep
    def single_question(self):
        """题目"""
        item = self.driver \
            .find_elements_by_id(self.question_value)
        return item

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

    @teststeps
    def option_button(self):
        """当前页面中所有题目的选项"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@resource-id,'%s')]"
                                    "/parent::android.widget.LinearLayout"
                                    "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView" % self.question_value)

        item = []  # 当前页面中所有题目的选项
        var = []  # 所有题目的正确选项
        count = []  # text为A的元素index

        for i in range(0, len(ele), 2):
            if ele[i].text == 'A':
                count.append(i)
        count.append(len(ele))  # 多余 只为最后一题

        for i in range(len(count) - 1):
            options = []  # 每个题目的选项
            for j in range(count[i], count[i + 1], 2):
                if j + 1 == count[-1] and (j + 1) % 2 != 0:  # len(ele)为奇数 去掉
                    break

                options.append(ele[j + 1].text)  # 选项内容
                if GetAttribute().selected(ele[j]) == 'true':
                    var.append(ele[j + 1])  # ABCD元素
            item.append(options)

        return item, var

    @teststep
    def question_judge(self, var):
        """元素 resource-id属性值是否为题目"""
        value = GetAttribute().resource_id(var)
        if value == self.question_value:
            return True
        else:
            return False

    @teststeps
    def get_first_num(self):
        """获取 当前页面第一个题号"""
        item = self.single_question()[0].text.split(".")[0]
        return item

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1]

    @teststeps
    def swipe_operation(self, swipe_num):
        """滑屏 获取所有题目内容"""
        ques_last_index = 0  # 每个页面最后操作过的题号

        if self.wait_check_option_list_page():
            for i in range(swipe_num):
                if ques_last_index < swipe_num:
                    ques_num = self.single_question()  # 题目
                    ques_first_index = int(ques_num[0].text.split(".")[0])

                    if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                        for step in range(0, 10):
                            SwipeFun().swipe_vertical(0.5, 0.5, 0.62)
                            if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                                ques_num = self.single_question()
                                break
                            elif int(self.get_first_num()) < ques_last_index + 1:  # 下拉拉过了
                                SwipeFun().swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                                if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                                    ques_num = self.single_question()
                                    break
                            # else:
                            #     print('再下拉一次:', int(self.get_first_num()), ques_last_index)

                    last_one = self.get_last_element()  # 页面中最后一个元素

                    if self.question_judge(last_one):  # 判断最后一项是否为题目
                        options = self.option_button()  # 当前页面中所有题目的选项
                        for j in range(len(ques_num) - 1):
                            current_index = int(ques_num[j].text.split(".")[0])
                            if current_index > ques_last_index:
                                print('-----------------------------------------')
                                print(ques_num[j].text, '\n',
                                      '选项:', options[0][j])
                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                    else:  # 判断最后一题是否为选项
                        options = self.option_button()  # 当前页面中所有题目的选项
                        for k in range(len(ques_num)):
                            if k < len(ques_num) - 1:  # 前面的题目照常点击
                                current_index = int(ques_num[k].text.split(".")[0])
                                if current_index > ques_last_index:
                                    print('-----------------------------------------')
                                    print(ques_num[k].text, '\n',
                                          '选项:', options[0][k])
                                    if k == len(ques_num) - 2:
                                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                            elif k == len(ques_num) - 1:  # 最后一个题目上滑一部分再进行选择
                                SwipeFun.swipe_vertical(0.5, 0.76, 0.60)
                                ques_num = self.single_question()
                                options = self.option_button()  # 当前页面中所有题目的选项
                                for z in range(len(ques_num)):
                                    current_index = int(ques_num[z].text.split(".")[0])
                                    if current_index > ques_last_index:
                                        print('-----------------------------------------')
                                        print(ques_num[z].text, '\n',
                                              '选项:', options[0][z])
                                        ques_last_index = int(ques_num[z].text.split(".")[0])
                                        break

                    if i != swipe_num - 1:
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
                else:
                    break
