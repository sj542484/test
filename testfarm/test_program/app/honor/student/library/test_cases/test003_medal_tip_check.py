#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/30 16:37
# -----------------------------------------
import unittest

from app.honor.student.library.object_pages.game_page import LibraryGamePage
from app.honor.student.library.object_pages.library_page import LibraryPage
from app.honor.student.library.object_pages.medal_page import MedalPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.decorator import setup, teardown, testcase
from utils.get_attribute import GetAttribute


class Medal(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.medal = MedalPage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_medal_tip(self):
        """测试勋章弹框"""
        if self.home.wait_check_home_page():
            self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
            self.home.check_more()[1].click()
            if LibraryPage().wait_check_mine_reading_page():
                self.medal.medal_icon().click()
                if self.medal.wait_check_medal_page():
                    medals = self.medal.medals()
                    for x in medals:
                        if self.medal.wait_check_medal_page():
                            if GetAttribute().selected(x) == 'false':
                                x.click()
                                if not self.medal.wait_check_medal_img_page():
                                    print('★★★ 点击置灰勋章未发现弹框')
                                else:
                                    print(self.medal.medal_content(), '\n')
                                    self.home.click_blank()
                            else:
                                x.click()
                                if not LibraryGamePage().wait_check_punch_share_page():
                                    print('★★★ 点亮勋章点击后未进入分享页面')
                                else:
                                    LibraryGamePage().share_page_operate()
                    if self.medal.wait_check_medal_page():
                        self.medal.click_back_up_button()
                    if LibraryPage().wait_check_mine_reading_page():
                        self.medal.click_back_up_button()
                    if self.home.wait_check_home_page():
                        print('返回主页面')




