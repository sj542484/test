# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/12 15:31
# -------------------------------------------
import random
import time

from app.honor.student.games.choice_images import ListenSelectImageGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class ListenSelectImg(ListenSelectImageGame):

    def __init__(self):
        self.public = LibraryPubicPage()

    @teststep
    def result_images(self):
        """结果页图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'result')
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
        image_list = [x for x in self.result_images() if x.get_attribute('contentDescription').split('## ')[1].strip()
                      == str(ques_index)]
        return image_list

    @teststeps
    def listen_select_image_operate(self, fq, sec_answer):
        """听音选图"""
        timer = []
        mine_answer = {}
        total_num = self.public.rest_bank_num()
        for i in range(total_num):
            if self.wait_check_listen_image_page():
                ques_index = self.ques_index()
                question = ques_index + '.' + self.listen_question()
                print('问题：', question)
                self.public.rate_judge(total_num, i)
                if fq == 1:
                    random_index = random.randint(0, len(self.image_options()) - 1)
                    random_choice = self.image_options()[random_index]
                    choice_desc = random_choice.get_attribute('contentDescription')
                    print('选择答案：', choice_desc)
                    mine_answer[question] = choice_desc
                    random_choice.click()
                    time.sleep(1)
                else:
                    right_answer = sec_answer[question]
                    for x in self.image_options():
                        if x.get_attribute('contentDescription') == right_answer:
                            x.click()
                            time.sleep(1)
                            break
                    print('选择正确答案：', right_answer)

                timer.append(self.public.bank_time())
                print('-'*20, '\n')

                if i == total_num - 1:
                    if not self.public.wait_check_next_btn_page():
                        print('★★★ 未发现下一步按钮')
                    while True:
                        self.fab_commit_btn().click()
                        if Toast().find_toast('请听完音频，再提交答案'):
                            time.sleep(3)
                        else:
                            break

        self.public.judge_timer(timer)
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







