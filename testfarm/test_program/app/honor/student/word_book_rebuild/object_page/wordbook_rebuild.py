#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/3 10:59
# -----------------------------------------
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.flash_card_page import FlashCard
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.listen_spell_page import ListenSpellWordPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.restore_word_page import WordRestore
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_spelling_page import SpellingWord
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.vocabulary_choose_page import VocabularyChoose
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_match_page import MatchingWord
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep


class WordBookRebuildPage(BasePage):
    @teststep
    def wait_check_start_page(self):
        """将'你准备好了吗?'作为 单词本首页 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '你准备好了吗?')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_game_title_page(self):
        """游戏标题页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_title')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def word_start_button(self):  # Go标志按钮
        self.driver \
            .find_element_by_id(self.id_type() + "word_start").click()

    @teststep
    def game_title(self):  # 题型标题
        title = self.driver\
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    @teststep
    def total_word(self):
        """已背单词 数"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "total").text
        return int(word)

    @teststep
    def write_words_to_file(self, word_info):
        """将字典写入json文件"""
        with open('app/student/word_book_rebuild/test_data/new_words.json', 'w') as f:
            json.dump(word_info, f)

    @teststep
    def read_words_info_from_file(self):
        """从json文件中读取数据"""
        with open('app/student/word_book_rebuild/test_data/new_words.json', 'r') as f:
            word_info = json.load(f)
            return word_info

    @teststep
    def flash_study_operate(self, game_title, mode_id, word_info, group_count, new_explain_words, stu_id):
        familiar_words = {}
        star_words, all_words, repeat_words = [], [], []
        index = 0

        while '闪卡练习' in game_title and mode_id == 1:
            FlashCard().flash_study_model(all_words, star_words, familiar_words, word_info,
                                          index, group_count, new_explain_words, repeat_words, stu_id)
            index += 1
        return all_words, familiar_words, star_words, repeat_words

    @teststep
    def study_new_word_operate(self, word_info, group_count, new_explain_words, stu_id):
        """单词学习过程"""
        flash_result = 0
        while self.wait_check_game_title_page():
            title_ele = self.game_title()
            game_title = title_ele.text
            mode_id = int(title_ele.get_attribute('contentDescription').split('  ')[1])
            if '闪卡练习' in game_title and mode_id == 1:
                flash_result =  self.flash_study_operate(game_title, mode_id, word_info,
                                                         group_count, new_explain_words, stu_id)

            else:
                star_words = flash_result[2]
                familiar_words = flash_result[1]
                bank_count = len(flash_result[0]) - len(familiar_words)
                remove_repeat_count = bank_count - len(flash_result[3])
                print('标星单词：', star_words)
                print('标熟单词：', familiar_words)
                print('做题数：', bank_count)
                print('去除重复单词数：', remove_repeat_count)


                if '闪卡练习' in game_title and mode_id == 2:
                    FlashCard().flash_copy_model(star_words)
                    if '闪卡练习' in self.game_title().text:
                        print('★★★ 标星个数与抄写个数不一致')
                        break

                elif '单词拼写(新词)' in game_title:
                    SpellingWord().new_word_spell_operate(familiar_words)
                    if '单词拼写(新词)' in self.game_title().text:
                        print('★★★ 标熟单词与单词拼写个数不一致')
                        break

                elif '词汇选择(新词)' in game_title:
                    VocabularyChoose().new_word_listen_select_operate(remove_repeat_count, new_explain_words)

                elif '连连看' in game_title:
                    MatchingWord().link_link_game_operate(bank_count)

                elif '还原单词' in game_title:
                    WordRestore().restore_word_operate(remove_repeat_count, new_explain_words)

                elif '单词听写' in game_title:
                    ListenSpellWordPage().listen_spell_operate(remove_repeat_count, new_explain_words)

                else:
                    break

    @teststep
    def study_recite_word_operate(self):
        pass
