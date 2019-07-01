import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.student.login.object_page.home_page import HomePage
from app.student.test_paper.object_page.answer_page import AnswerPage
from app.student.test_paper.object_page.banked_cloze import BankCloze
from app.student.test_paper.object_page.cloze_test import ClozeTest
from app.student.test_paper.object_page.complete_text import CompleteText
from app.student.test_paper.object_page.conjunctions import Conjunctions
from app.student.test_paper.object_page.guessing_word import GuessingWord
from app.student.test_paper.object_page.listen_select import ListenSelect
from app.student.test_paper.object_page.listen_spell import ListenSpell
from app.student.test_paper.object_page.listen_to_sentence import ListenSentence
from app.student.test_paper.object_page.read_understand import ReadUnderstand
from app.student.test_paper.object_page.restore_word import RestoreWord
from app.student.test_paper.object_page.sentence_enhance import SentenceEnhance
from app.student.test_paper.object_page.sentence_exchange import SentenceExchange
from app.student.test_paper.object_page.single_choice import SingleChoice
from app.student.test_paper.object_page.vocab_select import VocabSelect
from app.student.test_paper.object_page.word_match import WordMatch
from app.student.test_paper.object_page.word_spell import WordSpell
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv


class ExamPage(BasePage):
    """试卷页面"""

    def __init__(self):
        self.home = HomePage()
        self.game = VocabSelect()
        self.answer = AnswerPage()

    @teststep
    def wait_check_exam_title_page(self):
        """以 试卷的标题作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'试卷')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_exam_counter_page(self):
        """以 做试卷时的计时作为 页面检查点"""
        locator = (By.ID, self.id_type() + "time_container")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_exam_confirm_page(self):
        """以 试卷确认的标题作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'试卷确认')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_rank_page(self):
        """以 炫耀一下的text作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'炫耀一下')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_end_page(self):
        """等待 滑到底提示"""
        try:
            self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"到底啦 下拉刷新试试")]')
            return True
        except:
            return False

    @teststep
    def exam_names(self):
        """试卷名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_name')
        return ele

    @teststep
    def finish_count(self):
        """完成人数"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_finishcount')
        return ele

    @teststep
    def finish_status(self):
        """完成状态"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'rtv_mode')
        return ele

    @teststep
    def get_all_text(self):
        """获取所有文本"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def click_start_exam_button(self):
        """点击 开始考试"""
        self.driver.\
            find_element_by_id(self.id_type() + 'start_write')\
            .click()

    @teststep
    def index_group(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'recyclerview')
        return ele

    @teststep
    def close_answer(self):
        """关闭答题卷页面"""
        self.driver.find_element_by_id(self.id_type() + 'answerclose').click()

    @teststep
    def exam_back_to_home(self):
        self.home.click_back_up_button()
        if self.wait_check_exam_title_page():
            self.home.click_back_up_button()
            if self.home.wait_check_home_page():
                print('返回主页面')

    @teststeps
    def select_one_exam(self, exam_index):
        """随机选择一个试卷"""
        exams_info = {}     # 将试卷存入一个字典当周，以试卷名作为key，试卷描述与完成状态作为value
        while True:
            exams = self.exam_names()
            finish_status = self.finish_status()  # 试卷完成状态
            finish_count = self.finish_count()   # 试卷几人完成
            for i in range(len(exams)):
                exams_info[exams[i].text] = finish_status[i].text + ' -- '+finish_count[i].text
            if not self.wait_check_end_page():  # 没有发现滑动到底的则进行滑动
                self.home.screen_swipe_up(0.5, 0.9, 0.7, 1000)
            else:
                # exams_info[exams[-1].text] = finish_status[-1].text + ' -- ' + finish_count[-1].text
                self.home.screen_swipe_down(0.5, 0.2, 0.9, 1000)
                break

        for name in exams_info.keys():
            print(name, '   ', exams_info[name])

        exam = self.exam_names()[exam_index]
        test_name = exam.text
        print('选择试卷：', test_name)
        exam.click()
        print('------------------------------\n')
        return test_name

    @teststeps
    def exam_confirm_ele_operate(self):
        """确认页面 文本展示"""
        ele = self.get_all_text()
        print('\n<试卷确认页面>：\n')
        self.print_exam_info(ele)
        print(ele[14].text + '\n' + ele[15].text + '\n' + ele[16].text + '\n' + ele[17].text)  # 说明
        print('--------------------------------\n')
        return int(ele[9].text)

    @teststep
    def print_exam_info(self, ele):
        """打印出试卷头部信息"""
        print(ele[1].text, ':', ele[2].text)     # 试卷名称
        print(ele[5].text, ':', ele[3].text+ele[4].text)  # 试卷模式
        print(ele[8].text, ':', ele[6].text+ele[7].text)  # 时间
        print(ele[11].text, ':', ele[9].text+ele[10].text)  # 题数
        print(ele[13].text, ':', ele[12].text)  # 限制

    @teststeps
    def get_ques_name(self, total):
        """获取所有题型"""
        if self.wait_check_exam_counter_page():
            self.answer.answer_check_button().click()
            if self.answer.wait_check_answers_page():
                tip_num = []
                tips = []
                while True:
                    titles = self.answer.question_titles()
                    ele = self.get_all_text()
                    last_text_attr = ele[-2].get_attribute('resourceId')

                    for i in range(len(titles) - 1):
                        if titles[i].text in tips:
                            continue
                        else:
                            self.print_ques_type(titles[i].text, tip_num, tips)

                    if last_text_attr == self.id_type() + 'rtv_num'\
                    or last_text_attr == self.id_type() + 'tv_sheet_num':
                        self.home.screen_swipe_up(0.5, 0.878, 0.7, 1000)
                        self.print_ques_type(titles[-1].text, tip_num, tips)

                    if sum(tip_num) < total:
                        self.home.screen_swipe_up(0.5, 0.9, 0.3, 2000)
                    else:
                        break

                self.close_answer()
                print('--------------------------------\n')
                return tips

    @teststep
    def print_ques_type(self, title, tip_num, tips):
        """打印题型 和题目个数"""
        ques_num = self.answer.ques_num(title)
        num = int(''.join(re.findall(r'\d', ques_num)))
        tips.append(title)
        print(title, ' ', ques_num)
        tip_num.append(num)

    @teststeps
    def play_examination(self, tips, exam_json):
        """做题过程"""
        if self.wait_check_exam_counter_page():
            self.answer.answer_check_button().click()   # 查看答题卷
            if self.answer.wait_check_answers_page():
                index = 0
                while index < len(tips):
                    title_list = [x.text for x in self.answer.question_titles()]       # 题型数组
                    if tips[index] in title_list:
                        first_index = self.answer.tip_index(tips[index])    # 题型的第一道题
                        ques_num = self.answer.ques_num(tips[index])          # 题数描述 （共*题）
                        num = int(''.join(re.findall(r'\d+', ques_num)))  # 从描述中获取题数
                        first_index[0].click()     # 点击第一题进入习题
                        self.exam_process(tips[index], num, exam_json)   # 对应习题的游戏过程
                        self.answer.answer_check_button().click()    # 游戏结束后点击答题卷进入下一题
                        if self.answer.wait_check_answers_page():
                            pass
                        index = index + 1
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.4, 2000)

                if self.answer.wait_check_answers_page():
                    self.answer.submit_tip_operate()  # 交卷
                    if self.wait_check_rank_page():
                        self.exam_back_to_home()  # 返回

    @teststeps
    def exam_process(self, title, num, exam_json):
        print('\n-------%s-共%d题------\n' % (title, num))
        if title == '听后选择':
            ListenSelect().play_listening_select_game(num, exam_json)
            self.answer.wait_result_btn_enabled()
            # pass

        elif title == '猜词游戏':
            GuessingWord().play_guessing_word_game(num, exam_json)
            # pass

        elif title == '单项选择':
            SingleChoice().play_single_choice_game(num, exam_json)
            # pass

        elif title == '连词成句':
            Conjunctions().play_conjunctions_game(num, exam_json)
             # pass

        elif title == '连连看':
            WordMatch().play_word_match_game(num, exam_json)
            # pass

        elif title == '句型转换':
            SentenceExchange().play_sentence_exchange_game(num, exam_json)
            # pass

        elif title == '完形填空':
            ClozeTest().play_cloze_test_game(num, exam_json)
            # pass

        elif title == '还原单词':
            RestoreWord().play_restore_word_game(num, exam_json)
            # pass

        elif title == '选词填空':
            BankCloze().play_bank_cloze_game(num, exam_json)
            # pass

        elif title == '强化炼句':
            SentenceEnhance().play_sentence_enhance_game(num, exam_json)
            # pass

        elif title == '补全文章':
            CompleteText().play_complete_article_game(num, exam_json)
            # pass

        elif title == '听音连句':
            ListenSentence().play_listen_sentence_game(num, exam_json)
            # pass

        elif title == '词汇选择':
            VocabSelect().play_vocab_select_game(num, exam_json)
            # pass

        elif title == '阅读理解':
            ReadUnderstand().play_read_understand_game(num, exam_json)
            # pass

        elif title == '单词拼写':
            WordSpell().play_word_spell_game(num, exam_json)
            # pass

        elif title == '单词听写':
            ListenSpell().play_listen_spell_game(num, exam_json)
            # pass

        else:
            pass
















