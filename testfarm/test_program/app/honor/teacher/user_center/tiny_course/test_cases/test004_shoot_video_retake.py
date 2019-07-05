# coding=utf-8
import time
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.object_page.tiny_course_page import TinyCoursePage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.object_page.video_page import VideoPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import testcase, teststeps, setup, teardown
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 重新拍摄视频"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.tiny = TinyCoursePage()
        cls.video = VideoPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_retake_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    self.shoot_video_operation()  # 视频拍摄 具体操作
                    if self.tiny.wait_check_page():
                        self.tiny.edit_course_name('视频重拍后保存')  # 编辑课程名称
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
            print('---------视频拍摄 操作---------')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[0].click()  # 点击 拍摄视频

                self.video.permission_allow()  # 拍照权限
                self.video.permission_allow()  #

                if self.video.wait_check_shoot_page():
                    self.video.shoot_button()  # 拍摄按钮
                    if self.video.wait_check_suspend_page():
                        self.video.suspend_button()  # 暂停按钮
                        if self.video.wait_check_done_page():
                            print('----------重新拍摄视频---------')
                            self.video.delete_button()  # 删除 按钮
                            if self.video.wait_check_shoot_page():
                                time3 = self.video.shoot_time()  # 拍摄时长
                                self.time_clear(time3)  # 点击删除按钮，时长清空

                                print('------切换前后摄像头，重新拍摄-----')
                                self.video.rotate_button()  # 切换前后摄像头
                                if self.video.wait_check_shoot_page():
                                    self.video.shoot_button()  # 拍摄按钮
                                    if self.video.wait_check_suspend_page():
                                        self.video.suspend_button()  # 暂停按钮
                                        if self.video.wait_check_done_page():
                                            self.video.done_button()  # 完成 按钮
                    else:
                        print('!!!未进入视频拍摄暂停页面')
                else:
                    print('!!!未进入视频拍摄页面')
            else:
                print('!!!未进入微课页面')

    @testcase
    def test_002_play_video_operation(self):
        """视频播放 操作"""
        if self.tiny.wait_check_page():
            print('---------视频播放 操作--------')
            self.tiny.play_button()  # 播放 按钮

            if self.tiny.wait_check_play_page():
                self.tiny.exo_play_button()  # 播放键
                time.sleep(3)
                if self.tiny.wait_check_play_page():
                    time_str = self.tiny.exo_position()
                    var = self.tiny.exo_progress()  # 进度条

                    if time_str != GetAttribute().description(var):
                        print('★★★ Error - 视频时长展示有误', time_str, var)
                    else:
                        print('--播放视频时长展示无误--')
            else:
                print('!!!未进入视频播放页面')

            if self.tiny.wait_check_play_page():
                self.tiny.back_up_button()  # 返回 微课创建按钮

    @teststeps
    def time_clear(self, time1):
        """点击删除按钮，时长清空"""
        item = self.tiny.video_duration_deal(time1)
        print(item)
        if item != 0:
            print('★★★ Error - 点击拍摄按钮，拍摄时长有误', time1)
        else:
            print('--点击删除按钮，视频时长已清空--')
