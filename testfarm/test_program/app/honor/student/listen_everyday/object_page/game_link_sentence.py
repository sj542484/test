#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/5 20:05
# -----------------------------------------
import random
import time

from app.honor.student.library.object_pages.games.listen_link_sentence import ListenLinkSentence
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep
from utils.get_attribute import GetAttribute


class LinkWordSentencePage(ListenLinkSentence):

    @teststep
    def play_link_word_to_sentence_game(self):
        print('<--- 听音连句游戏 --->\n')
        mine_answers = {}
        timer = []
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_listen_sentence_page():
                self.next_btn_judge('false', self.fab_commit_btn)  # 下一步按钮状态校验
                self.next_btn_operate('false', self.listen_link_clear_btn)  # 清除按钮状态校验
                self.common.rate_judge(total_num, i)  # 剩余题数校验
                input_num = self.get_rich_text_input_count()
                for j in range(input_num):
                    random.choice(self.text_for_select()).click()
                finish_answer = ' '.join(self.get_rich_text_answer())
                print('我的答案：', finish_answer)
                mine_answers[i] = finish_answer
                timer.append(self.common.bank_time())
                self.next_btn_judge('true', self.listen_link_clear_btn)
                self.next_btn_operate('true', self.fab_commit_btn)
                self.fab_next_btn().click()
                time.sleep(3)
        self.common.judge_timer(timer)
        return mine_answers

    @teststep
    def link_word_to_sentence_result_operate(self, bank_info):
        """听音连句结果页操作"""
        tips = []
        print("我的答案的个数：", len(bank_info))
        if ResultPage().wait_check_answer_page():
            while len(tips) < len(bank_info):
                result_explains = self.result_explain()
                for explain in result_explains:
                    if explain.text in tips:
                        continue
                    else:
                        mine_answer = self.mine_answer(explain.text)
                        result_right_answer = self.right_answer(explain.text)
                        record_answer = bank_info[len(tips)]
                        self.result_voice(explain.text).click()
                        print(explain.text)
                        print(result_right_answer)
                        print(mine_answer)
                        print('记录答案:', record_answer)
                        tips.append(explain.text)

                        if mine_answer.split(': ')[1].strip() != record_answer:
                            print('★★★ 输入的答案与页面展示的不一致！')

                        mine_icon = self.right_wrong_icon(explain.text)
                        if mine_answer != result_right_answer:
                            if GetAttribute().selected(mine_icon) == 'true':
                                print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                            else:
                                print('图标验证正确')
                        else:
                            if GetAttribute().selected(mine_icon) == 'false':
                                print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                            else:
                                print('图标验证正确')
                        print('-' * 20, '\n')
                self.screen_swipe_up(0.5, 0.8, 0.3, 1000)
        self.click_back_up_button()