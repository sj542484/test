from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.student.login.object_page.home_page import HomePage
from app.student.homework.object_page.homework_page import Homework
from app.student.test_paper.object_page.answer_page import AnswerPage
from app.student.word_book.object_page.sql_data.data_action import DataActionPage
from app.student.word_book.object_page.restore_word_page import WordRestore
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class RestoreWord(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.restore = WordRestore()
        self.answer = AnswerPage()
        self.common = DataActionPage()

    @teststep
    def wait_restore_word_explain_page(self):
        locator = (By.ID, self.id_type() + "tv_prompt")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele.text

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststeps
    def play_restore_word_game(self, num, exam_json):
        """还原单词"""
        exam_json['还原单词'] = bank_json = {}
        for i in range(num):
            explain = self.explain()
            print('解释：', explain)
            word_alpha = self.word_alpha()
            word = []
            for char in word_alpha:
                word.append(char.text)
            print('还原前单词：', ''.join(word))

            self.restore.drag_operate(word_alpha[0], word_alpha[-1])

            finish_word = [x.text for x in self.word_alpha()]
            final_word = ''.join(finish_word)
            print('还原后单词：', ''.join(finish_word))
            bank_json[explain] = ''.join(finish_word)
            self.answer.skip_operator(i, num, '还原单词', self.wait_restore_word_explain_page,
                                      self.judge_tip_status, final_word)

    @teststeps
    def judge_tip_status(self, final_word):
        if final_word == ''.join([x.text for x in self.word_alpha()]):
            print('跳转题目后单次顺序未发生改变')
        else:
            print("★★★ 跳转题目后单词顺序发生改变！")








