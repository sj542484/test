#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:47
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class LinkWordToSentenceGame(PublicPage):
    @teststep
    def wait_check_link_sentence_page(self):
        """连词成句页面检查点"""
        locator = (By.ID, '{}tv_prompt'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def wait_check_right_answer_page(self):
        """检查是否出现正确答案"""
        locator = (By.ID, '{}tv_sentence'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def sentence_explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele.text

    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_sentence')
        return ele.text
