#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:46
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class SentenceStrengthenGame(PublicPage):

    @teststep
    def wait_check_sentence_page(self):
        """强化炼句页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
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
    def sentence_explain(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'explain')
        return ele.text


    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'correct')
        return ele.text



