#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststeps, teststep
from utils.click_bounds import ClickBounds
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import Element
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class PictureDictation(BasePage):
    """听音选图"""
    progress_value = gv.PACKAGE_ID + "tv_progress"   # 进度
    drop_down_value = gv.PACKAGE_ID + "report_content"  # 下拉菜单 内容

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:听音选图”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'听音选图')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“progress”的xpath-index为依据"""
        locator = (By.ID, self.progress_value)
        return self.wait.wait_check_element(locator)

    # 以下为答案详情页面元素
    @teststep
    def result_voice(self):
        """语音按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "iv_play") \
            .click()

    @teststep
    def result_progress(self):
        """进度"""
        ele = self.driver \
            .find_element_by_id(self.progress_value).text
        return ele

    @teststep
    def result_sentence(self):
        """句子"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "text")
        return ele

    @teststep
    def result_option(self):
        """图片 选项"""
        ele = self.driver \
            .find_elements_by_xpath("//android.support.v7.widget.RecyclerView"
                                    "/android.widget.RelativeLayout/android.widget.TextView")  # 包括 选项+得分
        count = []
        for i in range(len(ele)):
            if ele[i].text == 'A':
                count.append(i)
        count.append(len(ele))  # 多余 只为最后一题

        score = []  # 得分
        item = []  # 所有选项

        for k in range(len(count)-1):
            options = []  # 每一题的选项
            for j in range(count[k], count[k + 1]):
                if GetAttribute().resource_id(ele[j]) == gv.PACKAGE_ID + 'score':
                    score.append(ele[j])
                if GetAttribute().resource_id(ele[j]) == gv.PACKAGE_ID + 'num':
                    options.append(ele[j].text)
            item.append(options)

        return score, item

    @teststep
    def drop_down_button(self, var):
        """正确选项后答对率 下拉按钮"""
        loc = Element().get_element_bounds(var)
        self.driver.tap([(loc[2], loc[3])])

    @teststeps
    def verify_drop_down_content(self, var=5):
        """验证 正确选项后答对率 下拉菜单 是否存在"""

        locator = (By.ID, self.drop_down_value)
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def drop_down_content(self):
        """x% 下拉菜单 内容"""
        item = self.driver \
            .find_element_by_id(self.drop_down_value).text
        print('答题错误详情：', item)
        return item

    @teststeps
    def click_block(self):
        """点击 空白处"""
        ClickBounds().click_bounds(540, 200)

    @teststeps
    def get_num(self, var=0):
        """获取 当前页面第一个题号"""
        item = self.result_sentence()[var].text.split(".")[0]
        return int(item)

    @teststep
    def question_judge(self, var):
        """元素 resource-id属性值是否为题目"""
        value = GetAttribute().resource_id(var)
        if value == gv.PACKAGE_ID + "text":
            return True
        else:
            return False

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1]

    @teststeps
    def error_sum(self, rate):
        """查看答案 滑屏 获取所有题目内容"""
        self.result_voice()  # 听力按钮
        ques_last_index = 0

        for i in range(rate):
            if ques_last_index < rate:
                ques_first_index = self.get_num()  # 当前页面中第一题 题号
                if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                    for step in range(0, 10):
                        SwipeFun().swipe_vertical(0.5, 0.5, 0.8)
                        if self.get_num() == ques_last_index + 1:  # 正好
                            break
                        elif self.get_num() < ques_last_index + 1:  # 下拉拉过了
                            SwipeFun().swipe_vertical(0.5, 0.6, 0.2)  # 滑屏
                            if self.get_num() == ques_last_index + 1:  # 正好
                                break

                last_one = self.get_last_element()  # 页面最后一个元素
                ques_num = self.result_sentence()  # 题目

                if self.question_judge(last_one):  # 判断最后一项为题目
                    for j in range(len(ques_num) - 1):
                        print('-----------------------------')
                        current_index = self.get_num(j)
                        if current_index > ques_last_index:
                            print(ques_num[j].text)
                            options = self.result_option()  # 选项
                            print('选项:', options[1][j])
                            # self.drop_down_operation(j)  # 选项内容及下拉按钮是否可点击
                            ques_last_index = self.get_num(j)  # 当前页面中 做过的最后一题 题号
                else:  # 判断最后一题为选项
                    for k in range(len(ques_num)):
                        print('-----------------------------')
                        if len(ques_num) == 1 or k < len(ques_num) - 1:  # 前面的题目照常点击
                            current_index = self.get_num(k)

                            if current_index > ques_last_index:
                                print(ques_num[k].text)
                                options = self.result_option()  # 选项
                                print('选项:', options[1][k])
                                # self.drop_down_operation(k)  # 选项内容及下拉按钮是否可点击
                                ques_last_index = self.get_num(k)  # 当前页面中 做过的最后一题 题号
                        elif k == len(ques_num) - 1:  # 最后一个题目上滑一部分再进行选择
                            SwipeFun().swipe_vertical(0.5, 0.9, 0.3)

                            ques_num = self.result_sentence()
                            for z in range(len(ques_num)):
                                current_index = self.get_num(z)
                                if current_index > ques_last_index:
                                    print(ques_num[z].text)
                                    options = self.result_option()  # 选项
                                    print('选项:', options[1][z])
                                    # self.drop_down_operation(z)  # 选项内容及下拉按钮是否可点击
                                    ques_last_index = self.get_num(z)  # 当前页面中 做过的最后一题 题号
                                    break

                if i != rate - 1:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.4)  # 滑屏
            else:
                break

    @teststeps
    def drop_down_operation(self, k):
        """下拉按钮"""
        options = self.result_option()  # 选项
        print('选项:', options[1][k])
        rate = re.sub("\D", "", options[0][k].text.split()[-1])  # 准确率

        if rate == '' and options[2][k].text.split()[-1] == '未作答':
            print('该题还没有学生完成')
        else:
            if int(rate) < 100:
                self.drop_down_button(options[0][k])
                if self.verify_drop_down_content():
                    content = self.drop_down_content()
                    self.click_block()

                    item = self.rm_bracket(content)  # 去掉括号及其中的内容
                    var = item.split('\n')  # 以'\n'分割字符串

                    for i in range(0, len(var) - 1, 2):  # len()-1是为了去掉最后一个换行符分割出的空元素
                        if var[i] not in options[1][k]:
                            print('★★★ Error -下拉菜单内容不是本题选项', options[1][k], var[i])
            elif int(rate) == 100:
                print('该题正确率100%')
            else:
                print('★★★ Error -该题正确率', rate)

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

