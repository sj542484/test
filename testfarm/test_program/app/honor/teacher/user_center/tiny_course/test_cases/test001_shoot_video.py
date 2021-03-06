#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
import unittest

from app.honor.pc_operation.my_resource.test_cases.delete_tiny_course.delete_course import Delete
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from app.honor.teacher.user_center.tiny_course.object_page.video_page6X import VideoPage
from app.honor.teacher.user_center.tiny_course.test_data.video_name import name_data
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.base_page import BasePage
from conf.decorator import testcase, teststeps, setup
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class Shoot(unittest.TestCase):
    """微课 拍摄视频"""
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

        BasePage().set_assert(cls.ass)

    def tearDown(self):
        for i in self.ass.get_error():
            self.ass_result.addFailure(self, i)

    def run(self, result=None):
        self.ass_result = result
        super(Shoot, self).run(result)

    @testcase
    def test_shoot_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    name = self.save_button_operation()  # 保存 按钮具体操作

                    if self.tiny.wait_check_page():
                        self.shoot_video_operation()  # 视频拍摄 具体操作
                        if self.tiny.wait_check_page():
                            self.tiny.save_button()  # 点击 保存按钮
                            self.tiny.judge_upload_operation()  # 判断视频是否 正在上传中...  及 加入公共题库tips

                            if self.home.wait_check_tips_page():
                                self.home.tips_content_commit()  # 提示 页面信息
                                self.home.tips_content_commit()  # 提示 页面信息

                            if GamesPage().wait_check_page():  # 游戏详情页
                                self.home.back_up_button()  # 返回个人中心页面
                                self.tiny.judge_save_result(name)  # 验证保存结果

                                # if gv.ENV == '线上':
                                #     Delete().delete_tiny()
                                # else:
                                #     self.tiny.recovery_data(name)  # 恢复测试数据
                            else:
                                print("!!!未进入 微课详情页面")
                        else:
                            print("!!!视频拍摄结束未返回 微课页面")
                    else:
                        print("!!!未返回 微课页面")
                else:
                    print("!!!未进入 微课页面")
                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
                # Delete().delete_tiny()  # 恢复测试数据
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @teststeps
    def save_button_operation(self):
        """保存 按钮具体操作"""
        print('------------------保存 按钮具体操作-------------------')
        self.tiny.save_button()  # 不操作，直接点击 保存按钮
        Toast().toast_operation('课程名不能为空')

        if self.user.wait_check_page(3):
            print('★★★ Error - 不操作，直接点击 保存按钮，保存成功')
        else:
            print('不操作，直接点击 保存按钮，未保存成功')
            print('------------------')

        if self.tiny.wait_check_page():
            var = self.tiny.course_name()  # 微课名称
            var.send_keys(name_data[1]['name'])
            item = var.text
            print('输入微课名称：', item)
            self.tiny.save_button()  # 点击 保存按钮
            Toast().toast_operation('视频不能为空')

            if self.user.wait_check_page(3):
                print('★★★ Error - 未插入视频内容，保存成功')
            else:
                print('未插入视频内容，未保存成功')
            print('--------------------------------------------------')
            return item

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
                    time.sleep(5)  # 验证拍摄时长是否增加

                    self.video.suspend_button(loc)  # 暂停按钮
                    if self.video.wait_check_done_page():
                        # time2 = self.video.shoot_time()  # 拍摄时长
                        self.video.done_button()  # 完成 按钮

                        # self.time_operation(time2)  # 时长验证
                        print('---------------------------------------')
                    else:
                        print('!!!未进入视频拍摄暂停页面')
                else:
                    print('!!!未进入视频拍摄页面')
            else:
                print('!!!未进入微课页面')

    @teststeps
    def time_operation(self, time1):
        """拍摄时长验证"""
        item = self.video.video_duration_deal(time1)
        print('视频时长：', time1)
        if item <= 0:
            print('★★★ Error - 拍摄时长有误：', time1)
        else:
            print('拍摄时长有增加，展示无误')
        print('-----------------------------')
