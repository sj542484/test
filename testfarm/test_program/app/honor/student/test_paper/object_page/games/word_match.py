
import time
from app.honor.student.games.word_match import LinkWordGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class WordMatch(LinkWordGame):

    def __init__(self):
        self.answer = AnswerPage()

    @teststeps
    def play_word_match_game(self, num, exam_json):
        """连连看 """
        exam_json['连连看'] = {}
        tips = []
        while True:
            no_selected_cards = self.get_not_selected_hans_card()
            hans_card = [x for x in no_selected_cards if not self.is_word(x.text)]
            english_card = [x for x in no_selected_cards if self.is_word(x.text)]

            for ch in hans_card:
                for en in english_card:
                    ch.click()
                    en.click()
                    time.sleep(0.8)
                    if len(self.get_not_selected_hans_card()) < len(no_selected_cards):
                        tips.append(ch)
                        print('英文：', en.text)
                        print('中文：', ch.text)
                        break
                break

            self.answer.skip_operator(len(tips) - 1, num, '连连看', self.wait_check_word_match_page,
                                      self.judge_tip_status, tips[-1], next_page=1)
            if len(tips) == num:
                break

    @teststep
    def judge_tip_status(self, ele):
        if ele.get_attribute('selected') == 'true':
            print('题目跳转后选中状态未发生改变')
        else:
            print("★★★ 题目跳转后选中状态发生改变!")



