
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.toast_find import Toast


class ResultPage(BasePage):

    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_result_page(self):
        """结果页 以今日已练单词图片的Id为依据"""
        locator = (By.ID, self.id_type() + 'word_count')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_wx_login_page(self):
        """微信登陆页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"登录微信")]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_share_page(self):
        """打卡页，以分享图片id为依据"""
        locator = (By.ID, self.id_type() + "share_img")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_next_grade(self):
        """再来一组 以继续挑战的图片的Id为依据"""
        locator = (By.ID, self.id_type() + "img")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def date(self):
        """时间日期"""
        ele = self.driver.find_element_by_id(self.id_type() + 'date')
        return ele.text

    @teststep
    def today_word(self):
        """今日已练单词"""
        ele = self.driver.find_element_by_id(self.id_type() + "word_count")
        return ele.text

    @teststep
    def already_remember_word(self):
        """已被单词"""
        ele = self.driver.find_element_by_id(self.id_type() + "all_word_count")
        return ele.text

    @teststep
    def word_detail_info(self):
        """复习新词组"""
        ele = self.driver.find_element_by_id(self.id_type() + "text")
        return ele.text


    @teststep
    def share_button(self):
        """打卡"""
        self.driver.\
            find_element_by_id(self.id_type() + 'punch_clock')\
            .click()
        time.sleep(2)

    @teststep
    def rank_button(self):
        """右上角排名按钮"""
        self.driver.\
            find_element_by_id(self.id_type() + "rank")\
            .click()
        time.sleep(3)

    @teststep
    def more_again_button(self):
        """再来一组"""
        print('再来一组')
        self.driver.\
            find_element_by_id(self.id_type() + "again")\
            .click()

    @teststep
    def level_up_text(self):
        """单词已练完说明"""
        ele = self.driver.find_element_by_id(self.id_type() + "level_up_hint").text
        print(ele)


    @teststep
    def no_study_btn(self):
        """不练了"""
        self.driver.\
            find_element_by_id(self.id_type() + "cancel")\
            .click()

    @teststep
    def wx_btn(self):
        """微信按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "weixin")
        return ele

    @teststep
    def wx_friend(self):
        """朋友圈"""
        ele = self.driver.find_element_by_id(self.id_type() + 'weixin_friends')
        return ele

    @teststep
    def save_img(self):
        """保存图片"""
        ele = self.driver.find_element_by_id(self.id_type() + 'save_img')
        return ele

    @teststep
    def nex_level_text(self):
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[@index,0]")
        print('已选年级 :%s'% ele)
        print('-'*30, '\n')


    @teststep
    def confirm_button(self):
        """继续练习"""
        self.driver.\
            find_element_by_id(self.id_type() + "confirm")\
            .click()

    @teststep
    def wx_back_up_btn(self):
        """微信页面返回按钮"""
        ele = self.driver.find_element_by_accessibility_id('返回')
        return ele

    @teststep
    def share_page_operate(self):
        """分享页面操作"""
        if self.wait_check_share_page():
            self.wx_btn().click()
            if self.wait_check_wx_login_page():
                self.wx_back_up_btn().click()
            else:
                print('★★★ 未进入微信登陆页面')

        if self.wait_check_share_page():
            self.wx_friend().click()
            if self.wait_check_wx_login_page():
                self.wx_back_up_btn().click()
            else:
                print('★★★ 未进入微信登陆页面')
        if self.wait_check_share_page():
            self.save_img().click()
            if not Toast().find_toast('已保存到本地'):
                print('★★★ 未发现保存图片提示')
            self.click_back_up_button()

    @teststeps
    def check_result_word_data(self, word_info, new_explain_words, recite_words, group_count):
        """结果页面"""
        print(' <结果页>：')
        print('今日已练单词：%s' % self.today_word())
        print('日期：%s' % self.date())
        print(self.already_remember_word())
        print(self.word_detail_info())
        today_word_count = int(self.today_word())
        already_count = int(re.findall(r'\d+', self.already_remember_word())[0])
        detail = re.findall(r'\d+', self.word_detail_info())
        study_group_count = int(detail[0])
        recite_count = int(detail[1])
        new_set_words = int(detail[2])
        new_explain_count = int(detail[3])
        all_word = sum([len(x) for x in list(word_info.values())])

        if already_count != len(word_info):
            print('★★★ 已学单词数不正确，应为', len(word_info))

        if today_word_count != all_word:
            print('★★★ 今日单词总数不正确， 应为', all_word)

        if study_group_count != group_count+1:
            print('★★★ 已练组数不正确， 应为', group_count+1)

        if new_set_words != len(word_info):
            print('★★★ 新词学单词数不正确，应为', len(word_info))

        if new_explain_count != len(new_explain_words):
            print('★★★ 新释义单词个数不正确， 应为', len(new_explain_words))

        if recite_count != len(recite_words):
            print('★★★ 复习单词个数不正确， 应为', len(recite_words))


    @teststep
    def back_to_home(self):
        self.home.click_back_up_button()
        if self.home.wait_check_tips_page():
            self.home.commit_button()
        if self.home.wait_check_word_title():
            self.home.click_back_up_button()
            if self.home.wait_check_home_page():  # 页面检查点
                print('返回主界面')

    @teststeps
    def result_page_handle(self, word_info, new_explain_words, recite_words, x):
        """结果页处理"""
        if self.wait_check_result_page():
            print('进入结果页面')
            self.check_result_word_data(word_info, new_explain_words, recite_words, x)  # 结果页元素
            self.share_button()  # 打卡
            self.share_page_operate()  # 炫耀一下页面
            if self.wait_check_result_page():
                self.more_again_button()  # 再练一次
                if self.wait_check_next_grade():  # 继续挑战页面
                    self.level_up_text()
