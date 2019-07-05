import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


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
    def wait_check_show_page(self):
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
    def clock_button(self):
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
    def nex_level_text(self):
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[@index,0]")
        print('已选年级 :%s'%ele)
        print('--------------------------------------')


    @teststep
    def confirm_button(self):
        """继续练习"""
        self.driver.\
            find_element_by_id(self.id_type() + "confirm")\
            .click()

    @teststeps
    def get_result_all_ele(self):
        """结果页面"""
        print(' <结果页>：')
        word_count = self.driver.find_element_by_id(self.id_type() + "word_count").text
        print('今日已练单词：%s' % word_count)
        date = self.driver.find_element_by_id(self.id_type() + 'date').text
        print('日期：%s' % date)
        all_word_count = self.driver.find_element_by_id(self.id_type() + "all_word_count").text
        print(all_word_count)
        remark_text = self.driver.find_element_by_id(self.id_type() + "text").text
        print(remark_text)
        print('----------------------------------------')

    @teststeps
    def show_page_ele(self):
        """炫耀一下页面"""
        if self.wait_check_show_page():
            print('<炫耀一下>：')
            print('功能按钮：')
            wx = self.driver.find_element_by_id(self.id_type() + "weixin").text
            wx_friend = self.driver.find_element_by_id(self.id_type() + 'weixin_friends').text
            img_save = self.driver.find_element_by_id(self.id_type() + 'save_img').text
            print(wx, wx_friend, img_save)
            print('-----------------------------------------')

    @teststeps
    def result_page_handle(self):
        """结果页处理"""
        if self.wait_check_result_page():
            print('进入结果页面')
            self.get_result_all_ele()  # 结果页元素
            self.clock_button()  # 打卡
            self.show_page_ele()  # 炫耀一下页面
            self.home.click_back_up_button()  # 返回
            if self.wait_check_result_page():
                self.more_again_button()  # 再练一次
                if self.wait_check_next_grade():  # 继续挑战页面
                    self.level_up_text()
                self.back_to_home()

    @teststep
    def back_to_home(self):
        self.home.click_back_up_button()
        if self.home.wait_check_tips_page():
            self.home.commit_button()
        if self.home.wait_check_word_title():
            self.home.click_back_up_button()
            if self.home.wait_check_home_page():  # 页面检查点
                print('返回主界面')

