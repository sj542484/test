#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:45
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class VocabChoiceGame(PublicPage):
    @teststep
    def wait_check_head_page(self):
        """判断是否有题目"""
        locator = (By.ID, "{}tv_head".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_voice_page(self):
        """以“词汇选择 -句子选单词模式”的 提示按钮 为依据"""
        locator = (By.ID, self.id_type() + "sound")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_explain_page(self):
        """单词解释"""
        locator = (By.ID, self.id_type() + "explain")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_vocab_apply_explain_page(self):
        """词汇运用解释页面检查点"""
        locator = (By.ID, self.id_type() + "tv_explain")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_listen_explain_page(self):
        """词汇运用解释页面检查点"""
        locator = (By.ID, self.id_type() + "explain")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def vocab_question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_head')
        return ele

    @teststep
    def vocab_options(self):
        """选项"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'option')
        return ele

    @teststep
    def vocab_right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_accessibility_id('true')
        return ele.text

    @teststep
    def vocab_word_explain(self):
        """听音选词的单词解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'explain')
        return ele

    @teststep
    def listen_choice_speak_icon(self):
        """听音选词的上方喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "iv_speak")
        return ele

    @teststep
    def apply_hint_button(self):
        """提示按钮"""
        ele = self.driver \
                  .find_element_by_id(self.id_type() + "hint")
        return ele

    @teststep
    def apply_sentence_explain(self):
        """点击 提示按钮后，出现中文解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return explain



