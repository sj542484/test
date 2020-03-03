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


class Shoot(unittest.TestCase):
    """微课 拍摄视频 -创建页面播放"""
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
        super(Shoot, self).run(result)

    @testcase
    def test_shoot_video_play(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    self.shoot_video_operation()  # 视频拍摄 具体操作
                    self.play_video_operation()  # 视频播放 具体操作

                    if self.tiny.wait_check_page():
                        name = self.tiny.edit_course_name('游戏播放裁剪')  # 编辑课程名称
                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()  # 返回个人中心页面

                        self.tiny.judge_save_result(name)  # 验证保存结果
                    else:
                        print("!!!视频拍摄及播放结束未返回 微课页面")
                        self.home.back_up_button()
                else:
                    print("!!!未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
                # Delete().delete_tiny()  # 恢复测试数据
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def shoot_video_operation(self):
        """拍摄视频 操作"""
        if self.tiny.wait_check_list_page():
            print('-------------------视频拍摄 操作-------------------')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[0].click()  # 点击 拍摄视频

                self.video.permission_allow()  # 拍照和录像权限
                self.video.permission_allow()  # 通话及本地录音权限

                if self.video.wait_check_shoot_page():
                    loc = self.video.shoot_button_location()
                    self.video.shoot_button()  # 拍摄按钮
                    time.sleep(5)  # 验证拍摄时长是否增加

                    self.video.suspend_button(loc)  # 暂停按钮
                    if self.video.wait_check_done_page():
                        self.video.done_button()  # 完成 按钮
                else:
                    print('!!!未进入视频拍摄页面')
            else:
                print('!!!未进入微课页面')

    @teststeps
    def play_video_operation(self):
        """视频播放 操作"""
        if self.tiny.wait_check_page():
            print('-----------------视频播放 操作-----------------')
            self.tiny.play_video()  # 播放 按钮

            if self.video.wait_check_cut_page():
                self.video.rule_hint()
                self.video.control_button()  # 播放 按钮
                self.video.control_button()  # 再次点击播放键

                self.cut_video_operation()  # 视频裁剪
            else:
                print('!!!未进入视频裁剪页面')

    @teststeps
    def cut_video_operation(self, duration=2):
        """视频裁剪"""
        print('----------------视频裁剪---------------')
        if self.video.wait_check_cut_page():
            length = self.video.video_cut_operation(duration)  # 裁剪具体操作

            item = self.video.video_time()  # 视频时长
            length1 = self.video.video_duration_deal(item)  # 视频时长
            if length1 >= length:
                print('★★★ Error - 视频裁剪有误', length, length1)

            self.video.finish_button()
