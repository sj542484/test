# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/8 16:07
# -------------------------------------------
import random
import re
import string
import time
from app.honor.student.games.sentence_strengthen import SentenceStrengthenGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class SentenceStrengthen(SentenceStrengthenGame):

    def __init__(self):
        self.common = LibraryPubicPage()

    @teststep
    def result_explains(self):
        """结果页解释"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_hint')
        return ele

    @teststep
    def result_answers(self, explain):
        """答案"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/preceding-sibling::android.widget.TextView'
                                                .format(explain))
        return ele.text

    @teststep
    def mine_icon(self, explain):
        """对错标识"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../following-sibling::android.widget.ImageView'
                                                .format(explain))
        return ele

    @teststeps
    def sentence_strengthen_operate(self,  fq, sec_answer, half_exit):
        """强化炼句游戏过程"""
        timer = []
        mine_answers = {}
        total_num = self.common.rest_bank_num()
        for i in range(total_num):
            if self.wait_check_sentence_page():
                self.next_btn_judge('false', self.fab_commit_btn)              # 判断下一步状态
                self.common.rate_judge(total_num, i)
                explain = self.sentence_explain().strip()
                print('解释：', explain)
                sentence = self.rich_text().text  # 获取答案
                print('句子：', sentence)

                input_num = self.get_rich_text_input_count()
                if i == 2:
                    if half_exit and fq == 1:
                        mine_answers.clear()
                        self.click_back_up_button()
                        break
                if fq == 1:
                    print('需要输入单词', input_num)
                    for j in range(input_num):
                        random_str = random.sample(string.ascii_letters, random.randint(2, 4))   # 随机输入2个字母
                        for x in random_str:
                            Keyboard().games_keyboard(x)
                        time.sleep(0.5)
                        Keyboard().games_keyboard('enter')
                else:
                    right_answer = sec_answer[explain]
                    reform_right_answer = right_answer.split(' ')
                    reform_sentence = re.sub(r'\s{4}[, ?]', '{}', sentence).replace('{}', '{} ').replace('  ', ' ').strip().split(' ')
                    print("分割正确答案：", reform_right_answer)
                    print("分割页面原句：", reform_sentence)
                    right_input_words = [x for x, y in zip(reform_right_answer, reform_sentence) if x not in y]
                    for word in right_input_words:
                        for x in list(word):
                            Keyboard().games_keyboard(x)
                        time.sleep(0.5)
                        Keyboard().games_keyboard('enter')

                if not self.wait_check_correct_answer_page():
                    print('★★★ 点击下一步后未出现正确答案')
                else:
                    desc = self.rich_text().get_attribute('contentDescription')
                    mine_answers_desc = re.findall(r'\w+', desc.split('##')[1])
                    print('我的答案：', ' '.join(self.rich_text().text.split()))
                    print('我输入的：', mine_answers_desc)
                    mine_answers[explain] = mine_answers_desc
                    right_answer = self.right_answer()
                    print('正确答案：', right_answer)
                    timer.append(self.common.bank_time())

                self.fab_next_btn().click()
                time.sleep(2)
                print('-'*20, '\n')

        self.common.judge_timer(timer)
        answer = mine_answers if fq == 1 else sec_answer
        print('我的答案：', answer)
        return answer, total_num

    @teststeps
    def sentence_strengthen_result_operate(self, mine_answer):
        """强化炼句结果页处理"""
        right_answer = {}
        right, wrong = [], []
        explain_info = []
        if ResultPage().wait_check_answer_page():                          # 结果页
            while True:
                explains = self.result_explains()                          # 获取页面所有解释
                for i, exp in enumerate(explains):
                    exp_text = exp.text.strip()
                    if exp_text in explain_info:
                        continue
                    else:
                        explain_info.append(exp_text)
                        result_answer = self.result_answers(exp_text)   # 获取页面的句子
                        print('解释：', exp_text)
                        print('答案：', result_answer)
                        reform_answer = self.get_right_and_mine_answer(result_answer)   # 对句子操作 获得我的和正确答案
                        right_result_answer = ' '.join([x.split('(')[0] for x in result_answer.split(' ') if x != ''])
                        print('正确答案：', right_result_answer)
                        right_answer[exp_text] = right_result_answer
                        mine_icon = self.mine_icon(exp_text)
                        if '(' in result_answer:
                            if mine_answer[exp_text] != reform_answer[1]:
                                print('★★★ 输入的答案与页面展示的不一致')

                            if GetAttribute().selected(mine_icon) == 'true':
                                print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                            else:
                                print('图标验证正确')
                            wrong.append(exp_text)

                        else:
                            if GetAttribute().selected(mine_icon) == 'false':
                                print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                            else:
                                print('图标验证正确')
                            right.append(exp_text)
                        print('-' * 20, '\n')

                if len(right_answer) != len(mine_answer):
                    self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
                else:
                    break
        print('正确答案：', right_answer)
        self.click_back_up_button()
        return wrong, right, right_answer

    @teststep
    def get_right_and_mine_answer(self, ans):
        """获取正确答案和我的答案"""
        reform, right = [], []
        for x in ans.split(' '):
            if '(' in x:
                right.append(x.split('(')[0])
                reform.append(x.split('(')[1].replace(')', ''))
            else:
                reform.append(x)
        mine_ans = ' '.join(reform).strip()
        print('我的答案：', mine_ans)
        print('正确填空单词为：', right)
        wrong = re.findall(r'\((.*?)\)', ans)
        return right, wrong
