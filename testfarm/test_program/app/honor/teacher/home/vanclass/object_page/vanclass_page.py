#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.vue_context import VueContext
from utils.wait_element_vue import WaitElement


class VanclassPage(BasePage):
    """ 班级 页面"""
    tab_icon_locator = (By.XPATH, '//span[@class="van-grid-item__text"]')  # 各tab icon

    van_tips = '★★★ Error- 未进入班级详情页'
    van_vue_tips = '★★★ Error- 未进入班级详情vue页'
    van_list_tips = '★★★ Error- 班级详情页未加载成功'

    more_tips = '★★★ Error- 未进入 班级/学校名称 修改条目'
    more_van_tips = '★★★ Error- 未进入 班级名称 修改页面'
    more_school_tips = '★★★ Error- 未进入 学校名称 修改页面'

    def __init__(self):
        self.wait = WaitElement()
        self.home = ThomePage()
        self.get = GetAttribute()
        self.vue = VueContext()
        self.my_assert = MyAssert()

    @teststeps
    def wait_check_app_page(self, var):
        """以“title:班级名”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="{}"]'.format(var))
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self, var, index=10):
        """以“title: 班级名称”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="%s"]' % var)
        return self.wait.wait_check_element(locator, index)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait.wait_find_element(locator).click()

    # 菜单
    @teststep
    def vanclass_hw(self):
        """本班作业"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="口语/习题"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def vanclass_paper(self):
        """本班卷子"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="卷子"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def word_book(self):
        """单词本"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="单词本"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def daily_listen(self):
        """每日一听"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="每日一听"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def score_ranking(self):
        """积分排行榜"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="积分"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def star_ranking(self):
        """星星排行榜"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="星星"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def vanclass_member(self):
        """班级成员"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="成员"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def invite_st_button(self):
        """以“邀请学生 按钮”的id为依据"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="邀请学生"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststep
    def vanclass_application(self):
        """入班申请"""
        locator = (By.XPATH, '//span[@class="van-grid-item__text" and text()="入班申请"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststeps
    def more_button(self):
        """更多 按钮"""
        locator = (By.XPATH, '//i[@class="class-detail-icon-nav-right van-icon van-icon-ellipsis"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_check_more_tips_page(self):
        """以“更多按钮的条目”为依据"""
        locator = (By.XPATH, '//div[@class="van-popup van-popup--round van-popup--bottom van-action-sheet"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def modify_van_name(self):
        """班级名称 修改"""
        locator = (By.XPATH, '//span[@class="van-action-sheet__name" and text()="班级名称"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def modify_school_name(self):
        """学校名称 修改"""
        locator = (By.XPATH, '//span[@class="van-action-sheet__name" and text()="学校名称"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def delete_van_button(self):
        """删除班级"""
        locator = (By.XPATH, '//span[@class="van-action-sheet__name" and text()="删除班级"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//div[@class="van-action-sheet__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """确认 按钮"""
        locator = (By.XPATH, '//span[text()="确认"]/parent::button')
        self.wait.wait_find_element(locator).click()

    # 列表
    @teststeps
    def wait_check_list_page(self):
        """以“菜单title 元素”为依据"""
        locator = (By.XPATH, '//div[@id="homework-list"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_no_hw_page(self):
        """无作业"""
        locator = (By.XPATH, '//div[text()="[用户指南]学生练得不够?给学生布置个作业吧!"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def hint_text(self):
        """最近2周动态（可点击查看）"""
        locator = (By.XPATH, '//span[@class="class-detail-icon-tip-container-left"]')
        item = self.wait.wait_find_element(locator).text
        print(item)

    @teststeps
    def hint_button(self):
        """帮助 按钮"""
        locator = (By.XPATH, '//img[@class="class-detail-icon-tip-container-right"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def hw_name(self):
        """作业name"""
        locator = (By.XPATH, '//div[@class="homework-list-content-title-text"]')
        return self.wait \
            .wait_find_elements(locator)

    @teststeps
    def hw_create_time(self):
        """作业创建时间"""
        locator = (By.XPATH, '//div[@class="homework-list-content-subtitle-text"]')
        return self.wait \
            .wait_find_elements(locator)

    @teststeps
    def judge_van_modify(self):
        """班级名称 修改验证"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis"]')
        return self.wait \
            .wait_find_element(locator).text

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
    def tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def tips_cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def tips_commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__confirm van-hairline--left"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        return self.wait.wait_check_element(locator)

    # 学校名称修改
    @teststeps
    def wait_check_school_tips_page(self):
        """以“”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__content"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def school_tips_content(self):
        """ 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def commit_button(self):
        """确认 按钮"""
        locator = (By.XPATH, '//span[text()="确认"]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststep
    def input(self):
        """输入框"""
        locator = (By.XPATH, "//input")
        return self.wait \
            .wait_find_element(locator)

    @teststeps
    def judge_vanclass_result_operation(self, van, assign):
        """班级 验证布置结果 具体操作
        :param van:班级
        :param assign:名称
        """
        if self.home.wait_check_page():  # 页面检查点
            print('------------------验证布置结果------------------')
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)

            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                print(var)
                if var == van:
                    name[i].click()  # 进入班级
                    MyAssert().assertTrue_new(self.wait_check_app_page(van), self.van_tips)  # 页面检查点
                    self.vue.switch_h5()  # 切到vue

                    MyAssert().assertTrue(self.wait_check_page(van), self.van_vue_tips)  # 页面检查点
                    if self.wait_check_no_hw_page():
                        MyAssert().assertTrue(self.wait_check_list_page(), self.van_list_tips)  # 页面检查点
                    else:
                        MyAssert().assertTrue(self.wait_check_list_page(), self.van_list_tips)  # 页面检查点
                        hw = self.hw_name()  # 作业名
                        title = self.home.vanclass_name(hw[0].text)
                        MyAssert().assertEqual(title, assign, '★★★ Error- 布置作业失败, {} {}'.format(assign, title))
                        print('布置作业成功')

                    if self.wait_check_page(van):
                        self.back_up_button()  # 返回 主界面
                        self.vue.switch_app()  # 切到apk
                    break

    @teststeps
    def button_enabled_judge(self, length, button, size, max_length=10):
        """按钮enabled状态 与 字符数
        :param length:展示的字符数
        :param button:按钮
        :param size:实际输入的字符数
        :param max_length: 最大字符数
        """
        if 0 < length <= max_length:
            if length != int(size):
                print('★★★ Error- 字符数展示有误', length, size)
            else:
                if self.get.enabled(button) == 'false':
                    print('★★★ Error- 确定按钮不可点击')
        elif length == 0:
            if length != int(size):
                print('★★★ Error- 字符数展示有误', length, size)
            else:
                if self.get.enabled(button) == 'true':
                    print('★★★ Error- 确定按钮未置灰可点击')
        elif length > max_length:
            if length != int(size):
                print('★★★ Error- 字符数展示有误', length, size)
            else:
                if self.get.enabled(button) == 'true':
                    print('★★★ Error- 确定按钮未置灰可点击')
        return self.get.enabled(button)
