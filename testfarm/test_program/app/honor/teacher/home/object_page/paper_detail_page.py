#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.wait_element import WaitElement


class PaperPage(BasePage):
    """ 试卷详情 页面"""
    more_button_item_value = gv.PACKAGE_ID + "title"  # 更多按钮 -条目元素
    vanclass_score_value = gv.PACKAGE_ID + "tv_desc"  # 全班平均得分x分; 总分x分
    st_finish_value = gv.PACKAGE_ID + "status"  # 学生完成情况

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title: 答卷分析”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'答卷分析')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def all_element(self):
        """页面内所有class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        content = []
        for i in range(len(ele)):
            # print(ele[i].text)
            content.append(ele[i].text)
        # print('++++++++++++++++')
        return ele, content

    # 本班试卷 -- 试卷list
    @teststep
    def hw_name(self):
        """作业name"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def progress(self):
        """完成进度 - 已完成x/x"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "progress")
        return ele

    @teststep
    def create_time(self):
        """作业创建时间"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_create_date")
        return ele

    @teststep
    def remind(self):
        """提醒 按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "remind")
        return ele

    # 单个试卷
    @teststep
    def analysis_tab(self):
        """答卷分析 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'答卷分析')]")
        return ele

    @teststep
    def finished_tab(self):
        """完成情况 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'完成情况')]")
        return ele

    @teststep
    def more_button(self):
        """更多 按钮"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView") \
            .click()

    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.ID, self.more_button_item_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def edit_delete_button(self, index):
        """编辑& 删除 按钮"""
        self.driver \
            .find_elements_by_id(self.more_button_item_value)[index] \
            .click()

    # 答卷分析 tab
    @teststeps
    def wait_check_paper_list_page(self):
        """以“共x题 x分/全班得分情况 元素”为依据"""
        locator = (By.ID, self.vanclass_score_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def game_type(self):
        """游戏类型"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type")
        return ele

    @teststep
    def game_level(self):
        """提分"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "level")
        return ele

    @teststep
    def game_num(self):
        """共x题"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "exercise_num")
        return ele

    @teststep
    def game_name(self):
        """游戏 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        return ele

    @teststep
    def van_average_achievement(self):
        """全班平均得分x分; 总分x分"""
        ele = self.driver \
            .find_elements_by_id(self.vanclass_score_value)
        return ele

    # 完成情况tab
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生完成情况 元素”为依据"""
        locator = (By.ID, self.st_finish_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def st_score(self):
        """学生 完成与否"""
        ele = self.driver \
            .find_elements_by_id(self.st_finish_value)
        return ele

    @teststep
    def st_name(self):
        """学生 昵称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def st_icon(self):
        """学生 头像"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "head")
        return ele

    # 完成情况tab -- 个人答题结果页
    @teststeps
    def wait_check_per_detail_page(self, var):
        """以“”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststep
    def paper_type(self):
        """ 类型"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_paper")
        return ele

    @teststep
    def paper_name(self):
        """ 名称"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_paper_name")
        return ele

    # 个人答题结果页 -- 题型list
    @teststep
    def game_title(self):
        """ 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_name")
        return ele

    @teststep
    def game_desc(self):
        """ 共x题 xx分"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_desc")
        return ele

    @teststep
    def game_score(self):
        """ 得分"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_score")
        return ele

    # 答题结果页 -详情页面
    @teststeps
    def wait_check_per_answer_page(self):
        """以“游戏title”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_title")
        return self.wait.wait_check_element(locator)

    @teststep
    def first_report(self):
        """首次正答"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "first_report").text
        print(ele)

    # 编辑试卷 页面
    @teststeps
    def wait_check_edit_page(self):
        """以“title:编辑试卷”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'编辑试卷')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def assign_button(self):
        """布置试卷 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_assign") \
            .click()

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_first") \
            .click()

    @teststep
    def confirm_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_second") \
            .click()

    # 删除试卷tips 页面
    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "md_title")
        return self.wait.wait_check_element(locator)

    @teststeps
    def delete_commit_operation(self):
        """删除试卷 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.edit_delete_button(1)  # 删除按钮

            if self.wait_check_tips_page():
                print('---------删除试卷---------')
                ThomePage().commit_button().click()  # 确定按钮
                print('确定删除')

    @teststeps
    def delete_cancel_operation(self):
        """删除试卷 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.edit_delete_button(1)  # 删除按钮

            if self.wait_check_tips_page():
                print('---------删除试卷---------')
                ThomePage().tips_title()
                ThomePage().tips_content()
                ThomePage().cancel_button()  # 取消按钮
                print('---------------')
                print('取消删除')
            else:
                print('★★★ Error- 无删除提示框')
