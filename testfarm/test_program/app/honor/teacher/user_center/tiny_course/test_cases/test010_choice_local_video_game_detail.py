#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import datetime
import time
import unittest

from app.honor.pc_operation.my_resource.test_cases.delete_tiny_course.delete_course import Delete
from conf.base_page import BasePage
from conf.decorator import testcase, teststeps, setup
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.tiny_course_page import TinyCourse
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page6X import VideoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class Detail(unittest.TestCase):
    """微课 本地视频 详情页"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.ass_result = unittest.TestResult()
        cls.ass = ExpectingTest(cls, cls.ass_result)
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.tiny = CreateTinyCourse()
        cls.video = VideoPage()
        cls.game = GamesPage()

        BasePage().set_assert(cls.ass)

    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Detail, self).run(result)

    @testcase
    def test_local_video_game_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                nick = self.user.nickname()  # 老师昵称
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    self.choice_local_video(nick)  # 选择本地视频 具体操作
                else:
                    print("!!!未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
                # Delete().delete_tiny()  # 恢复测试数据
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def choice_local_video(self, nick):
        """选择本地视频 操作"""
        if self.tiny.wait_check_list_page():
            print('------选择本地视频 操作-----')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[1].click()  # 点击 本地视频
                if self.video.wait_check_local_page():
                    self.video.menu_button()  # 左上角
                    time.sleep(2)
                    self.video.video_file_button()
                    if self.video.wait_check_video_file_page('视频'):
                        self.video.album_button()[0].click()

                        if self.video.wait_check_local_list_page():
                            self.video.album_button()[0].click()  # 选择视频
                            if self.video.wait_check_cut_page(5):
                                self.video.rule_hint()
                                self.video.control_button()
                                self.video.finish_button()

                            if self.tiny.wait_check_page():
                                name = self.tiny.edit_course_name('本地视频游戏详情')  # 编辑课程名称
                                self.check_game_detail_operation(name, nick)  # 查看小游戏详情页 具体操作
                                self.tiny.judge_save_result(name)  # 验证保存结果
                                # self.tiny.recovery_data(name)  # 恢复测试数据
                            else:
                                print("!!!未返回 微课页面")

    @teststeps
    def check_game_detail_operation(self, name, nickname):
        """查看小游戏详情页 具体操作"""
        if self.game.wait_check_page():  # 游戏详情页
            if self.game.wait_check_list_page():
                print('---------------------游戏详情页---------------------')
                title = self.game.game_title()  # title
                if name != title:
                    print("★★★ Error - 微课名称有误", name, title)

                print(self.game.game_info())
                count = self.game.game_num()  # 小题数/日期
                if count[0] != 1:
                    print("★★★ Error - 小题数不为1", count[0])
                if count[1] != datetime.datetime.now().strftime('%Y-%m-%d'):
                    print("★★★ Error - 创建日期有误", count[1])

                teacher = self.game.teacher_nickname()  # 老师昵称
                if teacher != nickname:
                    print('★★★ Error - 老师昵称有误', teacher, nickname)
                print('------------------------------')

                self.tiny_course_play_operation()  # 视频播放
                self.home.back_up_button()
        else:
            print("!!!未进入 微课详情页面")

    @teststeps
    def tiny_course_play_operation(self):
        """播放过程"""
        if self.game.wait_check_list_page():  # 页面检查点
            print('-----------------视频播放过程---------------')
            TinyCourse().play_button()  # 播放 按钮
            if TinyCourse().wait_check_play_page():
                TinyCourse().back_up_button()  # 返回 按钮
            else:
                print('!!!未进入视频播放页面')
        else:
            print("!!!未进入 微课详情页面")
