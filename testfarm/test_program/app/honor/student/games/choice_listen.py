#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:42
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.game_public_element import PublicPage
from conf.decorator import teststep


class ListenChoiceGame(PublicPage):
    @teststep
    def wait_check_listen_select_page(self):
        """听力选择页面 以选项id作为依据"""
        locator = (By.ID, self.id_type() + "fab_audio")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_red_hint_page(self):
        """红色提示检查点"""
        locator = (By.ID, self.id_type() + "tv_hint")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def red_hint(self):
        """红色提示"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_hint')
        return ele.text

    @teststep
    def voice_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id('{}fab_audio'.format(self.id_type()))
        return ele

