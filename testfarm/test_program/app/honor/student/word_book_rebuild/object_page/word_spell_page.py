from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard


class WordSpell(BasePage):

    def __init__(self):
        self.key = Keyboard()

    @teststeps
    def word_explain(self):
        explain = self.driver.find_element_by_id(self.id_type() + "tv_explain").text
        return explain

    @teststeps
    def spelling_play(self, data):
        explain = self.word_explain()
        word = data[explain]

        for j in range(0, len(word)):
            if j == 4:
                self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                self.key.games_keyboard(word[j].upper())  # 点击键盘对应 大写字母
            else:
                if j == 5:
                    self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                    self.key.games_keyboard(word[j].lower())  # 点击键盘对应字母