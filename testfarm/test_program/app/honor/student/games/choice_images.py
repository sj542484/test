#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:44
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.game_public_element import PublicPage
from conf.decorator import teststep


class ListenSelectImageGame(PublicPage):
    @teststep
    def wait_check_listen_image_page(self):
        """听音选图页面检查点 以题目索引id作为依据"""
        locator = (By.ID, self.id_type() + "img")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def ques_index(self):
        """问题索引"""
        ele = self.driver.find_element_by_id(self.id_type() + 'num')
        return ele.text

    @teststep
    def listen_question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sentence')
        return ele.text

    @teststep
    def image_options(self):
        """图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'img')
        return ele
