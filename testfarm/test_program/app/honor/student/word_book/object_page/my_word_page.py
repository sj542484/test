import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.word_book.object_page.data_action import WordBookDataHandle
from testfarm.test_program.app.honor.student.word_book.object_page.mysql_data import WordBookSql
from testfarm.test_program.app.honor.student.word_book.object_page.word_book import WordBook
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep


class MyWordPage(BasePage):
    """单词本 - 我的单词"""
    def __init__(self):
        self.home = HomePage()
        self.mysql = WordBookSql()
        self.word = WordBook()
        self.common = WordBookDataHandle()

    @teststeps
    def wait_check_mine_word_page(self):
        """以“我的单词”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的单词')]")
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def no_word_tips(self):
        """wording:您还没有已背单词哦，快开始背单词吧"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "status_error_hint_view")
            return True
        except Exception:
            return False

    @teststeps
    def no_word_tip_text(self):

        """wording:您还没有已背单词哦，快开始背单词吧"""
        ele = self.driver.find_element_by_id(self.id_type() + 'status_error_hint_view').text
        print(ele.text)

    @teststep
    def click_my_word_btn(self):
        """我的单词"""
        self.driver.\
            find_element_by_id(self.id_type() + 'my_word')\
            .click()

    @teststep
    def total_word(self):
        """单词总数"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "total_word").text
        return ele

    @teststep
    def word_detail_text(self):
        """查看单词详情"""
        ele = self.driver\
            .find_element_by_xpath("//android.widget.TextView[contains(@text, '点单词可看详情')]").text
        print(ele)

    @teststep
    def voice_button(self):
        """听音 按钮"""
        ele = self.driver\
                  .find_elements_by_id(self.id_type() + "iv_speak")
        return ele

    @teststep
    def get_words(self):
        """单词"""
        ele = self.driver\
            .find_elements_by_id(self.id_type() + "word")
        return ele

    @teststep
    def progress(self):
        """每个单词的轮次"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "progress")
        return ele

    @teststep
    def order_info(self):
        """排名"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_order")
        return ele

    @teststep
    def st_icon(self):
        """头像"""
        ele = self.driver\
            .find_elements_by_id(self.id_type() + "iv_head")
        return ele

    @teststep
    def st_name(self):
        """学生姓名"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_name")
        return ele

    @teststep
    def wait_check_end_page(self):
        """滑到底 页面检查"""
        try:
            self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"到底啦 下拉刷新试试")]')
            return True
        except:
            return False

    @teststep
    def get_all_words(self):
        """将所有单词存储在一个数组中"""
        word_list = []
        while True:
            words = self.get_words()
            for j in range(len(words)):
                if words[j].text in word_list:
                    continue
                else:
                    word_list.append(words[j].text)
            if self.wait_check_end_page():
                self.screen_swipe_down(0.5, 0.4, 0.7, 1000)
                break
            else:
                self.screen_swipe_up(0.5, 0.9, 0.4, 1500)
        return word_list

    @teststep
    def play_mine_word(self, stu_id,  total):
        """我的单词 主要过程"""
        total_text = self.total_word()
        if total_text.split(":")[1] != total:
            print('★★★ Error--题目总数不正确！')
        else:
            print('\n----<我的单词页面>-----\n')
            print(total_text)
            self.word_detail_text()

            all_words = self.get_all_words()  # 获取所有单词
            print(len(all_words))
            print('所有单词：', all_words)

            words = self.get_words()
            words[random.randint(0, len(words)-4)].click()  # 随机点击一个单词
            self.word.play_word_book(stu_id)  # 我的单词练习过程

            time.sleep(3)
            self.word.back_to_home()



