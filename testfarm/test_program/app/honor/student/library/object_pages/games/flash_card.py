# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/12 8:24
# -------------------------------------------
import random
import re
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.utils.games_keyboard import Keyboard
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class FlashCard(BasePage):

    def __init__(self):
        self.common = CommonPage()

    # =========================== 学习模式 =========================

    @teststep
    def wait_check_study_page(self):
        """以“闪卡练习 -学习模式”的xpath-text为依据"""
        locator = (By.ID, self.id_type() + "iv_rotate")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
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
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def study_word(self):
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

    # ================================== 抄写模式 ====================================
    @teststep
    def wait_check_copy_page(self):
        """抄写模式页面检查点 以键盘id作为索引"""
        locator = (By.ID, self.id_type() + "keyboard")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def copy_word(self):
        """抄写页面单词"""
        ele = self.driver.find_element_by_id('{}tv_word'.format(self.id_type()))
        return ele.text

    @teststep
    def copy_explain(self):
        """抄写模式单词解释"""
        ele = self.driver.find_element_by_id('{}chinese'.format(self.id_type()))
        return ele.text

    @teststep
    def copy_input(self):
        """抄写模式输入答案"""
        ele = self.driver.find_element_by_id('{}english'.format(self.id_type()))
        return ele

    @teststep
    def keyboard_view(self):
        """小键盘 整体view元素"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "keyboard")
        return ele

    @teststep
    def play_flash_game(self):
        """闪卡的总体流程"""
        if self.wait_check_study_page():
            first_result = self.flash_study_operate()
            self.flash_card_result_operate(first_result[0], first_result[1])
            self.flash_study_operate(fq=2, star_list=first_result[1])
        elif self.wait_check_copy_page():
            first_result = self.flash_copy_operate()
            self.flash_card_result_operate(first_result[0], first_result[1])
            self.flash_copy_operate(fq=2, star_list=first_result[1])

        if self.wait_check_flash_result_page():
            print(self.study_sum())
            self.click_back_up_button()

    @teststeps
    def flash_study_operate(self, fq=1, star_list=0):
        """闪卡练习学习模式"""
        star_words = [] if fq == 1 else star_list
        if self.wait_check_study_page():
            total_num = self.common.rest_bank_num()
            for i in range(total_num):
                if self.wait_check_study_page():
                    self.common.rate_judge(total_num, i)  # 待完成数校验
                    self.common.judge_next_is_true_false('true')  # 下一步按钮状态检验
                    self.click_voice()
                    word = self.study_word()
                    print('单词：', word)
                    if not self.wait_check_explain_page():  # 验证页面是否默认选择英汉模式
                        print('★★★ 未发现单词解释，页面没有默认选择英汉模式')
                    print('解释：', self.explain())  # 单词解释
                    print(self.sentence())  # 句子
                    print(self.sentence_explain())  # 句子解释
                    print(self.author())  # 推荐老师

                    self.change_model_btn().click()  # 切换全英模式
                    if self.wait_check_explain_page():  # 校验翻译是否出现
                        print('★★★切换至全英模式依然存在解释')
                    self.change_model_btn().click()  # 切换回英汉模式

                    if i % 2 == 0:                   # 第一次，部分单词点击标星按钮
                        if fq == 1:
                            self.star_button().click()
                            star_words.append(word)
                            print('加入标星单词')
                        else:
                            if GetAttribute().selected(self.star_button()) == 'true':
                                print('标星校验正确')
                            else:
                                print('★★★ 单词已标星但标星按钮未被选中')

                    print('-' * 20, '\n')
                    self.common.next_btn().click()
            return total_num, star_words

    @teststeps
    def flash_copy_operate(self, fq=1, star_list=0, haex=False):
        """闪卡练习抄写模式"""
        star_words = [] if fq == 1 else star_list
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            self.click_voice()
            self.common.rate_judge(total_num, i)
            copy_word = self.copy_word()
            print('单词：', copy_word)

            if i % 2 == 0:                             # 奇数题
                if fq == 1:                            # 若为第一次
                    self.star_button().click()         # 标星
                    star_words.append(copy_word)
                    print('加入标星单词')
                else:                                  # 若为第二次 校验是否被标星
                    if GetAttribute().selected(self.star_button()) == 'true':
                        print('标星校验正确')
                    else:
                        print('★★★ 单词已标星但标星按钮未被选中')

            self.copy_input().click()
            if i == 1:
                if haex:
                    self.click_back_up_button()
                    break

                random_str = random.sample(string.ascii_lowercase, 4)       # 随机输入错误单词，
                for j, s in enumerate(random_str):
                    self.common.keyboard_operate(j, s)
                print('输入单词：', ''.join(random_str))
                time.sleep(2)

                if self.copy_word() != copy_word:                           # 验证是否跳转到下一题
                    print('★★★ 输入错误单词可以进入下一题')

                for x in range(4):                                          # 清除输入的单词
                    Keyboard().games_keyboard('backspace')
                time.sleep(1)

            for j, s in enumerate(list(copy_word)):                               # 输入抄写单词
                self.common.keyboard_operate(j, s)
            time.sleep(2)
            print('-'*30, '\n')
        return total_num, star_words

    @teststeps
    def flash_card_result_operate(self, total, star_words):
        """闪卡结果页面处理"""
        if self.wait_check_flash_result_page():
            print('完成学习！')
            summary = self.study_sum()
            print(summary)
            full_count = int(re.findall(r'\d+', summary)[0])  # 页面统计总个数
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
                print('没有标记★的内容\n')
            else:
                print('★★★ 未提示没有标星单词')

            self.cancel_or_add_star(total, star_words)
            self.study_star_again().click()

    @teststep
    def cancel_or_add_star(self, total, star_words, cancel=False):
        """添加或取消标星"""
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
