# coding=utf-8
import unittest
from app.student.login.object_page.home_page import HomePage
from app.student.login.object_page.login_page import LoginPage
from app.student.test_paper.object_page.data_action import DataPage
from app.student.test_paper.object_page.exam_detail import DetailPage
from app.student.test_paper.object_page.exam_page import ExamPage
from app.student.word_book.object_page.sql_data.data_action import DataActionPage
from conf.decorator import setup, teardown, testcase, teststeps


class Exam(unittest.TestCase):
    """试卷"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.exam = ExamPage()
        cls.detail = DetailPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.common = DataPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_check_detail_1(self):
        self.check_exam_detail(0)

    @testcase
    def test_check_detail_2(self):
        self.check_exam_detail(1)

    @testcase
    def test_check_detail_3(self):
        self.check_exam_detail(2)

    @testcase
    def test_check_detail_4(self):
        self.check_exam_detail(3)

    @teststeps
    def check_exam_detail(self, exam_index):
        """查看试卷详情"""
        nick_name = DataActionPage().get_id_nick_back_home()
        if self.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            self.home.click_hk_tab(3)  # 点击 做试卷
        if self.detail.wait_check_exam_title_page():
            exam_name = self.exam.select_one_exam(exam_index)
            data_json = self.common.get_data_json_from_file()
            exam_data = data_json[exam_name]
            if self.exam.wait_check_rank_page():
                # self.detail.rank_page_operate(nick_name)
                # if self.exam.wait_check_rank_page():
                self.detail.check_detail()
                if self.detail.wait_check_detail_page():
                    self.detail.check_ques_detail(exam_data)
                    self.home.click_back_up_button()
                    if self.detail.wait_check_rank_page():
                        self.home.click_back_up_button()






