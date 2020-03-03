#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
import unittest

from app.honor.pc_operation.my_resource.test_cases.delete_tiny_course.delete_course import Delete
from conf.base_page import BasePage
from conf.decorator import testcase, teststeps, setup
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page6X import VideoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 选择本地视频后播放"""
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
        super(TinyCourse, self).run(result)

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
                        name = self.tiny.edit_course_name('播放')  # 编辑课程名称
                        create_date = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()

                            self.tiny.judge_save_result(name)  # 验证保存结果
                else:
                    print("!!!未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
                # Delete().delete_tiny()  # 恢复测试数据
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def choice_local_video_operation(self):
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
                            self.video.album_button()[2].click()  # 选择视频

                            if self.video.wait_check_cut_page(3):  # 时长多于3min的视频
                                self.video.rule_hint()
                                self.video.control_button()
                                self.video.finish_button()

    @teststeps
    def play_video_operation(self):
        """视频播放 操作"""
        if self.tiny.wait_check_page():
            print('-----------------视频播放 操作-----------------')
            self.tiny.play_video()  # 播放 按钮

            if self.video.wait_check_cut_page():
                self.video.rule_hint()
                self.cut_video_operation()  # 视频裁剪

                self.video.control_button()  # 播放 按钮
                self.video.control_button()  # 再次点击播放键

                self.video.finish_button()

            else:
                print('!!!未进入视频裁剪页面')

    @teststeps
    def cut_video_operation(self, duration=2):
        """视频裁剪"""
        print('----------------视频裁剪---------------')
        if self.video.wait_check_cut_page():
            length = self.video.video_cut_operation(duration)  # 裁剪具体操作

            item = self.video.video_time()
            length1 = self.video.video_duration_deal(item)  # 视频时长
            if length1 >= length:
                print('★★★ Error - 视频裁剪有误', length, length1)
