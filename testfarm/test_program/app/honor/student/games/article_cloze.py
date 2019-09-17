#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:49
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.game_public_element import PublicPage
from conf.decorator import teststep


class ClozeGame(PublicPage):
    """完型填空游戏"""
    @teststep
    def wait_check_cloze_page(self):
        """完形填空页面检查点"""
        locator = (By.ID, self.id_type() + "rich_text")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False




