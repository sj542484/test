import unittest

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.clear_user_data import CleanDataPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.my_word_page import MyWordPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.word_book import WordBook
from testfarm.test_program.conf.decorator import setup, teardown, teststeps


class MineWord(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.home = HomePage()
        cls.word = WordBook()
        cls.mine = MyWordPage()
        cls.clear = CleanDataPage()


    @teardown
    def tearDown(self):
        pass

    @teststeps
    def test_mine_word(self):
        """我的单词"""
        if self.home.wait_check_home_page():  # 页面检查点
            self.clear.get_id_back()
            if self.home.wait_check_home_page():  # 页面检查点
                print('进入主界面')
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.home.wait_check_word_title():  # 页面检查点
                    total = self.word.total_word()
                    self.mine.click_my_word_btn()
                    if self.mine.wait_check_mine_word_page():
                        if self.mine.no_word_tips():
                            self.mine.no_word_tip_text()
                        else:
                            self.mine.play_mine_word(total)

