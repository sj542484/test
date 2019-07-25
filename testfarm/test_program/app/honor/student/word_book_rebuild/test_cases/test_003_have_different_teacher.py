#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 9:09
# -----------------------------------------
import unittest
from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.web.object_pages.assign_word import AssignWord
from testfarm.test_program.app.honor.student.web.object_pages.driver import Driver
from testfarm.test_program.app.honor.student.web.object_pages.login_page import LoginWebPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.class_operate import QuitAddClass
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.data_handle import DataActionPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.flash_card_page import FlashCard
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.public_ele import PublicElementPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_book import WordBook
from testfarm.test_program.app.honor.student.word_book_rebuild.test_data.account import *
from testfarm.test_program.conf.decorator import setup, teardown, testcase


class HaveClass(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.login.app_status(stu_account=STU_ACCOUNT, stu_password=STU_PASSWORD)   # 判断APP当前状态

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_have_different_teacher(self):
        """测试拥有不同老师，不同班级的情况"""
        if self.home.wait_check_home_page():
            test_class_num = VANCLASS_ID
            van_num = test_class_num.copy()
            QuitAddClass().apply_class_operate(van_num)
            web_driver = Driver()
            web_driver.set_driver()
            for x in TEACHER_ACCOUNT:
                AssignWord().assign_wordbook_operate(test_class_num, x, STU_PASSWORD)
                LoginWebPage().logout_operate()

            web_driver.quit_web()
            if self.home.wait_check_home_page():
                stu_info = UserCenterPage().get_user_info()
                stu_id = stu_info[0]
                teacher_trans_ids = DataActionPage().get_teacher_words_trans_id(stu_id)
                if self.home.wait_check_home_page():
                    self.home.click_hk_tab(1)  # 点击 背单词
                    if WordBook().wait_check_start_page():  # 开始页面检查点
                        WordBook().word_start_button()  # 点击 Go按钮
                        word_info = FlashCard().scan_game_operate()
                        PublicElementPage().check_word_order_is_right(teacher_trans_ids, word_info)