#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:38
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class GuessWordGame(PublicPage):
    """猜词游戏"""
    @teststep
    def wait_check_guess_word_page(self):
        """"""
        locator = (By.ID, 'level')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def keyboard(self):
        """键盘"""
        ele = self.driver.find_element_by_id(self.id_type() + "hm_keyboard")
        return ele

    @teststep
    def keyboard_key(self):
        ele = self.driver.find_elements_by_xpath('//*[@resource-id="{}hm_keyboard"]/'
                                                 'android.widget.TextView'.format(self.id_type()))
        return ele

    @teststep
    def word_explain(self):
        """翻译"""
        ele = self.driver.find_element_by_id(self.id_type() + 'chinese')
        return ele.text

    @teststep
    def guess_word(self):
        """单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'english')
        return ele.text