# coding=utf-8
import time
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.user_center import CreateTinyCourse
from app.honor.teacher.user_center import VideoPage
from app.honor.teacher.user_center import TuserCenterPage
from conf.decorator import testcase, teststeps, setup, teardown
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 拍摄视频，删除后重拍"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.tiny = CreateTinyCourse()
        cls.video = VideoPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_delete_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():

                    self.shoot_video_operation()  # 视频拍摄 具体操作
                    self.delete_video_operation()  # 视频删除具体操作
                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

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
                    time.sleep(185)  # 验证拍摄时长3min暂停拍摄

                    if self.video.wait_check_done_page():
                        print('拍摄时长3min暂停拍摄')
                        print('----------超时后，重新拍摄视频---------')
                        self.video.shoot_button()  # 拍摄按钮
                        if self.video.wait_check_shoot_page():
                            time.sleep(10)  # 拍摄时长至少大于3s
                            self.video.suspend_button(loc)  # 暂停按钮
                            if self.video.wait_check_done_page():
                                self.video.done_button()  # 完成 按钮

    @teststeps
    def delete_video_operation(self):
        """删除视频 操作"""
        if self.tiny.wait_check_list_page():
            print('超时后，重新拍摄视频成功')
            print('---------微课创建页面，视频删除操作--------')
            self.tiny.delete_tiny_course_button()  # 删除 按钮
            if self.tiny.wait_check_list_page():
                if not self.tiny.judge_video_exist():
                    print('视频删除成功')
                else:
                    print('★★★ Error - 视频删除失败')
