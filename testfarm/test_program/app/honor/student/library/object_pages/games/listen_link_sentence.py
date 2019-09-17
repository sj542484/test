# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/8 13:18
# -------------------------------------------
import random
import time

from app.honor.student.games.sentence_listen_link import ListenLinkSentenceGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep
from utils.get_attribute import GetAttribute


class ListenLinkSentence(ListenLinkSentenceGame):
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststep
    def result_explain(self):
        """结果页答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_explain')
        return ele

    @teststep
    def mine_answer(self, explain):
        """我的答案"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '{}')]/preceding-sibling::"
                                                "android.widget.TextView".format(explain))
        return ele.text

    @teststep
    def right_answer(self, explain):
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '{}')]/preceding-sibling::"
                                                "android.widget.LinearLayout/android.widget.TextView".format(explain))
        return ele.text

    def result_voice(self, explain):
        """结果页声音按钮"""
        voice_btn = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{}")]/../following'
                                                      '-sibling::android.widget.ImageView'.format(explain))
        return voice_btn

    def right_wrong_icon(self, explain):
        """结果图标"""
        icon = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{}")]/preceding-sibling::'
                                                 'android.widget.LinearLayout/android.widget.ImageView'.format(explain))
        return icon

    @teststep
    def listen_to_sentence_operate(self, fq, sec_answer):
        """听音连句游戏过程"""
        timer = []
        mine_answers = {}
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_listen_sentence_page():
                self.next_btn_judge('false', self.fab_commit_btn)     # 下一步按钮状态校验
                self.next_btn_operate('false', self.listen_link_clear_btn)                     # 清除按钮状态校验
                self.common.rate_judge(total_num, i)              # 剩余题数校验
                input_num = self.get_rich_text_input_count()
                if fq == 1:                                       # 第一轮，按下方单词或词组顺序依次点击
                    for j in range(input_num):
                        random.choice(self.text_for_select()).click()
                else:                                            # 第二轮，依次点击正确答案拆分后的顺序
                    right_answer = sec_answer[i].split(' ')
                    print('正确答案：', right_answer)
                    index = 0
                    while ' '.join(self.rich_text().text.split()) != sec_answer[i]:
                        for x in self.text_for_select():       # 每次只点击一个（与答案相同的词组）
                            if x.text == right_answer[index]:
                                index += 1
                                x.click()
                                break
                self.next_btn_judge('true', self.listen_link_clear_btn)
                self.next_btn_operate('true', self.fab_commit_btn)

                if self.wait_check_clear_btn_page():
                    print('★★★ 点击下一步后，清除按钮依然存在')

                finish_answer = ' '.join(self.rich_text().text.split())
                mine_answers[i] = finish_answer
                print('我的答案: ', finish_answer)
                print(self.right_sentence_answer())
                print(self.sentence_explain()[0].text)
                timer.append(self.common.bank_time())
                print('-'*20, '\n')
                self.fab_next_btn().click()

        self.common.judge_timer(timer)
        answer = mine_answers if fq == 1 else sec_answer
        return answer, total_num

    @teststep
    def listen_to_sentence_result_operate(self, mine_done_answer):
        right_answer = {}
        tips = []
        right, wrong = [], []
        if ResultPage().wait_check_answer_page():
            while len(tips) < len(mine_done_answer):
                result_explains = self.result_explain()
                for explain in result_explains:
                    if explain.text in tips:
                        continue
                    else:
                        mine_answer = self.mine_answer(explain.text)
                        result_right_answer = self.right_answer(explain.text)
                        record_answer = mine_done_answer[len(tips)]
                        self.result_voice(explain.text).click()
                        print(explain.text)
                        print(result_right_answer)
                        print(mine_answer)
                        print('记录答案:', record_answer)
                        if mine_answer.split(': ')[1].strip() != record_answer:
                            print('★★★ 输入的答案与页面展示的不一致！')

                        mine_icon = self.right_wrong_icon(explain.text)
                        if mine_answer != result_right_answer:
                            if GetAttribute().selected(mine_icon) == 'true':
                                print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                            else:
                                print('图标验证正确')
                            wrong.append(explain.text)
                            right_answer[len(tips)] = result_right_answer.split(': ')[1].strip()
                        else:
                            if GetAttribute().selected(mine_icon) == 'false':
                                print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                            else:
                                print('图标验证正确')
                            right.append(explain.text)

                        tips.append(explain.text)
                        print('-' * 20, '\n')
                self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
        print(right_answer)
        self.click_back_up_button()
        return wrong, right, right_answer
