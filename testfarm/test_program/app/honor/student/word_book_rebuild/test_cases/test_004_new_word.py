#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 11:00
# -----------------------------------------
import unittest

from ddt import ddt,data

from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.data_handle import DataActionPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_result_page import ResultPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.wordbook_rebuild import WordBookRebuildPage
from testfarm.test_program.app.honor.student.word_book_rebuild.test_data.account import *
from testfarm.test_program.conf.decorator import setup, teardown, testcase


class NewWord(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.login.app_status(stu_account=STU_ACCOUNT, stu_password=STU_PASSWORD)  # 判断APP当前状态
        cls.word_info = {}             # 记录所有单词

    @teardown
    def tearDown(self):
        self.word_rebuild.write_words_to_file(self.word_info)


    @testcase
    def test_new_word(self):
        """测试新词"""
        if self.home.wait_check_home_page():
            stu_info = UserCenterPage().get_user_info()
            stu_id = stu_info[0]
            DataActionPage().clear_student_word_data(stu_id)
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)                # 点击 背单词
                if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                    studied_words = self.word_rebuild.total_word()  # 获取已学单词数
                    if studied_words != 0:
                        print('★★★ 单词记录未清空成功')
                    self.word_rebuild.word_start_button()      # 点击 Go按钮
                else:
                    print('★★★ 缓存未清空成功')

                new_explain_words = []                   # 新释义单词
                recite_words = []                        # 复习单词
                for x in range(2):
                    WordBookRebuildPage(). \
                        study_word_operate(self.word_info, x, new_explain_words, recite_words, stu_id)  # 游戏过程
                    if ResultPage().wait_check_result_page():
                        ResultPage().result_page_handle(self.word_info, new_explain_words, recite_words, x)
                    print(self.word_info)
