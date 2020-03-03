#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page.homework_page import Homework
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


class WordReadPage(BasePage):
    """单词跟读"""
    img_value = gv.PACKAGE_ID + "img"  # 图片
    max_tips_value = gv.PACKAGE_ID + "result_hint"  # 5次录音提示信息

    again_value = gv.PACKAGE_ID + "again"  # 再练一遍 按钮
    result_word_value = gv.PACKAGE_ID + "word"  # 结果页word

    def __init__(self):
        self.result = ResultPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:单词跟读”的xpath为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词跟读')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_play_page(self):
        """以“图片”的xpath为依据"""
        locator = (By.ID, self.img_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_img(self):
        """展示的图片"""
        locator = (By.XPATH, self.img_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def recording_button(self):
        """录音按钮"""
        # print('点击 录音按钮')
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "game_record_button")
        return ele

    @teststeps
    def recording_button_location(self):
        """'录音按钮 坐标"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "game_record_button")
        return ElementBounds().get_element_location(ele)

    @teststep
    def pattern_switch(self):
        """全英/英汉模式切换 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "hint_switch") \
            .click()

    @teststeps
    def word(self):
        """展示的句子"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "english")
        return ele

    # @teststeps
    # def wait_check_no_hint_page(self, var=10):
    #     """以“显示解释”的ID为依据"""
    #     locator = (By.XPATH, '//android.widget.TextView[contains(@text, "显示解释")]')
    #     return self.wait.wait_check_element(locator, var)
    #
    # @teststeps
    # def wait_check_hint_page(self, var=10):
    #     """以“隐藏解释”的ID为依据"""
    #     locator = (By.XPATH, '//android.widget.TextView[contains(@text, "隐藏解释")]')
    #     return self.wait.wait_check_element(locator, var)

    @teststep
    def hint(self):
        """解释"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "hint")
        return item

    @teststep
    def sound_audio_button(self):
        """播录语音按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_play").click()

    @teststeps
    def suspend_button(self, loc):
        """'暂停'按钮  由于拿不到元素信息，因为暂停 和 开始 是同一个view，故用坐标点击"""
        # print('点击暂停按钮', loc)
        ClickBounds().click_bounds(loc[0], loc[1])

    @teststep
    def question_audio_button(self):
        """语音按钮"""
        self.driver \
            .find_elements_by_class_name('android.widget.ImageView')[0].click()
        print('题目播放按钮')

    @teststep
    def next_button_judge(self, var):
        """‘下一步’按钮 状态判断"""
        item = self.next_button()  # ‘下一步’按钮
        value = GetAttribute().enabled(item)

        if value != var:  # 测试 下一步 按钮 状态
            print('★★★ 下一步按钮 状态Error', value)
        else:
            return True

    @teststep
    def next_button(self):
        """点击‘下一步’按钮"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "fab_next")
        return item

    @teststeps
    def next_button_operation(self, var):
        """下一步 按钮 判断 加 点击操作"""
        if self.next_button_judge(var):  # 下一步 按钮 状态判断
            self.next_button().click()  # 点击 下一步 按钮

    @teststeps
    def wait_check_num_tips_page(self, var=10):
        """以“录音五次 提示信息”的ID为依据"""
        locator = (By.ID, self.max_tips_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def max_tips(self):
        """录音五次 提示信息"""
        item = self.driver \
            .find_element_by_id(self.max_tips_value).text
        return item

    # 以下为结果页面元素
    @teststeps
    def wait_check_result_page(self, var=15):
        """以“再练一遍 按钮”的ID为依据"""
        locator = (By.ID, self.again_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_result_list_page(self, var=15):
        """以“再练一遍 按钮”的ID为依据"""
        locator = (By.ID, self.result_word_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def result_title(self):
        """本次单词跟读时长: """
        ele = self.driver. \
            find_element_by_id(gv.PACKAGE_ID + "game_name").text
        print(ele)

    @teststep
    def author_img(self):
        """头像"""
        locator = (By.ID, gv.PACKAGE_ID + "avatar")
        if not self.wait.judge_is_exists(locator):
            print('★★★ Error - 无头像')
        else:
            return self.wait.wait_find_element(locator)

    @teststep
    def author_name(self):
        """上传者 """
        ele = self.driver. \
            find_element_by_id(gv.PACKAGE_ID + "name").text
        print(ele)

    @teststeps
    def result_item(self):
        """展示的 条目"""
        ele = self.driver \
            .find_elements_by_xpath('//android.view.ViewGroup[@resource-id="{}"]'
                                    .format(gv.PACKAGE_ID + "item_container"))

        content = []
        for i in range(len(ele)):
            var = ele[i].find_elements_by_xpath('.//child::*')
            if len(var) == 6:
                item = [x for x in var[1:]]
                content.append(item)
        return content

    @teststep
    def result_img(self):
        """头像"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "img")
        return ele

    @teststeps
    def result_word(self):
        """展示的句子"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "word")
        return ele

    @teststep
    def result_explain(self):
        """解释"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "explain")
        return item

    @teststep
    def result_audio_button(self):
        """播音按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "audio")
        return ele

    @teststep
    def result_check_button(self):
        """单选框"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "check")
        return ele

    @teststeps
    def word_reading_operation(self):
        """《单词跟读》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                print('================================================================')
                timestr = []  # 获取每小题的时间
                rate = Homework().rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    self.next_button_operation('false')  # 下一步 按钮 判断 加点击

                    self.question_audio_button()  # 题目播放按钮
                    loc = self.recording_button_location()
                    if i == 1:  # 验证5次录音
                        self.judge_max_operation(loc)
                        print('5次录音')
                    elif i == 2:  # 验证 录音超时
                        self.recording_button().click()  # 录音按钮
                        print('录音按钮，最大时长20秒')
                        time.sleep(19)
                        # Toast().toast_operation('录音时长不得超过 20秒')
                    else:
                        if i == 0:  # 权限申请
                            self.recording_button().click()  # 录音按钮
                            if self.get_permission_operation():  # 权限申请
                                if self.wait_check_play_page():
                                    self.recording_button().click()  # 录音按钮
                        else:
                            self.recording_button().click()  # 录音按钮
                            print('录音按钮')

                        time.sleep(2)
                        self.suspend_button(loc)  # 录音暂停按钮
                        print('录音暂停按钮')
                        # Toast().toast_operation('播放录音')
                    if self.wait_check_play_page():
                        self.sound_audio_button()  # 录音播放按钮
                        print('录音播放按钮')
                        if self.wait_check_play_page():
                            print('------------------------------')
                            word = self.word().text  # 题目
                            hint = self.hint().text  # 解释
                            print('题目 %s 解释:%s' % (word, hint))
                            print('------------------------------')

                    time.sleep(3)
                    timestr.append(Homework().time())  # 统计每小题的计时控件time信息
                    self.next_button_operation('true')  # 下一步 按钮 判断 加点击
                    print('--------------------------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                return rate

    @teststeps
    def judge_max_operation(self, loc):
        """验证 5次机会"""
        k = 0
        while k < 5:
            self.recording_button().click()  # 录音按钮
            time.sleep(2)
            self.suspend_button(loc)  # 录音暂停按钮
            # Toast().toast_operation('播放录音')
            k += 1

        if self.wait_check_num_tips_page():  # 文案
            tips = self.max_tips()
            if tips != '读得很好呢，进入下一题吧':
                print('★★★ Error - 最多5次机会，文案有误', tips)

        if GetAttribute().enabled(self.recording_button()) != 'false':
            print('★★★ Error - 录音按钮状态有误:true')

    @teststeps
    def result_detail_page(self):
        """《单词跟读》 结果页 操作过程 """
        if self.wait_check_result_page():  # 结果页检查点
            print('=============================结果页=============================')
            self.author_img()
            self.author_name()
            print('----------------------------')
            self.swipe_operation()

    @teststeps
    def swipe_operation(self, content=None):
        """ 查看答案 - 点击 听力按钮
        :param content: 翻页
        """
        if self.wait_check_result_page():
            if content is None:
                content = []

            ques = self.result_item()
            if len(ques) > 5 and not content:
                self.ergodic_list(ques, len(ques) - 1)
                content = [ques[-2]]

                if self.result.wait_check_detail_page():
                    SwipeFun().swipe_vertical(0.5, 0.85, 0.2)
                    self.swipe_operation(content)
            else:
                var = 0
                if content:
                    for k in range(len(ques)):
                        if content[0] == ques[k]:
                            var = k + 1
                            break

                self.ergodic_list(ques, len(ques), var)

    @teststeps
    def ergodic_list(self, ques, length, var=0):
        """遍历列表
        :param ques:
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        for i in range(var, length):
            print('单词:', ques[i][2].text)  # 正确word
            print('解释:', ques[i][3].text)  # 解释
            print('勾选标识:', GetAttribute().enabled(ques[i][-1]))

            print('------------------------------')
            ques[i][1].click()  # 点击发音按钮

    @teststeps
    def study_again(self):
        """再听一遍 操作过程"""
        if self.wait_check_result_page():  # 结果页检查点
            print('================================================================')
            if self.wait_check_result_list_page():
                self.result_check_button()[0].click()

            if self.wait_check_result_list_page():
                self.result.again_button()[0].click()  # 结果页 再听一遍 按钮

                self.word_reading_operation()  # 游戏过程

    @teststeps
    def back_operation(self):
        """从结果页返回小游戏list"""
        if self.wait_check_result_page():
            ThomePage().back_up_button()  # 返回小游戏界面
            if GamesPage().wait_check_page():
                ThomePage().back_up_button()  # 返回 题单详情页

    @teststeps
    def get_permission_operation(self):
        """获取 录音权限"""
        if ThomePage().wait_check_permission():
            ThomePage().allow_button()
            if ThomePage().wait_check_permission():
                ThomePage().allow_button()
                if ThomePage().wait_check_permission():
                    ThomePage().allow_button()

                    return True
