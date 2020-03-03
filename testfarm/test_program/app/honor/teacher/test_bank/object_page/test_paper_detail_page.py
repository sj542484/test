#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class PaperDetailPage(BasePage):
    """试卷 详情页面"""
    assign_van_locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选择班级')]")

    paper_tips = '★★★ Error- 未进入试卷 详情页面'
    back_paper_tips = '★★★ Error- 未返回试卷 详情页面'

    paper_assign_tips = '★★★ Error- 未进入试卷布置页面'

    def __init__(self):
        self.wait = WaitElement()
        self.change_image = ChangeImage()

    @teststeps
    def wait_check_page(self):
        """以“title:布置试卷”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'布置试卷')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def recommend_button(self):
        """推荐到学校 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "recommend")
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def collect_button(self):
        """收藏/取消收藏 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "collect")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def share_button(self):
        """分享 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "share")
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def paper_type(self):
        """试卷"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_paper")
        return self.wait \
                .wait_check_element(locator)

    @teststeps
    def paper_title(self):
        """title"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_paper_name")
        item = self.wait \
            .wait_find_element(locator).text
        print('试卷名称:', item)
        return item

    @teststeps
    def teacher(self):
        """作者"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_author")
        item = self.wait \
            .wait_find_element(locator).text
        print(item)

    # 测评模式 - 百分制/AB制
    @teststeps
    def score_type(self):
        """测评模式 - 百分制/AB制"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'模式')]")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststeps
    def score(self):
        """百分制"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_score")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststeps
    def score_unit(self):
        """百分制 单位"""
        locator = (By.ID, gv.PACKAGE_ID + "score")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    # 考试时间
    @teststep
    def time_title(self):
        """测评模式 - 百分制/AB制"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'考试时间')]")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststep
    def time_unit(self):
        """考试时间 单位"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'分钟')]")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststep
    def time_str(self):
        """时间"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_time")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    # 小题数
    @teststep
    def num_title(self):
        """小题数"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'小题数')]")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststep
    def num_unit(self):
        """小题数 单位"""
        locator = (By.XPATH, "//android.widget.TextView[@text='题']")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststep
    def game_num(self):
        """小题数"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_exercise_num")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    # 限制交卷
    @teststep
    def limit_type(self):
        """限制交卷"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'限制交卷')]")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststeps
    def limit_judge(self):
        """限制交卷: 限制"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_limit_m")
        return self.wait.judge_is_exists(locator)

    @teststep
    def limit_hand(self):
        """限制交卷"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_limit")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststeps
    def limit_unit(self):
        """不限制交卷"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_limit_m")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    # 题型
    @teststep
    def game_list_title(self):
        """题型"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题型')]")
        item = self.wait \
            .wait_find_element(locator).text
        return item

    @teststep
    def question_name(self):
        """小游戏名"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_name")
        item = self.wait \
            .wait_find_elements(locator)
        return item

    @teststep
    def num(self, index):
        """每个小游戏 题数"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_desc")
        item = self.wait \
            .wait_find_elements(locator)[index]
        return item

    @teststep
    def arrow(self, index):
        """箭头"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_arrow")
        item = self.wait \
            .wait_find_elements(locator)[index]
        return item

    @teststep
    def assign_button(self):
        """布置试卷 按钮"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_assign")
        self.wait\
            .wait_find_element(locator).click()

    @teststep
    def sentence(self):
        """句子"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_answer")
        item = self.wait \
            .wait_find_elements(locator)
        return item

    # 布置试卷 页面
    @teststeps
    def wait_check_assign_list_page(self):
        """以“title:”为依据"""
        return self.wait\
            .wait_check_element(self.assign_van_locator)

    @teststep
    def assign_title(self):
        """选择班级"""
        item = self.wait \
            .wait_find_element(self.assign_van_locator)
        print(item.text)

    @teststep
    def assign_hint(self):
        """点击选择班级，暂无学生班级已经从列表中隐藏"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'点击选择班级，暂无学生班级已经从列表中隐藏')]")
        item = self.wait \
            .wait_find_element(locator).text
        print(item)
        return item

    @teststeps
    def tips_page_info(self):
        """温馨提示 页面信息"""
        print('------------------------------------------')

        if ThomePage().wait_check_tips_page():
            ThomePage().tips_title()
            ThomePage().tips_content()
            ThomePage().never_notify()  # 不再提醒
            ThomePage().cancel_button()  # 取消按钮

            self.assign_button()  # 布置试卷 按钮
            if ThomePage().wait_check_tips_page():
                ThomePage().commit_button().click()
        else:
            print('★★★ Error- 无icon')
