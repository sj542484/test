# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/12 8:24
# -------------------------------------------
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class FlashCard(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_study_page(self):
        """以“闪卡练习 -学习模式”的xpath-text为依据"""
        locator = (By.ID, self.id_type() + "iv_star")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_explain_page(self):
        """判断解释是否存在"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_chinese")
            return True
        except:
            return False

    @teststep
    def wait_check_flash_result_page(self):
        """结果页页面检查点"""
        locator = (By.XPATH, "//*[@text='完成学习']")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def word(self):
        """页面单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_english')
        return ele.text

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver.find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def author(self):
        """例句推荐老师"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "author").text
        return english

    @teststep
    def english_study(self):
        """全英模式 页面内展示的word"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "tv_english").text
        return english

    @teststep
    def explain(self):
        """英汉模式 页面内展示的word解释"""
        explain = self.driver.find_element_by_id(self.id_type() + "tv_chinese")
        return explain.text

    @teststep
    def sentence(self):
        """全英模式 页面内展示的句子"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "sentence").text
        return english


    @teststep
    def sentence_explain(self):
        """英汉模式 页面内展示的句子解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "sentence_explain").text
        return explain

    @teststep
    def star_button(self):
        """星标按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "iv_star")
        return ele

    @teststep
    def change_model_btn(self):
        """英汉切换按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'iv_rotate')
        return ele

    # =====  结果页定位元素  ======
    @teststep
    def study_sum(self):
        """学习统计"""
        ele = self.driver.find_element_by_id(self.id_type() + 'study_sum')
        return ele.text

    @teststep
    def get_start_sum(self):
        """星星标记个数"""
        return int(re.findall(r'\d+', self.study_sum())[1])

    @teststep
    def study_again(self):
        """再学一遍"""
        ele = self.driver.find_element_by_id(self.id_type() + 'study_again')
        return ele

    @teststep
    def study_star_again(self):
        """把标星的单词再练一遍"""
        ele = self.driver.find_element_by_id(self.id_type() + 'star_again')
        return ele

    @teststep
    def result_words(self):
        """结果页单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def word_voice(self, word):
        """单词左侧声音按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/preceding-sibling::android.widget.ImageView'
                                                '[contains(@resource-id,"{}iv_voice")]'.format(word, self.id_type()))
        return ele

    @teststep
    def word_explain(self, word):
        """单词对应的解释"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../following-sibling::android.widget.LinearLayout/'
                                                'android.widget.TextView'.format(word))
        return ele.text

    @teststep
    def word_star(self, word):
        """单词对应的星标按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../../following-sibling::android.widget.ImageView'
                                                .format(word))
        return ele

    @teststep
    def play_flash_card_game(self, half_exit=False):
        """闪卡的总体流程"""
        first_result = self.flash_card_operate(haex=half_exit)
        self.flash_card_result_operate(first_result[0], first_result[1])
        self.flash_card_operate(fq=2, star_list=first_result[1])
        if self.wait_check_flash_result_page():
            print(self.study_sum())
            self.click_back_up_button()

    @teststeps
    def flash_card_operate(self, fq=1, star_list=0, haex=False):
        """闪卡游戏过程"""
        star_words = [] if fq == 1 else star_list
        if self.wait_check_study_page():
            total_num = self.common.rest_bank_num()
            for i in range(total_num):
                if self.wait_check_study_page():
                    self.common.rate_judge(total_num, i)
                    self.common.judge_next_is_true_false('true')
                    self.click_voice()
                    word = self.word()
                    print('单词：', word)
                    if not self.wait_check_explain_page():     # 验证页面是否默认选择英汉模式
                        print('★★★ 未发现单词解释，页面没有默认选择英汉模式')
                    print('解释：', self.explain())          # 单词解释
                    print(self.sentence())                 # 句子
                    print(self.sentence_explain())         # 句子解释
                    print(self.author())                   # 推荐老师

                    self.change_model_btn().click()        # 切换全英模式
                    if self.wait_check_explain_page():     # 校验翻译是否出现
                        print('★★★切换至全英模式依然存在解释')
                    self.change_model_btn().click()       # 切换回英汉模式

                    if i == 2:
                        if haex:
                            self.click_back_up_button()
                            break

                    if fq == 1:
                        if i % 2 == 0:
                            self.star_button().click()
                            star_words.append(word)
                            print('加入标星单词')
                    else:
                        if GetAttribute().selected(self.star_button()) == 'true':
                            print('标星校验正确')
                        else:
                            print('★★★ 单词已标星但标星按钮未被选中')

                    print('-'*20, '\n')
                    self.common.next_btn().click()
            return total_num, star_words


    @teststep
    def flash_card_result_operate(self, total, star_words):
        """闪卡结果页面处理"""
        if self.wait_check_flash_result_page():
            print('完成学习！')
            summary = self.study_sum()
            print(summary)
            full_count = int(re.findall(r'\d+', summary)[0])    # 页面统计总个数
            star_count = self.get_start_sum()

            if full_count != total:
                print('★★★ 页面统计个数与做题个数不一致')

            if len(star_words) != star_count:
                print('★★★ 标星个数与页面统计个数不一致')

            self.cancel_or_add_star(total, star_words, cancel=True)
            if self.get_start_sum() != len(star_words):
                print('★★★ 单词标星取消，页面标星统计数未发生变化，与实际标星数不一致')

            self.study_star_again().click()
            if Toast().find_toast('没有标记★的内容'):
                print('没有标记★的内容')
            else:
                print('★★★ 未提示没有标星单词')

            self.cancel_or_add_star(total, star_words)
            self.study_star_again().click()


    @teststep
    def cancel_or_add_star(self, total, star_words, cancel=False):
        word_list = []
        while True:
            words = self.result_words()
            for i, w in enumerate(words):
                if w.text in word_list:
                    continue
                else:
                    if i == len(words) - 1:
                        self.screen_swipe_up(0.5, 0.8, 0.72)
                    result_word = w.text
                    word_list.append(result_word)
                    self.word_voice(result_word).click()
                    if cancel:
                        print('单词：', result_word, end='\t')
                        print('解释', self.word_explain(result_word))
                        if GetAttribute().selected(self.word_star(result_word)) == 'true':
                            self.word_star(result_word).click()
                            print('取消标星')
                            star_words.remove(result_word)
                        print('-' * 20, '\n')
                    else:
                        if i == 2 or i == 4:
                            print('单词：', result_word, end='\t')
                            self.word_star(result_word).click()
                            print('添加标星')
                            star_words.append(result_word)
                            print('-' * 20, '\n')

            if len(word_list) != total:
                self.screen_swipe_up(0.5, 0.8, 0.3, 1000)
            else:
                break


