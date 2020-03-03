#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time

from selenium.webdriver.common.by import By

from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from conf.base_config import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.click_bounds import ClickBounds
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import ElementBounds
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class TinyCourse(BasePage):
    """微课"""
    video_img_value = gv.PACKAGE_ID + "subtitle"  # 视频图片
    spend_time_value = gv.PACKAGE_ID+ "spend_time"  # 总时长

    exo_pause_value = gv.PACKAGE_ID + 'exo_pause'  # 视频播放页面 暂停 按钮
    exo_play_value = gv.PACKAGE_ID + 'exo_play'  # 视频播放页面 播放 按钮
    exo_rotate_value = gv.PACKAGE_ID + 'rotate'  # 视频播放页面 横竖屏切换 按钮

    def __init__(self):
        self.result = ResultPage()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def play_button(self):
        """播放按钮"""
        print('点击 播放按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "play") \
            .click()

    @teststeps
    def wait_check_play_page(self):
        """以“横竖屏切换”的id为依据"""
        locator = (By.ID, self.exo_rotate_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def back_up_button(self):
        """返回 按钮"""
        print('点击返回 按钮，返回详情页')
        ele = self.driver \
            .find_elements_by_class_name('android.widget.ImageButton')
        for i in range(len(ele)):
            if GetAttribute().description(ele[i]) == '转到上一层级':
                ele[i].click()
                break

    @teststeps
    def screen_switch_button(self):
        """横竖屏切换 按钮"""
        self.driver \
            .find_element_by_id(self.exo_rotate_value).click()

    @teststeps
    def exo_play_button(self):
        """播放键"""
        print('点击播放按钮')
        self.driver \
            .find_element_by_id(self.exo_play_value).click()

    @teststeps
    def exo_pause_button(self):
        """暂停键"""
        self.driver \
            .find_element_by_id(self.exo_pause_value).click()

    @teststeps
    def exo_position(self):
        """播放到的位置"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'exo_position').text
        return item

    @teststeps
    def exo_progress(self):
        """进度条 description == exo_position的text值"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'exo_progress')
        return ele

    @teststeps
    def exo_duration(self):
        """视频时长"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'exo_duration').text
        return ele

    @teststep
    def click_blank(self):
        """点击页面 空白处, 元素出现"""
        time.sleep(3)
        ClickBounds().click_bounds(300, 300)

    @teststeps
    def video_duration_deal(self, duration):
        """视频时长处理"""
        value = duration.split(':')
        return 10 * int(value[0]) + int(value[1])

    # 以下为结果页面元素
    @teststeps
    def wait_check_detail_page(self):
        """以“spend_time”的ID为依据"""
        locator = (By.ID, self.spend_time_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def judge_img(self):
        """图片"""
        locator = (By.CLASS_NAME, "//android.widget.ImageView")
        return self.wait.judge_is_exists(locator)

    @teststep
    def wording(self):
        """本次磨耳朵时长: """
        ele = self.driver.\
            find_element_by_xpath("//android.widget.TextView[contains(@text, '本次磨耳朵时长: ')]").text
        return ele

    @teststep
    def spend_time(self):
        """XX (秒) """
        ele = self.driver. \
            find_element_by_id(self.spend_time_value).text
        return ele

    @teststeps
    def tiny_course_play_operation(self):
        """《微课》 游戏过程"""
        if GamesPage().wait_check_list_page():  # 页面检查点
            self.play_button()  # 播放 按钮
            if self.wait_check_play_page():
                time_str = self.exo_position()  # 播放进度  时间
                var = GetAttribute().description(self.exo_progress())  # 进度条 元素content-desc值
                print(time_str, var)

                if time_str != var:
                    print('★★★ Error - 视频时长展示有误', time_str, var)
                else:
                    print('--播放视频时长展示无误--')

                self.click_blank()  # 点击页面 空白处
                if self.wait_check_play_page():
                    location = ElementBounds().get_element_location(self.exo_progress())

                    self.screen_switch_button()  # 横竖屏切换 按钮  竖屏切横屏
                    if self.wait_check_play_page():
                        location1 = ElementBounds().get_element_location(self.exo_progress())
                        if location[1] < location1[1]:
                            print('★★★ Error - 竖屏切横屏有误', location, location1)
                        else:
                            print('--横竖屏切换 按钮  竖屏切横屏--')

                        self.click_blank()  # 点击页面 空白处
                        self.screen_switch_button()  # 横竖屏切换 按钮 横屏切竖屏
                        if self.wait_check_play_page():
                            location2 = ElementBounds().get_element_location(self.exo_progress())

                            if location1[1] > location2[1]:
                                print('★★★ Error - 横屏切竖屏有误', location1, location2)
                            else:
                                print('--横竖屏切换 按钮 横屏切竖屏--')

                            if location[0] != location2[0] or location[1] != location2[1]:
                                print('★★★ Error - 横屏切回竖屏有误，进度条坐标不一致', location, location2)
            else:
                print('!!!未进入视频播放页面')

            self.click_blank()  # 点击页面 空白处
            self.result.back_up_button()  # 返回 按钮

    @teststeps
    def time_operation(self, time1, time2):
        """时长比较"""
        item = self.video_duration_deal(time1)
        item2 = self.video_duration_deal(time2)
        print(item, item2)
        if item2 < item:
            print('★★★ Error - 拍摄时长无增加', time1, time2)
        else:
            print('--拍摄时长展示无误--')
    print('==============================================')
