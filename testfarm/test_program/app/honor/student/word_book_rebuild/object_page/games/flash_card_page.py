import random
import string
import time

from app.honor.student.games.word_flash_card import FlashCardGame
from app.honor.student.word_book_rebuild.object_page.data_handle import WordDataHandlePage
from utils.games_keyboard import Keyboard
from conf.decorator import teststeps, teststep
from utils.get_attribute import GetAttribute


class FlashCard(FlashCardGame):
    """单词本 - 闪卡练习"""

    @teststep
    def check_alert_tip_operate(self, index, group_count):
        """看是否有弹框提示"""
        if index == 0 and group_count == 0:
            if self.wait_check_tips_page():
                self.tips_operate()
            else:
                print('★★★第一次点击标星未显示提示')
            if self.wait_check_study_page():
                pass

    @teststep
    def first_group_familiar_operate(self, word, explain_id, word_has_different_explain, familiar_words, familiar_count):
        """第一组标熟操作"""
        if word in word_has_different_explain:
            familiar_words[explain_id] = word
            self.familiar_button().click()
            if not familiar_count:
                self.tips_operate()
            familiar_count += 1
        return familiar_count

    @teststep
    def first_group_not_familiar_operate(self, word, explain_id, word_has_different_explain, familiar_words, familiar_count):
        """第一组不标熟"""
        if word not in word_has_different_explain and familiar_count < 5:
            familiar_words[explain_id] = word
            self.familiar_button().click()
            if not familiar_count:
                self.tips_operate()
            familiar_count += 1
        return familiar_count

    @teststep
    def second_group_familiar_operate(self, word, explain_id, first_group_familiar, familiar_words, familiar_count):
        """第二组标熟操作"""
        if word in first_group_familiar:
            self.familiar_button().click()
            familiar_words[explain_id] = word
            if not familiar_count:
                self.tips_operate()
            familiar_count += 1
        return familiar_count


    @teststep
    def second_group_not_familiar_operate(self, word, explain_id, first_group_familiar, familiar_words, familiar_count):
        """第二组不标熟操作"""
        if word not in first_group_familiar and familiar_count < 5:
            self.familiar_button().click()
            if not familiar_count:
                self.tips_operate()
            familiar_words[explain_id] = word
            familiar_count += 1
        return familiar_count


    @teststep
    def flash_different_familiar_operate(self, stu_id, word_info, familiar_type, group_count,
                                         first_group_familiar, word_has_different_explain):
        index, familiar_count = 0, 0
        familiar_words, all_words = {}, {}
        group_new_explain_words = []

        while self.wait_check_study_page():
            if index == 0:
                if familiar_type == 1:
                    print('===== 🌟🌟 第一组单词标熟，第二组该单词不标熟（全对） 🌟🌟 =====\n')
                elif familiar_type == 2:
                    print('===== 🌟🌟 第一组单词不标熟，单词做错，第二组该单词标熟 🌟🌟 =====\n')
                elif familiar_type == 3:
                    print('===== 🌟🌟 第一组单词不标熟，单词做错， 第二组该单词不标熟（全对） 🌟🌟 =====\n')
                elif familiar_type == 4:
                    print('===== 🌟🌟 第一组单词不标熟，单词全对， 第二组该单词标熟 🌟🌟 =====\n')
                elif familiar_type == 5:
                    print('===== 🌟🌟 第一组单词不标熟, 单词全对， 第二组该单词不标熟（全对） 🌟🌟 =====\n')

            word = self.english_study()
            self.next_btn_judge('true', self.fab_next_btn)
            explain = self.study_word_explain()  # 解释
            explain_id = explain.get_attribute('contentDescription').split(' ')[0]

            if '新释义' in self.game_title().text:
                group_new_explain_words.append(explain_id)
                if WordDataHandlePage().check_has_other_studied_explain(stu_id, explain_id):
                    print('此单词为新释义单词')
                else:
                    print('★★★ 该单词不为新释义单词，但是标题出现新释义字样')

            if word in list(all_words.keys()):  # 判断单词是否去重
                print('★★★ 本组已存在本单词，单词未去重！')
            else:
                all_words[word] = explain_id

            if word not in list(word_info.keys()):
                word_info[word] = [explain_id]
            else:
                explain_id_list = word_info[word]
                if explain_id in explain_id_list:
                    print('★★★ 该解释已作为新词出现过')
                else:
                    word_info[word].append(explain_id)

            print('单词：', word, '\n',
                  '解释：', explain.text, '\n',
                  '句子：', self.study_sentence(), '\n',
                  '句子解释：', self.study_sentence_explain(), '\n',
                  '推荐老师：', self.author(), '\n'
                  )
            self.pattern_switch()  # 切换到 全英模式
            if self.wait_check_explain_page():  # 校验是否成功切换
                print('★★★ 切换全英模式， 依然存在解释')
            self.pattern_switch()  # 切换回 英汉模式

            if familiar_type == 1:
                if group_count == 0:
                    familiar_count = self.first_group_familiar_operate(word, explain_id, word_has_different_explain,
                                                                       familiar_words, familiar_count)
                elif group_count == 1:
                    familiar_count = self.second_group_not_familiar_operate(word, explain_id, first_group_familiar,
                                                                            familiar_words, familiar_count)

            elif familiar_type == 2 or familiar_type == 4:
                if group_count == 0:
                    familiar_count = self.first_group_not_familiar_operate(word, explain_id, word_has_different_explain,
                                                                           familiar_words, familiar_count)
                elif group_count == 1:
                    familiar_count = self.second_group_familiar_operate(word, explain_id, first_group_familiar,
                                                                        familiar_words, familiar_count)

            elif familiar_type == 3 or familiar_type == 5:
                if group_count == 0:
                    familiar_count = self.first_group_not_familiar_operate(word, explain_id, word_has_different_explain,
                                                                           familiar_words, familiar_count)
                elif group_count == 1:
                    familiar_count = self.second_group_not_familiar_operate(word, explain_id, first_group_familiar,
                                                                            familiar_words, familiar_count)

            # self.next_word(index, word)
            self.next_btn_operate('true', self.fab_next_btn)
            index += 1
            print('-' * 30, '\n')
        return all_words, familiar_words, 0, group_new_explain_words


    # ====================== 学习模式 ===========================
    @teststeps
    def flash_study_model(self, stu_id, word_info, group_count, do_right):
        """:param word_info: 记录今日所做的所有新
           :param group_count: 做的组数
           :param stu_id: 学生id
           :param do_right: 是否做全对
        """
        """学习模式  新词操作"""

        familiar_words, all_words = {}, {}
        star_words, group_new_explain_words = [], []
        index = 0
        while self.wait_check_study_page():
            if index == 0:
                print('===== 🌟🌟 闪卡练习 学习模式 🌟🌟 =====\n')
            word = self.english_study()
            if self.wait_check_explain_page():
                self.next_btn_judge('true', self.fab_next_btn)
                explain = self.study_word_explain()       # 解释
                explain_id = explain.get_attribute('contentDescription').split(' ')[0]

                if '新释义' in self.game_title().text:
                    group_new_explain_words.append(explain_id)
                    if WordDataHandlePage().check_has_other_studied_explain(stu_id, explain_id):
                        print('此单词为新释义单词')
                    else:
                        print('★★★ 该单词不为新释义单词，但是标题出现新释义字样')

                if word in list(all_words.keys()):  # 判断单词是否去重
                    print('★★★ 本组已存在本单词，单词未去重！')
                else:
                    all_words[word] = explain_id

                if word not in list(word_info.keys()):
                    word_info[word] = [explain_id]
                else:
                    explain_id_list = word_info[word]
                    if explain_id in explain_id_list:
                        print('★★★ 该解释已作为新词出现过')
                    else:
                        word_info[word].append(explain_id)

                print('单词：', word, '\n',
                      '解释：', explain.text, '\n',
                      '句子：', self.study_sentence(), '\n',
                      '句子解释：', self.study_sentence_explain(), '\n',
                      '推荐老师：', self.author(), '\n'
                      )
                self.pattern_switch()               # 切换到 全英模式

                if self.wait_check_explain_page():  # 校验是否成功切换
                    print('★★★ 切换全英模式， 依然存在解释')

                self.pattern_switch()               # 切换回 英汉模式
                if not do_right:
                    if index % 2 == 0:                      # 标熟
                        if index == 2:
                            self.familiar_button().click()
                            if self.familiar_button().text != '取消熟词':
                                print('★★★ 点击熟词后内容未发生变化')
                            self.familiar_button().click()
                            if self.familiar_button().text != '设置熟词':
                                print('★★★ 点击熟词后内容未发生变化')

                        self.familiar_button().click()
                        self.check_alert_tip_operate(index, group_count)    # 判断首次标熟是否有提示

                        familiar_words[explain_id] = word

                    if index in [0, 1, 3]:
                        if index == 1:
                            self.star_button().click()              # 标星
                            if self.star_button().get_attribute('selected') != 'true':
                                print('★★★ 点击标星按钮后，按钮未点亮')
                            self.star_button().click()
                            if self.star_button().get_attribute('selected') != 'false':
                                print('★★★ 取消标星后，按钮未置灰')
                        self.star_button().click()  # 标星
                        self.check_alert_tip_operate(index, group_count)   # 判断首次标星是否有提示
                        star_words.append(explain_id)
            else:
                print('★★★ 默认不是英汉模式')

            self.next_btn_operate('true', self.fab_next_btn)
            # self.next_word(index, word)
            index += 1
            print('-'*30, '\n')
        return all_words, familiar_words, star_words, group_new_explain_words


    @teststeps
    def flash_copy_model(self, star_words, new_explain_words):
        """闪卡抄写模式"""
        print('===== 🌟🌟 闪卡抄写模式 🌟🌟 =====\n')
        for x in range(len(star_words)):
            word = self.copy_word()
            word_explain = self.copy_explain()
            explain_id = word_explain.get_attribute('contentDescription')
            if explain_id in new_explain_words:
                if '新释义' not in self.game_title().text:
                    print('★★★ 该单词为新释义单词，但是标题未标明新释义字样')
            input_word = self.copy_word()

            if explain_id not in star_words:
                print('★★★ 单词未标星，但是有抄写模式', word)
            print("单词：%s\n解释：%s" % (word, word_explain.text))

            if len(input_word) != 0:
                print('★★★ Error-- 抄写栏不为空', input_word)
                for i in range(len(input_word)):
                    Keyboard().games_keyboard('backspace')

            random_str = random.sample(string.ascii_lowercase, len(word) + 1)
            if x == 1:
                for i, alpha in enumerate(list(random_str)):
                    self.keyboard_operate(i, alpha)
                if len(self.copy_word()) > len(word):
                    print('★★★ 输入栏可输入超过抄写单词长度的单词')
                for y in range(len(self.copy_word())):
                    Keyboard().games_keyboard('backspace')

            for i, alpha in enumerate(list(word)):
                self.keyboard_operate(i, alpha)
            time.sleep(5)
            print('-'*30, '\n')


    # @teststeps
    # def study_mine_word(self, i, star_list, familiar_list, star_add, familiar_add):
    #     """学习模式  单词详情操作"""
    #     if i == 0:
    #         print('\n闪卡练习-单词详情(我的单词)\n')
    #
    #     if i in(range(0, 5)):
    #         word = self.study_word_core()
    #
    #         if word in star_list:                      # 单词是否在标星数组中
    #             self.judge_word_is_star(i)             # 判断单词星标是否被标注
    #             self.judge_word_is_familiar(familiar_list, word, i, familiar_add)     # 判断单词是否同时被标熟
    #         else:
    #             if i == 1 or i == 3:
    #                 self.click_star()
    #                 self.tips_operate()
    #                 star_add.append(word)
    #             self.judge_word_is_familiar(familiar_list, word, i, familiar_add)     # 判断单词是否被标熟
    #
    #         self.next_btn_operate('true', self.fab_next_btn)
    #         # self.next_word(i)                                  # 下一单词滑屏还是点击按钮
    #     else:
    #         print('用户下所有标星单词：', star_list + star_add)
    #         print('用户下所有标熟单词：', familiar_list + familiar_add )
    #         print('-------------------------------------')
    #         self.home.click_back_up_button()

    @teststeps
    def next_word(self, i, word):
        """进入下一单词的方式"""
        if i == 1:  # 向左滑屏
            self.screen_swipe_left(0.9, 0.5, 0.1, 1000)
            if self.wait_check_study_page():
                if self.english_study() == word:
                    print('★★★ 左右滑屏未成功，仍处于已学单词页面')
        else:
            self.next_btn_operate('true', self.fab_next_btn)
        time.sleep(2)

    @teststep
    def judge_word_is_star(self, i):
        """判断单词是否被标星"""
        if GetAttribute().selected(self.star_button()) == 'true':  # 判断但是标星是否被标注
            print('单词已标星')
            if i == 3:
                self.star_button().click() # 取消标星
        else:
            print("★★★ Error--此题未被标星")

    @teststep
    def judge_word_is_familiar(self, familiar, word, i, familiar_add):
        """判断单词是否被标熟"""
        if word in familiar:
            if GetAttribute().selected(self.familiar_button()) == 'true':
                print("★★★ Error-- 此题未被标熟")
                self.familiar_button().click()
                self.tips_operate()
                familiar_add.append(word)
            else:
                print('单词已标熟')
        else:
            if i == 2 or i == 4:
                self.familiar_button().click()
                self.tips_operate()
                familiar_add.append(word)


    @teststeps
    def scan_game_operate(self, familiar=False, is_exit=False):
        """闪卡游戏过滤"""
        word_info, familiar_words = {}, {}
        star_words = 0
        new_explain_words = []
        if self.wait_check_study_page():
            while '闪卡练习' in self.game_title().text and self.game_mode_id() == 1:
                word = self.english_study()                        # 单词
                explain = self.study_word_explain()                # 解释
                print('单词：', word, '\n',
                      '解释：', explain.text, '\n',
                      '句子：', self.study_sentence(), '\n',
                      '句子解释：', self.study_sentence_explain(), '\n',
                      '推荐老师：', self.author(), '\n'
                      )
                explain_id = explain.get_attribute('contentDescription')   # 解释id
                if '新释义' in self.game_title().text:
                    new_explain_words.append(explain_id)

                if familiar:
                    self.familiar_button().click()
                    if len(word_info) == 0:
                        self.tips_operate()
                word_info[explain_id] = word         # 将解释id与解释存入字典中
                self.next_btn_operate('true', self.fab_next_btn)
                print('-' * 30, '\n')

        if is_exit:
            self.click_back_up_button()  # 退出弹框处理
            self.tips_operate()
        return word_info, familiar_words, star_words, new_explain_words
