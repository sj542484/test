# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 13:13
# -------------------------------------------
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from app.honor.student.library.object_pages.games.word_match import LibraryWordMatch
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class ResultPage(BasePage):
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststep
    def wait_check_result_page(self):
        """结果页面检查点"""
        locator = (By.ID, self.id_type()+'detail')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_medal_page(self):
        """勋章页面检查点"""
        locator = (By.ID, self.id_type() + 'share_img')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_answer_page(self):
        """查看答案页面"""
        locator = (By.XPATH, '//*[@text="查看答案"]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def check_result_btn(self):
        """查看答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'detail')
        return ele

    @teststep
    def again_btn(self):
        """错题再练 再练一次按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'again')
        return ele

    @teststep
    def correct_rate(self):
        """正确率"""
        ele = self.driver.find_element_by_id(self.id_type() + 'correct_rate')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def score(self):
        """积分"""
        ele = self.driver.find_element_by_id(self.id_type() + 'score')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def star(self):
        """星星"""
        ele = self.driver.find_element_by_id(self.id_type() + 'star')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def time(self):
        """时间"""
        ele = self.driver.find_element_by_id(self.id_type() + 'time')
        return ele

    @teststep
    def explains(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'explain')
        return ele

    @teststep
    def words(self, explain):
        """单词"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="%s"]/'
                                                'preceding-sibling::android.widget.TextView' % explain)
        return ele.text

    @teststep
    def voices(self, explain):
        """声音图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="%s"]/'
                                                'preceding-sibling::android.widget.ImageView[contains(@resource-id, "audio")]' % explain)
        return ele

    @teststep
    def correct_wrong_icon(self, explain):
        """我的结果图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="%s"]/'
                                                'preceding-sibling::android.widget.ImageView[contains(@resource-id, "result")]' % explain)
        return ele

    @teststep
    def result_multi_data_check(self, fq, result, first_num, current_count):
        if self.wait_check_result_page():  # 返回结果页
            print('===== 结果页数据核对 =====\n')
            print('上次做的题数：', first_num)
            print('本次做的题数：', current_count)
            right_list = result[1]                                # 本次所有题
            right_rate = round(len(right_list) / current_count * 100) if fq == 1 else 100

            if right_rate != self.correct_rate():
                print("★★★  准确率有误", right_rate, self.correct_rate())
            else:
                print('准确率核实正确')

            right_score = len(result[1]) if fq == 1 else first_num
            if right_score != self.score():
                print('积分有误', "应当为", len(right_list), '页面为', self.score())
            else:
                print('积分核实正确')

            compare_star = current_count if fq == 1 else first_num + current_count
            if compare_star != self.star():
                print('★★★ 星星有误', '应为：', compare_star, '页面为：', self.star())
            else:
                print('星星核实正确')

            print('===== 结果页数据核实完毕 =====\n')

    @teststeps
    def word_game_answer_detail_operate(self, mine_answer):
        """单词类游戏查看答案页面处理过程"""
        right, wrong, right_answer = {}, {}, {}
        if any([LibraryWordMatch().is_word(x) for x in list(mine_answer.keys())]):
            word_is_key = True
        else:
            word_is_key = False

        if self.wait_check_answer_page():
            print('===== 查看结果页 =====\n')
            explains = self.explains()

            for explain in explains:
                self.voices(explain.text).click()
                time.sleep(0.5)
                word = self.words(explain.text)
                print('单词：', word)
                print('解释：', explain.text)
                if word_is_key:
                    right_answer[word.lower()] = explain.text
                else:
                    right_answer[explain.text] = word

                value = explain.text if word_is_key else word
                mine = mine_answer[word] if word_is_key else mine_answer[explain.text]

                if value != mine:
                    if GetAttribute().selected(self.correct_wrong_icon(explain.text)) == 'true':
                        print('★★★ 单词与我输入的不一致，但图标显示正确\n')
                    else:
                        print('图标标识正确\n')
                        wrong[word] = explain.text

                else:
                    if GetAttribute().selected(self.correct_wrong_icon(explain.text)) == 'false':
                        print('★★★ 单词与我输入一致，但图标显示错误\n')
                    else:
                        print('图标标识正确\n')
                        right[word] = explain.text

        print("错误：", wrong)
        print("正确：", right)
        self.click_back_up_button()
        return wrong, right, right_answer

    @teststeps
    def word_match_result_operate(self, mine_answer):
        word_list = []
        while len(word_list) < len(mine_answer):
            explains = self.explains()
            for x in explains:
                if x.text in word_list:
                    continue
                else:
                    word_list.append(x.text)
                    word = self.words(x.text)
                    print('单词：', word)
                    print('解释：', x.text)

                    self.voices(x.text).click()
                    correct_icon = self.correct_wrong_icon(x.text)
                    if correct_icon.get_attribute('selected') == 'false':
                        print('★★★ 单词选择正确， 但是图标显示错误！')
                    print('-'*30, '\n')
            self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
        right = list(mine_answer.values())
        right_answer = mine_answer
        self.click_back_up_button()
        return mine_answer, right, right_answer
