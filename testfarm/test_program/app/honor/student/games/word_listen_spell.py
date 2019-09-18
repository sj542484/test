#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:37
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class ListenSpellGame(PublicPage):
    @teststep
    def wait_check_listen_spell_word_page(self):
        locator = (By.XPATH, '//*[@text="点击喇叭听写单词"]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_answer_word_page(self):
        """判断 答案是否展示"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_voice(self):
        """声音按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'play_voice')\
            .click()

    @teststep
    def input_word(self):
        """完成的单词"""
        word = self.driver.find_element_by_id(self.id_type() + 'tv_word')
        return word.text[::2]

    @teststep
    def word_explain(self):
        """单词解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele

    @teststep
    def right_answer(self):
        """拼写单词答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return ele.text

    @teststep
    def input_wrap_side(self):
        """单词听写输入栏外侧"""
        ele = self.driver.find_element_by_id(self.id_type() + 'll_container')
        return ele
