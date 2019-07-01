# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/27 13:12
# -------------------------------------------
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.cloze import Cloze
from testfarm.test_program.app.honor.student.library.object_pages.games.complete_article import CompleteArticle
from testfarm.test_program.app.honor.student.library.object_pages.games.flash_card import FlashCard
from testfarm.test_program.app.honor.student.library.object_pages.games.guess_word import GuessWord
from testfarm.test_program.app.honor.student.library.object_pages.games.link_link import LinkLink
from testfarm.test_program.app.honor.student.library.object_pages.games.link_to_sentence import LinkToSentence
from testfarm.test_program.app.honor.student.library.object_pages.games.listen_choice import ListenChoice
from testfarm.test_program.app.honor.student.library.object_pages.games.listen_link_sentence import ListenLinkSentence
from testfarm.test_program.app.honor.student.library.object_pages.games.listen_select_img import ListenSelectImg
from testfarm.test_program.app.honor.student.library.object_pages.games.listen_spell import ListenSpell
from testfarm.test_program.app.honor.student.library.object_pages.games.read_understand import ReadUnderstand
from testfarm.test_program.app.honor.student.library.object_pages.games.restore_word import RestoreWord
from testfarm.test_program.app.honor.student.library.object_pages.games.select_word_blank import SelectWordBlank
from testfarm.test_program.app.honor.student.library.object_pages.games.sentence_exchange import ChangeSentence
from testfarm.test_program.app.honor.student.library.object_pages.games.sentence_strengthen import SentenceStrengthen
from testfarm.test_program.app.honor.student.library.object_pages.games.single_choice import SingleChoice
from testfarm.test_program.app.honor.student.library.object_pages.games.word_chioce import WordChoice
from testfarm.test_program.app.honor.student.library.object_pages.games.word_spell import WordSpell
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class GamePage(BasePage):
    def __init__(self):
        self.result = ResultPage()

    @teststep
    def wait_check_test_label_page(self):
        """[其他] 标签页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[@text="其他教材"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_punch_share_page(self):
        """分享页面检查点"""
        locator = (By.ID, '{}share_img'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_login_wechat_page(self):
        """微信登陆页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"登录微信")]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_share_page(self):
        """分享页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"万星空港学校")]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_bank_list_page(self):
        """大题列表页面检查点"""
        locator = (By.ID, '{}tv_testbank_name'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_game_page(self):
        """游戏页面检查点"""
        locator = (By.ID, '{}rate'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_share_area_page(self):
        """分享页面检查点"""
        locator = (By.ID, '{}share_area'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def share_btn(self):
        """分享"""
        ele = self.driver.find_element_by_id(self.id_type() + 'share')
        return ele

    @teststep
    def share_page_menu_share_btn(self):
        """分享页面的分享按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'menu_share')
        return ele

    @teststep
    def punch_share_btn(self):
        """立即打卡 -分享页面"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sign')
        return ele

    @teststep
    def start_game_btn(self):
        """开始阅读 -做题页面"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sign_bottom')
        return ele

    @teststep
    def wechat(self):
        """微信"""
        ele = self.driver.find_element_by_id(self.id_type() + 'weixin')
        return ele

    @teststep
    def friends(self):
        """朋友圈"""
        ele = self.driver.find_element_by_id(self.id_type() + "weixin_friends")
        return ele

    @teststep
    def download(self):
        """保存图片"""
        ele = self.driver.find_element_by_id(self.id_type() + 'save_img')
        return ele

    @teststep
    def wechat_back_up_btn(self):
        """微信页面退回按钮"""
        ele = self.driver.find_element_by_id('com.tencent.mm:id/kb')
        return ele

    @teststep
    def testbank_name(self, bank_type):
        """大题名称"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../android.widget.RelativeLayout'
                                                '/android.widget.TextView[@resource-id="{}tv_testbank_name"]'
                                                .format(bank_type, self.id_type()))
        return ele

    @teststep
    def ban_num(self, bank_type):
        """大题个数"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../android.widget.RelativeLayout'
                                                '/android.widget.TextView[@resource-id="{}tv_testbank_count"]'
                                                .format(bank_type, self.id_type()))
        return ele

    @teststep
    def testbank_type(self):
        """大题类型"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_testbank_type')
        return ele

    @teststep
    def bank_total_num(self):
        """大题总题数"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_testbank_count')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def bank_progress(self, bank_type):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/'
                                                'following-sibling::android.widget.TextView'.format(bank_type))

        return ele

    @teststep
    def game_name(self):
        """游戏名称"""
        ele = self.driver.find_element_by_xpath('//*[@resource-id="{}common_toolbar"]/'
                                                'android.widget.TextView'.format(self.id_type()))
        return ele.text

    @teststeps
    def share_page_operate(self):
        """分享页面具体操作"""
        if self.wait_check_punch_share_page():
            self.wechat().click()
            if not self.wait_check_login_wechat_page():
                print('★★★ 未跳转到微信登录页面')
            self.wechat_back_up_btn().click()

            if self.wait_check_punch_share_page():
                self.friends().click()
                if not self.wait_check_login_wechat_page():
                    print('★★★ 未跳转到微信登录页面')
                self.wechat_back_up_btn().click()

            if self.wait_check_punch_share_page():
                self.click_back_up_button()

    @teststep
    def play_book_games(self, fq, sec_answer=0, half_exit=False, first_num=0, bank_progress=0):
        """各种游戏过程
           fq:: 大题练习次数
           sec_answer :: 第二次练习的正确答案
           half_exit :: 是否中途退出 针对第三个脚本
           total_num :: 记录每道大题的总数
        """
        game_name = self.game_name()
        print('*-' * 20, '\n')
        print(game_name, '\n')
        mine_answer = 0
        if game_name == "猜词游戏":
            mine_answer = GuessWord().play_guess_game_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '还原单词':
            mine_answer = RestoreWord().restore_word_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '连连看':
            mine_answer = LinkLink().word_match_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '单词拼写':
            mine_answer = WordSpell().spell_word_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '单词听写':
            mine_answer = ListenSpell().listen_spell_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '词汇选择':
            if fq == 1:
                WordChoice().word_choice_operate(fq, sec_answer, half_exit=True)
                if self.wait_check_bank_list_page():
                    if self.bank_progress('词汇选择').text != bank_progress:
                        print('★★★ 中途返回进度却发生变化！')
                    self.bank_progress('词汇选择').click()
                    time.sleep(3)
            mine_answer = WordChoice().word_choice_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '句型转换':
            mine_answer = ChangeSentence().sentence_game_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '听音连句':
            mine_answer = ListenLinkSentence().listen_to_sentence_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '强化炼句':
            if fq == 1:
                print('中途退出处理\n')
                SentenceStrengthen().sentence_strengthen_operate(fq, sec_answer, half_exit=True)
                if self.wait_check_bank_list_page():
                    if self.bank_progress('强化炼句').text != bank_progress:
                        print('★★★ 中途返回进度却发生变化！')
                    self.bank_progress('强化炼句').click()
                    time.sleep(3)
            mine_answer = SentenceStrengthen().sentence_strengthen_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '连词成句':
            mine_answer = LinkToSentence().link_sentence_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '选词填空':
            mine_answer = SelectWordBlank().select_word_blank_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '补全文章':
            if fq == 1:
                CompleteArticle().complete_article_operate(fq, sec_answer, half_exit=True)
                if self.wait_check_bank_list_page():
                    print(self.bank_progress('补全文章').text)
                    print(bank_progress)
                    if self.bank_progress('补全文章').text != bank_progress:
                        print('★★★ 中途返回进度却发生变化！')
                    self.bank_progress('补全文章').click()
            mine_answer = CompleteArticle().complete_article_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '完形填空':
            mine_answer = Cloze().cloze_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '阅读理解':
            mine_answer = ReadUnderstand().read_understand_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '单项选择':
            mine_answer = SingleChoice().single_choice_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '听后选择':
            mine_answer = ListenChoice().listen_choice_operate(fq, sec_answer, half_exit)
            pass

        elif game_name == '闪卡练习':
            FlashCard().play_flash_card_game(half_exit)

        elif game_name == '听音选图':
            mine_answer = ListenSelectImg().listen_select_image_operate(fq, sec_answer, half_exit)

        else:
            pass

        if self.result.wait_check_medal_page():
            print('获取勋章')
            self.share_page_operate()

        if self.result.wait_check_result_page():  # 进入结果页
            result = 0
            self.result.check_result_btn().click()  # 查看结果
            print('----- 查看答案页面 ------\n')
            mine_done_answer = mine_answer[0]

            if game_name in ['猜词游戏', '还原单词', '连连看', '单词拼写', '单词听写', '词汇选择']:
                result = self.result.word_game_answer_detail_operate(mine_done_answer)
                pass

            elif game_name in ['句型转换']:
                result = ChangeSentence().sentence_game_result_operate(mine_done_answer)
                pass

            elif game_name in ['听音连句']:
                result = ListenLinkSentence().listen_to_sentence_result_operate(mine_done_answer)
                pass

            elif game_name in ['强化炼句']:
                result = SentenceStrengthen().sentence_strengthen_result_operate(mine_done_answer)
                pass

            elif game_name in ['连词成句']:
                result = LinkToSentence().link_sentence_result_operate(mine_done_answer)
                pass

            elif game_name in ['选词填空']:
                result = SelectWordBlank().select_word_blank_result_operate(mine_done_answer)
                pass

            elif game_name in ['补全文章']:
                result = CompleteArticle().complete_article_result_operate(mine_done_answer)
                pass

            elif game_name in ['完形填空']:
                result = Cloze().cloze_result_operate(mine_done_answer, store_key=False)
                pass

            elif game_name in ['阅读理解', '单项选择']:
                result = Cloze().cloze_result_operate(mine_done_answer, store_key=True)
                pass

            elif game_name in ['听后选择']:
                result = ListenChoice().listen_choice_result_operate(mine_done_answer)

            elif game_name in ['听音选图']:
                result = ListenSelectImg().listen_select_image_result_operate(mine_done_answer)

            self.result.result_multi_data_check(fq, result, first_num)
            return result[2], mine_answer[1]

        # print('*_'*20, '\n')
