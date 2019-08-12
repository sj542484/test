import random

from app.honor.student.games.choice_single import SingleChoiceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps


class SingleChoice(SingleChoiceGame):
    """单项选择"""

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()

    @teststeps
    def play_single_choice_game(self, num, exam_json):
        """单项选择 游戏过程 """
        exam_json['单项选择'] = bank_json = {}
        for i in range(num):
            question = self.question()[0].text
            print(i+1, '.', question)

            opt_char = self.opt_char()
            opt_text = self.opt_text()
            for j in range(len(opt_char)):
                print(opt_char[j].text, '  ', opt_text[j].text)

            select_index = random.randint(0, len(opt_char)-1)
            select_char_text = opt_text[select_index].text
            opt_text[select_index].click()
            print('选择选项：', select_char_text)
            bank_json[question] = select_char_text
            self.answer.skip_operator(i, num, "单项选择", self.wait_check_single_choice_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        selected_char = [x for x in self.opt_char() if x.get_attribute('selected') == 'true']
        if len(selected_char) == 0:
            print('★★★ Error-- 跳转回来后题目完成状态发生变化')
        elif len(selected_char) == 1:
            print('题目跳转后题目状态未改变：已完成')