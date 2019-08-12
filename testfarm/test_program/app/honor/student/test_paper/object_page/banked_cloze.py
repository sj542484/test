import random
import re
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.click_bounds import ClickBounds
from utils.games_keyboard import Keyboard


class BankCloze(BasePage):
    """选词填空"""

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_hint_word_page(self):
        """提示词页面检查点"""
        locator = (By.ID, "{}md_root".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_bankcloze_page(self):
        """选词填空页面检查点"""
        locator = (By.ID, "{}prompt".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def prompt_word(self):
        """提示词"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def article(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tb_content')
        return ele

    @teststep
    def prompt_btn(self):
        """提示词"""
        ele = self.driver.find_element_by_id('{}prompt'.format(self.id_type()))
        return ele


    @teststeps
    def play_bank_cloze_game(self, num, exam_json):
        """选词填空 答卷过程 """
        exam_json['选词填空'] = bank_json = {}
        article = self.article()  # 获取文章
        print(article.text)
        self.prompt_btn().click()
        if self.wait_check_hint_word_page():
            tip = self.prompt_word()
            print(tip[0].text, tip[1].text, '\n')
            self.home.click_blank()
        else:
            print('★★★ 未发现提示词！')

        desc = article.get_attribute('contentDescription')
        position_info = re.findall(r'\[(.*?)\]', desc)  # 从属性中获取每个填空的位置
        x_position = position_info[1].split(',')
        y_position = position_info[2].split(',')
        container_position = article.location
        ClickBounds().click_bounds(int(float(x_position[0])) + container_position['x'] + 55,
                                   int(float(y_position[0])) + container_position['y'])  # 点击第一个填空
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
            self.answer.skip_operator(i, num, '选词填空', self.wait_check_bankcloze_page,
                                      self.judge_tip_status, input_word, next_page=1)
        print('我的答案：', answers, '\n')

    @teststeps
    def judge_tip_status(self, input_word):
        desc = self.article().get_attribute('contentDescription')
        if input_word in re.findall(r'\[(.*?)\]', desc)[0]:
            print('跳转后填空内容未发生变化')
        else:
            print('★★★ Error-- 跳转回来填空内容发生改变')

    @teststeps
    def bank_cloze_detail(self, bank_info):
        """选词填空 试卷详情页"""
        article = self.article()
        print(article.text)
        desc = article.get_attribute('contentDescription')
        answers = re.findall(r'\[(.*?)\]', desc)[0]
        print('正确答案：', answers)

        print('我的答案：', ', '.join(list(bank_info.values())))



