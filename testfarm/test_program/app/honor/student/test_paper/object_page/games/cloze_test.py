
import random
from app.honor.student.games.article_cloze import ClozeGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps


class ClozeTest(ClozeGame):
    """完形填空"""

    def __init__(self):
        self.answer = AnswerPage()

    @teststeps
    def play_cloze_test_game(self, num, exam_json):
        """完型填空  答卷过程"""
        exam_json['完形填空'] = bank_json = {}
        text = self.rich_text()
        print(text)
        for i in range(num):
            question = self.question()[0].text
            print('题目：', question)

            opt_chars = self.opt_char()
            opt_text = self.opt_text()
            for j in range(len(opt_chars)):   # 随机点击一个选项，然后左滑进入下一题
                print(opt_chars[j].text, ' ', opt_text[j].text)
            random_index = random.randint(0, len(opt_chars)-1)
            select_char_text = opt_text[random_index].text
            opt_text[random_index].click()
            bank_json[question] = select_char_text
            self.answer.skip_operator(i, num, "完形填空", self.wait_check_cloze_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        select_char = [x for x in self.opt_char() if x.get_attribute('selected') == 'true']
        if len(select_char) == 0:
            print('★★★ Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')