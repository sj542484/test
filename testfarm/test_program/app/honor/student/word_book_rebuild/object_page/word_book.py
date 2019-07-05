import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.buy_tips_page import BuyTipsPage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.data_action import DataActionPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.flash_card_page import FlashCard
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.restore_word_page import WordRestore
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.spelling_word_page import SpellingWord
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.vocabulary_choose_page import VocabularyChoose
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_dictation_page import WordDictation
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_match_page import MatchingWord
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_result_page import ResultPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.conf.base_config import GetVariable as gv


class WordBook(BasePage):
    """单词本首页"""

    def __init__(self):
        self.login = LoginPage()
        self.home = HomePage()
        self.tips = BuyTipsPage()
        self.spell = SpellingWord()
        self.result = ResultPage()
        self.vchoose = VocabularyChoose()
        self.common = DataActionPage()

    @teststep
    def rank_button(self):
        """排行榜 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "rank") \
            .click()

    @teststep
    def my_word_button(self):
        """我的单词 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "my_word") \
            .click()

    @teststep
    def word_test_button(self):
        """单词测试 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "word_test") \
            .click()

    # 多种情况下的 单词本首页
    @teststeps
    def wait_check_start_page(self):
        """将'你准备好了吗?'作为 单词本首页 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '你准备好了吗?')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_continue_page(self):
        """将'欢迎回来!继续上一次的练习吧?'作为 继续页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '欢迎回来!继续上一次的练习吧?')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_great_page(self):
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '欢迎回来!继续上一次的练习吧?')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def word_start_button(self):  # Go标志按钮
        self.driver\
            .find_element_by_id(self.id_type() + "word_start").click()

    @teststep
    def word_continue_button(self):  # 继续标志按钮
        self.driver\
            .find_element_by_id(self.id_type() + "word_continue").click()

    @teststep
    def total_word(self):
        """已背单词 数"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "total").text
        return word

    # 年级
    @teststeps
    def wait_check_class_page(self):
        """ 将'请选择你所处年级'作为 选择年级页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '请选择你所处年级')]")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def grade_list(self):
        """ 年级列表 选择年级"""
        grades = self.driver \
            .find_elements_by_id(self.id_type() + "tv_grade")
        return grades

    # 做题过程
    @teststeps
    def wait_check_game_page(self):
        """ 将'title'作为 选择做题过程中 页面检查点"""
        locator = (By.ID, "{}tv_title".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    def game_title(self):  # 题型标题
        title = self.driver\
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    # 结果页
    @teststeps
    def wait_check_result_page(self):
        """将'单词本'作为 继续页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '单词本')]")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def result_text(self):   # 结果页面新词和复习描述
        result = self.driver\
            .find_element_by_id(self.id_type() + "text")
        return result

    @teststep
    def get_word_count(self):  # 结果页已背单词描述
        count = self.driver\
            .find_element_by_id(self.id_type() + 'all_word_count')
        return count

    @teststeps
    def click_again(self):
        """再来一组 按钮"""
        self.driver\
            .find_element_by_id(self.id_type() + "again")\
            .click()

    # 单词本 已背完
    @teststeps
    def wait_check_no_word_page(self):
        """太棒了，太棒啦！你的词汇量已到达一定阶段 页面检查点"""
        locator = (By.ID, "'{}status_error_hint_view')]".format(self.id_type()))
        try:
            ele = WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            print(ele.text)
            return True
        except:
            return False

    # 次数达到限制
    @teststeps
    def wait_check_count_limit_page(self):
        locator = (By.ID, self.id_type() + "error_img")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def limit_confirm_button(self):
        """次数限制页面的【确定】 按钮"""
        self.driver.\
            find_element_by_id(self.id_type() + 'confirm')\
            .click()

    @teststep
    def back_to_home(self):
        self.home.click_back_up_button()
        if self.home.wait_check_word_title():
            self.home.click_back_up_button()
            if self.home.wait_check_home_page():  # 页面检查点
                print('返回主界面')

    @teststep
    def more_group(self):
        """再来一组"""
        if self.wait_check_result_page():
            print('进入结果页面')
            self.result.check_result_word_data()  # 结果页元素
            self.result.more_again_button()  # 再练一次
            self.play_word_book()
            self.result.result_page_handle()

    @teststeps
    def word_book_operate(self):
        """单词本 具体操作"""
        if self.wait_check_start_page():  # 页面检查点
            print("开始单词本练习")
            self.word_start_button()  # 点击 Go按钮
            """
            点击准备好后，有四种情况：
            1、未选择年级将跳转到年级选择页面
            2、进行新词游戏界面
            3、单词已练完的提示页面
            4、购买提示页面 
            """
            if self.wait_check_class_page():  # 页面检查点
                print("选择年级:")
                grades = self.grade_list()  # 年级列表
                for i in range(0, len(grades)):
                    if grades[i].text == gv.GRADE:
                        grades[i].click()
                        print('已选择', gv.GRADE)
                        break
                if self.wait_check_start_page():  # 页面检查点
                    self.word_start_button()  # 点击 Go按钮
                    self.play_word_book()  # 单词本 具体过程

            elif self.tips.wait_check_pay_page():  # 购买提示 页面检查点
                self.tips.tips_goto_pay_operate()  # 去购买 提示页面
                if self.wait_check_start_page():
                    self.home.click_back_up_button()

            elif self.result.wait_check_next_grade():
                """提示练习更高年级"""
                self.result.level_up_text()  # 词汇升级提示
                self.result.no_study_btn()
                if self.wait_check_start_page():
                    self.home.click_back_up_button()

            elif self.wait_check_count_limit_page():
                print('今日练习次数已用完，休息一下，明天再练！')
                self.limit_confirm_button()  # 确定
                if self.wait_check_start_page():
                    self.home.click_back_up_button()

            elif self.wait_check_no_word_page():  # todo 无词可练
                print("单词已练完，暂不安排新词学习！！")

            else:
                if self.wait_check_game_page():
                    self.play_word_book()  # 单词本 具体过程

        # elif self.wait_check_continue_page():  # 页面检查点
        #     print("继续单词本练习")
        #     self.word_continue_button()  # 点击 继续 按钮
        #     if self.wait_check_game_page():
        #         self.play_word_book()
        #         # 单词本 具体过程
                #  elif self.result.wait_check_again_image():
                #     self.result.more_again_button()
                #     self.play_word_book()

    @teststeps
    def play_word_book(self):
        """单词本游戏过程"""
        fs = fc = ws = vc = ll = rw = ls = 0
        vc_wse = vc_esw = va = ws_r = 0
        m_fs = m_fc = m_ws = 0
        wrong_ex = 0
        """
        以下变量均为各个游戏的计数变量
        fs：闪卡 学习模式(flash study)
        fc：闪卡 抄写模式(flash copy)
        ws：单词默写模式(新词)(word spell)
        vc：词汇选择新词模式(vocab choose)
        ll：连连看模式(link link)
        rw：还原单词模式(restore word)
        ls：单词听写模式(listen spell) 
        vc_wse：词汇选择根据单词选解释模式(复习)(vocab choose - word select explain)
        vc_esw：词汇选择根据解释选单词模式(复习)(vocab choose - explain select word)
        va：词汇运用模式(vocab apply)
        ws_r：单词默写模式(复习)(word spell recite)
        m_fs：我的单词——闪卡学习模式(mine flash study)
        m_fc: 我的单词--闪卡抄写模式(mine flash copy)
        wrong_ex :错题再练
        """
        answer = ['']  # 词汇选择的答案是否正确
        star = []  # 标星单词
        familiar = []  # 标熟单词
        familiar_add = []  # 新增的标熟单词
        star_add = []  # 新增的标星单词
        spell_word = ['']

        first_game = []  # 复习时首个游戏名称
        vocab_recite = []  # 复习词汇选择的组数
        word_spell = []  # 单词拼写(复习)的组数
        vocab_app = []  # 词汇运用正确答案数组

        while True:
            if self.wait_check_game_page():  # 页面检查点
                # 新词
                if self.wait_check_result_page():
                    break
                else:
                    if self.game_title().text == "闪卡练习(新词)":
                        """闪卡练习模式有三种情况：
                        1、点击star星标会进行闪卡抄写模式
                        2、点击熟词后会进入单词默写模式
                        3、什么都不点会进入下一游戏模式
                        """
                        if FlashCard().wait_check_study_page():  # 页面检查点
                            if fs == 0:
                                first_game.append(self.game_title().text)
                            FlashCard().study_new_word(fs, star, familiar)  # 闪卡 学习模式 游戏过程
                            fs = fs + 1

                        elif FlashCard().wait_check_copy_page():  # 页面检查点  标星
                            FlashCard().copy_new_word(fc)  # 闪卡 抄写模式 游戏过程
                            fc = fc + 1

                    elif self.game_title().text == "单词拼写(新词)":  # 标熟
                        self.spell.dictation_pattern_new(ws, spell_word)  # 单词拼写·默写模式 游戏过程
                        ws = ws + 1

                    elif self.game_title().text == "词汇选择(新词)":
                        self.vchoose.vocab_select_listen_choice(answer, vc, fc, ws, star, familiar)  # 词汇选择 听音选词 游戏过程
                        vc = vc + 1

                    elif self.game_title().text == "连连看(新词)":
                        MatchingWord().card_match(ll)  # 连连看 游戏过程
                        ll = ll + 1

                    elif self.game_title().text == "还原单词(新词)":
                        WordRestore().restore_word(rw)  # 还原单词 游戏过程
                        rw = rw + 1

                    elif self.game_title().text == "单词听写(新词)":
                        WordDictation().word_dictation(ls, answer)  # 单词听写 游戏过程
                        ls = ls + 1

                    # 错题再练
                    elif self.game_title().text == '错题再练':
                        print("系统整理了上一组的易错题，将错题再练一遍吧")
                        self.result.confirm_button()  # 开始练习按钮

                    # 复习
                    elif self.game_title().text == "词汇选择(复习)":
                        if vc_wse == 0 or vc_esw == 0:
                            first_game.append(self.game_title().text)

                        if self.vchoose.wait_check_head_page():
                            if self.vchoose.wait_check_voice_page():
                                self.vchoose.vocab_select_choice_explain(vc_wse)  # 词汇选择 选解释 游戏过程
                                vc_wse = vc_wse + 1
                            else:
                                self.vchoose.vocab_select_choice_word(vc_esw)  # 词汇选择 选单词 游戏过程
                                vc_esw = vc_esw + 1

                    elif self.game_title().text == "词汇运用(复习)":
                        if va == 0:
                            first_game.append(self.game_title().text)

                            if vc_wse == 0 and vc_esw != 0:
                                vocab_recite.append(vc_esw)
                            elif vc_esw == 0 and vc_wse != 0:
                                vocab_recite.append(vc_wse)
                            vc_wse = vc_esw = ws_r = 0

                        self.vchoose.vocab_apply(va, vocab_app)
                        va = va + 1

                    elif self.game_title().text == "单词拼写(复习)":
                        if ws_r == 0:
                            if va != 0:
                                word_spell.append(va-2)
                            va = 0

                        if self.spell.wait_check_word_random_page():  # 出现英文 则为错题再练 单词拼写 随机模式
                            self.spell.dictation_random_pattern_recite(wrong_ex)
                            wrong_ex = wrong_ex + 1

                        else:
                            self.spell.dictation_pattern_recite(ws_r, first_game, spell_word)  # 单词拼写·默写模式 游戏过程
                            ws_r = ws_r + 1

                    # 单词详情
                    elif self.game_title().text == "单词详情":
                        star_list = self.common.get_star_words()
                        familiar_list = self.common.get_familiar_words()

                        FlashCard().study_mine_word(m_fs, star_list, familiar_list, star_add, familiar_add)
                        m_fs = m_fs + 1

                    elif self.game_title().text == "闪卡练习":
                        FlashCard().copy_mine_word(m_fc, star_add)
                        m_fc = m_fc + 1

                    elif self.game_title().text == "单词拼写":
                        SpellingWord().dictation_pattern_mine(m_ws, familiar_add, spell_word)  # 单词拼写·默写模式 游戏过程
                        m_ws = m_ws + 1

                    else:
                        print('=============== 一组单词练习完毕！===============\n')
                        break

            else:
                break
        print('词汇选择组数：', vocab_recite, '单词拼写组数：', word_spell)
        return fs, ws_r, len(vocab_recite), len(word_spell), first_game  # 返回闪卡练习、单词拼写(复习)、词汇选择 的个数

