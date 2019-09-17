#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/2 9:03
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.game_public_element import PublicPage
from conf.decorator import teststep


class ListenLinkSentenceGame(PublicPage):

    @teststep
    def wait_check_listen_sentence_page(self):
        """听音连句页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_btn_page(self):
        """检查是否存在清除按钮"""
        locator = (By.ID, '{}clear'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def listen_link_clear_btn(self):
        """听音连句"""
        ele = self.driver.find_element_by_id(self.id_type() + 'clear')
        return ele

    @teststep
    def text_for_select(self):
        """下方可点击的文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + "text")
        return [x for x in ele if x.text]

    @teststep
    def right_sentence_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_right')
        return ele.text

    @teststep
    def sentence_explain(self):
        """解释"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_explain')
        return ele


