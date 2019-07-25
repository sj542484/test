# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/8 16:07
# -------------------------------------------
import random
import re
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard
from testfarm.test_program.utils.get_attribute import GetAttribute


class SentenceStrengthen(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_sentence_page(self):
        """强化炼句页面检查点"""
        locator = (By.ID, '{}input2'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_correct_answer_page(self):
        """检查是否出现正确答案页面"""
        locator = (By.ID, '{}correct'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'explain')
        return ele.text

    @teststep
    def sentence_need_spell(self):
        """选项组 id"""
        ele = self.driver.find_element_by_id(self.id_type() + 'input2')
        return ele

    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'correct')
        return ele.text

    @teststep
    def result_explain(self):
        """解释"""
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
        for i in range(0, total_num):
            if self.wait_check_sentence_page():
                self.common.judge_next_is_true_false('false')              # 判断下一步状态
                self.common.rate_judge(total_num, i)
                explain = self.explain().strip()
                print('解释：', explain)
                sentence = self.sentence_need_spell().text  # 获取答案
                print('句子：', sentence)
                input_num = len(re.findall(r'{}', sentence))
                if i == 2:
                    if half_exit and fq == 1:
                        mine_answers.clear()
                        self.click_back_up_button()
                        break

                for j in range(input_num):
                    if fq == 1:
                        random_str = random.sample(string.ascii_letters, random.randint(2, 5))   # 随机输入2个字母
                        for x in random_str:
                            Keyboard().games_keyboard(x)
                    else:
                        right_answer = sec_answer[explain]
                        for x in right_answer[j]:
                            Keyboard().games_keyboard(x)
                    Keyboard().games_keyboard('enter')  # 点击enter键切换到下一个填空

                self.common.judge_next_is_true_false('true')
                if not self.wait_check_correct_answer_page():
                    print('★★★ 点击下一步后未出现正确答案')
                else:
                    description = self.sentence_need_spell().get_attribute('contentDescription').strip()
                    mine_answers_desc = description.split('## ')[1].split('  ')  # 拆分desc,获取输入列表
                    mine_ans = sentence.format(*mine_answers_desc)    # 格式化答案，获取完整的答案
                    print('我的答案：', mine_ans)
                    print('我输入的：', mine_answers_desc)
                    mine_answers[explain] = mine_answers_desc
                    right_answer = self.right_answer()
                    print('正确答案：', right_answer)
                    timer.append(self.common.bank_time())

                    print('-'*20, '\n')
                self.common.next_btn().click()
        self.common.judge_timer(timer)
        answer = mine_answers if fq == 1 else sec_answer
        print('我的答案：', answer)
        return answer, total_num

    @teststeps
    def sentence_strengthen_result_operate(self, mine_answer):
        right_answer = {}
        right, wrong = [], []
        explain_info = []
        if ResultPage().wait_check_answer_page():                          # 结果页
            while True:
                explains = self.result_explain()                          # 获取页面所有解释
                for i, exp in enumerate(explains):
                    exp_text = exp.text.strip()
                    if exp_text in explain_info:
                        continue
                    else:
                        result_answer = self.result_answers(exp_text)   # 获取页面的句子
                        print('解释：', exp_text)
                        print('答案：', result_answer)
                        reform_answer = self.get_right_and_mine_answer(result_answer)   # 对句子操作 获得我的和正确答案
                        print('正确答案：', reform_answer[0])
                        right_answer[exp_text] = reform_answer[0]
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
                    self.screen_swipe_up(0.5, 0.9, 0.2, 1000)
                else:
                    break

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
        wrong = re.findall(r'\((.*?)\)', ans)
        return right, wrong
