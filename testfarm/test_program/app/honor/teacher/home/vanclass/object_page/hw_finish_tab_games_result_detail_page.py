#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.swipe_screen import SwipeFun
from utils.wait_element_vue import WaitElement


class MatchExerciseResult(BasePage):
    """连连看 图片模式"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”的为依据"""
        locator = (By.XPATH, '//div[@id="game-word-image-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def img(self):
        """图片"""
        locator = (By.XPATH, '//div[@class="game-cell-img van-image"]/img')
        return self.wait.wait_find_elements(locator)

    @teststep
    def word(self):
        """单词"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]/div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def status(self):
        """对错标识"""
        locator = (By.XPATH, '//div[@id="game-word-image-cell"]/i')
        return self.wait.wait_find_elements(locator)

    @teststep
    def voice_button(self):
        """播音按钮"""
        locator = (By.XPATH, '//div[@id="audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)


class FlashSentenceResult(BasePage):
    """闪卡（句子学习）"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”的为依据"""
        locator = (By.XPATH, '//div[@class="van-cell__title flash-sentence-title"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def sentence(self):
        """句子"""
        locator = (By.XPATH, '//div[@class="van-cell__title flash-sentence-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def explain(self):
        """解释"""
        locator = (By.XPATH, '//div[@class="van-cell__label flash-sentence-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def status(self):
        """对错标识"""
        locator = (By.XPATH, '//div[@class="van-cell"]/div/i')
        return self.wait.wait_find_elements(locator)


class FlashResult(BasePage):
    """闪卡（单词抄写&学习）"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“答案 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@class="game-cell van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def first_report(self):
        """首次正答率"""
        locator = (By.XPATH, '//span[contains(text(),"首次正答")]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def result_voice(self):
        """语音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_img(self):
        """图片"""
        locator = (By.XPATH, '//img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_answer(self):
        """单词"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]/div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_explain(self):
        """解释"""
        locator = (By.XPATH, '//div[@class="van-cell__label"]/div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_mine(self):
        """我的"""
        locator = (By.XPATH, '//div[@class="game-cell van-cell"]/i')
        return self.wait.wait_find_elements(locator)



class WordFormSentenceResult(BasePage):
    """连词成句"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”的为依据"""
        locator = (By.XPATH, '//div[@class="van-cell__title detail-fc-title"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def question(self):
        """单词"""
        locator = (By.XPATH, '//div[@class="van-cell__title detail-fc-title"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def explain(self):
        """解释"""
        locator = (By.XPATH, '//div[@class="van-cell__label detail-fc-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def status(self):
        """对错标识"""
        locator = (By.XPATH, '//div[@class="van-cell"]/div/i')
        return self.wait.wait_find_elements(locator)


class StrengthenSentenceResult(BasePage):
    """强化炼句"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“句子”为依据"""
        locator = (By.XPATH, '//div[@class="detail-sf-text"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def question(self):
        """单词"""
        locator = (By.XPATH, '//div[@class="detail-sf-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def explain(self):
        """解释"""
        locator = (By.XPATH, '//div[@class="detail-sf-label"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def status(self):
        """对错标识"""
        locator = (By.XPATH, '//div[@class="van-cell"]/div/i')
        return self.wait.wait_find_elements(locator)


class WordReadingResult(BasePage):
    """单词跟读"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”的为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="详情"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def st_icon(self):
        """学生 头像"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-icon van-image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-icon van-image"]/following-sibling::span')
        return self.wait.wait_find_element(locator).text

    @teststep
    def hint(self):
        """句子"""
        locator = (By.XPATH, '//div[@class="completion-detail-header-tip"]')
        return self.wait.wait_find_element(locator).text

    @teststep
    def result_voice(self):
        """语音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_word_explain(self):
        """单词 解释"""
        locator = (By.XPATH, '//div[@class="completion-detail-wr-center"]/span')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_img(self):
        """图片"""
        locator = (By.XPATH, '//div[@class="completion-detail-wr-icon van-image"]/img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)


class ListenFormSentenceResult(BasePage):
    """听音连句"""
    result_right_value = 'detail-tylj-right-icon van-icon van-icon-success'  # 正确标识

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”的为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__content"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def question_items(self):
        """题目数"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def correct_answer(self):
        """展示的答案"""
        locator = (By.XPATH, '//div[@class="detail-tylj-text"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def correct_detail(self, var):
        """展示的答案 为空时，"""
        ele = var.find_elements_by_xpath('.//span')
        content = [k.text for k in ele]
        return content

    @teststeps
    def explain(self):
        """展示的翻译"""
        locator = (By.XPATH, '//div[@class="detail-tylj-label"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def mine_answer(self):
        """答错时，我的答题结果"""
        locator = (By.XPATH, '//div[@class="detail-tylj-text"]/span')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def result_mine(self):
        """我的"""
        locator = (By.XPATH, '//div[@class="van-cell"]/div/i')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def result_voice(self):
        """语音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)


class EarsResult(BasePage):
    """磨耳朵 答题结果"""
    hint_word_value = '//div[@class="game-report-tb-content-title"]'  # 提示词
    play_button_value = '//i[@class="van-icon van-icon-play"]'  # 播音按钮

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“spend_time”的ID为依据"""
        locator = (By.XPATH, '//img[@class="report-pl-image"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def exo_play_button(self):
        """播放按钮"""
        locator = (By.XPATH, self.play_button_value)
        self.wait.wait_find_element(locator).click()

    @teststep
    def exo_pause_button(self):
        """暂停按钮"""
        locator = (By.XPATH, '//i[@class="van-icon van-icon-pause"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_progress(self):
        """播放 进度"""
        locator = (By.XPATH, '//div[@vt-audio-player__wrapper-buffer]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_position(self):
        """播放 位置"""
        locator = (By.XPATH, '//span[@class="vt-audio-player__time-current"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_duration(self):
        """音频长短"""
        locator = (By.XPATH, '//span[@class="vt-audio-player__time-duration"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def ears_sentence(self):
        """磨耳朵"""
        locator = (By.XPATH, '//div[@class="report-pl-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def ears_explain(self):
        """磨耳朵"""
        locator = (By.XPATH, '//div[@class="report-pl-cell-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def ears_img(self):
        """磨耳朵"""
        locator = (By.XPATH, '//img[@class="report-pl-image"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def sound_operation(self):
        """音频 操作"""
        self.exo_play_button()  # 播音按钮

        duration = self.exo_duration().text  # 音频总时长
        progress = self.exo_position().text  # 进度
        print('当前播放位置：', progress, duration)
        var = re.sub("\D", "", progress)
        if int(var) == 0000:
            print('★★★ Error- 听力时间进度', var)
        elif var > re.sub("\D", "", duration):
            print('★★★ Error- 听力时间进度大于总时长', var, duration)


class ChooseClozeResult(BasePage):
    """选词填空"""
    hint_word_value = '//div[@class="game-report-tb-content-title"]'  # 提示词

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“spend_time”的ID为依据"""
        locator = (By.XPATH, '//div[@class="game-report-tb-content"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def verify_hint_word(self):
        """验证 选词填空的wording: 提示词 是否存在"""
        locator = (By.XPATH, self.hint_word_value)
        return self.wait.judge_is_exists(locator)

    @teststep
    def hint_word(self):
        """wording: 提示词"""
        locator = (By.XPATH, self.hint_word_value)
        return self.wait.wait_find_element(locator).text

    @teststep
    def prompt_word(self):
        """提示的单词"""
        locator = (By.XPATH, '//div[@class="game-report-tb-content-extras"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        print('-----------------------------------')

    @teststep
    def choice_vocabulary_content(self):
        """选词填空的文章"""
        locator = (By.XPATH, '//div[@class="game-article"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        print('-----------------------------------')


class ReadingArticleResult(BasePage):
    """阅读理解 答题情况"""
    result_right_value = 'game-cell-item-options game-cell-item-options-right'  # 正确选项
    options_value = '//div[@class="game-cell van-cell"]'  # 选项元素

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, self.options_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def reading_article_content(self):
        """阅读理解 文章元素"""
        locator = (By.XPATH, '//div[@class="game-report-rc-content-article"]')
        if self.wait.wait_check_element(locator):
            var = self.wait.wait_find_element(locator).find_elements_by_xpath('.//child::div')
            content = [k.text for k in var if k.text != '']
            print(content)
        else:
            print('★★★ Error- 文章元素不存在')

    @teststeps
    def question_item(self):
        """题目数"""
        locator = (By.XPATH, '//span[@class="game-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def option_items(self):
        """当前页面中所有题目的选项"""
        locator = (By.XPATH, '//div[@class="van-cell__label"]')
        ele = self.wait.wait_find_elements(locator)

        content = []
        for i in range(len(ele)):
            item = {}
            option = ele[i].find_elements_by_xpath('.//div/div')
            item[option[0].text] = option[1].text
            content.append(item)
        return ele, content


class ClozeTestResult(BasePage):
    """完型填空 答题情况"""
    result_right_value = 'game-cell-item-options game-cell-item-options-right'  # 正确选项
    options_value = '//div[@class="game-cell van-cell"]'  # 选项元素

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, self.options_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def cloze_article_content(self):
        """完形填空 文章元素"""
        locator = (By.XPATH, '//div[@class="game-article"]')
        if self.wait.wait_check_element(locator):
            var = self.wait.wait_find_element(locator).find_elements_by_xpath('.//div')
            content = [k.text for k in var if k.text != '']
            print(content)
        else:
            print('★★★ Error- 文章元素不存在')

    @teststeps
    def question_item(self):
        """题目数"""
        locator = (By.XPATH, '//span[@class="game-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def option_items(self):
        """当前页面中所有题目的选项"""
        locator = (By.XPATH, '//div[@id="game-article-options-cell"]')
        ele = self.wait.wait_find_elements(locator)

        content = []
        for i in range(len(ele)):
            item = {}
            var = ele[i].find_elements_by_xpath('.//div/div/div/div')
            item[var[0].text] = var[1].text
            content.append(item)
        return ele, content


class CompleteArticleResult(BasePage):
    """补全文章 答题情况"""
    result_right_value = 'game-report-ss-content-item-options game-report-ss-content-item-options-right'  # 正确选项
    options_value = '//div[@class="game-report-ss-content-item"]'  # 选项元素

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, self.options_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def complete_article_content(self):
        """补全文章 文章元素"""
        locator = (By.XPATH, '//div[@class="game-article"]')
        if self.wait.wait_check_element(locator):
            var = self.wait.wait_find_element(locator).find_elements_by_xpath('.//child::div')
            content = [k.text for k in var if k.text != '']
            print(content)
        else:
            print('★★★ Error- 文章元素不存在')

    @teststep
    def option_char(self):
        """选项"""
        locator = (By.XPATH, '//div[@class="game-report-ss-content-item"]/div')
        return self.wait.wait_find_elements(locator)[::2]

    @teststep
    def option_content(self):
        """选项"""
        locator = (By.XPATH, '//div[@class="game-report-ss-content-item-content"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def option_items(self):
        """选项"""
        locator = (By.XPATH, '//div[@class="game-report-ss-content-item"]')
        ele = self.wait.wait_find_elements(locator)

        content = []
        element = []
        for i in range(len(ele)):
            var = ele[i].find_elements_by_xpath('.//div')
            item = [var[0].text, var[1].text]
            content.append(item)
            element.append(ele[i])
        return element, content


class SentenceTransResult(BasePage):
    """句型转换"""
    result_right_value = 'van-icon van-icon-success game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@class="game-cell van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def result_question(self):
        """展示的题目"""
        locator = (By.XPATH, '//div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)[::2]

    @teststeps
    def result_answer(self):
        """展示的 正确答案"""
        locator = (By.XPATH, '//div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)[1::2]

    @teststeps
    def result_mine(self):
        """我的答案"""
        locator = (By.XPATH, '//div[@class="game-cell-content game-cell-content-last"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def result_mine_state(self):
        """我的答案对错标识 selected属性"""
        locator = (By.XPATH, '//div[@id="game-st-cell"]/i')
        return self.wait.wait_find_elements(locator)


class PictureDictationResult(BasePage):
    """听音选图 答题结果"""
    result_right_value = 'game-cell-item-options game-cell-item-options-right'

    def __init__(self):
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@class="vt-audio-player sp-audio"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def exo_play(self):
        """播放按钮"""
        locator = (By.XPATH, '//div[@class="vt-audio-player sp-audio"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def exo_pause(self):
        """暂停按钮"""
        locator = (By.XPATH, '//i[@class="van-icon van-icon-pause"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_progress(self):
        """播放 进度"""
        locator = (By.XPATH, '//div[@vt-audio-player__wrapper-buffer]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_position(self):
        """播放 位置"""
        locator = (By.XPATH, '//span[@class="vt-audio-player__time-current"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_duration(self):
        """音频长短"""
        locator = (By.XPATH, '//span[@class="vt-audio-player__time-duration"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def result_article(self):
        """听力 解析"""
        locator = (By.XPATH, '//div[@class="sp-article"]/div')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_sentence(self):
        """题目"""
        locator = (By.XPATH, '//span[@class="game-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_options(self):
        """列表选项"""
        locator = (By.XPATH, '//div[@class="van-grid"]')
        ele = self.wait.wait_find_elements(locator)

        content = []
        element = []
        for i in range(len(ele)):
            img = ele[i].find_elements_by_xpath('.//div/div/div/img')
            option = ele[i].find_elements_by_xpath('.//div/div/div/span')

            options = []
            for j in range(len(option)):
                if option[j].text in ('A', 'B', 'C', 'D', 'E'):
                    options.append(option[j].text)

            item = []  # ABCD & 内容
            for j in range(len(img)):
                item.extend([options[j], img[j].get_attribute('src')])
            content.append(item)
            element.append(option[i])

        return element, content

    @teststeps
    def sound_operation(self):
        """音频 操作"""
        self.exo_play()  # 播音按钮
        duration = self.exo_duration().text  # 音频总时长
        progress = self.exo_position().text  # 进度
        print('当前播放位置：', progress, duration)

        var = re.sub("\D", "", progress)
        if int(var) == 0000:
            print('★★★ Error- 听力时间进度', var)
        elif var > re.sub("\D", "", duration):
            print('★★★ Error- 听力时间进度大于总时长', var, duration)


class SingleChooseResult(BasePage):
    """单项选择 答题结果"""
    play_button_value = '//div[@class="vt-audio-player fs-audio"]/audio'  # 播音按钮
    result_right_value = 'game-cell-item-options game-cell-item-options-right'

    def __init__(self):
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@id="game-sq-cell"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def question_items(self):
        """题目数"""
        locator = (By.XPATH, '//span[@class="game-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def option_element(self, var):
        """当前页面中所有题目的选项"""
        ele = var.find_elements_by_xpath(".//following-sibling::div/div/div")
        content = [item.text for item in ele]
        print(content)
        return ele, content


class ListenDictationResult(BasePage):
    """听后选择 答题结果"""
    result_right_value = 'game-cell-item-options game-cell-item-options-right'

    def __init__(self):
        self.swipe = SwipeFun()
        self.wait = WaitElement()

    @teststep
    def exo_play_button(self):
        """播放按钮"""
        locator = (By.XPATH, '//i[@class="van-icon van-icon-play"]')
        self.wait.wait_find_element(locator).click()

    @teststep
    def exo_pause_button(self):
        """暂停按钮"""
        locator = (By.XPATH, '//i[@class="van-icon van-icon-pause"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_progress(self):
        """播放 进度"""
        locator = (By.XPATH, '//div[@vt-audio-player__wrapper-buffer]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_position(self):
        """播放 位置"""
        locator = (By.XPATH, '//span[@class="vt-audio-player__time-current"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def exo_duration(self):
        """音频长短"""
        locator = (By.XPATH, '//span[@class="vt-audio-player__time-duration"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def result_article(self):
        """听力 解析"""
        locator = (By.XPATH, '//div[@class="fs-article"]/div')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@id="game-article-options-cell"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def question_items(self):
        """题目数"""
        locator = (By.XPATH, '//span[@class="game-cell-title"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def option_element(self, var):
        """当前页面中所有题目的选项"""
        ele = var.find_elements_by_xpath(".//parent::div/div/div/div")
        content = [item.text for item in ele]
        return ele, content

    @teststeps
    def sound_operation(self):
        """音频 操作"""
        self.exo_play_button()  # 播音按钮
        time.sleep(2)

        duration = self.exo_duration().text  # 音频总时长
        progress = self.exo_position().text  # 进度
        print('当前播放位置：', progress, duration)
        var = re.sub("\D", "", progress)
        if int(var) == 0000:
            print('★★★ Error- 听力时间进度有误', var)
        elif var > re.sub("\D", "", duration):
            print('★★★ Error- 听力时间进度大于总时长', var, duration)
