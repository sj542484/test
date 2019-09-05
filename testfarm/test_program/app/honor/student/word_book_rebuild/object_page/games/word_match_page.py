
import time
from app.honor.student.games.word_match import LinkWordGame
from conf.decorator import teststeps



class MatchingWord(LinkWordGame):
    """连连看"""
    @teststeps
    def link_link_game_operate(self, bank_count):
        """连连看游戏过程"""
        print('====== 🌟🌟 连连看  新词 🌟🌟======= \n')
        tips = []
        while self.wait_check_word_match_page():
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
                            break
                    else:
                        tips.append(ch)
                        print('英文：', en.text)
                        print('中文：', ch.text)
                        print('-' * 30, '\n')
                        ch.click()
                        en.click()
                        break
                break

            if len(tips) == bank_count:
                break
        time.sleep(3)

