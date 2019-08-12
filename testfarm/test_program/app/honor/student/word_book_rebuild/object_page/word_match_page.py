
import time
from math import ceil

from app.honor.student.games.word_match import LinkWordGame
from conf.decorator import teststeps



class MatchingWord(LinkWordGame):
    """连连看"""
    @teststeps
    def link_link_game_operate(self, bank_count):
        """连连看游戏过程"""
        print('====== 连连看  新词 ======= \n')
        for i in range(ceil(bank_count / 5)):
            if self.wait_check_word_match_page():
                english = []  # 单词list
                english_index = []  # 单词在所有button中的索引
                explain = []  # 解释list
                explain_index = []  # 解释在所有button中的索引

                word_list = self.get_word_cards()         # 获取所有文本
                for x in range(1, len(word_list)):
                    if self.is_word(word_list[x].text):  # 如果是字母
                        english.append(word_list[x].text)
                        english_index.append(x)
                    else:                               # 如果是汉字
                        explain.append(word_list[x].text)
                        explain_index.append(x)
                print("英文序列:%s" % english_index, "\n英文单词:%s" % english,
                      "\n解释序列:%s" % explain_index, "\n英文解释:%s\n" % explain)

                for y in explain_index:
                    for z in english_index:
                        explain_ele = self.get_word_cards()[y]
                        english_ele = self.get_word_cards()[z]
                        if len(english_index) == 1:
                            print('单词：', english_ele.text)
                            print('解释：', explain_ele.text)
                            explain_ele.click()  # 点击解释
                            english_ele.click()  # 点击英文
                            print('-' * 30, '\n')

                        else:
                            explain_ele.click()             # 点击解释
                            english_ele.click()             # 点击英文
                            if self.get_word_cards()[y].get_attribute('selected') == 'true':
                                print('单词：', english_ele.text)
                                print('解释：', explain_ele.text)
                                english_index.remove(z)
                                print('-' * 30, '\n')
                                break

                print('='*30, '\n')
                time.sleep(3)


