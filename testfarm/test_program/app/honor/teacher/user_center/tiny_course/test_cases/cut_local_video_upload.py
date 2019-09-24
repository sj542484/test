#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.local_video_album_page import MIAlbumPage
from app.honor.teacher.user_center.tiny_course.object_page.video_page import VideoPage
from app.honor.teacher.user_center.tiny_course.test_data.upload_video_name import sheets
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import testcase, teststeps, setup, teardown
from utils.excel_read_write import ExcelUtil
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 本地视频 小米5C"""

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
        cls.album = MIAlbumPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_upload_local_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    if self.tiny.wait_check_list_page():
                        self.tiny.create_tiny_course()  # + 微课内容
                        if self.tiny.wait_check_menu_page():
                            self.tiny.menu_item()[1].click()  # 点击 本地视频

                            self.upload_local_video()  # 上传本地视频 具体操作

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def upload_local_video(self):
        """上传本地视频 操作"""
        for i in range(len(sheets)):
            name_data = ExcelUtil().data_read(sheets[i])  # 读取video data

            index = 1
            for key in name_data:
                print('=============================================================')
                print(key)
                if self.choose_album_operation(i):
                    if self.video.wait_check_video_file_page(sheets[i]):
                        # self.album.more_button()  # 视频排序
                        # if self.album.wait_check_more_page():
                        #     self.album.order_button()
                        #     if self.album.wait_check_order_page():
                        #         self.album.order_item_button()  # 按名称排序

                        if self.album.wait_check_video_list_page():
                            index = self.choose_video_list_operation(name_data[key])  # 选择视频条目
                            if index == 10:
                                print("!!!!未找到该视频:", name_data[key])
                                self.album.cancel_button()
                                break

                            # self.cut_video_operation()  # 视频裁剪

                            if self.tiny.wait_check_page():
                                if self.tiny.wait_check_list_page():
                                    var = self.tiny.course_name()  # 微课名称
                                    var.send_keys(key)
                                    print('输入微课名称：', var.text)  # 编辑课程名称

                                    self.tiny.save_operation()  # 保存 操作

                                    if self.game.wait_check_page():  # 游戏详情页
                                        self.home.back_up_button()

                                        if self.user.wait_check_page():  # 页面检查点
                                            self.user.click_tiny_course()  # 进入 微课页面
                                    elif self.tiny.wait_check_page():
                                        print('！！！已上传过了或视频过长或课程名不符合规则')
                                        self.tiny.delete_tiny_course_button()

                                    if self.tiny.wait_check_page():
                                        if self.tiny.wait_check_list_page():
                                            self.tiny.create_tiny_course()  # + 微课内容

                        index += 1

    @teststeps
    def choose_video_list_operation(self, name):
        """视频列表 具体操作
        :param name: 视频名
        """
        k = 0
        while True:
            if self.album.wait_check_video_list_page():
                video = self.album.choose_video_operation(name)  # 视频条目信息
                if video[1] == 1:
                    self.album.confirm_button()  # 确定按钮
                    if self.video.wait_check_cut_page():
                        self.video.video_time()  # 视频时长
                        self.video.finish_button()
                    break
                else:
                    SwipeFun().swipe_vertical(0.5, 0.8, 0.3)
                    k += 1
        return k

    @teststeps
    def choose_album_operation(self, i):
        """选择相册"""
        while True:
            index = 0
            if not self.video.wait_check_video_file_page(sheets[i], 5):
                files = self.album.files_name()
                for k in range(len(files)):
                    if files[k].text == 'Movies':
                        index += 1
                        files[k].click()
                        break

            if index == 0:
                SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            elif index == 1:
                break

        while True:
            index = 0
            if self.video.wait_check_video_file_page('Movies', 5):
                album = self.album.files_name()
                for k in range(len(album)):
                    if album[k].text == sheets[i]:
                        print(album[k].text)
                        index += 1
                        album[k].click()
                        break

            if index == 0:
                SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            elif index == 1:
                return True

    @teststeps
    def cut_video_operation(self, duration=8, button='after'):
        """视频裁剪"""
        if self.video.wait_check_cut_page():
            self.video.video_cut_operation(duration, button)  # 裁剪具体操作

            self.video.video_time()  # 视频时长
            self.video.finish_button()

    # @teststeps
    # def cut_video_operation(self):
    #     """视频裁剪 - 只剩三分钟"""
    #     if self.video.wait_check_cut_page():
    #         after = self.video.after_cut_button()
    #         loc = Element().get_element_location(after)  # 裁剪按钮 坐标值
    #         length = self.video.video_time()
    #         item = int(length.split(':')[0]) * 60 + int(length.split(':')[1])
    #
    #         duration = item - 180
    #         if duration > 0:  # 需要裁剪
    #             self.video.video_cut_after_operation(duration, loc)  # 裁剪具体操作
    #             self.video.video_time()  # 视频时长
    #
    #         self.video.finish_button()

