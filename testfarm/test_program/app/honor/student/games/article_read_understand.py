#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:49
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class ReadUnderstandGame(PublicPage):

    @teststep
    def wait_check_read_understand_page(self):
        locator = (By.ID, self.id_type() + "rich_text")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


