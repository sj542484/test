#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class FilterPage(BasePage):
    """ 筛选 页面"""
    label_name_value = gv.PACKAGE_ID + "tv_label_name"  # 标签名
    filter_tips = '★★★ Error- 未进入 筛选页面'

    def __init__(self):
        self.get = GetAttribute()
        self.wait = WaitElement()
        self.question = TestBankPage()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self):
        """以“”为依据"""
        locator = (By.ID, self.label_name_value)
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.filter_tips)
        return ele

    @teststep
    def click_public(self):
        """以“公共”的text为依据"""
        locator = (By.ID, self.label_name_value)
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_school(self):
        """以“本校”的text为依据"""
        locator = (By.ID, self.label_name_value)
        self.wait.wait_find_elements(locator)[1].click()

    @teststep
    def question_menu(self):
        """以“题单”的text为依据"""
        locator = (By.ID, self.label_name_value)
        return self.wait.wait_find_elements(locator)[2]

    @teststep
    def click_question_menu(self):
        """以“题单”的text为依据"""
        locator = (By.ID, self.label_name_value)
        self.wait.wait_find_elements(locator)[2].click()

    @teststep
    def game_list(self):
        """以“大题”的text为依据"""
        locator = (By.ID, self.label_name_value)
        return self.wait.wait_find_elements(locator)[3]

    @teststep
    def click_game_list(self):
        """以“大题”的text为依据"""
        locator = (By.ID, self.label_name_value)
        self.wait.wait_find_elements(locator)[3].click()

    @teststep
    def test_paper(self):
        """以“试卷”的text为依据"""
        locator = (By.ID, self.label_name_value)
        return self.wait.wait_find_elements(locator)[4]

    @teststep
    def click_test_paper(self):
        """以“试卷”的text为依据"""
        locator = (By.ID, self.label_name_value)
        self.wait.wait_find_elements(locator)[4].click()

    @teststep
    def reset_button(self):
        """以“重置按钮”的text为依据"""
        print('点击重置按钮')
        locator = (By.ID, gv.PACKAGE_ID + "action_first")
        self.wait.wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """以“确定按钮”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "action_second")
        self.wait.wait_find_element(locator).click()

    @teststep
    def expand_button(self):
        """以“上下拉 按钮”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_expand")
        self.wait.wait_find_element(locator).click()

    @teststeps
    def label_title(self):
        """以“标签 title”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_title")
        ele = self.wait.wait_find_elements(locator)

        content = [i.text for i in ele]
        return content

    @teststep
    def label_name(self):
        """以“标签 name”的id为依据"""
        locator = (By.ID, self.label_name_value)
        return self.wait.wait_find_elements(locator)

    @teststep
    def expand_icon(self):
        """以“收起 icon”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_expand")
        return self.wait.wait_find_elements(locator)

    @teststeps
    def all_element(self):
        """页面内所有label元素"""
        locator = (By.XPATH, "//android.widget.LinearLayout/android.support.v7.widget.RecyclerView"
                             "/android.widget.LinearLayout/"
                             "descendant::*/android.widget.TextView")
        return self.wait.wait_find_elements(locator)

    # 本校标签
    @teststeps
    def wait_check_school_label_page(self):
        """以“title:学校标签”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学校标签')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_label_list_page(self):
        """以“存在 标签列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "label_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def check_button(self):
        """以“单选 按钮”的class name为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "check")
        return self.wait.wait_find_elements(locator)

    @teststep
    def school_label_name(self):
        """以“本校标签 name”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "label_name")
        return self.wait.wait_find_elements(locator)

    @teststep
    def confirm_button(self):
        """确定 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "confirm")
        self.wait.wait_find_element(locator).click()

    @teststeps
    def reset_filter_operation(self):
        """恢复 筛选"""
        self.question.filter_button()  # 筛选按钮

        if self.wait_check_page():  # 页面检查点
            self.reset_button()  # 点击 重置按钮
            if self.wait_check_page():  # 页面检查点
                self.commit_button()  # 点击 确定按钮

                if self.question.wait_check_page():  # 页面检查点
                    ThomePage().click_tab_hw()  # 返回主界面

    @teststeps
    def filter_all_element(self, var):
        """所有label title+小标签"""
        ele = self.all_element()  # 所有元素

        content = []  # 所有元素
        item = []  # 翻页前最后元素
        for i in range(len(ele)):
            item.append(ele[-1].text)
            content.append(ele[i].text)

        SwipeFun().swipe_vertical(0.5, 0.7, 0.2)
        if self.wait_check_page():
            ele = self.all_element()  # 所有元素

            index = 0
            for i in range(len(ele)):
                if ele[i].text == item[0]:
                    index = i+1
                    break

            for j in range(index, len(ele)):
                content.append(ele[j].text)

        self.label_content(var, content)  # print所有元素

    @teststeps
    def label_content(self, var, content):
        """筛选 每个标题下的所有label"""
        count = []
        if var == 3:  # 试卷
            for i in range(len(content)):
                if content[i] == '题库':
                    count.append(i)
                elif content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '本校标签':
                    count.append(i)
                    break
        elif var == 4:  # 题单
            for i in range(len(content)):
                if content[i] == '题库':
                    count.append(i)
                elif content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                elif content[i] == '本校标签':
                    count.append(i)
                    break
        elif var == 5:  # 大题
            for i in range(len(content)):
                if content[i] == '题库':
                    count.append(i)
                elif content[i] == '资源类型':
                    count.append(i)
                elif content[i] == '活动类型':
                    count.append(i)
                elif content[i] == '系统标签':
                    count.append(i)
                elif content[i] == '本校标签':
                    count.append(i)
                    break

        count.append(len(content))
        for i in range(len(count)):  # print 所有元素
            if i + 1 == len(count):
                print('---------------------')
                for j in range(count[i], count[-1]):
                    print(content[j])
            else:
                print('---------------------')
                for j in range(count[i], count[i + 1]):
                    print(content[j])
        return count

    @teststeps
    def source_type_selected(self):
        """选中的资源类型"""
        if self.get.selected(self.question_menu()) == 'true':  # 题单
            print('======================选择题单======================')
            self.filter_all_element(4)  # 所有label title+小标签
        else:
            if self.get.selected(self.game_list()) == 'true':  # 大题
                print('======================选择大题======================')
                self.filter_all_element(5)  # 所有label title+小标签
            else:
                if self.get.selected(self.test_paper()) == 'true':  # 试卷
                    print('======================选择试卷======================')
                    self.filter_all_element(3)  # 所有label title+小标签
        print('============================================')

    @teststeps
    def choose_school_label(self):
        """选择本校标签"""
        if self.wait_check_school_label_page():
            print('--------')

            cancel = 0
            choose = 0
            if self.wait_check_label_list_page():
                button = self.check_button()  # 单选框
                label = self.school_label_name()  # 本校标签名

                for i in range(len(button)):
                    if GetAttribute().checked(button[i]) == 'true':
                        cancel = label[i].text
                        print('取消选择标签:', cancel)
                        button[i].click()  # 取消选择 一个标签
                    else:
                        print('所选择的标签:', label[i].text)
                        choose = label[i].text
                        button[i].click()  # 选择 一个班
                        print('-----------')
                        break
                self.confirm_button()  # 确定按钮
                return cancel, choose
            elif ThomePage().wait_check_empty_tips_page():
                print('%% 本校暂无标签 %%')
                self.confirm_button()  # 确定按钮

    @teststeps
    def judge_school_label_result(self, name, label, mode='大题'):
        """ 验证 - 选择本校标签 结果 （本校标签设置 -- PC题库-本校-标签管理）
        :param name: 题名
        :param label:标签名
        :param mode:类型
        """
        print('------------验证 -选择本校标签 结果------------')
        if self.question.wait_check_page('搜索'):  # 页面检查点
            self.question.filter_button()  # 筛选按钮

            if self.wait_check_page():  # 页面检查点
                self.click_school()  # 选择本校

                if self.wait_check_page():  # 页面检查点
                    if mode == '大题':
                        if GetAttribute().selected(self.game_list()) == 'false':  # 大题
                            self.click_game_list()  # 选择大题
                    elif mode == '试卷':
                        if GetAttribute().selected(self.test_paper()) == 'false':  # 试卷
                            self.click_test_paper()  # 选择试卷
                    elif mode == '题单':
                        if GetAttribute().selected(self.question_menu()) == 'false':  # 题单
                            self.click_question_menu()  # 选择题单

                if self.wait_check_page():  # 页面检查点
                    all_label = self.label_name()  # 所有标签
                    for k in range(len(all_label)):
                        if all_label[k].text == label:   # 标签名
                            print('选择的标签为:', all_label[k].text)
                            all_label[k].click()  # 选择一个标签
                            break
                    self.commit_button()  # 确定按钮

                if not self.question.wait_check_page(mode):  # 页面检查点
                    print('★★★ Error- 选择 {} 标签不成功'.format(mode))

                count = 0
                item = self.question.question_name()  # 获取题目
                for k in range(len(item[1])):
                    if name == item[1][k]:
                        count += 1
                        break
                if count == 0:
                    print('★★★ Error- 选择本校标签失败', name)
                else:
                    print('选择本校标签成功')

                self.question.filter_button()  # 筛选按钮
                if self.wait_check_page():  # 页面检查点
                    self.click_public()  # 选择公共
                    self.commit_button()  # 确定按钮
