# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/27 13:12
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.cloze import ClozePage
from testfarm.test_program.app.honor.student.library.object_pages.games.complete_article import CompleteArticle
from testfarm.test_program.app.honor.student.library.object_pages.games.flash_card import FlashCard
from testfarm.test_program.app.honor.student.library.object_pages.games.guess_word import GuessWord
from testfarm.test_program.app.honor.student.library.object_pages.games.word_match import LibraryWordMatch
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
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class LibraryGamePage(BasePage):
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
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
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

    @teststeps
    def wait_check_game_list_page(self, var):
        """以 小游戏的class_name为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, %s)]" % var)
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_homework_list_page(self):
        """作业页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}tv_homework_name')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def homework_list(self):
        """作业列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_homework_name')
        return ele

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
        ele = self.driver.find_element_by_id('com.tencent.mm:id/kx')
        return ele

    @teststep
    def bank_name_list(self):
        """大题列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_testbank_name')
        return ele

    @teststep
    def testbank_type(self):
        """大题类型"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_testbank_type')
        return ele


    @teststep
    def testbank_name(self, bank_type):
        """大题名称"""
        ele = self.driver.find_elements_by_xpath('//*[@text="{}"]/../preceding-sibling::android.widget.RelativeLayout/'
                                                 'android.widget.TextView[contains(@resource-id, "tv_testbank_name")]'.format(bank_type))
        return [x for x in ele]

    @teststep
    def bank_progress_by_name(self, bank_name):
        """根据大题名称获取"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling::android.widget.RelativeLayout/'
                                                'android.widget.TextView[contains(@resource-id, "tv_testbank_status")]'.format(bank_name))
        return ele.text

    @teststep
    def click_bank_by_name(self, bank_name):
        """通过名称定为大题并点击"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]'.format(bank_name))
        ele.click()

    @teststep
    def game_name(self):
        """游戏名称"""
        ele = self.driver.find_element_by_xpath('//*[@resource-id="{}common_toolbar"]/'
                                                'android.widget.TextView'.format(self.id_type()))
        return ele.text

    @teststep
    def check_process_change(self, bank_name, bank_progress):
        """检查大题进度变化"""
        print(self.wait_check_bank_list_page())
        if self.wait_check_bank_list_page():
            print(bank_name)
            if self.bank_progress_by_name(bank_name) != bank_progress:
                print('★★★ 中途返回进度却发生变化！')
            self.click_bank_by_name(bank_name)
            if self.wait_check_game_page():
                pass

    @teststep
    def enter_into_game(self, hw_name, bank_type):
        """进入游戏过程"""
        hw_name_list = 0
        if self.wait_check_homework_list_page():  # 页面检查点
            homework_name = []
            while True:
                for hw in self.homework_list():
                    if hw.text in homework_name:
                        continue
                    else:
                        homework_name.append(hw.text)
                        if hw_name == hw.text:
                            hw.click()
                            break
                if hw_name not in homework_name:
                    self.screen_swipe_up(0.5, 0.9, 0.2, 1000)
                else:
                    break

            if self.wait_check_game_list_page(hw_name):
                while True:
                    game_list = self.testbank_type()
                    if bank_type not in [x.text for x in game_list]:
                        self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
                    else:
                        break
                hw_name_list = self.testbank_name(bank_type)
            else:
                print('★★★ 未进入大题列表')
        return  hw_name_list

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
    def play_book_games(self, fq, bank_name, first_result='', half_exit=False, bank_progress=0):
        """各种游戏过程
           fq:: 大题练习次数
           sec_answer :: 第二次练习的正确答案
           half_exit :: 是否中途退出 针对第三个脚本
           total_num :: 记录每道大题的总数
           bank_name :: 大题名称
        """
        if fq == 1:
            print('========== 第一次做错操作 ========== \n')
        else:
            print('========== 第二次做对操作 ========== \n')

        if fq == 1:
            second_ans = {}
        else:
            # 若第一次做的全对， 则第二次结果参数更改为第一次的记录的正确答案

            if first_result[2]:
                second_ans = first_result[2]
            else:
                second_ans = first_result[1]

        first_count = 0 if fq == 1 else len(first_result[0]) + len(first_result[1])
        game_name = self.game_name()
        game_result = 0
        if game_name == "猜词游戏":
            game_result = GuessWord().play_guess_game_operate(fq, second_ans)

        elif game_name == '还原单词':
            game_result = RestoreWord().restore_word_operate(fq, second_ans)

        elif game_name == '连连看':
            game_result = LibraryWordMatch().word_match_operate(fq, second_ans)

        elif game_name == '单词拼写':
            game_result = WordSpell().spell_word_operate(fq, second_ans)

        elif game_name == '单词听写':
            game_result = ListenSpell().listen_spell_operate(fq, second_ans)

        elif game_name == '词汇选择':
            game_result = WordChoice().word_choice_operate(fq, first_result, half_exit)

        elif game_name == '句型转换':
            game_result = ChangeSentence().sentence_game_operate(fq, second_ans)

        elif game_name == '听音连句':
            game_result = ListenLinkSentence().listen_to_sentence_operate(fq, second_ans)

        elif game_name == '强化炼句':
            # if fq == 1:
            #     SentenceStrengthen().sentence_strengthen_operate(fq, second_ans, half_exit=True)
            #     self.check_process_change(bank_name, bank_progress)
            game_result = SentenceStrengthen().sentence_strengthen_operate(fq, second_ans, half_exit)

        elif game_name == '连词成句':
            game_result = LinkToSentence().link_sentence_operate(fq, second_ans)

        elif game_name == '选词填空':
            game_result = SelectWordBlank().select_word_blank_operate(fq, second_ans)

        elif game_name == '补全文章':
            game_result = CompleteArticle().complete_article_operate(fq, second_ans, half_exit)

        elif game_name == '完形填空':
            game_result = ClozePage().cloze_operate(fq, second_ans)

        elif game_name == '阅读理解':
            game_result = ReadUnderstand().read_understand_operate(fq, second_ans)

        elif game_name == '单项选择':
            game_result = SingleChoice().single_choice_operate(fq, second_ans)

        elif game_name == '听后选择':
            game_result = ListenChoice().listen_choice_operate(fq, second_ans)

        elif game_name == '闪卡练习':
            FlashCard().play_flash_game()

        elif game_name == '听音选图':
            game_result = ListenSelectImg().listen_select_image_operate(fq, second_ans)

        else:
            pass

        if self.result.wait_check_medal_page():
            print('获取勋章')
            self.share_page_operate()

        if game_result:
            check_info = self.check_bank_result(game_name, game_result)
            total_num = game_result[1]
            self.result.result_multi_data_check(fq, check_info, first_num=first_count, current_count=total_num)
            return check_info

    @teststep
    def check_bank_result(self, game_name, mine_answer):
        """结果页面答案对照"""
        result = 0
        if self.result.wait_check_result_page():  # 进入结果页
            self.result.check_result_btn().click()  # 查看结果
            time.sleep(2)
            print('----- 查看答案页面 ------\n')
            mine_done_answer = mine_answer[0]

            if game_name in ['猜词游戏', '还原单词', '单词拼写', '单词听写', '词汇选择']:
                result = self.result.word_game_answer_detail_operate(mine_done_answer)

            if game_name in '连连看':
                result = self.result.word_match_result_operate(mine_done_answer)

            elif game_name in ['句型转换']:
                result = ChangeSentence().sentence_game_result_operate(mine_done_answer)

            elif game_name in ['听音连句']:
                result = ListenLinkSentence().listen_to_sentence_result_operate(mine_done_answer)

            elif game_name in ['强化炼句']:
                result = SentenceStrengthen().sentence_strengthen_result_operate(mine_done_answer)

            elif game_name in ['连词成句']:
                result = LinkToSentence().link_sentence_result_operate(mine_done_answer)

            elif game_name in ['选词填空']:
                result = SelectWordBlank().select_word_blank_result_operate(mine_done_answer)

            elif game_name in ['补全文章']:
                result = CompleteArticle().complete_article_result_operate(mine_done_answer)

            elif game_name in ['完形填空', '单项选择']:
                result = ClozePage().cloze_result_operate(mine_done_answer, store_key=False)

            elif game_name in ['阅读理解']:
                result = ClozePage().cloze_result_operate(mine_done_answer, store_key=True)

            elif game_name in ['听后选择']:
                result = ListenChoice().listen_choice_result_operate(mine_done_answer)

            elif game_name in ['听音选图']:
                result = ListenSelectImg().listen_select_image_result_operate(mine_done_answer)

        return result

