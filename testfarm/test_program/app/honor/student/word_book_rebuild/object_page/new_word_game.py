# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/4 14:21
# -------------------------------------------
import json
import time
from operator import eq

from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.flash_card_page import FlashCard
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.restore_word_page import WordRestore
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.spelling_word_page import SpellingWord
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.vocabulary_choose_page import VocabularyChoose
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_book import WordBook
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_dictation_page import WordDictation
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_match_page import MatchingWord
from testfarm.test_program.conf.decorator import teststeps


class NewWordGame:

    @staticmethod
    def write_data_to_json_file(word):
        with open('app/student/word_book_rebuild/test_data/spell_copy', 'w') as f:
            json.dump(word, f, ensure_ascii=False)

    @staticmethod
    def read_data_from_json():
        with open('app/student/word_book_rebuild/test_data/spell_copy', 'r') as f:
            data_json = json.load(f)
            return data_json


    @teststeps
    def play_new_word_game_operate(self, word_explain_list, group_num, change_words):
        data_json = self.read_data_from_json()
        new_word = data_json['新词']
        familiar_word = data_json['标熟新词']
        star_word = data_json['标星新词']
        review_word = data_json['复习单词']
        group_star = star_word[group_num] = {}
        group_new_word = new_word[group_num] = {}
        group_familiar = familiar_word[group_num] = {}
        group_review = review_word[group_num] = {}
        spell_word, dictation_answer = [], ['']
        listen_select_word = ['']
        index = 0
        while True:
            title = WordBook().game_title().text
            if title == "闪卡练习(新词)":
                if FlashCard().wait_check_study_page():     # 闪卡练习
                    FlashCard().study_new_word(index, group_familiar, group_star,
                                               group_new_word, group_review, int(group_num) - 1)
                    index += 1
                    if not FlashCard().wait_check_study_page():
                        index = 0
                        data = {"新词": new_word, "标熟新词": familiar_word, "标星新词": star_word, "复习单词": group_review}
                        self.write_data_to_json_file(data)
                        if int(group_num) - 1 == 0:
                            if len(group_new_word) != 10:
                                print("★★★ 新词推送个数不正确, 应推新词数%s， 实际新词数%s" % (10, len(group_new_word)))
                        g = list(set(group_new_word.values()))
                        g.sort(key=list(group_new_word.values()).index)
                        if g != list(group_new_word.values()):
                            print('★★★ 本组单词出现重复单词！')

                        check_words = [y for x in change_words for y in list(set(x.values()))]
                        if not set(check_words).issubset(set(group_new_word.values())):
                            print('★★★ 本组单词未包含作业去重单词数小于3的单词', check_words)

                elif FlashCard().wait_check_copy_page():  # 闪卡抄写模式
                    if len(group_star) == 0:
                        spell_word_json = self.read_data_from_json()
                        group_star = spell_word_json['标星新词'][group_num]
                    FlashCard().copy_new_word(index, group_star)  # 闪卡 抄写模式 游戏过程
                    index += 1
                    if not FlashCard().wait_check_copy_page():
                        if len(group_star) != index:
                            print("★★★ 抄写单词数与标星个数不一致！", len(group_star))
                        index = 0
            else:
                data_json = self.read_data_from_json()
                familiar = data_json['标熟新词'][group_num]
                new = data_json['新词'][group_num]
                if title == "单词拼写(新词)":      # 单词拼写
                    SpellingWord().dictation_pattern_new(index, spell_word, familiar)
                    index += 1
                    print(SpellingWord().wait_check_spell_page())
                    if not SpellingWord().wait_check_spell_page():
                        if len(familiar) != index:
                            print('★★★ 默写单词数与标熟个数不一致！')
                        index = 0

                elif title == "词汇选择(新词)":
                    VocabularyChoose().vocab_select_listen_choice(index, listen_select_word, new)
                    index += 1
                    if not VocabularyChoose().wait_check_voice_page():
                        index = 0

                elif title == "连连看(新词)":
                    MatchingWord().card_match(index, new)
                    index = index+1
                    if not MatchingWord().wait_check_word_mach_page():
                        index = 0

                elif title == "还原单词(新词)":
                    WordRestore().restore_word(index, new)
                    index += 1
                    if not WordRestore().wait_check_word_restore_page():
                        index = 0

                elif title == "单词听写(新词)":
                    WordDictation().word_dictation(index, dictation_answer)  # 单词听写 游戏过程
                    index += 1
                    if not WordDictation().wait_check_word_dictation_page():
                        break
                else:
                    break






        #
        # for j in range(range(familiar_word)):
        #     if






