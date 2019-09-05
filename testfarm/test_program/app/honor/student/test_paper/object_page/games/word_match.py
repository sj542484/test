
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
        exam_json['连连看'] = bank_json = {}
        tips = []
        while True:
            hans_card = self.get_not_selected_hans_card()
            english_card = self.get_english_cards()

            for ch in hans_card:
                for en in english_card:
                    if len(hans_card) != 1:
                        ch.click()
                        en.click()
                        time.sleep(0.8)
                        if len(self.get_not_selected_hans_card()) < len(hans_card):
                            tips.append(ch)
                            print('英文：', en.text)
                            print('中文：', ch.text)
                            print('-' * 30, '\n')
                            bank_json[ch.text] = en.text
                            break
                    else:
                        tips.append(ch)
                        print('英文：', en.text)
                        print('中文：', ch.text)
                        print('-' * 30, '\n')
                        bank_json[ch.text] = en.text
                        ch.click()
                        en.click()
                        break
                break

            if len(tips) == num:
                break


