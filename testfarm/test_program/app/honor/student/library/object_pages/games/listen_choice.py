# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/11 13:54
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.cloze import Cloze
from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class ListenChoice(BasePage):
    """听力选择"""

    def __init__(self):
        self.common = CommonPage()
        self.cloze = Cloze()

    @teststep
    def wait_check_select_char_page(self):
        """听力选择页面 以选项id作为依据"""
        locator = (By.ID, self.id_type() + "tv_char")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_red_hint_page(self):
        """红色提示检查点"""
        locator = (By.ID, self.id_type() + "tv_hint")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_listen_text_page(self):
        """听力原文页面检查点"""
        locator = (By.ID, self.id_type() + "fs_content")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def voice_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id('{}fab_audio'.format(self.id_type()))
        return ele

    @teststep
    def hint(self):
        """红色提示"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_hint')
        return ele.text

    @teststep
    def listen_text(self):
        """听力原文"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fs_content')
        return ele.text

    @teststep
    def voice_play_btn(self):
        """听力播放按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'iv_play')
        return ele

    @teststep
    def submit_btn(self):
        """下一步提交按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_submit')
        return ele

    @teststep
    def judge_voice_btn_status(self, var):
        """判断声音按钮状态"""
        if GetAttribute().enabled(self.voice_button()) != var:
            print('★★★ 声音按钮状态错误', var)

    @teststeps
    def listen_choice_operate(self, fq, sec_answer, half_exit):
        """听力选择游戏过程"""
        timer = []
        mine_answer = {}
        if self.wait_check_select_char_page():   # 点击喇叭验证红色字体是否消失
            print(self.hint())
            self.judge_voice_btn_status('true')
            self.voice_button().click()
            if self.wait_check_red_hint_page():
                print('★★★ 点击喇叭后,红色提示未消失')

            self.judge_voice_btn_status('false')
            total_num = self.common.rest_bank_num()   # 总题数
            ques_info = []            # 用以存储题目,滑动过滤 中断循环
            timer = []
            flag = False
            while True:
                if flag or self.common.rest_bank_num() == 0:
                    break
                question = self.cloze.result_question()
                for i, ques in enumerate(question):
                    if ques.text in ques_info:
                        continue
                    else:
                        self.common.rate_judge(total_num, len(timer))
                        ques_text = ques.text
                        print('问题：', ques_text)
                        ques_info.append(ques_text)
                        if i == len(question) - 1:
                            self.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        for x, opt in enumerate(self.cloze.result_opt_text(ques_text)):   # 打印输出题目及选项
                            print(self.cloze.result_opt_char(ques_text)[x].text, opt.text)

                        if fq == 1:    # 第一轮 随机选择选项
                            random_index = random.randint(0, len(self.cloze.result_opt_char(ques_text)) - 1)
                            random_opt = self.cloze.result_opt_text(ques_text)[random_index].text
                            mine_answer[ques_text] = random_opt
                            print('我的答案：', random_opt)
                            self.cloze.result_opt_char(ques_text)[random_index].click()
                        else:       # 第二轮选择正确选项
                            for x, opt in enumerate(self.cloze.result_opt_text(ques_text)):
                                if opt.text == sec_answer[ques_text]:
                                    self.cloze.result_opt_char(ques_text)[x].click()
                                    break
                            print('我的答案：', sec_answer[ques_text])

                    print('-'*20, '\n')
                    timer.append(self.common.bank_time())  # 添加学生
                    if i == 2:
                        if half_exit:
                            self.click_back_up_button()
                            flag = True
                            break
                self.screen_swipe_up(0.5, 0.9, 0.3, 1000)    # 滑动

            self.common.judge_timer(timer)
            while True:
                if GetAttribute().enabled(self.submit_btn()) == 'true':
                    self.submit_btn().click()
                    break
                else:
                    time.sleep(3)
            answer = mine_answer if fq == 1 else sec_answer
            print(answer)
            return answer, total_num

    @teststeps
    def listen_choice_result_operate(self, mine_answer):
        """听力选择结果页处理"""
        right_answer = {}
        right, wrong = [], []
        if ResultPage().wait_check_answer_page():
            self.voice_play_btn().click()
            if self.wait_check_listen_text_page() and self.listen_text() != '':
                listen_text = self.listen_text()
                print(listen_text)
                while True:
                    if len(self.cloze.result_question()) == 2:
                        break
                    else:
                        self.screen_swipe_up(0.5, 0.8, 0.6, 1000)
            ques_info = []
            while True:
                questions = self.cloze.result_question()
                for x, ques in enumerate(questions):
                    if ques.text in ques_info:
                        continue
                    else:
                        print('问题：', ques.text)
                        ques_info.append(ques.text)
                        if x == len(questions) - 1:
                            self.screen_swipe_up(0.5, 0.8, 0.62, 1000)
                        for y, opt in enumerate(self.cloze.result_opt_text(ques.text)):
                            char = self.cloze.result_opt_char(ques.text)[y]
                            if opt.text == mine_answer[ques.text]:
                                if char.get_attribute('contentDescription') == 'right':
                                    right.append(opt.text)
                                    right_answer[ques.text] = opt.text
                                    print('答案正确', opt.text)
                                elif char.get_attribute('contentDescription') == 'error':
                                    wrong.append(opt.text)
                                    print('答案错误', opt.text)
                            else:
                                if char.get_attribute('contentDescription') == 'right':
                                    right_answer[ques.text] = opt.text
                                    print('正确答案：', opt.text)

                        print('-'*20, '\n')
                if len(ques_info) != len(mine_answer):
                    self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
                else:
                    break

            print('结果页答案:', right_answer)
            self.click_back_up_button()
            return wrong, right, right_answer