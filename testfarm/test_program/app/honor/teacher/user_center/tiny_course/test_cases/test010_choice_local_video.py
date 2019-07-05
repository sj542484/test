# coding=utf-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.object_page.tiny_course_page import TinyCoursePage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.object_page.video_page import VideoPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import testcase, teststeps, setup, teardown
from testfarm.test_program.utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 本地视频"""
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
    def test_choice_local_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():
                    self.choice_local_video()  # 选择本地视频 具体操作

                    if self.tiny.wait_check_page():
                        self.tiny.save_button()  # 点击 保存按钮
                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def choice_local_video(self):
        """选择本地视频 操作"""
        content = self.local_video_operation()  # 视频列表

        for i in range(len(content)):
            if self.video.wait_check_local_page():
                if self.video.wait_check_local_list_page():
                    self.video_name_verify(content[i])  # 视频后缀验证

                    self.video.click_video_item(i)  # 选择 不同后缀的视频

                    if self.tiny.wait_check_page():
                        self.tiny.edit_course_name('选择本地视频后保存')  # 编辑课程名称
                        self.tiny.judge_save_result('选择本地视频后保存')  # 验证保存结果

                        if self.user.wait_check_page():  # 页面检查点
                            self.user.click_tiny_course()  # 进入 微课页面
                            if self.tiny.wait_check_page():
                                if self.tiny.wait_check_list_page():
                                    self.tiny.create_tiny_course()  # + 微课内容
                                    if self.tiny.wait_check_menu_page():
                                        self.tiny.menu_item()[1].click()  # 点击 本地视频

    @teststeps
    def local_video_operation(self):
        """本地视频 列表"""
        if self.tiny.wait_check_list_page():
            print('-----------选择本地视频 操作-----------')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[1].click()  # 点击 本地视频

                if self.video.wait_check_local_page():
                    if self.video.wait_check_local_list_page():
                        content = self.video.video_item()  # 视频条目信息
                        for i in range(len(content)):
                            print(content[i])
                        print('------------------------------')
                        return content
                    else:
                        print('！！！暂无本地视频')

    @teststeps
    def video_name_verify(self, item):
        """视频 后缀验证"""
        value = item[0].split('.')[1]
        print(value)
