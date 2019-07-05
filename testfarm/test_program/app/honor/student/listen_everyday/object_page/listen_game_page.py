# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 10:59
# -------------------------------------------
import random
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from testfarm.test_program.app.honor.student.listen_everyday.object_page.listen_result_page import ListenResultPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.toast_find import Toast


class ListenGamePage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.listen = ListenHomePage()

    @teststep
    def wait_check_gaming_page(self):
        """以游戏界面计时的id作为根据"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"待完成:")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_image_page(self):
        """听音选图 -- 以题号的id作为根据"""
        locator = (By.ID, self.id_type() + 'num')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_rich_page(self):
        locator = (By.ID, self.id_type() + 'rich')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_next_button_page(self):
        """以下一步按钮的id作为根据"""
        locator = (By.ID, self.id_type() + 'fab_next')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_next_submit_page(self):
        """以下一步按钮的id作为根据"""
        locator = (By.ID, self.id_type() + 'fab_submit')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_right_answer(self):
        locator = (By.ID, self.id_type() + 'tv_right')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_button_page(self):
        locator = (By.ID, self.id_type() + 'clear')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_red_hint_page(self):
        locator = (By.ID, self.id_type() + 'tv_hint')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_choice_question_page(self):
        locator = (By.ID, self.id_type() + 'question')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def game_num(self):
        """游戏剩余个数"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rate')
        return ele

    @teststep
    def game_use_time(self):
        """游戏使用时间"""
        ele = self.driver.find_element_by_id(self.id_type() + 'time')
        return ele

    @teststep
    def images(self):
        """图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + "img")
        return ele

    @teststep
    def question(self):
        """题目"""
        ele = self.driver.find_element_by_id(self.id_type() + "sentence")
        return ele

    @teststep
    def question_index(self):
        """题号"""
        ele = self.driver.find_element_by_id(self.id_type() + "num")
        return ele

    # 听音连句
    @teststep
    def need_input_word(self):
        """需要填补的空格"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rich')
        word_num = len(ele.text.split(' '))
        return word_num

    @teststep
    def finish_word(self):
        """填补后的单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rich')
        return ele

    @teststep
    def clear_button(self):
        """清除按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'clear')
        return ele

    @teststep
    def audio_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'play_voice')
        return ele

    @teststep
    def split_sentence_word(self):
        """候选单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + "text")
        word_list = [i for i in ele if i.text != '']
        return word_list

    @teststep
    def correct_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_right')
        return ele

    @teststep
    def red_hint(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_hint')
        return ele

    @teststep
    def play_voice(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_audio')
        return ele

    @teststep
    def choice_question(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'question')
        return ele

    @teststep
    def choice_char(self, question):
        ele = self.driver.\
                find_elements_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/following-sibling::'
                                       'android.widget.LinearLayout/android.widget.LinearLayout/'
                                       'android.widget.LinearLayout/android.widget.TextView[contains(@resource-id,'
                                       '"{1}tv_char")]'.format(question, self.id_type()))
        return ele

    @teststep
    def choice_item(self, question):
        ele = self.driver.\
            find_elements_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/following-sibling::'
                                   'android.widget.LinearLayout/android.widget.LinearLayout/'
                                   'android.widget.LinearLayout/android.widget.TextView[contains(@resource-id,'
                                   '"{1}tv_item")]'.format(question, self.id_type()))

        return ele

    @teststep
    def text_views(self):
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        text_list = [x for x in ele if x.text != '' or x.text is not None]
        return text_list

    @teststep
    def last_text(self):
        all_text = self.text_views()
        return all_text[-1].get_attribute('resourceId')

    @teststep
    def next_button(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_submit')
        return ele

    @teststep
    def play_listen_game_process(self):
        result = 0
        if self.wait_check_image_page():
            result = self.play_listen_identity_image_game()

        elif self.wait_check_rich_page():
            result = self.play_listen_form_sentence()

        elif self.wait_check_red_hint_page():
            result = self.play_listen_choice()

        ListenResultPage().result_page_operate(result[0], result[1])

        self.home.click_back_up_button()
        if ListenResultPage().wait_check_result_page():
            self.home.click_back_up_button()

    @teststep
    def check_game_num_and_time(self, count_time, total, i):
        """时间和个数校验方法"""
        game_num = self.game_num().text
        rest_time = self.game_use_time().text
        print('剩余题目：', game_num)
        print('已用时间：', rest_time)
        if count_time[0] != rest_time:
            count_time[0] = rest_time
        else:
            print('★★★ Error-- 时间未发生变化', rest_time)

        if int(game_num) != total - i:
            print('★★★ Error-- 剩余题目个数不正确', game_num)

    # ================================= 听音选图 ========================================

    @teststep
    def play_listen_identity_image_game(self):
        """听音选图游戏过程"""
        print('----- < 听音选图 > -----\n')
        total = int(self.game_num().text)
        count_time = ['']
        tips = []
        for i in range(int(total)):
            self.check_game_num_and_time(count_time, total, i)   # 校验剩余个数和时间

            question = self.question().text
            question_index = self.question_index().text
            if str(i+1) != question_index:
                print('★★★ Error-- 题号未发生改变')

            images = self.images()
            random_index = random.randint(0, len(images)-1)   # 图片随机选择
            print(question_index, question)
            print("选择：第"+str(random_index + 1)+"张图")
            images[random_index].click()
            tips.append((question, random_index, len(images)))
            time.sleep(3)

            if i == int(total) - 1:
                # 最后一道题时，若听力未结束，会提示请听完音频，则继续等待并不断点击
                while True:
                    if self.wait_check_gaming_page():
                        if self.wait_check_next_button_page():
                            self.listen.next_button().click()
                            if Toast().find_toast('请听完音频，再提交答案'):
                                print('请听完音频，再提交答案')
                                time.sleep(5)
                        else:
                            time.sleep(5)
                    elif ListenResultPage().wait_check_result_page():
                        print('进入结果页')
                        break
            print('-'*30, '\n')
        return total, tips

    # ================================= 听音连句 ========================================

    @teststeps
    def play_listen_form_sentence(self):
        print('----- < 听音连句 > -----\n')
        total = int(self.game_num().text)
        count_time = ['']
        answer = []
        for i in range(int(total)):
            if self.wait_check_rich_page():    # 没点击任何单词之前，清除按钮不可点
                if self.clear_button().get_attribute('enabled') == 'true':
                    print('★★★ Error-- 尚未选择,清除图标已激活')

                if self.audio_button().get_attribute("enabled") == 'false':
                    print('★★★ Error-- 声音按钮不可点击')

                self.check_game_num_and_time(count_time, total, i)
                need_word_num = self.need_input_word()

                for k in range(need_word_num):
                    split_word = self.split_sentence_word()

                    if len(split_word) == 0:
                        break
                    index = random.randint(0, len(split_word)-1)
                    split_word[index].click()    # 对下面的单词随机点击， 点击后清除图标可点击

                    if self.clear_button().get_attribute('enabled') == 'false':
                        print('★★★ Error-- 已选择单词,清除图标未激活')
                    if k == need_word_num - 1:  # 句子填补完成后， 提交按钮可点击
                        if self.listen.next_button_status_judge('false'):
                            print('★★★ Error-- 句子已连成,提交按钮未激活')

                if self.listen.next_button().get_attribute('enabled') == 'true':
                    self.listen.next_button().click()
                else:
                    print('★★★ Error-- 下一步按钮状态错误')

                if not self.wait_check_right_answer():
                    print('★★★ Error--未发现正确答案')
                else:
                    if self.wait_check_clear_button_page():
                        print('★★★ Error-- 提交后页面清除按钮依然存在')
                    finish_word = self.finish_word().get_attribute('contentDescription')
                    mine_answer = re.findall(r'\[(.*?)\]', finish_word)[0].replace(",", '')
                    print('我的答案:', mine_answer)
                    answer.append(mine_answer)
                    print(self.correct_answer().text)
                    self.listen.next_button_operate('true')  # 进入下一题
                    print('-'*30, '\n')
        return total, answer

    # ================================= 听后选择 ========================================

    @teststep
    def play_listen_choice(self):
        print('----- < 听音选择 > -----\n')
        total = int(self.game_num().text)
        count_time = ['']

        if not self.wait_check_red_hint_page():
            print('★★★ Error-- 红色提示未出现')

        self.play_voice().click()

        if self.wait_check_red_hint_page():
            print('★★★ Error-- 播放听力后，提示未消失')

        if self.play_voice().get_attribute('enabled') == 'true':
            print('★★★ Error-- 点击播放按钮后，图标未置灰')

        tips = []
        while True:
            if len(tips) != total:
                questions = self.choice_question()
                question_text = [x.text for x in questions]
                tips_ques = tips if len(tips) == 0 else [x[0] for x in tips]
                quest_list = [x for x in question_text if x not in tips_ques]

                for i in range(len(quest_list)):
                    if i != len(quest_list)-1:
                        self.click_operate(quest_list[i], count_time, total, tips)
                    else:
                        self.home.screen_swipe_up(0.5, 0.9, 0.6, 1000)
                        self.click_operate(quest_list[-1], count_time, total, tips)
                        self.home.screen_swipe_down(0.5, 0.6, 0.9, 1000)

                self.home.screen_swipe_down(0.5, 0.9, 0.2, 2000)
            else:
                if self.wait_check_next_submit_page():
                    if self.next_button().get_attribute('enabled') == 'true':
                        self.next_button().click()
                        break

                time.sleep(3)
        return total, tips

    @teststep
    def click_operate(self, question, count_time, total, tips):
        self.check_game_num_and_time(count_time, total, len(tips))
        print(question)
        char = self.choice_char(question)
        item = self.choice_item(question)
        for i in range(len(char)):
            print(char[i].text, ' ', item[i].text)
        index = random.randint(0, len(char) - 1)
        tips.append((question, char[index].text))
        char[index].click()
        print('选择答案：', char[index].text)
        print('-'*30, '\n')

