import random
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class GuessingWord(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()

    @teststep
    def wait_check_guessing_img_page(self):
        locator = (By.ID, self.id_type() + "level")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """解释 """
        ele = self.driver.find_element_by_id(self.id_type() + 'chinese')
        return ele.text

    @teststep
    def word_need_write(self):
        """填写前字样"""
        ele = self.driver.find_element_by_id(self.id_type() + 'english')
        return re.sub('-', '', ele.text)

    @teststep
    def finish_word(self):
        """完成后 单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'english')
        return re.sub('-', '', ele.text)

    @teststep
    def keyboard(self):
        """键盘"""
        ele = self.driver.find_element_by_id(self.id_type() + 'hm_keyboard')
        return ele

    @teststep
    def key_alpha(self):
        """键盘 中的字母"""
        ele = self.keyboard().find_elements(By.CLASS_NAME, 'android.widget.TextView')
        return ele

    @teststeps
    def play_guessing_word_game(self, num, exam_json):
        """猜词游戏 """
        exam_json['猜词游戏'] = bank_json = {}
        for i in range(num):
            explain = self.explain()
            print('解释：', explain)

            word = self.word_need_write()
            print('填充前单词：', word)

            key_put = []
            while True:
                word = self.word_need_write()
                alphas = self.key_alpha()
                keys = []
                for k in range(len(alphas)):
                    if alphas[k].get_attribute('enabled') == 'true':
                        keys.append(alphas[k])

                if '_' in word:
                    for j in range(2):
                        random_index = random.randint(0, len(keys)-1)
                        keys[random_index].click()
                        key_put.append(keys[random_index].text)
                else:
                    break

            print('我输入的单词：', ''.join(key_put))
            bank_json[explain] = ''.join(key_put)
            finish_word = self.finish_word()
            print('最终提示单词：', finish_word)
            self.answer.skip_operator(i, num, '猜词游戏', self.wait_check_guessing_img_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        if '_' in self.word_need_write():
            print('★★★ Error-- 跳转回来题目处于未完成状态')
        else:
            print('滑屏后题目处于完成状态')