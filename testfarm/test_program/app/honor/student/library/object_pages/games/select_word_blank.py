# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/9 15:01
# -------------------------------------------
import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.article_select_blank import SelectBlankGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from app.honor.student.library.object_pages.result_page import ResultPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class SelectWordBlank(SelectBlankGame):
    """选词填空"""

    def __init__(self):
        self.common = LibraryPubicPage()

    @teststeps
    def select_word_blank_operate(self, fq, sec_answer):
        """选词填空游戏过程"""
        timer = []
        mine_answer = {}
        print(self.wait_check_select_blank_page())
        if self.wait_check_select_blank_page():
            total_num = self.common.rest_bank_num()
            if self.wait_check_hint_btn_page():
                self.hint_btn().click()              # 点击提示词，检验提示页面是否出现
                if not self.wait_check_hint_content_page():
                    print('★★★ 点击提示词按钮未出现提示词')
                else:
                    print('提示词：', self.hint_answer())
                HomePage().click_blank()
            if self.wait_check_select_blank_page():
                content = self.rich_text()
                print(content.text)
                for i in range(total_num):
                    if self.wait_check_select_blank_page():
                        self.next_btn_judge('false', self.fab_commit_btn)          # 判断下一步状态
                        self.common.rate_judge(total_num, i)

                        if fq == 1:
                            random_str = ''.join(random.sample(string.ascii_letters, 2))
                            for x in random_str:
                                Keyboard().games_keyboard(x)
                            mine_answer[i] = random_str

                        else:
                            right_answer = sec_answer[i]
                            for x in right_answer:
                                Keyboard().games_keyboard(x)

                    timer.append(self.common.bank_time())
                    if i != total_num - 1:
                        Keyboard().games_keyboard('enter')
                    timer.append(self.common.bank_time())

                print('我的答案：', mine_answer)

            self.common.judge_timer(timer)
            self.check_position_change()
            self.next_btn_operate('true', self.fab_commit_btn)  # 判断下一步状态
            answer = mine_answer if fq == 1 else sec_answer
            return answer, total_num

    @teststep
    def select_word_blank_result_operate(self, mine_answer):
        """选词填空结果页操作"""
        right_answer = {}
        right, wrong = [], []
        index = 0
        if ResultPage().wait_check_answer_page():
            if self.wait_check_hint_btn_page():
                self.hint_btn().click()                   # 点击提示词，校验是否出现提示答案页面
                if not self.wait_check_hint_content_page():
                    print('★★★ 点击提示词按钮未出现提示词')
                else:
                    print('提示词：', self.hint_answer())
                HomePage().click_blank()
            content = self.rich_text()          # 从desc中获取正确答案
            content_desc = content.get_attribute('contentDescription')
            answers = [x for x in content_desc.split('## ')[1].strip().split('  ') if '(' not in x]
            print("正确答案：", answers)
            for i in range(len(answers)):                  # 将正确答案与输入的答案依次对比，并根据对错存入数组中
                if answers[i] != mine_answer[i]:
                    wrong.append(answers[i])
                    right_answer[index] = answers[i]
                    index += 1
                else:
                    right.append(answers[i])
        print('正确答案：', right_answer)
        self.click_back_up_button()
        return wrong, right, right_answer


