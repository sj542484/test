#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/22 10:18
# -----------------------------------------
import datetime
import time
import unittest

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.speaking.object_page.enter_into_speaking import SpeakingPage
from testfarm.test_program.conf.decorator import teardown, setup, testcase


class SpeakGame(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.speak = SpeakingPage()
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_speak_game(self):
        print('测试口语')
        if self.speak.home.wait_check_home_page():
            self.speak.home.click_hk_tab(0)
            if self.speak.wait_check_speak_page():
                if self.speak.wait_check_speak_homework_list_page():
                    self.speak.select_one_homework().click()
                    start_time = datetime.datetime.now()
                    while True:
                        game_time = datetime.datetime.now()
                        if (game_time - start_time).seconds >= 3600:
                            break
                        if self.speak.wait_check_homework_bank_page():
                            if self.speak.wait_check_bank_list_page():
                                self.speak.select_one_bank().click()
                                if self.speak.wait_check_game_page():
                                    self.speak.microphone_btn().click()
                                    if self.speak.wait_check_permission_page():
                                        self.speak.allow_btn().click()
                                    time.sleep(4)
                                    if self.speak.wait_check_microphone_btn_page():
                                        self.speak.microphone_btn().click()
                                        time.sleep(2)
                                        print(self.speak.microphone_btn().get_attribute('contentDescription'))
                                    if self.speak.wait_check_game_page():
                                        self.home.click_back_up_button()
                                        print('-'*30, '\n')
                else:
                    print('暂无作业列表')
