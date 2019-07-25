# coding=utf-8
import unittest

from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.test_paper.object_page.exam_data_handle import DataPage
from testfarm.test_program.app.honor.student.test_paper.object_page.exam_page import ExamPage
from testfarm.test_program.app.honor.student.web.object_pages.driver import Driver
from testfarm.test_program.app.honor.student.web.object_pages.resign_exam_page import ResignExamPage
from testfarm.test_program.app.honor.student.word_book.object_page.clear_user_data import CleanDataPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase


class Exam(unittest.TestCase):
    """试卷"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.exam = ExamPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.common = DataPage()
        # cls.common.write_json_to_file({})

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_play_exam_game_progress(self):
        """做试卷"""
        # 删除所有试卷 重新布置
        stu_id = UserCenterPage().get_user_info()[0]
        self.common.delete_student_exam_record(stu_id)
        web_driver = Driver()
        web_driver.set_driver()
        ResignExamPage().reassign_exam_operate()      # web端随机布置一套试卷
        web_driver.quit_web()
        if self.home.wait_check_home_page():          # 页面检查点
            print('进入主界面')
            CleanDataPage().clean_cache_back_to_home()  # 清除缓存
            self.home.click_hk_tab(3)                   # 点击 做试卷
            if self.exam.wait_check_exam_title_page():
                test_name = self.exam.select_one_exam(0)
                data_json = self.common.get_data_json_from_file()
                data_json[test_name] = {}
                if self.exam.wait_check_exam_confirm_page():
                    total = self.exam.exam_confirm_ele_operate()
                    self.exam.click_start_exam_button()
                    tips = self.exam.get_ques_name(int(total))
                    self.exam.play_examination(tips, data_json[test_name])
                    self.common.write_json_to_file(data_json)
                    # self.exam.play_test_examination(int(total))
