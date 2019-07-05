# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/12 15:31
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class ListenSelectImg(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_listen_image_page(self):
        """听音选图页面检查点 以题目索引id作为依据"""
        locator = (By.ID, self.id_type() + "num")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def ques_index(self):
        """问题索引"""
        ele = self.driver.find_element_by_id(self.id_type() + 'num')
        return ele.text

    @teststep
    def question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sentence')
        return ele.text

    @teststep
    def images(self):
        """图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'img')
        return ele

    @teststep
    def voice_play_btn(self):
        """音频播放按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'iv_play')
        return ele

    @teststep
    def result_question(self):
        """结果页问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'text')
        return ele

    @teststep
    def result_ques_images(self, ques_text):
        """结果页图片"""
        ques_index = int(ques_text.split('.')[0]) - 1
        image_list = [x for x in self.images() if x.get_attribute('contentDescription').split('## ')[1].strip()
                      == str(ques_index)]
        return image_list

    @teststeps
    def listen_select_image_operate(self, fq, sec_answer, half_exit):
        """听音选图"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            if self.wait_check_listen_image_page():
                ques_index = self.ques_index()
                question = ques_index + '.' + self.question()
                print('问题：', question)
                self.common.rate_judge(total_num, i)
                if fq == 1:
                    random_index = random.randint(0, len(self.images()) - 1)
                    random_choice = self.images()[random_index]
                    choice_desc = random_choice.get_attribute('contentDescription')
                    print('选择答案：', choice_desc)
                    mine_answer[question] = choice_desc
                    random_choice.click()
                    time.sleep(1)
                else:
                    right_answer = sec_answer[question]
                    for x in self.images():
                        if x.get_attribute('contentDescription') == right_answer:
                            x.click()
                            time.sleep(1)
                            break
                    print('选择正确答案：', right_answer)

                timer.append(self.common.bank_time())
                print('-'*20, '\n')

                if i == 1:
                    if half_exit:
                        self.click_back_up_button()
                        break

                if i == total_num - 1:
                    if not self.common.wait_check_next_btn_page():
                        print('★★★ 未发现下一步按钮')
                    while True:
                        self.common.next_btn().click()
                        if ResultPage().wait_check_result_page():
                            break
                        else:
                            if Toast().find_toast('请听完音频，再提交答案'):
                                time.sleep(3)
                            else:
                                print('★★★ 未提示请听完音频')

        self.common.judge_timer(timer)
        done_answer = mine_answer if fq == 1 else sec_answer
        print('我的答案：', done_answer)
        return done_answer, total_num

    @teststeps
    def listen_select_image_result_operate(self, mine_answer):
        """听音选图结果页处理"""
        right_answer = {}
        right, wrong = [], []
        if ResultPage().wait_check_answer_page():
            self.voice_play_btn().click()
            banks = []
            while True:
                questions = self.result_question()
                for i, ques in enumerate(questions):
                    if ques.text in banks:
                        continue
                    else:
                        if i == len(questions) - 1:
                            self.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        banks.append(ques.text)
                        print('问题：', ques.text)
                        mine = mine_answer[ques.text]
                        print('我的选择：', mine)
                        result_images = self.result_ques_images(ques.text)
                        # print([x.get_attribute('contentDescription') for x in result_images])
                        for x in result_images:
                            desc = x.get_attribute('contentDescription')
                            if mine in desc:
                                if GetAttribute().selected(x) == 'false':
                                    print('★★★ 所选与页面展示的不一致')
                                if 'true' in desc:
                                    print('选择正确', mine)
                                    right.append(ques.text)
                                    right_answer[ques.text] = desc.split('##')[0].strip()
                                elif 'false' in desc:
                                    print('选择错误', end=' ')
                                    wrong.append(ques.text)
                            else:
                                if 'true' in desc:
                                    print('正确选项：', desc.split('##')[0].strip())
                                    right.append(ques.text)
                                    right_answer[ques.text] = desc.split('##')[0].strip()

                            print('-'*20, '\n')

                if len(banks) != len(mine_answer):
                    self.screen_swipe_up(0.5, 0.9, 0.5, 1000)
                else:
                    break
        self.click_back_up_button()
        print(right_answer)
        return wrong, right, right_answer







