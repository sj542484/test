import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.test_paper.object_page.answer_page import AnswerPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class ClozeTest(BasePage):
    """完形填空"""

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_cl_content_page(self):
        locator = (By.ID, self.id_type() + "cl_content")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def article(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'cl_content')
        return ele.text

    @teststep
    def question(self):
        """问题 """
        ele = self.driver.find_element_by_id(self.id_type() + 'question')
        return ele.text

    @teststep
    def opt_text(self):
        """选项 文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_item')
        return ele

    @teststep
    def opt_char(self):
        """选项 字母 ABCD"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_char')
        return ele

    @teststeps
    def play_cloze_test_game(self, num, exam_json):
        """完型填空  答卷过程"""
        exam_json['完形填空'] = bank_json = {}
        text = self.article()
        print(text)
        for i in range(num):
            question = self.question()
            print('题目：', question)

            opt_chars = self.opt_char()
            opt_text = self.opt_text()
            for j in range(len(opt_chars)):   # 随机点击一个选项，然后左滑进入下一题
                print(opt_chars[j].text, ' ', opt_text[j].text)
            random_index = random.randint(0, len(opt_chars)-1)
            select_char_text = opt_text[random_index].text
            opt_text[random_index].click()
            bank_json[question] = select_char_text
            self.answer.skip_operator(i, num, "完形填空", self.wait_check_cl_content_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        select_char = [x for x in self.opt_char() if x.get_attribute('selected') == 'true']
        if len(select_char) == 0:
            print('★★★ Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')