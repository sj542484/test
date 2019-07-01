import random
import time

from selenium.webdriver.common.by import By

from app.student.login.object_page.home_page import HomePage
from app.student.homework.object_page.homework_page import Homework
from app.student.test_paper.object_page.listen_select import ListenSelect
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class ReadUnderstand(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()

    @teststep
    def drag_btn(self):
        """拖拽按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'dragger')
        return ele

    @teststep
    def text_views(self):
        """获取所有文本"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def rs_article(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'ss_view')
        return ele.text

    @teststep
    def cl_article(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'cl_content')
        return ele.text

    @teststep
    def questions(self):
        """问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'question')
        return ele

    @teststep
    def option_char(self):
        """选项字母"""
        ele = self.driver.find_elements(By.ID, self.id_type() + 'tv_char')
        return ele

    @teststep
    def option_text(self):
        """选项内容"""
        ele = self.driver.find_elements(By.ID, self.id_type() + 'tv_item')
        return ele

    @teststeps
    def play_read_understand_game(self, num, exam_json):
        exam_json['阅读理解'] = bank_json = {}
        text = self.rs_article()
        print(text)
        loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
        self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 50)  # 拖拽至最上方
        time.sleep(5)
        ListenSelect().select_operate(num, '阅读理解', bank_json)

    @teststeps
    def read_understand_detail(self, bank_info):
        text = self.cl_article()
        print(text)

        loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
        self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
        ListenSelect().check_result_detail_operate(bank_info, quote_type=2)