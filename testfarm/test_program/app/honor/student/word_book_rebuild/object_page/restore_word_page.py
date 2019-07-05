import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.data_action import DataActionPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep


class WordRestore(BasePage):
    """还原单词"""

    @teststep
    def wait_check_word_restore_page(self):
        locator = (By.ID, '{}tv_prompt'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def prompt(self):
        """展示的提示词"""
        ele = self.driver \
            .find_element_by_id("{}tv_prompt".format(self.id_type())).text
        return ele

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id("{}fab_sound".format(self.id_type())) \
            .click()

    @teststep
    def word(self):
        """展示的 待还原的单词"""
        word = self.driver \
            .find_elements_by_xpath('//android.widget.TextView[@resource-id="{}tv_word" and @index=0]'.format(self.id_type()))
        return word

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

    @teststeps
    def restore_word(self, i, new_word):
        if i == 0:
            print('\n还原单词模式(新词)\n')

        self.click_voice()  # 听力按钮
        Homework().next_button_operate('false')

        explain = self.prompt()  # 展示的提示词
        english = new_word[explain]
        print("英文解释：%s" % explain)

        before_word = ''
        alphas = self.word()

        for j in range(0, len(alphas)):
            before_word = before_word + alphas[j].text
        print("还原前单词为：", before_word)
        self.restore_word_core(english)
        print('还原后单词为：%s' % english)
        time.sleep(4)
        print('----------------------------------')

    @teststep
    def restore_word_core(self, english):
        """还原单词主要步骤"""
        index = 0
        count = 0
        sort_word = ''
        while True:
            alphas = self.word()
            for x in range(count, len(alphas)):
                alpha_len = len(alphas[x].text)
                if index + alpha_len >= len(english) - 1:
                    english += ' ' * alpha_len
                word_part = ''.join([english[x] for x in range(index, index + alpha_len)])

                if alphas[x].text == word_part.strip():
                    if count != x:
                        self.drag_operate(alphas[x], alphas[count])
                        sort_word = ''.join([k.text for k in self.word()])
                    index += alpha_len
                    count += 1
                    break

            if english.strip() == sort_word:
                break
