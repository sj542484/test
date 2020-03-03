#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.dynamic_info.test_data.draft_data import GetVariable as gv
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class RecommendSchoolPage(BasePage):
    """ 推荐到学校 页面"""
    question_title_value = '//div[text()="题单名称"]'

    def __init__(self):
        self.wait = WaitElement()
        self.filter = FilterPage()
        self.recommend = RecommendPage()
        self.user = TuserCenterPage()
        self.mine_bank = MineTestBankPage()
        self.home = ThomePage()

    @teststeps
    def wait_check_page(self):
        """以“title: 推荐到学校”为依据"""
        locator = (By.XPATH, '//div[text()="推荐到学校"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以 题单名称 为依据"""
        locator = (By.XPATH, self.question_title_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_empty_page(self, var=10):
        """ 以提示text作为依据"""
        locator = (By.XPATH, "//div[text()='暂无数据']")
        return self.wait.wait_check_element(locator, var)

    # 本校标签
    @teststeps
    def wait_check_label_list_page(self):
        """以“存在 标签列表”的text为依据"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def question_title(self):
        """以“题单名称”的class name为依据"""
        locator = (By.XPATH, self.question_title_value)
        ele = self.wait.wait_find_element(locator)
        return ele

    @teststep
    def question_name(self):
        """以“题单名称”的class name为依据"""
        locator = (By.XPATH, '//input[@class="van-field__control"]')
        ele = self.wait.wait_find_element(locator)
        return ele

    @teststep
    def check_button(self):
        """以“单选 按钮”的class name为依据"""
        locator = (By.XPATH, '//div[@class="labels-check van-checkbox"]')
        ele = self.wait.wait_find_elements(locator)
        return ele

    @teststep
    def school_label_name(self):
        """以“本校标签 name”的id为依据"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]')
        ele = self.wait.wait_find_elements(locator)
        return ele

    @teststep
    def wait_check_empty_tips_page(self, var=3):
        """暂时没有数据"""
        locator = (By.XPATH, '//div[text()="暂无数据"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def confirm_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//div[text()="确定"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//img[@class="vt-page-left-img-Android"]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def choose_school_label_operation(self):
        """选择本校标签"""
        if self.wait_check_page():
            name = self.question_name()
            name.clear()
            name.send_keys(gv.RECOMMEND)

            cancel = []
            choose = []
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
                        button[i].click()  # 选择 一个标签
                        break
            elif self.wait_check_empty_tips_page():
                print('本校暂无标签')

            self.confirm_button()  # 确定按钮
            return gv.RECOMMEND, choose, cancel

    @teststeps
    def verify_recommend_result(self, menu, games):
        """验证 添加推荐 结果"""
        if self.recommend.wait_check_page():
            if self.recommend.wait_check_list_page():

                name = self.mine_bank.question_name()[1]  # 条目名称
                count = []
                for i in range(len(name)):
                    if menu in name[i]:
                        count.append(i)
                        break

                if not count:
                    print('★★★ Error- 加入推荐失败', menu, name)
                else:
                    print('加入推荐成功')
                    # if self.recommend.wait_check_list_page():
                    #     self.recommend.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入推荐的题单取消
                    #     self.home.tips_commit()  # 温馨提示 -- 确定
                    #     print('确定删除')
                    #     print('-------------')
            elif self.home.wait_check_empty_tips_page():
                print('★★★ Error- 暂无数据，加入推荐失败')

            if self.recommend.wait_check_page():
                print('---------------我的推荐 大题验证-------------')
                self.user.filter_button()  # 筛选按钮
                if self.filter.wait_check_page():
                    self.user.click_game_list()  # 点击大题
                    if self.filter.wait_check_page():
                        self.filter.commit_button()  # 确定按钮

                if self.recommend.wait_check_list_page():
                    item = self.recommend.question_name()  # 获取
                    count = []
                    for k in games:
                        for i in range(len(item[1])):
                            if item[1][i] in k:
                                count.append(i)
                                break

                    if count:
                        print('加入推荐成功')
                        # for z in range(len(count)):
                        #     print(item[1][z])
                        #     if self.recommend.wait_check_list_page():
                        #         self.recommend.menu_button(z)  # 为了保证脚本每次都可以运行，故将加入推荐的题单取消
                        #         self.home.tips_commit()  # 温馨提示 -- 确定
                        #         print('确定删除')
                        #         print('-------------')
                    else:
                        print('★★★ Error- 大题 加入推荐 失败', games, item[1])
                elif self.home.wait_check_empty_tips_page():
                    print('★★★ Error- 暂无数据，加入推荐失败')

            if self.recommend.wait_check_page():
                print('--------恢复测试数据--------')
                self.user.filter_button()  # 筛选按钮
                if self.filter.wait_check_page():
                    self.filter.reset_button()  # 点击 重置按钮
                    if self.filter.wait_check_page():
                        self.filter.commit_button()  # 确定按钮

            if self.recommend.wait_check_page():
                self.home.back_up_button()  # 返回 个人中心

    @teststeps
    def judge_mine_test_bank_operation(self, menu, games):
        """验证 我的题库 结果 具体操作"""
        if self.user.wait_check_page():  # 页面检查点
            print('------------------验证 我的题库 结果------------------')
            print(menu)
            self.user.click_mine_bank()  # 我的题库
            if self.mine_bank.wait_check_page():
                if self.mine_bank.wait_check_list_page():
                    name = self.mine_bank.question_name()[1]  # 条目名称
                    count = []
                    for i in range(len(name)):
                        if menu in name[i]:
                            count.append(i)
                            break

                    if not count:
                        print('★★★ Error- 题单 加入我的题库 失败', menu, name)
                    else:  # 恢复测试数据
                        print('题单 加入我的题库 成功')
                elif self.home.wait_check_empty_tips_page():
                    print('★★★ Error-我的题库为空, 加入我的题库 失败')

                if self.mine_bank.wait_check_page():
                    print('---------------我的题库 大题验证-------------')
                    print(games)
                    self.user.filter_button()  # 筛选按钮
                    if self.filter.wait_check_page():
                        self.user.click_game_list()  # 点击大题
                        if self.filter.wait_check_page():
                            self.filter.commit_button()  # 确定按钮

                            if self.mine_bank.wait_check_list_page():
                                item = self.mine_bank.question_name()  # 获取
                                count = []
                                for k in games:
                                    for i in range(len(item[1])):
                                        if k in item[1][i]:
                                            count.append(i)
                                            break

                                if not count:
                                    print('★★★ Error- 加入我的题库失败', games, item[1])
                                else:
                                    print('加入我的题库成功')
                            elif self.home.wait_check_empty_tips_page():
                                print('★★★ Error- 暂无数据，加入加入我的题库 失败')

                            if self.mine_bank.wait_check_page():
                                self.user.filter_button()  # 筛选按钮
                                if self.filter.wait_check_page():
                                    self.filter.reset_button()  # 点击 重置按钮
                                    if self.filter.wait_check_page():
                                        self.filter.commit_button()  # 确定按钮

                if self.mine_bank.wait_check_page():
                    self.home.back_up_button()  # 返回 个人中心
