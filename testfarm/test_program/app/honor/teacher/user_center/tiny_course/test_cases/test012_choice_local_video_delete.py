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
    """微课 选择本地视频后删除"""
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
    def test_delete_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():

                    self.choice_local_video_operation()  # 选择本地拍摄 具体操作
                    self.delete_video_operation()  # 视频删除具体操作

                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def choice_local_video_operation(self):
        """选择本地视频 操作"""
        if self.tiny.wait_check_list_page():
            print('------选择本地视频 操作-----')
            self.tiny.create_tiny_course()  # + 微课内容
            if self.tiny.wait_check_menu_page():
                self.tiny.menu_item()[1].click()  # 点击 本地视频

                if self.video.wait_check_local_page():
                    if self.video.wait_check_local_list_page():
                        content = self.video.video_item()  # 视频条目信息
                        for i in range(len(content)):
                            print(content[i])
                            print('------------------------------')

                        self.video.click_video_item(0)  # 选择第一个视频
                    else:
                        print('！！！暂无本地视频')  # 视频播放 操作
    @teststeps
    def delete_video_operation(self):
        """删除视频 操作"""
        if self.tiny.wait_check_list_page():
            print('---------视频删除 操作--------')
            self.tiny.delete_tiny_course_button()  # 删除 按钮
            if self.tiny.wait_check_list_page():
                if not self.tiny.judge_delete():
                    print('视频删除成功')
                else:
                    print('★★★ Error - 视频删除失败')

                self.home.back_up_button()  # 返回个人中心页面
