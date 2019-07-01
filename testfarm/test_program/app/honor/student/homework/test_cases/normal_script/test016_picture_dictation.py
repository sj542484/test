# coding=utf-8
import unittest

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.homework.object_page.picture_dictation_page import PictureDictation
from testfarm.test_program.app.honor.student.homework.test_data.homework_title_type import GetVariable as gv
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.toast_find import Toast


class Games(unittest.TestCase):
    """听音选图"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.picture = PictureDictation()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_picture_dictation(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():
            self.home_page.click_hk_tab(2)

            if self.homework.wait_check_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.PIC_DIC in var[0]:
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.PIC_DIC:
                            var[1][i].click()  # 点击进入该作业
                            count = self.homework.games_count(0, '听音选图', gv.PIC_DIC)  # 小游戏个数统计
                            self.game_exist(count[0])  # 具体操作

                            if count[1] == 10:  # 判断小游戏list是否需滑屏
                                game_count = self.homework.swipe_screen('听音选图')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                            break
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.PIC_DIC, '听音选图')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """听音选图游戏具体操作 及 结果页操作"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.PIC_DIC):
                    if index == 0:
                        continue
                    else:
                        print('##########################################')
                        self.homework.games_type()[index].click()  # 进入小游戏

                        result = self.picture.picture_dictation()  # 小游戏的 游戏过程
                        self.picture.result_detail_page(result[0])  # 结果页 查看答案 按钮
                        print('##########################################')
                        self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have单词听写小游戏')
        self.homework.back_up_button()  # 返回主界面
