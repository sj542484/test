# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/4 21:01
# -------------------------------------------
import time

from testfarm.test_program.app.honor.student.games.sentence_exchange import SentenceExchangeGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.utils.get_attribute import GetAttribute


class ChangeSentence(SentenceExchangeGame):

    def __init__(self):
        self.common = LibraryPubicPage()
        self.public = WorldBookPublicPage()

    @teststep
    def result_answer(self, question):
        """结果页问题对应的答案"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../..'.format(question))
        right_answer = ele.find_element_by_xpath('.//android.widget.TextView[contains(@resource-id,'
                                                 '"{}tv_answer")]'.format(self.id_type())).text
        mine_answer = ele.find_element_by_xpath('.//android.widget.TextView[contains(@resource-id,'
                                                '"{}tv_mine")]'.format(self.id_type())).text
        return right_answer, mine_answer

    @teststep
    def mine_icon(self, question):
        """题目图标"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../../following-sibling::android.widget.ImageView'
                                                .format(question))
        return ele

    @teststep
    def mine_answer(self):
        """结果页我的答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_mine')
        return ele

    @teststep
    def get_ques_size(self, question):
        """获取一个答案的大小"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../..'.format(question))
        return ele.size

    @teststep
    def sentence_game_operate(self, fq, sec_answer):
        """句型转换游戏过程"""
        timer = []
        mine_answers = {}
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_exchange_sentence_page():
                question = self.sentence_question()[0].text
                print('问题:', question)
                self.next_btn_judge('false', self.fab_commit_btn)
                self.next_btn_judge('false', self.clear_btn)
                if fq == 1:
                    while True:
                        if GetAttribute().enabled(self.fab_commit_btn()) == 'true':
                            break
                        self.text_bottom()[0].click()
                else:
                    right_answer = sec_answer[question].split(' ')
                    index = 0
                    while True:
                        if GetAttribute().enabled(self.fab_commit_btn()) == 'true':
                            break
                        wait_click_text = self.text_bottom()
                        for x in wait_click_text:
                            if x.text == right_answer[index]:
                                x.click()
                                index += 1
                                break

                finish_answer = ' '.join([x.text for x in self.input_text()])
                print('我的答案：', finish_answer)
                mine_answers[question] = finish_answer

                self.next_btn_judge('true', self.clear_btn)
                self.next_btn_operate('true', self.fab_commit_btn)
                print(self.sentence_answer())
                timer.append(self.common.bank_time())
                self.next_btn_operate('true', self.fab_next_btn)
                time.sleep(1)
                print('-'*20, '\n')
        self.common.judge_timer(timer)
        answer = mine_answers if fq == 1 else sec_answer
        return answer, total_num

    @teststep
    def sentence_game_result_operate(self, mine_answer):
        right_answer = {}
        right, wrong = [], []
        index = 0
        if ResultPage().wait_check_answer_page():
            ques_size = self.get_ques_size(self.sentence_question()[0].text)
            ques_scale = ques_size['height'] / self.get_window_size()[1]
            while True:
                questions = self.sentence_question()
                for i, ques in enumerate(questions):
                    if ResultPage().wait_check_answer_page():
                        if i == len(questions) - 1:
                            self.screen_swipe_up(0.5, 0.9, 0.9 - ques_scale, 1000)
                        result_answer = self.result_answer(ques.text)
                        print('问题：', ques.text)
                        print('答案：', result_answer[0])
                        print('我的：', result_answer[1])
                        mine_icon = self.mine_icon(ques.text)
                        if mine_answer[ques.text] != result_answer[1]:
                            print('★★★ 做题答案与页面展示的不一致')

                        if result_answer[0] != result_answer[1]:
                            if GetAttribute().selected(mine_icon) == 'true':
                                print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                            else:
                                print('图标验证正确')
                            wrong.append(ques.text)

                        else:
                            if GetAttribute().selected(mine_icon) == 'false':
                                print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                            else:
                                print('图标验证正确')
                            right.append(ques.text)

                        right_answer[ques.text] = result_answer[0]

                    index += 1
                    print('-'*20, '\n')
                if index != len(mine_answer):
                    self.screen_swipe_up(0.5, 0.9, 0.2, 1000)
                else:
                    break

        self.click_back_up_button()
        return wrong, right, right_answer





