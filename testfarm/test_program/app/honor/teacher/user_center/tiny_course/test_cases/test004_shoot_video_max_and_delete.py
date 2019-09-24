#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page import VideoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import testcase, teststeps, setup, teardown
from utils.connect_db import ConnectDB
from utils.toast_find import Toast


class Shoot(unittest.TestCase):
    """微课 拍摄视频 - 验证时长max & 删除后重拍"""
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

        ConnectDB().start_db()  # 启动数据库

    @classmethod
    @teardown
    def tearDown(cls):
        """关闭数据库"""
        ConnectDB().close_db()

    @testcase
    def test_time_max_and_delete_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():

                    self.shoot_video_operation()  # 视频拍摄 具体操作
                    self.time_operation()  # 拍摄时长验证
                    self.delete_video_operation()  # 视频删除具体操作

                    if self.tiny.wait_check_page():
                        name = self.tiny.edit_course_name()  # 编辑课程名称
                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()
                        self.tiny.judge_save_result(name)  # 验证保存结果
                else:
                    print("!!!未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def shoot_video_operation(self):
        """拍摄视频 操作"""
        if self.tiny.wait_check_list_page():
            print('--------------视频拍摄 操作---------------')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[0].click()  # 点击 拍摄视频

                self.video.permission_allow()  # 拍照和录像权限
                self.video.permission_allow()  # 通话及本地录音权限

                if self.video.wait_check_shoot_page():
                    loc = self.video.shoot_button_location()
                    self.video.shoot_button()  # 拍摄按钮
                    time.sleep(2)
                    self.video.suspend_button(loc)  # 暂停按钮
                    if self.video.wait_check_done_page():
                        self.video.done_button()  # 完成 按钮
                        if not Toast().find_toast('视频最短时长不得低于5秒'):  # 获取toast
                            print('★★★ Error - 未弹toast：视频最短时长不得低于5秒')
                        else:
                            print('视频最短时长不得低于5秒')
                        print('-------------------------')

                    if self.video.wait_check_done_page():
                        print('拍摄时长3min，超时暂停拍摄')
                        print("Start : %s" % time.ctime())
                        z = 0
                        while True:
                            time.sleep(1)
                            self.video.shoot_button()  # 拍摄按钮
                            time.sleep(30)
                            print(time.ctime())
                            z += 1
                            if z == 6:
                                break
                            else:
                                self.video.suspend_button(loc)  # 暂停按钮
                            print('-----------')
                        print("End : %s" % time.ctime())
                        # time.sleep(180)  # 验证拍摄时长3min暂停拍摄

                        if self.video.wait_check_done_page():
                            print('----------超时后，再点击拍摄视频---------')
                            self.video.shoot_button()  # 拍摄按钮
                            # if self.video.wait_check_shoot_page():
                            #     time.sleep(5)  # 拍摄时长至少大于5s
                            #     self.video.suspend_button(loc)  # 暂停按钮
                            if self.video.wait_check_done_page():
                                self.video.done_button()  # 完成 按钮

    @teststeps
    def time_operation(self):
        """拍摄时长验证"""
        if self.tiny.wait_check_list_page():  # 页面检查点
            self.tiny.play_video()  # 播放 按钮

            if self.video.wait_check_cut_page():
                length = self.video.video_time()
                item = self.video.video_duration_deal(length)  # 视频时长
                if item >= 180:
                    print('★★★ Error - 拍摄时长3min，超时未暂停拍摄', item)
                elif 8 > item <= 5:
                    print('超时后，重新拍摄视频成功', item)
                print('-----------------------------')

                self.video.finish_button()

    @teststeps
    def delete_video_operation(self):
        """删除视频 操作"""
        if self.tiny.wait_check_list_page():
            print('---------微课创建页面，视频删除操作--------')
            self.tiny.delete_tiny_course_button()  # 删除 按钮
            if self.tiny.wait_check_list_page():
                if not self.tiny.judge_video_exist():
                    print('视频删除成功')
                    self.shoot_video_operation()  # 视频拍摄 具体操作
                else:
                    print('★★★ Error - 视频删除失败')
