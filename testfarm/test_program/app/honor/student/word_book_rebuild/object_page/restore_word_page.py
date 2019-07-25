import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
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
    def wait_check_right_answer_page(self):
        """正确答案页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[@resource-id="{}tv_word" and @index=1]'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """解释"""
        ele = self.driver \
            .find_element_by_id("{}tv_prompt".format(self.id_type()))
        return ele

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id("{}fab_sound".format(self.id_type())) \
            .click()

    @teststep
    def word(self, index=0):
        """展示的 待还原的单词"""
        word = self.driver \
            .find_elements_by_xpath('//android.widget.TextView[@resource-id="{}tv_word" and @index={}]'
                                    .format(self.id_type(), index))
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
    def restore_word_operate(self, bank_count, new_explain_words):
        print('===== 还原单词模式(新词) =====\n')
        all_words, answer_word = [], []
        while len(all_words) < bank_count:
            self.click_voice()  # 听力按钮
            Homework().next_button_judge('false')

            explain = self.explain()  # 展示的提示词
            explain_id = explain.get_attribute('contentDescription')
            if explain_id in new_explain_words:
                print('★★★ 此单词为新释义，不应出现还原游戏')
            print("英文解释：%s" % explain.text)
            print("还原前单词为：", ''.join([x.text for x in self.word()]))

            if not answer_word:
                self.drag_operate(self.word()[0], self.word()[-1])
                Homework().next_button_operate('true')
                if self.wait_check_right_answer_page():
                    right_answer = self.word(index=1)[0].text
                    print('正确答案：', right_answer)
                    answer_word.append(right_answer)
                else:
                    all_words.append(explain)
                print('还原后单词为：%s' % ''.join([x.text for x in self.word()]))
                Homework().next_button_operate('true')
            else:
                self.restore_word_core(answer_word[0])
                answer_word.clear()
                all_words.append(explain)
                print('还原后单词为：%s' % ''.join([x.text for x in self.word()]))
                time.sleep(3)
            print('-'*30, '\n')

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
