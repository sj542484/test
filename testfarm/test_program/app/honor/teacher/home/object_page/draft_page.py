#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_bank_page import QuestionBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.utils.wait_element import WaitElement


class DraftPage(BasePage):
    """定时作业+草稿箱 页面"""
    def __init__(self):
        self.home = ThomePage()
        self.release = ReleasePage()
        self.detail = QuestionDetailPage()
        self.question = QuestionBankPage()
        self.basket = QuestionBasketPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var=20):
        """以“title:定时作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'定时作业')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_hw_list_page(self, var=20):
        """以“全部班级 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "name")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def all_vanclass(self):
        """全部班级 """
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "class_spinner").click()

    @teststep
    def all_time(self):
        """全部 """
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "time_spinner").click()

    @teststeps
    def wait_check_tab_page(self, var=20):
        """以“全部班级 元素”为依据"""
        locator = (By.ID, "android:id/text1")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def check_text(self):
        """全部班级/全部 菜单条目"""
        item = self.driver \
            .find_elements_by_id("android:id/text1")
        return item

    @teststep
    def draft_box_button(self):
        """以“草稿箱 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "draft") \
            .click()

    # 草稿箱
    @teststeps
    def wait_check_drat_page(self, var=10):
        """以“title:草稿”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'长按草稿,可删除草稿')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_draft_list_page(self):
        """以“草稿list 名称”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "name")
        return self.wait.wait_check_element(locator)

    @teststep
    def draft_name(self):
        """草稿名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def draft_time(self):
        """草稿创建时间"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "time")
        return ele

    @teststep
    def draft_count(self):
        """草稿 小题数"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "count")
        return ele

    @teststeps
    def add_to_basket(self):
        """加入题筐"""
        self.home.back_up_button()  # 返回按钮
        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入题库tab

            if self.question.wait_check_page('题单'):
                item = self.question.question_name()  # 获取
                item[0][1].click()  # 点击第一道题

                if self.detail.wait_check_page():  # 页面检查点
                    if self.detail.wait_check_list_page():
                        print('----------题单详情页----------')
                        self.detail.put_to_basket_button()  # 点击加入题筐按钮
                        print('加题进题筐')
                        self.home.back_up_button()  # 返回按钮

                        if self.question.wait_check_page('题单'):  # 页面检查点
                            self.question.question_basket()  # 题筐按钮

                            if self.basket.wait_check_page():  # 页面检查点
                                if self.basket.wait_check_list_page():
                                    if self.question_bank_operation():
                                        return True
                                elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                                    print('★★★ Error- 加入题筐失败')
                                    self.home.back_up_button()
                                    if self.question.wait_check_page('题单'):  # 页面检查点
                                        self.home.click_tab_hw()  # 返回 主界面
                                        return False
            else:
                print('★★★ Error- 未进入题库tab')
                return False

    @teststeps
    def question_bank_operation(self):
        """获取题筐所有题"""
        var = self.basket.question_name()  # 所有题
        if len(var) > 1:
            for i in range(2):
                check = self.basket.check_button()  # 单选按钮
                check[i].click()

        self.basket.assign_button().click()  # 点击 布置作业 按钮
        self.home.tips_content_commit()  # 提示 页面

        if self.release.wait_check_release_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                return True
        else:
            print('★★★ Error- 未进入 发布作业 页面')
            self.home.back_up_button()
            return False

