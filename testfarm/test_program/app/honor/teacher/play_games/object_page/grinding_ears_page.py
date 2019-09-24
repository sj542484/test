#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page.result_page import ResultPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from conf.base_config import GetVariable as gv
from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.click_bounds import ClickBounds
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class GrindingEars(BasePage):
    """磨耳朵"""
    video_img_value = gv.PACKAGE_ID + "subtitle"  # 视频图片
    spend_time_value = gv.PACKAGE_ID + "spend_time"  # 总时长

    def __init__(self):
        self.result = ResultPage()
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:磨耳朵”的xpath为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'磨耳朵')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_play_page(self):
        """以“视频图片”的xpath为依据"""
        locator = (By.ID, self.video_img_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def video_img_options(self):
        """展示的图片"""
        ele = self.driver \
            .find_elements_by_id(self.video_img_value)
        return ele

    @teststeps
    def start_button(self):
        """播放按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "start")
        return ele

    @teststep
    def pattern_switch(self):
        """全英/英汉模式切换 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "status") \
            .click()
        time.sleep(1)

    @teststep
    def full_button(self):
        """全屏 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "full") \
            .click()

    @teststeps
    def sentence(self):
        """展示的句子"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "sentence")
        return ele

    # @teststeps
    # def wait_check_explain_page(self, var=10):
    #     """以“解释”的ID为依据"""
    #     locator = (By.ID, gv.PACKAGE_ID + "explain")
    #     return self.wait.wait_check_element(locator, var)
    #
    @teststep
    def explain(self):
        """解释"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "explain")
        return item

    @teststep
    def audio_button(self):
        """语音按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "audio")
        return ele

    @teststep
    def commit_button_judge(self, var):
        """‘提交’按钮 状态判断"""
        item = self.commit_button()  # ‘提交’按钮
        value = GetAttribute().enabled(item)

        if value != var:  # 测试 提交 按钮 状态
            print('★★★ 提交按钮 状态Error', value)
        else:
            return True

    @teststep
    def commit_button(self):
        """点击‘提交’按钮"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "commit")
        return item

    @teststeps
    def commit_button_operation(self, var):
        """提交 按钮 判断 加 点击操作"""
        if self.commit_button_judge(var):  # 提交 按钮 状态判断
            self.commit_button().click()  # 点击 提交 按钮

    # full页面
    @teststeps
    def wait_check_full_page(self):
        """以“spend_time”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "english")
        return self.wait.wait_check_element(locator)

    @teststep
    def english(self):
        """句子/解释"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "english")
        return item

    @teststep
    def click_blank(self):
        """点击页面 空白处, 元素出现"""
        ClickBounds().click_bounds(200, 200)

    # 以下为结果页面元素
    @teststeps
    def wait_check_detail_page(self, var=15):
        """以“spend_time”的ID为依据"""
        locator = (By.ID, self.spend_time_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def judge_img(self):
        """图片"""
        locator = (By.CLASS_NAME, "android.widget.ImageView")
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
    def grinding_ears_operation(self):
        """《磨耳朵》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                question = self.sentence()  # 展示的句子
                audio = self.audio_button()  # 语音按钮
                for i in range(len(question)):
                    time.sleep(5)
                    if self.wait_check_play_page():
                        audio[i].click()  # 点击语音按钮
                        word = self.sentence()[i].text  # 题目
                        print('题目:%s' % word)
                        print('----------------')
                time.sleep(5)
                ThomePage().tips_content_commit()

                if self.wait_check_play_page():
                    self.start_button()  # 播放按钮

                    print('---------------------------------------')
                    print('---切换到 英汉模式:')
                    self.click_blank()  # 点击页面 空白处
                    self.pattern_switch()  # 切换到 英汉模式
                    question = self.sentence()  # 展示的句子
                    audio = self.audio_button()  # 语音按钮

                    for i in range(len(question)):
                        if self.wait_check_play_page():
                            audio[i].click()  # 语音按钮
                            word = self.sentence()[i].text  # 题目
                            print('题目 解释:%s' % word)
                            print('-------------------------------')

                            time.sleep(5)
                            ThomePage().tips_content_commit(5)

                    if self.wait_check_play_page():
                        self.start_button()  # 播放按钮
                    print('---------------------------------------')
                # self.click_blank()  # 点击页面 空白处
                # self.full_button()  # 全屏 按钮
                # if self.wait_check_full_page():
                #     self.pattern_switch()  # 切换到 全英模式
                #     print(self.english().text)  #
                #     self.click_blank()  # 点击页面 空白处
                #     ThomePage().back_up_button()  # 返回 按钮
                # print('---------------------------------------')

                while True:
                    if self.commit_button_judge('true'):
                        self.commit_button_operation('true')  # 提交 按钮 状态判断 加点击
                        if self.wait_check_detail_page(5):  # 结果页检查点
                            break
                        else:
                            time.sleep(3)

                print('==============================================')

    @teststeps
    def result_detail_page(self):
        """《磨耳朵》 结果页 操作过程"""
        if self.wait_check_detail_page():  # 结果页检查点
            if self.judge_img():
                print(self.wording(), self.spend_time())
            print('==============================================')

    @teststeps
    def study_again(self):
        """再听一遍 操作过程"""
        if self.wait_check_detail_page():  # 结果页检查点
            self.result.again_button()[0].click()  # 结果页 再听一遍 按钮
            self.grinding_ears_operation()  # 游戏过程

    @teststeps
    def back_operation(self):
        """从结果页返回小游戏list"""
        if self.wait_check_detail_page():
            ThomePage().back_up_button()  # 返回小游戏界面
            if GamesPage().wait_check_page():
                ThomePage().back_up_button()  # 返回 题单详情页
