# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/10 15:53
# -------------------------------------------
import random

from app.honor.student.games.article_read_understand import ReadUnderstandGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from conf.decorator import teststep


class ReadUnderstand(ReadUnderstandGame):

    def __init__(self):
        self.common = LibraryPubicPage()

    @teststep
    def read_understand_operate(self, fq, sec_answer):
        """阅读理解做题过程"""
        if self.wait_check_read_understand_page():
            total_num = self.common.rest_bank_num()
            article = self.rich_text()
            print(article.text)
            # SelectWordBlank().check_position_change()  # 校验字体大小是否发生变化
            self.next_btn_judge('false', self.fab_commit_btn)
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)     # 拖拽至最上方
            ques_info = []
            timer = []
            mine_answer = {}
            scale_info = self.get_ques_opt_scale()
            while True:
                if self.common.rest_bank_num() == 0:
                    break
                questions = self.common.result_question()
                last_text_attr = self.get_last_text_id()
                for i, ques in enumerate(questions):
                    if ques.text in ques_info:
                        continue
                    else:
                        if i == len(questions) - 1:
                            if last_text_attr == 'ques':
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[0], 1000)
                            elif last_text_attr == 'opt':
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[1], 1000)

                        ques_text = ques.text
                        print('问题：', ques_text)
                        self.common.rate_judge(total_num, len(timer))
                        ques_info.append(ques_text)
                        if fq == 1:
                            for x, opt in enumerate(self.common.result_opt_text(ques_text)):
                                print(self.common.result_opt_char(ques_text)[x].text, opt.text)
                            random_index = random.randint(0, len(self.common.result_opt_char(ques_text)) -1)
                            random_text = self.common.result_opt_text(ques_text)[random_index].text
                            mine_answer[ques_text] = random_text
                            print('我的答案：', random_text)
                            self.common.result_opt_char(ques_text)[random_index].click()
                        else:
                            right_answer = sec_answer[ques_text]
                            for x, opt in enumerate(self.common.result_opt_text(ques_text)):
                                print(self.common.result_opt_char(ques_text)[x].text, opt.text)
                                if opt.text == right_answer:
                                    self.common.result_opt_char(ques_text)[x].click()
                            print('我的答案：', right_answer)

                        print('-'*20, '\n')

                        timer.append(self.common.bank_time())
            self.common.judge_timer(timer)
            self.next_btn_operate('true', self.fab_commit_btn)
            answer = mine_answer if fq == 1 else sec_answer
            print(answer)
            return answer, total_num