import unittest

from ddt import ddt,data

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_book import WordBook
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_recite import ReciteProgress
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_result_page import ResultPage
from testfarm.test_program.conf.decorator import teardown, teststeps, setup

@ddt
class Word(unittest.TestCase):
    """单词本"""

    @classmethod
    @setup
    def setUp(cls):
        cls.word = WordBook()
        cls.home = HomePage()
        cls.result = ResultPage()
        cls.login = LoginPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.recite = ReciteProgress()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @data(1, 2, 3, 4)
    @teststeps
    def main_recite_word(self, level):
        """复习单词"""
        self.recite.set_recite_date(level)  # 更改复习单词的时间
        self.home.click_tab_hw()  # 返回主页面
        if self.home.wait_check_home_page():
            self.home.click_hk_tab(1)  # 点击 背单词
            if self.home.wait_check_word_title():
                if self.word.wait_check_start_page():
                    self.word.word_start_button()  # 点击 Go按钮

                    if self.word.wait_check_count_limit_page():
                        self.recite.limit_page_handle()  # 次数限制处理
                    else:
                        print('开始单词本练习')

                elif self.word.wait_check_continue_page():  # 继续按钮
                    self.word.word_continue_button()     # 继续练习

                # 复习过程
                for j in range(0, 7):
                    if self.word.wait_check_game_page():
                        self.recite.recite_progress(j, level)

                        if self.result.wait_check_result_page():
                            self.result.more_again_button()  # 再练一次

                            if self.word.wait_check_game_page():  # 出现游戏页面
                                self.recite.recite_progress(j, level)

                            elif self.word.wait_check_count_limit_page():  # 出现次数限制页面
                                self.recite.limit_page_handle()
                                self.word.back_to_home()

                            elif self.word.wait_check_no_word_page():
                                self.word.back_to_home()
                                break

                            elif self.result.wait_check_next_grade():
                                self.word.back_to_home()
                                break
                    else:
                        self.word.back_to_home()
                        break
        else:
            print("未进入主界面")
