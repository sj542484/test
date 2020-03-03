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
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import MineTestBankPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page6X import VideoPage
from app.honor.teacher.user_center.tiny_course.test_data.edit_video_name import name_data
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 本地视频 课程名"""
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
        cls.question = TestBankPage()

        BasePage().set_assert(cls.ass)

    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(TinyCourse, self).run(result)

    @testcase
    def test_edit_course_name(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    self.choice_local_video()  # 选择视频 具体操作
                    self.course_name_operation()  # 课程名编辑 具体操作
                else:
                    print("!!!未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
                # Delete().delete_tiny()  # 恢复测试数据
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def choice_local_video(self):
        """选择本地视频 操作"""
        print('---------------选择本地视频 操作----------------')
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
                            self.video.finish_button()

    @teststeps
    def course_name_operation(self):
        """课程名编辑 具体操作"""
        print('=========================编辑课程名 具体操作==========================')
        if self.tiny.wait_check_page():
            for i in range(len(name_data)):
                if self.tiny.wait_check_list_page():
                    var = self.tiny.course_name()  # 微课名称
                    var.send_keys(name_data[i]['name'])
                    print('输入微课名称：', var.text)  # 编辑课程名称
                    self.tiny.save_button()  # 点击 保存按钮

                    if len(name_data[i]) == 2:
                        Toast().toast_operation(name_data[i]['assert'])
                        print('=============================================================')
                    else:
                        self.judge_upload_operation()  # 判断视频 是否 正在上传中

                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()
                            if self.user.wait_check_page():
                                self.tiny.judge_save_result(name_data[i]['name'])  # 验证视频保存结果

                                if i != len(name_data)-1:
                                    print('=============================================================')
                                    if self.user.wait_check_page():  # 页面检查点
                                        self.user.click_tiny_course()  # 进入 微课页面
                                        if self.tiny.wait_check_page():
                                            if self.tiny.wait_check_list_page():
                                                self.choice_local_video()  # 选择视频 具体操作

    @teststeps
    def judge_upload_operation(self, var=3):
        """判断视频 是否 正在上传中  及取消加入公共题库"""
        if self.tiny.wait_check_upload_page():  # 上传中....
            # self.upload_rate()  # 上传百分率
            # self.upload_num()  # 上传数量
            while True:
                if self.tiny.check_upload_progress():  # 上传中....
                    time.sleep(1)
                else:
                    ThomePage().tips_content_cancel(var)  # 提示 页面信息
                    break

    # @teststeps
    # def recovery_data(self):
    #     """ 恢复测试数据"""
    #     print('------恢复测试数据-----')
    #     account_id = GetDBData().get_account_id()
    #     print(account_id)
    #     for i in range(len(name_data)):  # 恢复测试数据
    #         if len(name_data[i]) == 1:
    #             sql = "DELETE FROM `testbank` WHERE `account_id` = '{}' AND `name`= '{}'" \
    #                 .format(account_id, name_data[i]['name'])
    #             print(sql)
    #             ConnectDB().execute_sql(sql)
