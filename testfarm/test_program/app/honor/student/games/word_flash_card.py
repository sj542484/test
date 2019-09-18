#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:35
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.utils.games_keyboard import Keyboard


class FlashCardGame(PublicPage):
    @teststep
    def wait_check_study_page(self):
        """学习模式页面检查点"""
        locator = (By.ID, self.id_type() + "iv_rotate")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_copy_page(self):
        """抄写模式页面检查点 以键盘id作为索引"""
        locator = (By.ID, self.id_type() + "keyboard_abc_view")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_sentence_page(self):
        """以“闪卡练习 -句子模式”的句子id为依据"""
        locator = (By.ID, self.id_type() + "sentence")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def wait_check_explain_page(self):
        """判断解释是否存在"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_chinese")
            return True
        except:
            return False

    @teststep
    def wait_check_flash_result_page(self):
        """结果页页面检查点"""
        locator = (By.XPATH, "//*[@text='完成学习']")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def study_word(self):
        """页面单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_english')
        return ele.text

    @teststep
    def copy_word(self):
        """抄写页面单词"""
        ele = self.driver.find_element_by_id('{}english'.format(self.id_type()))
        return ele.text

    @teststep
    def copy_explain(self):
        """抄写模式单词解释"""
        ele = self.driver.find_element_by_id('{}chinese'.format(self.id_type()))
        return ele.text


    @teststep
    def copy_input(self):
        """抄写模式输入答案"""
        ele = self.driver.find_element_by_id('{}mine_word'.format(self.id_type()))
        return ele

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver.find_element_by_id(self.id_type() + "play_voice") \
            .click()

    def pattern_switch(self):
        """点击右上角的全英/英汉，切换模式"""
        self.driver\
            .find_element_by_id(self.id_type() + "side")\
            .click()

    @teststep
    def author(self):
        """例句推荐老师"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "author")
        return english.text

    @teststep
    def english_study(self):
        """全英模式 页面内展示的word"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "tv_english")
        return english.text

    @teststep
    def study_word_explain(self):
        """英汉模式 页面内展示的word解释"""
        explain = self.driver.find_element_by_id(self.id_type() + "tv_chinese")
        return explain

    @teststep
    def study_sentence(self):
        """全英模式 页面内展示的句子"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "sentence").text
        return english

    @teststep
    def study_sentence_explain(self):
        """英汉模式 页面内展示的句子解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "sentence_explain").text
        return explain

    @teststep
    def star_button(self):
        """星标按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "iv_star")
        return ele

    @teststep
    def familiar_button(self):
        """熟词按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "expert")
        return ele

    @teststep
    def change_model_btn(self):
        """英汉切换按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'iv_rotate')
        return ele

    @teststep
    def keyboard_operate(self, j, value):
        """点击键盘 具体操作"""
        if j == 3:
            Keyboard().games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            Keyboard().games_keyboard(value.upper())  # 点击键盘对应 大写字母
            Keyboard().games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            Keyboard().games_keyboard(value)  # 点击键盘对应字


