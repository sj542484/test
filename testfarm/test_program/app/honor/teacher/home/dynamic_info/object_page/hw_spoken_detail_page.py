#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys

from selenium.webdriver.common.by import By

from app.honor.teacher.home.dynamic_info.test_data.tips_data import TipsData
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert, MyToast
from utils.toast_find import Toast
from utils.wait_element_vue import WaitElement


class HwDetailPage(BasePage):
    """ 答题分析/完成情况 详情页面"""
    game_type_value = '//span[@class="van-tag van-tag--plain van-tag--large van-tag--primary van-hairline--surround"]'  # 小游戏类型

    st_item_value = "//div[@id='student-cell']"  # 完成情况 学生条目
    hw_item_value = "//div[@id='question-cell']"  # 答题分析 作业条目

    tab_class_value = 'van-tab van-tab--active'  # 完成情况/答题分析 tab被选中时 class值

    hw_report_tips = '★★★ Error- 未进入答题分析/完成情况 详情页面'
    hw_detail_tips = '★★★ Error- 未进入答题分析/完成情况 vue详情页面'

    st_list_tips = '★★★ Error- 完成情况tab 学生列表未加载成功'
    hw_list_tips = '★★★ Error- 答题分析 页面作业列表'

    more_tips = '★★★ Error- 未进入更多按钮详情'
    edit_tips = '★★★ Error- 未进入编辑作业 详情页'
    edit_list_tips = '★★★ Error- 编辑作业 详情页未加载成功'

    def __init__(self):
        self.wait = WaitElement()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_page(self, var=15):
        """以“title: 答题分析”为依据"""
        locator = (By.XPATH, "//span[text()='完成情况']")
        ele = self.wait.wait_check_element(locator, var)
        self.my_assert.assertTrue(ele, self.hw_detail_tips)
        return ele

    @teststeps
    def wait_check_empty_tips_page(self, var=10):
        """以 暂无数据提示 作为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error" and text()="暂无数据"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def page_source(self):
        """以“获取page_source”"""
        print('打开：', self.driver.page_source)

    @teststep
    def finished_tab(self):
        """完成情况"""
        locator = (By.XPATH, "//span[text()='完成情况']")
        self.wait.wait_find_element(locator).click()

    @teststep
    def analysis_tab(self):
        """答题分析"""
        locator = (By.XPATH, "//span[text()='答题分析']")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def check_tab_status(self, var):
        """按学生看/按题查看 tab 父元素  状态判断"""
        value = var.find_element_by_xpath('.//parent::div').get_attribute('class')
        return value

    @teststep
    def more_button(self):
        """更多 按钮"""
        locator = (By.XPATH, '//i[@class="nav-right-icon van-icon van-icon-ellipsis"]')
        self.wait \
            .wait_find_element(locator).click()

    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.XPATH, '//div[@class="van-popup van-popup--round van-popup--bottom van-action-sheet"]')
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.hw_detail_tips)
        return ele

    @teststeps
    def more_recommend_button(self):
        """推荐到学校 按钮"""
        locator = (By.XPATH, '//span[text()="推荐到学校"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def more_add_button(self):
        """加入题筐 按钮"""
        locator = (By.XPATH, '//span[text()="加入题筐"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def more_edit_button(self):
        """编辑 按钮"""
        locator = (By.XPATH, '//span[text()="编辑"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def more_publish_button(self):
        """再次发布 按钮"""
        locator = (By.XPATH, '//span[text()="再次发布"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def more_delete_button(self):
        """删除 按钮"""
        locator = (By.XPATH, '//span[text()="删除"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def more_cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//div[@class="van-action-sheet__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    # 完成情况tab 学生列表
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生完成情况 元素”为依据"""
        locator = (By.XPATH, self.st_item_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def finish_tab_st_items(self):
        """学生 条目"""
        locator = (By.XPATH, self.st_item_value)
        ele = self.wait.wait_find_elements(locator)

        content = []  # 页面内所有条目 元素text
        elements = []  # 页面内所有条目元素
        print(len(ele))
        for i in range(len(ele)):
            item = []  # 每一个条目的所有元素text
            element = []  # 每一个条目的所有元素
            descendant = ele[i].find_elements_by_xpath('.//descendant::*')[3:5]
            print('des:', descendant)

            for j in range(len(descendant)):
                item.append(descendant[j].text)
                element.append(descendant[j])

            content.append(item)
            elements.append(element)

        return elements, content

    @teststep
    def st_type(self):
        """基础班/提分版/试用期学生"""
        locator = (By.XPATH, '//div[@class="van-image van-icon__image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_finish_status(self):
        """学生 完成与否"""
        locator = (By.XPATH, '//span[@class="student-cell-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="van-cell__title student-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="van-image van-image--round"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    # 答题分析tab 页面
    @teststeps
    def wait_check_hw_list_page(self):
        """以“cup 元素”为依据"""
        locator = (By.XPATH, self.hw_item_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def analysis_tab_hw_items(self):
        """作业包 条目"""
        locator = (By.XPATH, self.hw_item_value)
        return self.wait.wait_find_elements(locator)

    @teststeps
    def analysis_tab_hw_list_info(self):
        """游戏 条目"""
        content = []  # 页面内所有条目 元素text
        elements = []  # 页面内所有条目元素

        ele = self.analysis_tab_hw_items()  # 作业包 条目
        for i in range(len(ele)):
            descendant = ele[i].find_elements_by_xpath('.//descendant::*')[0]
            elements.append(descendant)

            item = descendant.text.split('\n')
            if '提分' in item[0]:
                item.insert(1, '提分')
                item[0] = item[0][:4]

            content.append(item)

        return elements, content

    @teststep
    def game_type(self):
        """游戏类型"""
        locator = (By.XPATH, self.game_type_value)
        return self.wait.wait_find_elements(locator)

    @teststeps
    def game_level(self):
        """提分"""
        locator = (By.XPATH, '//span[@class="question-cell-tag van-tag van-tag--large van-tag--primary"]')
        ele = self.wait.wait_find_elements(locator)
        content = [k.text for k in ele if k.get_attribute('style') != 'background-color: rgb(65, 88, 177); display: none;']
        return content

    @teststep
    def game_num(self):
        """游戏 小题数"""
        locator = (By.XPATH, '//span[@class="question-cell-count"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_name(self):
        """游戏 名称"""
        locator = (By.XPATH, '//div[@class="question-cell-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def average_achievement(self):
        """全班首轮平均成绩x%"""
        locator = (By.XPATH, '//span[@class="question-cell-label-left"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def ranking_list(self):
        """排行榜"""
        locator = (By.XPATH, '//span[@class="question-cell-label-right"]')
        return self.wait.wait_find_elements(locator)

    # 编辑作业 页面
    @teststeps
    def wait_check_edit_page(self):
        """以“title:编辑作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[@text='编辑作业']")
        ele = self.wait.wait_check_element(locator)
        self.my_assert.assertTrue(ele, self.edit_tips)
        return ele

    @teststep
    def assign_button(self):
        """发布作业 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "action_first")
        self.wait\
            .wait_find_element(locator).click()

    # 删除作业/推荐到本校 tips 页面
    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def delete_tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__cancel"]')
        self.wait\
            .wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__confirm van-hairline--left"]')
        self.wait \
            .wait_find_elements(locator)[-1].click()

    @teststep
    def recommend_tips_content(self):
        """推荐到学校 温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="dialog-content-message"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststeps
    def delete_cancel_operation(self):
        """删除作业 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.more_delete_button()  # 删除按钮

            self.my_assert.assertEqual(self.wait_check_tips_page(), True, '★★★ Error- 无删除提示框')
            print('---------删除作业---------')
            self.tips_title()
            self.delete_tips_content()
            self.cancel_button()  # 取消按钮
            print('---------------')

            if not self.wait_check_tips_page():
                print('取消删除')

    @teststeps
    def delete_commit_operation(self):
        """删除作业 具体操作"""
        self.name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.more_delete_button()  # 删除按钮

            self.my_assert.assertEqual(self.wait_check_tips_page(), True, '★★★ Error- 无删除提示框')
            print('---------删除作业---------')
            self.commit_button()  # 确定按钮
            print('确定删除')
            MyToast().toast_assert(self.name, Toast().toast_vue_operation(TipsData().delete_success))  # 获取toast
