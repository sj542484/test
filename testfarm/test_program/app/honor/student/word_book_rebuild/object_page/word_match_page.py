import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.student.word_book_rebuild.object_page.data_action import DataActionPage
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from app.student.homework.object_page.homework_page import Homework


class MatchingWord(BasePage):
    """连连看"""

    def __init__(self):
        self.homework = Homework()
        self.common = DataActionPage()

    @teststep
    def wait_check_word_mach_page(self):
        locator = (By.ID, '{}mg_1'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def get_word_list(self):
        """获取页面内所有 word &解释"""
        ele = self.driver.find_elements_by_class_name("android.widget.TextView")
        return ele

    @teststeps
    def is_word(self, word):
        """判断 是否为字母"""
        pattern = re.compile(r'^[A-Za-z\-\'. ]+$')
        if pattern.match(word):
            return True
        else:
            return False

    @teststeps
    def get_no_selected_text(self):
        """获取未选择卡片列表"""
        not_select_list = [x for x in self.get_word_list() if x.get_attribute("selected") == 'false']
        return not_select_list

    @teststeps
    def get_selected_text(self):
        """获取未选择卡片列表"""
        select_list = [x for x in self.get_word_list() if x.get_attribute("selected") == 'true']
        return select_list

    @teststeps
    def card_match(self, ll, new_word):
        if ll == 0:
            print('\n单词连连看模式(新词) \n')
        english = []  # 单词list
        english_index = []  # 单词在所有button中的索引
        explain = []  # 解释list
        explain_index = []  # 解释在所有button中的索引

        word_list = self.get_word_list()  # 获取所有buton
        for i in range(1, len(word_list)):
            if self.is_word(word_list[i].text):  # 如果是字母
                english.append(word_list[i].text)
                english_index.append(i)
            else:  # 如果是汉字
                explain.append(word_list[i].text)
                explain_index.append(i)
        print("英文序列:%s" % english_index, "\n英文单词:%s" % english,
              "\n解释序列:%s" % explain_index, "\n英文解释:%s\n" % explain)

        while True:
            index = int(len(self.get_selected_text())/2)
            print("选中单词个数：", index)
            word = new_word[explain[index]]
            if index == len(explain) - 1:
                word_list[explain_index[index]].click()
                for x in self.get_no_selected_text():
                    if self.is_word(x.text):
                        print('解释：%s' % explain[index])
                        print('正确单词：', word)
                        print('目前单词为：', x.text)
                        x.click()
                        print('答案正确\n')
                        break
                break
            else:
                for k in range(len(english)):
                    word_list[explain_index[index]].click()
                    if english[k] in word:
                        print('解释：%s' % explain[index])
                        print('正确单词：', word)
                        print('目前单词为：', english[k])
                        word_ele = self.get_word_list()[english_index[k]]
                        if word_ele.get_attribute('selected') == 'false':
                            word_ele.click()
                            time.sleep(2)
                            if int(len(self.get_selected_text())/2) == index + 1:
                                print('答案正确')
                                print('~' * 20, '\n')
                                break
                    else:
                        continue

        time.sleep(3)
