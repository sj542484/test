#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/5 20:05
# -----------------------------------------
from app.honor.student.library.object_pages.games.listen_link_sentence import ListenLinkSentence
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep
from utils.get_attribute import GetAttribute


class LinkWordSentencePage(ListenLinkSentence):

    @teststep
    def play_link_word_to_sentence_game(self):
        mine_answers = {}
        timer = []
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_listen_sentence_page():
                self.next_btn_judge('false', self.fab_commit_btn)  # 下一步按钮状态校验
                self.next_btn_operate('false', self.listen_link_clear_btn)  # 清除按钮状态校验
                self.common.rate_judge(total_num, i)  # 剩余题数校验
                input_num = self.get_rich_text_input_count()
                index = 0
                while index < input_num:
                    select_text = self.text_for_select()
                    for x in select_text:
                        if x.text:
                            x.click()
                            index += 1
                rich_content = self.rich_text().get_attribute('contentDescription')  # 获取完成句子的desc
                finish_answer = rich_content.split('## ')[1].strip().replace('  ', '')
                mine_answers[i] = finish_answer.strip()
                timer.append(self.common.bank_time())
                self.next_btn_judge('true', self.listen_link_clear_btn)
                self.next_btn_operate('true', self.fab_commit_btn)
        self.common.judge_timer(timer)
        return mine_answers

    @teststep
    def link_word_to_sentence_result_operate(self, mine_answer):
        """听音连句结果页操作"""
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
                    else:
                        if GetAttribute().selected(mine_icon) == 'false':
                            print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                        else:
                            print('图标验证正确')
                    index += 1
                    print('-' * 20, '\n')
                if index == len(mine_answer):
                    break
                else:
                    self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
        print(right_answer)
        self.click_back_up_button()