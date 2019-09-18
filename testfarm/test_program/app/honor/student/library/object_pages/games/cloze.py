# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/10 11:53
# -------------------------------------------
import random
from testfarm.test_program.app.honor.student.games.article_cloze import ClozeGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.app.honor.student.library.object_pages.games.select_word_blank import SelectWordBlank
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.decorator import teststep, teststeps


class ClozePage(ClozeGame):

    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def cloze_operate(self, fq, sec_answer):
        """完形填空操作"""
        timer = []
        mine_answers = {}
        if self.wait_check_cloze_page():
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
            total_num = self.common.rest_bank_num()
            article = self.rich_text()
            print(article.text)

            for i in range(total_num):
                question = self.question()[0].text.strip()
                print('问题：', question)
                self.next_btn_judge('false', self.fab_next_btn)     # 判断下一题状态
                self.common.rate_judge(total_num, i)              # 剩余题数校验
                if fq == 1:
                    for j, char in enumerate(self.opt_char()):
                        print(char.text, self.opt_text()[j].text)

                    random_index = random.randint(0, len(self.opt_char()) - 1)
                    random_opt = self.opt_text()[random_index]
                    mine_answers[i+1] = random_opt.text
                    print('我的选项：', random_opt.text)
                    self.opt_char()[random_index].click()
                else:
                    right_answer = sec_answer[i+1]
                    for j, opt in enumerate(self.opt_text()):
                        print(self.opt_char()[j].text, opt.text)
                        if opt.text == right_answer:
                            self.opt_char()[j].click()

                    print('我的选项：', right_answer)
                timer.append(self.common.bank_time())
                if i != total_num - 1:
                    self.screen_swipe_left(0.9, 0.7, 0.2, 1000)
                print('-'*20, '\n')

            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, self.get_window_size()[1] - 20)  # 拖拽至最下方
            SelectWordBlank().check_position_change()  # 校验字体大小是否发生变化
            self.common.judge_timer(timer)
            self.next_btn_operate('true', self.fab_next_btn)
            answer = mine_answers if fq == 1 else sec_answer
            print('我的答案', answer)
            print('------ 游戏结束  -----\n')
            return answer, total_num

    @teststeps
    def cloze_result_operate(self, mine_answer, store_key):
        """完形填空、阅读理解、单项选择结果页处理"""
        right_answer = {}
        right, wrong = [], []
        if ResultPage().wait_check_answer_page():
            ques_info = []
            index = 0
            if self.wait_check_dragger_btn():
                loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
                self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方

            scale_info = self.get_ques_opt_scale()
            while len(ques_info) < len(mine_answer):
                questions = self.common.result_question()
                last_text_attr = self.get_last_text_id()
                for i, ques in enumerate(questions):
                    if ques.text in ques_info:
                        self.screen_swipe_up(0.5, 0.9, 0.8, 1000)
                    else:
                        if i == len(questions) - 1:
                            if last_text_attr == 'ques':
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[0], 1000)
                            elif last_text_attr == 'opt':
                                self.screen_swipe_up(0.5, 0.9, 0.9 - scale_info[1], 1000)

                        ques_info.append(ques.text)
                        print('问题：', ques.text, '\n')
                        for y, opt in enumerate(self.common.result_opt_text(ques.text)):
                            char = self.common.result_opt_char(ques.text)[y]
                            mine_ans = mine_answer[ques.text] if store_key else mine_answer[len(ques_info)]
                            if opt.text == mine_ans:
                                if char.get_attribute('contentDescription') == 'right':
                                    right.append(opt.text)
                                    print('我的：', mine_ans)
                                    print('答案正确：', opt.text)
                                    if store_key:
                                        right_answer[ques.text] = opt.text

                                elif char.get_attribute('contentDescription') == 'error':
                                    wrong.append(opt.text)
                                    print('我的答案错误', opt.text)
                                else:
                                    print('★★★ 选择的选项未标识对错信息！')
                            else:
                                if char.get_attribute('contentDescription') == 'right':
                                    if store_key:
                                        right_answer[ques.text] = opt.text
                                    else:
                                        index += 1
                                        right_answer[index] = opt.text
                                    print('正确答案：', opt.text)
                        print('-'*30, '\n')

            print('正确答案:', right_answer)
            self.click_back_up_button()
            return wrong, right, right_answer


