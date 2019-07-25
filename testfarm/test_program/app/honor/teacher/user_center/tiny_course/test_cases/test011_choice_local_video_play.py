# coding=utf-8
import time
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center import CreateTinyCourse
from app.honor.teacher.user_center import VideoPage
from app.honor.teacher.user_center import TuserCenterPage
from conf.decorator import testcase, teststeps, setup, teardown
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 选择本地视频后播放"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.tiny = CreateTinyCourse()
        cls.video = VideoPage()
        cls.game = GamesPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_local_video_play(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():

                    self.choice_local_video_operation()  # 选择本地拍摄 具体操作
                    self.play_video_operation()  # 视频播放 具体操作

                    if self.tiny.wait_check_page():
                        name = self.tiny.edit_course_name()  # 编辑课程名称
                        create_date = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()

                            self.tiny.judge_save_result(name)  # 验证保存结果
                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def choice_local_video_operation(self):
        """选择本地视频 操作"""
        if self.tiny.wait_check_list_page():
            print('------选择本地视频 操作-----')
            self.tiny.create_tiny_course()  # + 微课内容

            if self.video.wait_check_local_page():
                if self.video.wait_check_local_list_page():
                    self.video.click_video_item(0)  # 选择视频

                    if self.video.wait_check_cut_page():
                        self.video.rule_hint()
                        self.video.control_button()
                        self.video.finish_button()

    @teststeps
    def play_video_operation(self):
        """视频播放 操作"""
        if self.tiny.wait_check_page():
            print('---------视频播放 操作--------')
            self.tiny.play_video()  # 视频 按钮

            if self.video.wait_check_cut_page():
                self.video.rule_hint()
                self.video.control_button()
                self.video.finish_button()
