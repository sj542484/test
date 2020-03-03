#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import datetime
import time
import unittest

from app.honor.pc_operation.my_resource.test_cases.delete_tiny_course.delete_course import Delete
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.tiny_course_page import TinyCourse
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import \
    MineTestBankPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page6X import VideoPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.decorator import testcase, teststeps, setup
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class Shoot(unittest.TestCase):
    """微课 拍摄视频 -游戏详情页"""
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
        cls.mine = MineTestBankPage()

        BasePage().set_assert(cls.ass)

    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Shoot, self).run(result)

    @testcase
    def test_shoot_video_game_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                nick = self.user.nickname()  # 老师昵称
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():

                    self.shoot_video_operation()  # 视频拍摄 具体操作
                    if self.tiny.wait_check_page():
                        title = self.tiny.edit_course_name('游戏详情')  # 编辑课程名称
                        self.check_game_detail_operation(title, nick)  # 查看小游戏详情页 具体操作
                        self.tiny.judge_save_result(title)  # 验证保存结果
                    else:
                        print("!!!视频拍摄结束未返回 微课页面")
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
            print('--------------视频拍摄 操作---------------')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[0].click()  # 点击 拍摄视频

                self.video.permission_allow()  # 拍照和录像权限
                self.video.permission_allow()  # 通话及本地录音权限

                if self.video.wait_check_shoot_page():
                    loc = self.video.shoot_button_location()
                    self.video.shoot_button()  # 拍摄按钮
                    time.sleep(5)  # 拍摄时长至少大于10s

                    self.video.suspend_button(loc)  # 暂停按钮
                    if self.video.wait_check_done_page():
                        self.video.done_button()  # 完成 按钮

                        print('---------------------------------------')
                    else:
                        print('!!!未进入视频拍摄暂停页面')
                else:
                    print('!!!未进入视频拍摄页面')
            else:
                print('!!!未进入微课页面')

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
                if self.game.wait_check_page():  # 游戏详情页
                    self.home.back_up_button()  # 返回个人中心页面
        else:
            print("!!!未进入 微课详情页面")

    @teststeps
    def tiny_course_play_operation(self):
        """播放过程"""
        print('-------------视频播放--------------')
        if self.game.wait_check_list_page():  # 页面检查点
            TinyCourse().play_button()  # 播放 按钮
            if TinyCourse().wait_check_play_page():
                TinyCourse().back_up_button()  # 返回 按钮
            else:
                print('!!!未进入视频播放页面')
