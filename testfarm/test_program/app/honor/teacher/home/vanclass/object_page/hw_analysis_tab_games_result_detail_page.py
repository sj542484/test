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


class StrengthenSentenceResult(BasePage):
    """强化炼句"""
    drop_element = 'van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate-noarrow'
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“句子”为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__content"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def question(self):
        """单词"""
        locator = (By.XPATH, '//span[@class="detail-sf-text"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def explain(self):
        """解释"""
        locator = (By.XPATH, '//div[@class="detail-sf-label-text"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮

        for k in range(len(ele)):
            if ele[k].get_attribute('class') != 'rate-correct-arrow':
                content.append(ele[k].text)
            else:
                element.append(ele[k])
        print(content)
        return content, element


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
    drop_element = 'van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate'
    result_right_value = 'detail-tylj-right-icon van-icon van-icon-success'  # 正确标识

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“”的为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__content"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def sentence(self):
        """展示的答案"""
        locator = (By.XPATH, '//span[@class="detail-tylj-text"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def explain(self):
        """展示的翻译"""
        locator = (By.XPATH, '//div[@class="detail-tylj-label"]')
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

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮

        for k in range(len(ele)):
            if ele[k].get_attribute('class') != 'rate-correct-arrow':
                content.append(ele[k].text)
            else:
                element.append(ele[k])
        print(content)
        return content, element


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

    @teststep
    def question(self):
        """题目数"""
        locator = (By.XPATH, '//img[@class="report-pl-image"]')
        return self.wait.wait_find_elements(locator)

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
        locator = (By.XPATH, '//div[@class="game-article"]/div/div')
        ele = self.wait.wait_find_elements(locator)
        item = [k.text for k in ele]
        print(item)
        print('-----------------------------------')

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH, '//span[@class="article-correct-rate"]')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮
        for k in ele:
            content.append(k.text)
            if k.get_attribute('style') == 'padding-right:8px;':
                element.append('')
            else:
                element.append(k.find_element_by_xpath('.//span'))

        return content, element


class ReadingArticleResult(BasePage):
    """阅读理解 答题情况"""
    drop_element = 'van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate'
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
        locator = (By.XPATH, '//div[@class="game-reports-rc-content-article"]')
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
        locator = (By.XPATH, '//div[@class="van-cell__label"]')
        ele = self.wait.wait_find_elements(locator)

        content = []
        element = []
        for i in range(len(ele)):
            option = ele[i].find_elements_by_xpath('.//div/div')
            item = [option[0].text, option[1].text]
            content.append(item)
            element.append(ele[i])
        return element, content

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮

        for k in range(len(ele)):
            style = ele[k].find_element_by_xpath('.//parent::span/parent::span').get_attribute('style')
            if ele[k].get_attribute('class') != 'rate-correct-arrow' and style != 'display: none;':
                content.append(ele[k].text)
                if ele[k + 1].get_attribute('class') == 'rate-correct-arrow':
                    element.append(ele[k + 1])
        print(content)
        return content, element


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
        print(len(self.wait.wait_find_elements(locator)))
        return self.wait.wait_find_elements(locator)

    @teststeps
    def option_items(self):
        """当前页面中所有题目的选项"""
        locator = (By.XPATH, '//div[@id="game-article-options-cell"]')
        ele = self.wait.wait_find_elements(locator)

        content = []
        element = []
        for i in range(len(ele)):
            var = ele[i].find_elements_by_xpath('.//div/div/div/div')
            item = [var[0].text, var[1].text]
            content.append(item)

            element.append(ele[i])
        return element, content

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH, '//span[@class="article-correct-rate"]')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮
        for k in ele:
            content.append(k.text)
            if k.get_attribute('style') == 'padding-right:8px;':
                element.append('')
            else:
                element.append(k.find_element_by_xpath('.//span'))

        return content, element


class CompleteArticleResult(BasePage):
    """补全文章 答题情况"""
    result_right_value = 'game-report-ss-content-item-options game-report-ss-content-item-options-right'  # 正确选项

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_list_page(self):
        """以“ 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__content"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def complete_article_content(self):
        """补全文章 文章元素"""
        locator = (By.XPATH, '//div[@class="game-article"]')
        if self.wait.wait_check_element(locator):
            var = self.wait.wait_find_element(locator).find_elements_by_xpath('.//div')
            content = [k.text for k in var if k.text != '']
            print(content)
        else:
            print('★★★ Error- 文章元素不存在')

    @teststep
    def option_char(self):
        """选项"""
        locator = (By.XPATH, '//div[@class="game-reports-ss-content-item-options game-reports-ss-content-item-options-right"]')
        return self.wait.wait_find_elements(locator)[::2]

    @teststep
    def option_content(self):
        """选项"""
        locator = (By.XPATH, '//div[@class="game-reports-ss-content-item-content"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH, '//span[@class="article-correct-rate"]')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮
        for k in ele:
            content.append(k.text)
            if k.get_attribute('style') == 'padding-right:8px;':
                element.append('')
            else:
                element.append(k)

        return content, element


class SentenceTransResult(BasePage):
    """句型转换"""
    drop_element = 'van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate-noarrow'
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
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮

        for k in range(len(ele)):
            if ele[k].get_attribute('class') != 'rate-correct-arrow':
                content.append(ele[k].text)
            else:
                element.append(ele[k])
        print(content)
        return content, element


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

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮

        for k in range(len(ele)):
            style = ele[k].find_element_by_xpath('.//parent::span/parent::span').get_attribute('style')
            if ele[k].get_attribute('class') != 'rate-correct-arrow' and style != 'display: none;':
                content.append(ele[k].text)
                if ele[k + 1].get_attribute('class') == 'rate-correct-arrow':
                    element.append(ele[k + 1])
        print(content)
        return content, element

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
    drop_element = 'van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate'
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
        content = []  # 选项
        item = []  # 解析
        for k in range(len(ele)):
            if ele[k].get_attribute('class') == 'game-cell-item-content':
                option = {ele[k - 1].text: ele[k].text}
                content.append(option)
            elif 'game-cell-item-parse-title' in ele[k].get_attribute('class'):
                item.append(ele[k].text)

        print(content)
        print(item)
        return content

    @teststeps
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)
        content = []  # 答对率
        element = []  # 下拉按钮

        for k in range(len(ele)):
            style = ele[k].find_element_by_xpath('.//parent::span/parent::span').get_attribute('style')
            if ele[k].get_attribute('class') != 'rate-correct-arrow' and style != 'display: none;':
                content.append(ele[k].text)
                if ele[k + 1].get_attribute('class') == 'rate-correct-arrow':
                    element.append(ele[k + 1])
        print(content)
        return content, element


class ListenDictationResult(BasePage):
    """听后选择 答题结果"""
    drop_element = 'van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate-noarrow'
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
    def drop_down_rate(self):
        """正确选项后答对率 下拉text"""
        locator = (By.XPATH,
                   '//span[contains(@class,"van-tag van-tag--plain van-tag--default van-hairline--surround rate-correct-rate")]/span')
        ele = self.wait.wait_find_elements(locator)

        content = []  # 答对率
        element = []  # 下拉按钮
        for k in range(len(ele)):
            style = ele[k].find_element_by_xpath('.//parent::span/parent::span').get_attribute('style')
            if ele[k].get_attribute('class') != 'rate-correct-arrow' and style != 'display: none;':
                content.append(ele[k].text)
                if ele[k + 1].get_attribute('class') == 'rate-correct-arrow':
                    element.append(ele[k + 1])
        print(content)
        return content, element

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
