# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/27 11:59
# -------------------------------------------
import time
import unittest
from ddt import ddt,data

from testfarm.test_program.app.honor.student.library.object_pages.game_page import GamePage
from testfarm.test_program.app.honor.student.library.object_pages.library_page import LibraryPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.app.honor.student.library.object_pages.sql_data_page import DataHandlePage
from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps


@ddt
class BookGame(unittest.TestCase):
    """准确率"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.library = LibraryPage()
        cls.result = ResultPage()
        cls.game = GamePage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @data(*[
        # '单词',
        # '句子',
        '文章',
        # '其他'
    ])
    @teststeps
    def test_book_game(self, book_name):
        """测试书籍游戏"""
        user_info = UserCenterPage().get_user_info()
        school_name = user_info[1]
        stu_id = user_info[0]
        nickname = user_info[3]
        DataHandlePage().delete_student_book_data(stu_id)
        if self.home.wait_check_home_page():
            self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
            more_btn = self.home.check_more()

            more_btn[0].click()     # 点击推荐的查看更多按钮
            while True:
                if self.game.wait_check_test_label_page():
                    self.library.course_more_btn('其他教材').click()
                    time.sleep(2)
                    break
                else:
                    self.home.screen_swipe_up(0.5, 0.9, 0.4, 1000)

        # 点击系列，选择不同类型的游戏书籍，进行游戏操作
            books_list = []
            flag = False
            while True:
                books = self.library.book_names()
                for x in books:
                    if x.text in books_list:
                        continue
                    else:
                        books_list.append(x.text)
                        if x.text == '全题型':
                            x.click()
                            time.sleep(3)
                            books = self.library.book_names()
                            for y in books:
                                if y.text == book_name:
                                    book_progress = self.library.book_progress(y.text)
                                    y.click()
                                    self.game_operate(nickname, book_progress, school_name)
                                    break

                            flag = True
                            break
                if flag:
                    break
                else:
                    self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)

    @teststeps
    def game_operate(self, nickname, book_progress, school_name):
        if self.library.wait_check_book_punch_page():                  # 打卡页处理
            if self.library.wait_check_no_bank_page():
                print('暂无排行数据')
            else:
                self.library.read_data_operate(nickname, book_progress)   # 图书页数据处理
        self.game.start_game_btn().click()
        if self.game.wait_check_bank_list_page():               # 进入书籍， 遍历进入题型
            bank_types = self.game.testbank_type()
            for i in range(len(bank_types)):
                if self.game.wait_check_bank_list_page():
                    bank_ele = self.game.testbank_type()[i]
                    bank_progress = self.game.bank_progress(bank_ele.text).text
                    print(bank_ele.text, bank_progress)
                    bank_ele.click()

                    if self.game.wait_check_game_page():       # 进入游戏页面
                        first_result = self.game.play_book_games(fq=1, bank_progress=bank_progress)
                        if self.result.wait_check_result_page():  # 进入结果页
                            self.result.again_btn().click()
                            if self.game.wait_check_game_page():
                                self.game.play_book_games(fq=2, sec_answer=first_result[0],
                                                          first_num=first_result[1])
                            self.home.click_back_up_button()
        self.library.from_bank_back_to_home_operate(school_name)















