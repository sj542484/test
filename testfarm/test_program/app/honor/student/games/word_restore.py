#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:37
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep, teststeps


class RestoreWordGame(PublicPage):

    @teststep
    def wait_restore_word_explain_page(self):
        """还原单词页面检查点"""
        locator = (By.ID, self.id_type() + "tv_prompt")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_restore_answer_word_page(self):
        """还原单词页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[@resource-id = '
                             '"com.vanthink.student.debug:id/tv_word" and @index=1]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def word_explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def word(self, index=0):
        """展示的 待还原的单词"""
        word = self.driver.find_elements_by_xpath('//android.widget.TextView[@resource-id= '
                                                  '"com.vanthink.student.debug:id/tv_word" and @index={}]'.format(index))
        return word

    @teststep
    def voice(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_sound')
        return ele

    @teststep
    def button_swipe(self, from_x, from_y, to_x, to_y, steps=1000):
        """拖动单词button"""
        self.driver.swipe(from_x, from_y, to_x, to_y, steps)

    @teststep
    def get_element_location(self, ele):
        """获取元素坐标"""
        x = ele.location['x']
        y = ele.location['y']
        return x, y

    @teststeps
    def drag_operate(self, word2, word):
        """拖拽 操作"""
        loc = self.get_element_location(word2)
        y2 = self.get_element_location(word)[1] - 40
        self.button_swipe(loc[0], loc[1], loc[0], y2, 1000)
        time.sleep(1)
