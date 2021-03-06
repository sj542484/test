#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page6X import VideoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import testcase, teststeps, setup, teardown
from utils.excel_read_write import ExcelUtil
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 本地视频 MEIZU-M15/小米6X"""

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
        content = ExcelUtil().data_read()  # 读取video data

        for j in range(len(content[1])):  # 每个表
            count = 1
            for key in content[0][j]:
                print('=============================================================')
                print(content[0][j][key], key)

                if self.choose_album_operation(content[1][j]):
                    if self.video.wait_check_video_file_page(content[1][j]):
                        # self.video.order_menu_button()  # 视频排序
                        # if self.video.wait_check_order_page():
                        #     self.video.order_item_button()

                        if self.video.wait_check_local_list_page():
                            index = self.choose_video_list_operation(content[0][j][key])  # 选择视频条目
                            # if index == 20:
                            #     print("!!!!未找到该视频:", name_data[key])
                            #     self.home.back_up_button()
                            #     # self.album.cancel_button()
                            #     break

                            if self.video.wait_check_cut_page(3):
                                self.video.finish_button()

                            if self.tiny.wait_check_page():
                                if self.tiny.wait_check_list_page():
                                    var = self.tiny.course_name()  # 微课名称
                                    var.send_keys(key)
                                    print('输入微课名称：', var.text)  # 编辑课程名称

                                    self.tiny.save_button()  # 点击 保存按钮
                                    self.tiny.judge_upload_operation()  # 判断视频是否 正在上传中...  及 加入公共题库tips

                                    if ThomePage().wait_check_tips_page(5):
                                        ThomePage().tips_content_commit(5)  # 提示 页面信息
                                        ThomePage().tips_content_commit(5)  # 提示 页面信息

                                    if self.game.wait_check_page():  # 游戏详情页
                                        print('上传成功')
                                        self.home.back_up_button()  # 返回 个人中心 页面
                                        print(count, len(content[0]))
                                        if count != len(content[0])-1:
                                            if self.user.wait_check_page():  # 页面检查点
                                                self.user.click_tiny_course()  # 进入 微课页面
                                    elif self.tiny.wait_check_page():
                                        print('！！！已上传过了或视频过长或课程名不符合规则')
                                        self.tiny.delete_tiny_course_button()

                                    print(count, len(content[0]))
                                    if count != len(content[0])-1:
                                        if self.tiny.wait_check_page():
                                            self.tiny.create_tiny_course()  # + 微课内容
                                            if self.tiny.wait_check_menu_page():
                                                self.tiny.menu_item()[1].click()  # 点击 本地视频
                                    else:
                                        if self.tiny.wait_check_page():
                                            self.home.back_up_button()  # 返回 个人中心 页面

                        count += 1
                else:
                    print('！！！未进入相册')

    @teststeps
    def choose_video_list_operation(self, name):
        """视频列表 具体操作
        :param name: 视频名
        """
        k = 0
        while True:
            if self.video.wait_check_local_list_page():
                video = self.video.choose_video_operation(name)  # 选择视频条目
                if video[1] == 1:
                    break
                else:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.4)
                    k += 1
        return k

    @teststeps
    def choose_album_operation(self, sheet):
        """选择相册"""
        if not self.video.wait_check_video_file_page(sheet, 5):
            self.video.menu_button()  # 左上角
            time.sleep(2)
            self.video.video_file_button()

            while True:
                index = 0
                if self.video.wait_check_video_file_page('视频'):
                    album = self.video.album_button()
                    for k in range(len(album)):
                        print(album[k].text)
                        if album[k].text == sheet:
                            index += 1
                            album[k].click()
                            break

                if index == 0:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                elif index == 1:
                    return True
                elif index == 5:
                    print('！！！已遍历15遍，未找到视频文件夹')
                    self.video.back_up()
                    break
        else:
            return True
