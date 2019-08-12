import random
import re
import string
import time
from app.honor.student.games.article_select_blank import SelectBlankGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps
from utils.games_keyboard import Keyboard


class BlankCloze(SelectBlankGame):
    """选词填空"""

    def __init__(self):
        self.answer = AnswerPage()

    @teststeps
    def play_bank_cloze_game(self, num, exam_json):
        """选词填空 答卷过程 """
        exam_json['选词填空'] = bank_json = {}
        article = self.rich_text()  # 获取文章
        print(article.text)
        self.hint_btn().click()
        if self.wait_check_hint_content_page():
            print("提示词：", self.hint_answer())
            HomePage().click_blank()
        else:
            print('★★★ 未发现提示词！')

        answers = []
        for i in range(num):   # 其他点击回车键顺序填空，填空的文本为26个字母随机填写3-6个
            alphas = random.sample(string.ascii_letters, 52)
            length = random.randint(3, 6)
            random_input = []
            for j in range(length):
                index = random.randint(0, len(alphas)-1)
                Keyboard().games_keyboard(alphas[index])
                random_input.append(alphas[index])
                if j == length - 1:
                    Keyboard().games_keyboard('enter')
                    time.sleep(1)
            answers.append(''.join(random_input))
            input_word = ''.join(random_input).lower()
            print('我输入的：', input_word)
            bank_json[i] = input_word
            self.answer.skip_operator(i, num, '选词填空', self.wait_check_select_blank_page,
                                      self.judge_tip_status, input_word, next_page=1)
        print('我的答案：', answers, '\n')

    @teststeps
    def judge_tip_status(self, input_word):
        desc = self.rich_text().get_attribute('contentDescription')
        if input_word in re.findall(r'\[(.*?)\]', desc)[0]:
            print('跳转后填空内容未发生变化')
        else:
            print('★★★ Error-- 跳转回来填空内容发生改变')

    @teststeps
    def bank_cloze_detail(self, bank_info):
        """选词填空 试卷详情页"""
        article = self.rich_text()
        print(article.text)
        desc = article.get_attribute('contentDescription')
        answers = re.findall(r'\[(.*?)\]', desc)[0]
        print('正确答案：', answers)

        print('我的答案：', ', '.join(list(bank_info.values())))



