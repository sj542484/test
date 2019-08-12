# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/8 13:18
# -------------------------------------------
import time

from testfarm.test_program.app.honor.student.games.sentence_listen_link import ListenLinkSentenceGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.utils.get_attribute import GetAttribute


class ListenLinkSentence(ListenLinkSentenceGame):
    def __init__(self):
        self.common = LibraryPubicPage()

    @teststep
    def result_explain(self):
        """结果页答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_explain')
        return ele

    @teststep
    def result_answer(self, explain):
        """结果页答案"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(explain))
        mine_answer = ele.find_element_by_xpath('.//android.widget.TextView[contains(@resource-id,"{}tv_mine")]'
                                                .format(self.id_type())).text.strip()
        right_answer = ele.find_element_by_xpath('.//android.widget.TextView[contains(@resource-id,"{}tv_right")]'
                                                 .format(self.id_type())).text.strip()
        return mine_answer, right_answer

    def result_voice(self, explain):
        """结果页声音按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(explain))
        voice_btn = ele.find_element_by_xpath('.//android.widget.ImageView[contains(@resource-id, "{}iv_speak")]'
                                              .format(self.id_type()))
        return voice_btn

    def mine_icon(self, explain):
        """结果图标"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../..'.format(explain))
        icon = ele.find_element_by_xpath('.//android.widget.ImageView[contains(@resource-id, "{}iv_mine")]'
                                         .format(self.id_type()))
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
                print(input_num)
                if fq == 1:                                       # 第一轮，按下方单词或词组顺序依次点击
                    index = 0
                    # print([x.text for x in self.text_for_select() if x.text])
                    # self.text_for_select()[0].click()
                    # time.sleep(2)
                    # print([x.text for x in self.text_for_select() if x.text])
                    # self.text_for_select()[0].click()
                    while index < input_num:
                        select_text = self.text_for_select()
                        for x in select_text:
                            if x.text:
                                x.click()
                                index += 1
                else:                                            # 第二轮，依次点击正确答案拆分后的顺序
                    right_answer = sec_answer[i].split(' ')
                    print('正确答案：', right_answer)
                    index = 0
                    while ' '.join(self.rich_text().split()) != sec_answer[i]:
                        for x in self.text_for_select():       # 每次只点击一个（与答案相同的词组）
                            if x.text == right_answer[index]:
                                index += 1
                                x.click()
                                break
                self.next_btn_judge('true', self.listen_link_clear_btn)
                self.next_btn_operate('true', self.fab_commit_btn)

                if self.wait_check_clear_btn_page():
                    print('★★★ 点击下一步后，清除按钮依然存在')

                rich_content = self.rich_text().get_attribute('contentDescription')  # 获取完成句子的desc
                finish_answer = rich_content.split('## ')[1].strip().replace('  ', '')
                right_answer = self.right_sentence_answer().replace('\n', ': ')
                explain = self.sentence_explain().replace('\n', ': ')
                print('我的答案: ', finish_answer.strip())
                print(right_answer)
                print(explain)
                mine_answers[i] = finish_answer.strip()
                timer.append(self.common.bank_time())
                print('-'*20, '\n')
                self.fab_next_btn().click()

        self.common.judge_timer(timer)
        answer = mine_answers if fq == 1 else sec_answer
        return answer, total_num

    @teststep
    def listen_to_sentence_result_operate(self, mine_answer):
        right_answer = {}
        right, wrong = [], []
        index = 0
        if ResultPage().wait_check_answer_page():
            while True:
                explains = self.result_explain()
                for j, x in enumerate(explains):
                    result_answer = self.result_answer(x.text)
                    self.result_voice(x.text).click()
                    print('explain:', x.text)
                    print('right:', result_answer[1])
                    print('mine:', result_answer[0].split(': ')[1])
                    print('done:', mine_answer[j])

                    if result_answer[0].split(': ')[1] != mine_answer[j]:
                        print('★★★ 输入的答案与页面展示的不一致！')

                    mine_icon = self.mine_icon(x.text)
                    if result_answer[0] != result_answer[1]:
                        if GetAttribute().selected(mine_icon) == 'true':
                            print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                        else:
                            print('图标验证正确')
                        wrong.append(x.text)
                        right_answer[index] = result_answer[1].split(': ')[1]
                    else:
                        if GetAttribute().selected(mine_icon) == 'false':
                            print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                        else:
                            print('图标验证正确')
                        right.append(x.text)

                    index += 1
                    print('-' * 20, '\n')
                if index == len(mine_answer):
                    break
                else:
                    self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
        print(right_answer)
        self.click_back_up_button()
        return wrong, right, right_answer
