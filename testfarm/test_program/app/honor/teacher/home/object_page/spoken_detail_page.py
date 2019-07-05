#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.wait_element import WaitElement


class SpokenDetailPage(BasePage):
    """ 口语详情 页面"""
    st_finish_status_value = gv.PACKAGE_ID + "status"  # 学生 完成与否
    game_finish_status_value = gv.PACKAGE_ID + "test_bank_name"  #
    st_name_value = gv.PACKAGE_ID + "name"  # 学生名
    finish_ratio_value = gv.PACKAGE_ID + "finish_ratio"  # 完成率
    star_value = gv.PACKAGE_ID + "star"  # 星星

    @teststeps
    def __init__(self):
        self.home = ThomePage()
        self.get = GetAttribute()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以 title: xpath为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'完成情况')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def finished_tab(self):
        """完成情况 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'完成情况')]")
        return ele

    @teststep
    def analysis_tab(self):
        """答题分析 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'答题分析')]")
        return ele

    # 完成情况 tab
    @teststeps
    def wait_check_st_list_page(self):
        """以“过关状态：已完成/未完成”为依据"""
        locator = (By.ID, self.st_finish_status_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def st_finish_status(self):
        """学生 完成与否"""
        ele = self.driver \
            .find_elements_by_id(self.st_finish_status_value)
        return ele

    @teststep
    def st_name(self):
        """学生 昵称"""
        ele = self.driver \
            .find_elements_by_id(self.st_name_value)
        return ele

    @teststep
    def st_icon(self):
        """学生 头像"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "head")
        return ele

    # 完成情况tab 二级页面
    @teststeps
    def wait_check_game_list_page(self):
        """以“过关状态：已完成/未完成”为依据"""
        locator = (By.ID, self.game_finish_status_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def game_finish_status(self):
        """小游戏 -未完成/星星数"""
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@resource-id,'%s')]/"
                                    "parent::android.widget.LinearLayout/"
                                    "following-sibling::android.widget.FrameLayout/*" % self.game_finish_status_value)

        content = []
        for i in range(len(ele)):
            content.append(ele[i].text)

        return content

    # 答题分析 tab
    @teststeps
    def wait_check_spoken_list_page(self):
        """以“list 本班完成率”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_testbank_status")
        return self.wait.wait_check_element(locator)

    # 答题分析tab 二级页面
    @teststep
    def check_st_tab(self):
        """按学生看 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'按学生看')]")
        return ele

    @teststeps
    def wait_check_st_page(self):
        """以“学生名”为依据"""
        locator = (By.ID, self.st_name_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def st_unfinished_or_star(self):
        """学生 未完成/星星数"""
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@resource-id,'%s')]"
                                    "/parent::android.widget.RelativeLayout"
                                    "/following-sibling::android.widget.FrameLayout/*" % self.st_name_value)

        content = []
        for i in range(len(ele)):
            content.append(ele[i].text)

        return content

    @teststep
    def no_finish(self):
        """未完成"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "no_finish")
        return ele

    @teststep
    def star_num(self):
        """星星数"""
        ele = self.driver \
            .find_elements_by_id(self.star_value)
        return ele

    @teststep
    def check_question_tab(self):
        """按题查看 tab"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'按题查看')]")
        return ele

    @teststeps
    def wait_check_question_page(self):
        """以“过关状态”为依据"""
        locator = (By.ID, self.finish_ratio_value)
        return self.wait.wait_check_element(locator)

    # 答题分析 详情页
    @teststeps
    def wait_check_detail_page(self):
        """以“title: 详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'详情')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_detail_list_page(self):
        """以“ star”为依据"""
        locator = (By.ID, self.star_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def hint(self):
        """句子"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text, '听录音,点击星星可修改结果')]").text
        print(ele)

    @teststep
    def sentence(self):
        """句子"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "sentence")
        return ele

    @teststep
    def finish_ratio(self):
        """完成率"""
        ele = self.driver \
            .find_elements_by_id(self.finish_ratio_value)
        return ele

    @teststep
    def speak_button(self):
        """播音按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_speak")
        return ele

    # 修改成绩
    @teststeps
    def wait_check_modify_achieve_page(self):
        """以“修改成绩”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '修改成绩')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "cancel").click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "confirm").click()

    # 按学生看
    @teststep
    def click_st_star(self):
        """进入 已完成 学生"""
        ele = self.driver\
            .find_elements_by_xpath("//android.view.View[contains(@resource-id,'%s')]"
                                    "/parent::android.widget.FrameLayout"% self.star_value)
        return ele

    # 按题查看 详情页 检查点 wait_check_game_list_page(self)
    @teststep
    def explain(self):
        """说明"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "explain").text
        return ele

    @teststep
    def total_report(self):
        """小题 报告"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "report").text
        return ele

    @teststep
    def judge_element(self, index=3):
        """判断滑屏后页面中第一个/最后一个元素 是不是 完成率"""
        item = self.home.all_element()
        if item[index] == self.finish_ratio_value:
            return True
        else:
            return False
