#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:37
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class SpellWordGame(PublicPage):
    @teststep
    def wait_check_normal_spell_page(self):
        """单词拼写(默写模式)页面检查点"""
        locator = (By.ID, self.id_type() + "underline")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_tv_word_or_random_page(self):
        """单词拼写（随机模式）页面检查点"""
        locator = (By.ID, self.id_type() + "tv_word")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_right_answer_page(self):
        """正确单词页面检查点"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_hint_page(self):
        """默写模式页面检查点"""
        locator = (By.ID, self.id_type() + "hint")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_hint_word_page(self):
        """提示字母页面检查点"""
        locator = (By.ID, self.id_type() + "tv_word")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def word_explain(self):
        """拼写翻译"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele

    @teststep
    def hint_btn(self):
        """提示按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'hint')
        return ele

    @teststep
    def spell_word(self):
        """拼写单词"""
        word = self.driver.find_element_by_id(self.id_type() + 'tv_word')
        return word.text

    @teststep
    def right_answer_word(self):
        word = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return word.text

