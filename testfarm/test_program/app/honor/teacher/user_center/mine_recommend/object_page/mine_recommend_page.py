#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class RecommendPage(BasePage):
    """我的推荐 页面"""
    def __init__(self):
        self.filter = FilterPage()
        self.get = GetAttribute()
        self.wait = WaitElement()
        self.question = TestBankPage()
        self.detail = QuestionDetailPage()
        self.game = GamesPage()
        self.basket = TestBasketPage()
        self.home = ThomePage()
        self.user = TuserCenterPage()

    @teststeps
    def wait_check_page(self):
        """以“title:我的推荐”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的推荐')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“存在 我的推荐列表”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "author")
        return self.wait.wait_check_element(locator)

    @teststep
    def question_name(self):
        """以“题目名称”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        content = [x.text for x in ele]
        return ele, content

    @teststep
    def label_manage_button(self):
        """以“标签管理 按钮”的class name为依据"""
        self.driver \
            .find_elements_by_class_name("android.widget.ImageView") \
            .click()

    @teststep
    def the_end(self):
        """以“没有更多了”的text为依据"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'没有更多了')]") \
            .text
        return item

    @teststep
    def question_basket(self):
        """以 右下角“题筐 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_pool") \
            .click()

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class name为依据"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageButton") \
            .click()

    @teststep
    def menu_button(self, index):
        """以 条目右侧“菜单按钮”的id为依据"""
        self.driver\
            .find_elements_by_id(gv.PACKAGE_ID + "iv_eg")[index] \
            .click()

    # 标签管理
    @teststeps
    def wait_check_manage_page(self):
        """以“fb_add_label”的text为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "fb_add_label")
        return self.wait.wait_check_element(locator)

    # 菜单 内容
    @teststep
    def put_to_basket(self):
        """以 菜单- 加入题筐 的text为依据"""
        self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'加入题筐')]") \
            .click()

    @teststep
    def stick_label(self):
        """以 菜单- 贴标签 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'贴标签')]") \
            .click()

    @teststep
    def recommend_to_school(self):
        """以 菜单- 推荐到学校 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'推荐到学校')]") \
            .click()

    @teststep
    def cancel_collection(self):
        """以 菜单- 取消收藏 的text为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消收藏')]") \
            .click()

    # 贴标签
    @teststeps
    def wait_check_label_page(self):
        """以“title:贴标签”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'贴标签')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def save_button(self):
        """以 贴标签 - 保存按钮 的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "certain") \
            .click()

    @teststep
    def check_box(self, index):
        """以 贴标签 - 单选框 的id为依据"""
        self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "cb_checked")[index] \
            .click()

    @teststep
    def add_label(self):
        """以 贴标签 - 创建标签 的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fb_add_label") \
            .click()

    @teststep
    def click_negative_button(self):
        """以“取消按钮”的id为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消')]") \
            .click()

    @teststep
    def click_positive_button(self):
        """以“确认按钮”的id为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'确定')]") \
            .click()

    @teststep
    def expand_icon(self):
        """以“收起 icon”的id为依据"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_expand")
        return ele

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
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "check")
        return ele

    @teststep
    def commit_button(self):
        """确定 按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "confirm")
        return ele

    @teststeps
    def verify_recommend_result(self, menu, var='题单'):
        """验证 添加推荐 结果"""
        if self.wait_check_page():
            print('-----------------验证 -添加推荐结果-----------------')

            if var == '大题':
                self.user.filter_button()  # 筛选按钮
                if self.filter.wait_check_page():
                    self.user.click_game_list()  # 点击大题
                    self.filter.commit_button()  # 确定按钮
            elif '试卷' == var:
                self.user.filter_button()  # 筛选按钮
                if self.filter.wait_check_page():
                    self.user.click_test_paper()  # 点击试卷
                    self.filter.commit_button()  # 确定按钮

            if self.wait_check_page():
                if self.wait_check_list_page():
                    item = self.question_name()  # 获取
                    count = []
                    for z in range(len(item[0])):
                        print(item[1][z])
                        if self.wait_check_list_page():
                            menu1 = item[1][z]
                            if '提分' in menu:  # 提分类
                                menu = menu[:-2]

                            if menu == menu1:
                                count.append(z)

                    if count:
                        print('加入推荐成功')
                    else:
                        print('★★★ Error- 加入推荐失败', menu, item[1])

                    # for z in range(len(item[0])):
                    #     print(item[1][z])
                    #     if self.wait_check_list_page():
                    #         self.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入推荐的题单取消
                    #         self.home.tips_commit()  # 温馨提示 -- 确定
                    #         print('确定删除')
                    #         print('-------------')
                elif self.home.wait_check_empty_tips_page():
                    print('★★★ Error- 暂无数据，加入推荐失败')
            if self.wait_check_page():
                self.home.back_up_button()  # 返回 个人中心

    @teststeps
    def add_recommend_operation(self, check, mode='题单'):
        """添加推荐- 题单/大题/试卷"""
        self.home.back_up_button()  # 返回 个人中心页面
        if self.user.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page():  # 页面检查点
                if mode != '题单':
                    self.question.filter_button()  # 筛选按钮
                    if self.filter.wait_check_page():
                        if mode == '大题':
                            self.filter.click_game_list()  # 点击 大题
                        elif mode == '试卷':
                            self.filter.click_test_paper()  # 点击 试卷
                        self.filter.commit_button()  # 点击 确定按钮

                if self.question.wait_check_game_type_page():  # 页面检查点
                    print('添加推荐- {}'.format(mode))
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                    for i in range(1, 3):  # 加3道题
                        if self.question.wait_check_game_type_page():  # 页面检查点
                            item = self.question.question_name()  # 获取
                            item[0][i].click()  # 点击第X道题单

                            if check():  # 页面检查点
                                self.detail.recommend_button()  # 推荐按钮
                                self.filter.choose_school_label()  # 选择本校标签
                                Toast().toast_operation('加入成功')  # 获取toast

                                if check():  # 页面检查点
                                    self.home.back_up_button()

                    # 恢复测试数据！！
                    if mode != '题单':
                        if self.question.wait_check_game_type_page():  # 页面检查点
                            self.question.filter_button()  # 筛选按钮

                            if self.filter.wait_check_page():
                                self.filter.click_question_menu()  # 点击 题单
                                self.filter.commit_button()  # 点击 确定按钮

                                if not self.question.wait_check_page():  # 页面检查点
                                    print('★★★ Error- 恢复测试数据失败')

                # 回到我的推荐
                if self.question.wait_check_page('搜索'):  # 页面检查点
                    self.home.click_tab_profile()  # 个人中心
                    if self.user.wait_check_page():  # 页面检查点
                        self.user.click_mine_recommend()  # 点击 我的推荐
    #
    # @teststeps
    # def cancel_recommend_operation(self):
    #     """删除推荐"""
    #     if self.wait_check_page():  # 页面检查点
    #         if self.wait_check_list_page():
    #             print('---------------------删除推荐---------------------')
    #             item = self.question.question_name()  # 获取
    #             for z in range(len(item[0])):
    #                 if self.wait_check_list_page():
    #                     print(item[1][0])
    #                     self.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入收藏的题单取消收藏
    #                     self.home.tips_commit()  # 温馨提示 -- 确定
    #                     print('确定删除')
    #
    #                     self.judge_delete(item[1][0])  # 验证 删除推荐 结果
                            
    # @teststeps
    # def judge_delete(self, var):
    #     """验证 删除推荐 结果"""
    #     if self.wait_check_list_page():
    #         print('-------验证 删除推荐 结果-----')
    #         name = self.question.question_name()  # 题单
    #         if name[1][0] == var:
    #             print('★★★ Error- 取消推荐失败', name[1][0], var)
    #         else:
    #             print('取消推荐成功')
    #     elif self.home.wait_check_empty_tips_page():
    #         print('取消推荐成功')
    #     print('------------------------------------------')

    @teststeps
    def judge_label_title(self, mode, content):
        """判断标签 类型及个数
            筛选标签展示规则：资源类型
            自定义标签：学校自定义标签
            系统标签：有带系统标签的推荐内容，则展示
        """
        if mode == '试卷':  # 试卷
            if content[0] != '资源类型':  # 我的推荐
                print('★★★ Error- 标签类型有误', content)
        elif mode == '题单':  # 题单
            if content[0] == '资源类型':  # 我的收藏/推荐
                if len(content) == 2:
                    if content[1] != '系统标签':
                        print('★★★ Error- 标签个数 {}，类型有误'.format(len(content)), content)
            else:
                print('★★★ Error- 标签类型有误', content)
        elif mode == '大题':  # 大题
            if content[0] == '资源类型' and content[1] == '活动类型':  # 我的推荐
                if len(content) == 3:
                    if content[2] != '系统标签':
                        print('★★★ Error- 标签个数 {}，类型有误'.format(len(content)), content)
            else:
                print('★★★ Error- 标签类型有误', content)
        print('-------------------------------------------')
