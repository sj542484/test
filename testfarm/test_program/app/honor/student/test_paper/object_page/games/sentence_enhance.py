import random
import re
import string
import time

from app.honor.student.games.sentence_strengthen import SentenceStrengthenGame
from app.honor.student.login.object_page.home_page import HomePage
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
    def result_answer(self, explain):
        """详情页的答案"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'%s')]/"
                                                "preceding-sibling::android.widget.TextView" % explain)
        return ele.text

    @teststep
    def result_explains(self):
        """提示"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_hint')
        return ele

    @teststep
    def right_wrong_icon(self, explain):
        """结果图标 对或错"""

        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'{}')]/../following-sibling"
                                                "::android.widget.ImageView".format(explain))
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
            for j in range(count):
                word_length = random.randint(3, 5)
                word = []
                for k in range(word_length):
                    index = random.randint(0, len(alphas)-1)
                    Keyboard().games_keyboard(alphas[index])
                    word.append(alphas[index])
                word_spell.append(''.join(word))
                if j != count-1:
                    Keyboard().games_keyboard('enter')
            input_word = ' '.join(self.rich_text().text.split())
            print('我输入的：', input_word)
            bank_json[explain] = input_word
            time.sleep(2)
            self.answer.skip_operator(i, num, '强化炼句', self.wait_check_sentence_page, self.judge_tip_status, input_word)

    @teststeps
    def judge_tip_status(self, input_word):
        page_input_text = ' '.join(self.rich_text().text.split())
        if input_word == page_input_text:
            print('跳转后填空文本未发生变化')
        else:
            print('★★★ Error-- 跳转回来填空内容发生改变')

    @teststeps
    def sentence_enhance_detail(self, bank_info):
        """强化炼句的试卷详情"""
        tips = []
        while len(tips) < len(bank_info):
            result_explain = self.result_explains()
            for explain in result_explain:
                if explain.text in tips:
                    continue
                else:
                    tips.append(explain.text)
                    self.check_sentence_result(explain.text, bank_info)
            self.home.screen_swipe_up(0.5, 0.8, 0.3, 1000)

    @teststep
    def check_sentence_result(self, result_explain, bank_info):
        print("解释：", result_explain)
        mine_icon = self.right_wrong_icon(result_explain)
        answer = self.result_answer(result_explain)
        mine_answer = bank_info[result_explain][:-2]
        right_answer = ' '.join(re.findall(r'(.*?)\(.*?\).*?', answer))
        input_answer = ' '.join(re.findall(r'.*?\((.*?)\).*?', answer))
        print('正确答案：', right_answer)
        print('我的答案：', mine_answer)
        print('页面输入答案：', input_answer)

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





