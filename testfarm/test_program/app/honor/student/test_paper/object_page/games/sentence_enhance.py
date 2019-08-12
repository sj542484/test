import random
import re
import string
import time

from app.honor.student.games.sentence_strengthen import SentenceStrengthenGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.test_paper.object_page.exam_data_handle import DataPage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard


class SentenceEnhance(SentenceStrengthenGame):

    def __init__(self):
        self.home = HomePage()
        self.common = DataPage()
        self.answer = AnswerPage()

    @teststep
    def answers(self):
        """详情页的答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_answer')
        return ele

    @teststep
    def hint(self, answer):
        """提示"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'%s')]/"
                                                "following-sibling::android.widget.TextView" % answer)
        return ele

    @teststep
    def mine(self, answer):
        """结果图标 对或错"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'%s')]/../"
                                                "following-sibling::android.widget.ImageView" % answer)
        return ele

    @teststeps
    def play_sentence_enhance_game(self, num, exam_json):
        """强化炼句 """
        exam_json['强化炼句'] = bank_json = {}
        for i in range(num):
            explain = self.sentence_explain()
            print(explain)

            sentence = self.rich_text().text
            print('提示句：', sentence)
            count = self.get_rich_text_input_count()

            word_spell = []
            alphas = random.sample(string.ascii_letters, 52)
            for j in range(len(count)):
                word_length = random.randint(3, 5)
                word = []
                for k in range(word_length):
                    index = random.randint(0, len(alphas)-1)
                    Keyboard().games_keyboard(alphas[index])
                    word.append(alphas[index])
                word_spell.append(''.join(word))
                if j != len(count)-1:
                    Keyboard().games_keyboard('enter')
            input_word = ' '.join(word_spell)
            print('我输入的：', input_word)
            bank_json[sentence] = input_word
            time.sleep(2)
            self.answer.skip_operator(i, num, '强化炼句', self.wait_check_sentence_page, self.judge_tip_status, input_word)

    @teststeps
    def judge_tip_status(self, input_word):
        desc = self.rich_text().get_attribute('contentDescription')
        if input_word in re.findall(r'\[(.*?)\]', desc)[0]:
            print('跳转后填空文本未发生变化')
        else:
            print('★★★ Error-- 跳转回来填空内容发生改变')

    @teststeps
    def sentence_enhance_detail(self, bank_info):
        """强化炼句的试卷详情"""
        tips = []
        while True:
            answers = self.answers()
            for i in range(len(answers)):
                if answers[i].text in tips:
                    continue
                else:
                    if i != len(answers) - 1:
                        tips.append(answers[i].text)
                        self.check_sentence_result(answers[i].text, bank_info)
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        tips.append(answers[i].text)
                        self.check_sentence_result(answers[i].text, bank_info)
                        self.home.screen_swipe_down(0.5, 0.6, 0.75, 1000)
            if len(tips) < len(bank_info):
                self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
            else:
                break

    @teststep
    def check_sentence_result(self, answer, bank_info):
        hint = self.hint(answer)
        mine_icon = self.mine(answer)
        print(hint.text)
        print(answer)
        split_word = answer.split(' ')
        origin_sentence = ''
        for x in split_word:
            if '(' in x:
                x = re.sub(r'(.*?)\).*?', '{}', x)
                origin_sentence += x
            else:
                origin_sentence += x + " "
        origin_sentence = origin_sentence.strip()

        main_word = [x for x in answer.split(' ') if '(' in x][0]
        mine_answer = bank_info[origin_sentence].lower()
        right_answer = re.findall(r'(.*?)\(.*?', main_word)[0]
        input_answer = re.findall(r'.*?\((.*?)\).*?', main_word)[0]
        print('正确答案：', right_answer)
        print('我的答案：', mine_answer)

        if mine_answer != input_answer:
            print('★★★ 输入单词与页面展示不一致')
        else:
            if mine_answer != right_answer:
                if mine_icon.get_attribute('selected') == "false":
                    print('答案核实正确')
                else:
                    print("★★★答案不正确但是图标显示正确！")
            else:
                if mine_icon.get_attribute('selected') == "true":
                    print('答案核实正确')
                else:
                    print("★★★答案正确但是图标显示错误！")
        print('-'*20, '\n')




