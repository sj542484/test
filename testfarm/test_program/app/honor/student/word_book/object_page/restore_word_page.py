import time

from app.student.homework.object_page.homework_page import Homework
from app.student.word_book.object_page.sql_data.data_action import DataActionPage
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep


class WordRestore(BasePage):
    def __init__(self):
        self.common = DataActionPage()

    """还原单词"""
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
            .find_elements_by_xpath('//android.widget.TextView[@resource-id="com.vanthink.student.debug:id/tv_word" and @index=0]')
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
                if index + alpha_len >= len(english)-1:
                    english += ' '*alpha_len
                word_part = ''.join([english[x] for x in range(index, index + alpha_len)])

                if alphas[x].text == word_part.strip():
                    if count != x:
                        self.drag_operate(alphas[x], alphas[count])
                        sort_word = ''.join([k.text for k in self.word()])
                    index += alpha_len
                    count += 1
                    break
            if english.strip() == sort_word:
                print('sort_word', sort_word)
                break

    @teststeps
    def restore_word(self, i):
        if i == 0:
            print('\n还原单词模式(新词)\n')

        self.click_voice()  # 听力按钮
        Homework().next_button_operate('false')

        explain = self.prompt()  # 展示的提示词
        english = self.common.get_word_by_explain(explain)
        print("英文解释：%s" % explain)
        print('数据库获取单词：', english)

        before_word = ''
        alphas = self.word()

        for j in range(0, len(alphas)):
            before_word = before_word + alphas[j].text
        print("还原前单词为：", before_word)

        right_word = ''
        if len(english) != 1:
            for x in english:
                english_list = list(x)
                alpha_list = list(before_word)
                english_list.sort()
                alpha_list.sort()
                if english_list == alpha_list:
                    right_word = x
                    break
        else:
            right_word = english[0]
        self.restore_word_core(right_word)
        print('还原后单词为：%s' % right_word)
        time.sleep(4)
        print('----------------------------------')

