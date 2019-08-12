# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 13:13
# -------------------------------------------
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.app.honor.student.library.object_pages.games.word_match import LibraryWordMatch
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


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
    def answers(self):
        """单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_answer')
        return ele

    @teststep
    def voices(self, var):
        """声音图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/'
                                                'preceding-sibling::android.widget.ImageView' % var)
        return ele

    @teststep
    def explain(self, var):
        """解释"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/../'
                                                'following-sibling::android.widget.TextView' % var)
        return ele.text

    @teststep
    def mine_result(self, var):
        """我的结果图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/../'
                                                'following-sibling::android.widget.ImageView' % var)
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
            words = self.answers()

            for i in range(len(words)):
                self.voices(words[i].text).click()
                time.sleep(0.5)
                explain = self.explain(words[i].text)
                print('单词：', words[i].text)
                print('解释：', explain)
                if word_is_key:
                    right_answer[words[i].text.lower()] = explain
                else:
                    right_answer[explain] = words[i].text

                value = explain if word_is_key else words[i].text
                mine = mine_answer[words[i].text] if word_is_key else mine_answer[explain]
                if value != mine:
                    if GetAttribute().selected(self.mine_result(words[i].text)) == 'true':
                        print('★★★ 单词与我输入的不一致，但图标显示正确\n')
                    else:
                        print('图标标识正确\n')
                        wrong[words[i].text] = explain

                else:
                    if GetAttribute().selected(self.mine_result(words[i].text)) == 'false':
                        print('★★★ 单词与我输入一致，但图标显示错误\n')
                    else:
                        print('图标标识正确\n')
                        right[words[i].text] = explain

        print("错误：", wrong)
        print("正确：", right)
        self.click_back_up_button()
        return wrong, right, right_answer

