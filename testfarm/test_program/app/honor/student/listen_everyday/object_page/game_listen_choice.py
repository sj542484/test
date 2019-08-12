#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/5 20:04
# -----------------------------------------
import random
import time

from app.honor.student.library.object_pages.games.listen_choice import ListenChoice
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep, teststeps


class ListenChoicePage(ListenChoice):

    @teststeps
    def play_listen_choice_game(self):
        mine_answer = {}
        if self.wait_check_listen_select_page():  # 点击喇叭验证红色字体是否消失
            print(self.red_hint())
            self.next_btn_judge('true', self.voice_button)
            self.voice_button().click()
            if self.wait_check_red_hint_page():
                print('★★★ 点击喇叭后,红色提示未消失')

            self.next_btn_judge('false', self.voice_button)
            total_num = self.common.rest_bank_num()  # 总题数
            ques_info = []  # 用以存储题目,滑动过滤 中断循环
            timer = []
            flag = False
            scale_info = self.get_ques_opt_scale()
            while True:
                if flag or self.common.rest_bank_num() == 0:
                    break
                question = self.common.result_question()
                last_text_attr = self.get_last_text_id()
                for i, ques in enumerate(question):
                    if ques.text in ques_info:
                        continue
                    else:
                        self.common.rate_judge(total_num, len(timer))
                        if i == len(question) - 1:
                            if last_text_attr == 'ques':
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[0], 1000)
                            else:
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[1], 1000)

                        ques_text = ques.text
                        print('问题：', ques_text)
                        ques_info.append(ques_text)
                        for x, opt in enumerate(self.common.result_opt_text(ques_text)):  # 打印输出题目及选项
                            print(self.common.result_opt_char(ques_text)[x].text, opt.text)

                        random_index = random.randint(0, len(self.common.result_opt_char(ques_text)) - 1)
                        random_opt = self.common.result_opt_text(ques_text)[random_index].text
                        mine_answer[ques_text] = random_opt
                        print('我的答案：', random_opt)
                        self.common.result_opt_char(ques_text)[random_index].click()
                        print('-' * 20, '\n')
                        timer.append(self.common.bank_time())  # 添加学生
            self.common.judge_timer(timer)
            while self.wait_check_listen_select_page():
                time.sleep(3)
            self.next_btn_operate('true', self.fab_commit_btn)
            return mine_answer

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
                    if len(self.common.result_question()) == 2:
                        break
                    else:
                        self.screen_swipe_up(0.5, 0.8, 0.6, 1000)
            ques_info = []
            scale_info = self.get_ques_opt_scale()
            while len(ques_info) < len(mine_answer):
                questions = self.common.result_question()
                last_text_attr = self.get_last_text_id()
                for x, ques in enumerate(questions):
                    if ques.text in ques_info:
                        continue
                    else:
                        if x == len(questions) - 1:
                            if last_text_attr == 'ques':
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[0], 1000)
                            else:
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[1], 1000)

                        print('问题：', ques.text)
                        ques_info.append(ques.text)
                        for y, opt in enumerate(self.common.result_opt_text(ques.text)):
                            char = self.common.result_opt_char(ques.text)[y]
                            if opt.text == mine_answer[ques.text]:
                                if char.get_attribute('contentDescription') == 'right':
                                    print('答案正确', opt.text)
                                elif char.get_attribute('contentDescription') == 'error':
                                    print('答案错误', opt.text)
                            else:
                                if char.get_attribute('contentDescription') == 'right':
                                    print('正确答案：', opt.text)
                        print('-' * 20, '\n')
            print('结果页答案:', right_answer)
            self.click_back_up_button()
            return wrong, right, right_answer