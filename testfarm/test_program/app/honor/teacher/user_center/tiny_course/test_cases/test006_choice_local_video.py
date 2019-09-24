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

        ConnectDB().start_db()  # 启动数据库

    @classmethod
    @teardown
    def tearDown(cls):
        """关闭数据库"""
        ConnectDB().close_db()

    @testcase
    def test_choice_local_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    if self.tiny.wait_check_list_page():
                        self.tiny.create_tiny_course()  # + 微课内容
                        if self.tiny.wait_check_menu_page():
                            print('点击 本地视频')
                            self.tiny.menu_item()[1].click()  # 点击 本地视频

                            self.choice_local_video()  # 选择本地视频 具体操作
                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def choice_local_video(self):
        """选择本地视频 操作"""
        print('-----------选择本地视频 操作-----------')
        if self.video.wait_check_local_page():
            if self.video.wait_check_local_list_page():
                item = self.video.album_button()[0]
                print(item.text)
                item.click()  # 视频条目信息

                if self.video.wait_check_cut_page(3):  # 时长多于3min的视频
                    self.video.rule_hint()
                    self.video.control_button()
                    self.video.finish_button()

                if self.tiny.wait_check_page():
                    name = self.tiny.edit_course_name()  # 编辑课程名称
                    create_date = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

                    # if not Toast().find_toast('加入成功'):
                    #     print('★★★ Error - 未弹toast：加入成功')
                    # else:
                    #     print('加入成功')

                    if self.game.wait_check_page():  # 游戏详情页
                        self.home.back_up_button()
                    self.tiny.judge_save_result(name)  # 验证保存结果

    @teststeps
    def video_name_verify(self, item):
        """视频 后缀验证"""
        value = item[0].split('.')[1]
        print(value)
