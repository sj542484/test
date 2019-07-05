# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 16:45
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.toast_find import Toast


class ListenResultPage(BasePage):
    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_result_page(self):
        """结果检查点 以打卡的id作为依据"""
        locator = (By.ID, '{}share'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_answer_detail_page(self):
        """查看结果页页面检查点--带有播放进度的 以播放按钮的id作为依据"""
        locator = (By.ID, '{}iv_play'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_error_hint(self):
        """结果页红色错误提示 以id作为依据"""
        locator = (By.ID, '{}error_hint'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_punch_page(self):
        """打卡分享页， 以分享图片的id作为依据"""
        locator = (By.ID, '{}share_img'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_wechat_login_page(self):
        """微信登录页 以题目的text作为依据"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"登录微信")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_audio_bar_page(self):
        """音频播放按钮的id"""
        locator = (By.ID, '{}seek_bar'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_img_result_page(self):
        """听音选题结果页 -- 以图片的id作为依据"""
        locator = (By.ID, '{}img'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_listen_choice_question_page(self):
        """听后选择结果页 -- 以选项的id作为依据"""
        locator = (By.ID, '{}tv_char'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_sentence_speak_page(self):
        locator = (By.ID, '{}iv_speak'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_mine_answer_icon_page(self, right_answer):
        """连词成句结果页 --正误图标的检查点"""
        try:
            self.mine_right_wrong_icon(right_answer)
            return True
        except:
            return False

    @teststep
    def wait_check_listen_text(self):
        locator = (By.ID, '{}fs_content'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def text_view(self):
        ele = self.driver.find_elements_by_class_name("android.widget.TextView")
        return ele

    @teststep
    def last_text_attr(self):
        all_text = [x for x in self.text_view() if x.text != '' and x.text is not None]
        last_text_attr = all_text[-1].get_attribute('resourceId')
        return last_text_attr

    @teststep
    def today_excise_time(self):
        """今日已练时间"""
        ele = self.driver.find_element_by_id("{}today_minute".format(self.id_type()))
        return ele.text

    @teststep
    def excise_date(self):
        """练习日期"""
        ele = self.driver.find_element_by_id('{}date'.format(self.id_type()))
        return ele.text

    @teststep
    def excise_correct_rate(self):
        """正确率"""
        ele = self.driver.find_element_by_id("{}right_rate".format(self.id_type()))
        return ele.text

    @teststep
    def error_hint(self):
        """正确率不足60%提示"""
        ele = self.driver.find_element_by_id('{}error_hint'.format(self.id_type()))
        return ele

    @teststep
    def punch_button(self):
        """打卡"""
        ele = self.driver.find_element_by_id("{}share".format(self.id_type()))
        return ele

    @teststep
    def check_answer_button(self):
        """查看答案"""
        ele = self.driver.find_element_by_id("{}detail".format(self.id_type()))
        return ele

    @teststep
    def redo_button(self):
        """重练此题"""
        ele = self.driver.find_element_by_id("{}again".format(self.id_type()))
        return ele

    @teststep
    def rank_button(self):
        """排行榜"""
        ele = self.driver.find_element_by_id('{}rank'.format(self.id_type()))
        return ele

    @teststep
    def wechat_button(self):
        """微信"""
        ele = self.driver.find_element_by_id("{}weixin".format(self.id_type()))
        return ele

    @teststep
    def wechat_friend(self):
        """微信朋友圈"""
        ele = self.driver.find_element_by_id('{}weixin_friends'.format(self.id_type()))
        return ele

    @teststep
    def save_img(self):
        """保存图片"""
        ele = self.driver.find_element_by_id('{}save_img'.format(self.id_type()))
        return ele

    @teststep
    def quit_login_wechat(self):
        """退出微信登录页面"""
        ele = self.driver.find_element_by_id('com.tencent.mm:id/jc')
        return ele

    @teststep
    def audio_play(self):
        ele = self.driver.find_element_by_id("{}iv_play".format(self.id_type()))
        return ele

    @teststep
    def audio_time(self):
        ele = self.driver.find_element_by_id('{}tv_progress'.format(self.id_type()))
        return ele

    @teststep
    def listen_img_question_text(self):
        ele = self.driver.find_elements_by_id('{}text'.format(self.id_type()))
        return ele

    @teststep
    def listen_choice_question(self):
        ele = self.driver.find_elements_by_id('{}question'.format(self.id_type()))
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
        ele = self.driver. \
            find_elements_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/following-sibling::'
                                   'android.widget.LinearLayout/android.widget.LinearLayout/'
                                   'android.widget.LinearLayout/android.widget.TextView[contains(@resource-id,'
                                   '"{1}tv_item")]'.format(question, self.id_type()))

        return ele

    @teststep
    def selected_img_options(self, question):
        ele = self.driver.find_elements_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/../'
                                                 'following-sibling::android.widget.RelativeLayout/'
                                                 'android.widget.ImageView[contains(@resource-id,'
                                                 '"{1}img")]'.format(question, self.id_type()))
        return ele

    @teststeps
    def sentence_right_answer(self):
        ele = self.driver.find_elements_by_id('{}tv_right'.format(self.id_type()))
        return ele

    @teststeps
    def sentence_mine_answer(self, right_answer):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{0}")]/../'
                                                'following-sibling::android.widget.TextView[contains(@resource-id,'
                                                '"{1}tv_mine")]'.format(right_answer, self.id_type()))
        return ele

    @teststeps
    def sentence_explain(self, right_answer):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{0}")]/../'
                                                'following-sibling::android.widget.TextView[contains(@resource-id,'
                                                '"{1}tv_explain")]'.format(right_answer, self.id_type()))
        return ele

    @teststeps
    def sentence_speak(self, right_answer):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{}")]/preceding-sibling::'
                                                'android.widget.ImageView'.format(right_answer))
        return ele

    @teststeps
    def mine_right_wrong_icon(self, right_answer):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{}")]/../../'
                                                'following-sibling::android.widget.ImageView'.format(right_answer))
        return ele

    @teststep
    def listen_text(self):
        ele = self.driver.find_element_by_id('{}fs_content'.format(self.id_type()))
        return ele

    @teststeps
    def result_page_operate(self, total, question_info):
        if self.wait_check_result_page():
            print('----- < 结果页 > -----\n')
            today_excise = self.today_excise_time()
            date = self.excise_date()
            rate = self.excise_correct_rate()
            print(today_excise, '\n', date, '\n', rate, '\n')
            if self.wait_check_error_hint():
                print(self.error_hint().text, '\n')
            self.punch_button().click()
            # if self.wait_check_punch_page():
            #     self.home.back_up_button()
            self.share_page_operate()
            if self.wait_check_result_page():
                self.check_answer_button().click()
                self.answer_page_operate(total, question_info)

    @teststeps
    def share_page_operate(self):
        """分享页处理"""
        if self.wait_check_punch_page():
            wechat = self.wechat_button()
            friend = self.wechat_friend()
            save_img = self.save_img()

            print(wechat.text)
            wechat.click()
            if self.wait_check_wechat_login_page():
                print('微信登录界面\n')
                self.quit_login_wechat().click()
                if self.wait_check_punch_page():
                    pass

            print(friend.text)
            friend.click()
            if self.wait_check_wechat_login_page():
                print('微信登录界面\n')
                self.quit_login_wechat().click()
                if self.wait_check_punch_page():
                    pass

            print(save_img.text)
            save_img.click()
            if Toast().find_toast('已保存到本地'):
                print('已保存到本地', '\n')

        self.home.click_back_up_button()

    @teststeps
    def answer_page_operate(self, total, question_info):
        if self.wait_check_audio_bar_page():
            self.audio_play().click()
            if self.audio_time().text == '00:00/00:00':
                print("★★★ Error-- 点击播放按钮，时间未发生变化")

            if self.wait_check_img_result_page():
                print('----- < 听音选图答案详情页 > -----', '\n')
                self.listen_img_answer_page_operate(total, question_info)

            elif self.wait_check_listen_text():
                print(self.listen_text().text)
                while True:
                    if self.last_text_attr() == '{}tv_item'.format(self.id_type()):
                        break
                    else:
                        self.home.screen_swipe_up(0.5, 0.6, 0.5, 1000)
                self.listen_choice_answer_page_operate(total, question_info)

            elif self.wait_check_listen_choice_question_page():
                print('----- < 听后选择答案详情页 > -----', '\n')
                self.listen_choice_answer_page_operate(total, question_info)

        elif self.wait_sentence_speak_page():
            print('----- < 听音连句答案详情页 > -----', '\n')
            self.listen_form_sentence_answer_page_operate(total, question_info)

    @teststeps
    def listen_img_answer_page_operate(self, total, question_info):
        tips = []
        while True:
            questions = self.listen_img_question_text()
            question_num = range(1, len(questions)) if questions[0].text in tips else range(0, len(questions))
            for i in question_num:
                if i != len(questions) - 1:
                    self.check_selected_img(questions[i].text, question_info[len(tips)], tips)
                else:
                    self.home.screen_swipe_up(0.5, 0.9, 0.55, 1500)
                    self.check_selected_img(questions[-1].text, question_info[len(tips)], tips)
                    self.home.screen_swipe_down(0.5, 0.55, 0.9, 1500)

            if len(tips) != total:
                self.screen_swipe_down(0.5, 0.9, 0.3, 1500)
            else:
                break

    @teststeps
    def check_selected_img(self, question, ques_info, tips):
        img_options = self.selected_img_options(question)
        option_list = img_options[:ques_info[2]]
        selected_index = [x for x in range(len(option_list)) if option_list[x].get_attribute('selected') == 'true']
        if len(selected_index) != 1:
            print("★★★ Error--所选个数并非一个")
        else:
            if selected_index[0] != ques_info[1]:
                print("★★★ Error--所选答案与已选答案不一致", selected_index[0])
            print(question)
            print('所选答案为:', selected_index[0], '核实正确')
            tips.append(question)
            print('-'*30, '\n')

    @teststeps
    def listen_choice_answer_page_operate(self, total, question_info):
        tips = []
        while True:
            questions = self.listen_choice_question()
            question_text = [x.text for x in questions]
            tips_ques = tips if len(tips) == 0 else [x for x in tips]
            quest_list = [x for x in question_text if x not in tips_ques]
            for i in range(len(quest_list)):
                if i != len(quest_list) - 1:
                    self.check_selected_choice(quest_list[i], question_info[len(tips)], tips)
                else:
                    self.home.screen_swipe_down(0.5, 0.9, 0.55, 1500)
                    self.check_selected_choice(quest_list[-1], question_info[len(tips)], tips)
                    self.home.screen_swipe_down(0.5, 0.55, 0.9, 1500)

            if len(tips) != total:
                self.screen_swipe_down(0.5, 0.9, 0.3, 1500)
            else:
                break

    @teststeps
    def check_selected_choice(self, question, ques_info, tips):
        char = self.choice_char(question)
        item = self.choice_item(question)
        print(question)
        right_char = []
        wrong_char = []
        for i in range(len(char)):
            if char[i].get_attribute('contentDescription') == 'right':
                right_char.append(char[i].text)
            elif char[i].get_attribute('contentDescription') == 'error':
                wrong_char.append(char[i].text)

            print(char[i].text, ' ', item[i].text)

        if len(wrong_char) > 1:
            print('★★★ Error--所选答案非一个')
        else:
            if len(wrong_char) == 0:
                print("我的答案:", right_char[0])
                print('正确答案:', right_char[0])
            else:
                if len(right_char) == 0:
                    print('★★★ Error-- 未发现正确答案')
                else:
                    print('我的答案:', wrong_char[0])
                    print('正确答案:', right_char[0])

            tips.append(question)
            print('-' * 30, '\n')

    @teststeps
    def listen_form_sentence_answer_page_operate(self, total, question_info):
        tips = []
        while True:
            right_answers = self.sentence_right_answer()
            question_num = range(1, len(right_answers)) if right_answers[0].text in tips else range(0, len(right_answers))
            for i in question_num:
                if i != len(right_answers) - 1:
                    self.check_sentence_answer_operate(right_answers[i].text, question_info[len(tips)], tips)
                else:
                    self.home.screen_swipe_down(0.5, 0.9, 0.6, 1500)
                    self.check_sentence_answer_operate(right_answers[-1].text, question_info[len(tips)], tips)
                    self.home.screen_swipe_down(0.5, 0.6, 0.9, 1500)

            if len(tips) != total:
                self.screen_swipe_down(0.5, 0.9, 0.3, 1500)
            else:
                break

    @teststeps
    def check_sentence_answer_operate(self, right_answer, answer, tips):
        speak = self.sentence_speak(right_answer)
        mine_answer = self.sentence_mine_answer(right_answer)
        explain = self.sentence_explain(right_answer)

        speak.click()
        time.sleep(2)

        if not self.wait_check_mine_answer_icon_page(right_answer):
            print('★★★ Error-- 答案中未出现正确与错误图标')

        sentence = mine_answer.text.split(': ')[1].strip()
        print(list(sentence))
        print(list(answer))
        if sentence != answer:
            print('★★★ Error-- 所填答案与结果不一致', mine_answer.text)

        tips.append(right_answer)
        print(right_answer)
        print(mine_answer.text)
        print(explain.text)
        print('-'*30, '\n')
