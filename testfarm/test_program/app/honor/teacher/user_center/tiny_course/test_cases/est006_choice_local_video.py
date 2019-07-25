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
    """微课 本地视频"""
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
    def test_choice_local_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    self.choice_local_video()  # 选择本地视频 具体操作

                    if self.tiny.wait_check_page():
                        self.tiny.save_button()  # 点击 保存按钮
                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def choice_local_video(self):
        """选择本地视频 操作"""
        content = self.local_video_operation()  # 视频列表

        for i in range(len(content[0])):
            if self.video.wait_check_local_page():
                if self.video.wait_check_local_list_page():
                    self.video_name_verify(content[0][i])  # 视频后缀验证

                    content[1][i].click()  # 选择 视频

                    if self.tiny.wait_check_page():
                        name = self.tiny.edit_course_name()  # 编辑课程名称
                        create_date = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()
                            self.tiny.judge_save_result(name)  # 验证保存结果

                            if self.user.wait_check_page():  # 页面检查点
                                self.user.click_tiny_course()  # 进入 微课页面
                                if self.tiny.wait_check_page():
                                    if self.tiny.wait_check_list_page():
                                        self.tiny.create_tiny_course()  # + 微课内容

    @teststeps
    def local_video_operation(self):
        """本地视频 列表"""
        if self.tiny.wait_check_list_page():
            print('-----------选择本地视频 操作-----------')
            self.tiny.create_tiny_course()  # + 微课内容

            if self.video.wait_check_local_page():
                if self.video.wait_check_local_list_page():
                    content = self.video.video_item()  # 视频条目信息
                    for i in range(len(content[0])):
                        for j in range(0, len(content[0][i]), 2):
                            print(content[i][j])
                    print('------------------------------')
                    return content
                else:
                    print('！！！暂无本地视频')

    @teststeps
    def video_name_verify(self, item):
        """视频 后缀验证"""
        value = item[0].split('.')[1]
        print(value)
