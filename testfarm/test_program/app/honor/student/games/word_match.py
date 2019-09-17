#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:38
# -----------------------------------------
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.game_public_element import PublicPage
from conf.decorator import teststep
from utils.get_attribute import GetAttribute


class LinkWordGame(PublicPage):
    @teststep
    def wait_check_word_match_page(self):
        locator = (By.ID, '{}mg_1'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def get_word_cards(self):
        """获取所有卡片"""
        cards = self.driver.find_elements_by_xpath('//android.widget.TextView[contains(@resource-id, "mg")]')
        return cards

    @teststep
    def is_word(self, word):
        """判断 是否为字母"""
        pattern = re.compile(r'^[A-Za-z/\-. ]+$')
        if pattern.match(word) is not None:
            return True
        else:
            return False

    @teststep
    def get_english_cards(self):
        """获取英文卡片"""
        en_cards = [x for x in self.get_word_cards() if self.is_word(x.text) and GetAttribute().selected(x) == 'false']
        return en_cards

    @teststep
    def get_not_selected_hans_card(self):
        """获取中文未被选择的卡片"""
        ch_cards = [x for x in self.get_word_cards() if not self.is_word(x.text) and GetAttribute().selected(x) == 'false']
        return ch_cards