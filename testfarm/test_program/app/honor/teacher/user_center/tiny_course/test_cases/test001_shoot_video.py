# coding=utf-8
import time
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.mine_test_bank.object_page.mine_test_bank_page import \
    MineTestBankPage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.object_page.tiny_course_page import TinyCoursePage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.object_page.video_page import VideoPage
from testfarm.test_program.app.honor.teacher.user_center.tiny_course.test_data.tiny_video_name import name_data
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import testcase, teststeps, setup, teardown
from testfarm.test_program.utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 拍摄视频"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.tiny = TinyCoursePage()
        cls.video = VideoPage()

        cls.mine = MineTestBankPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_shoot_video(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_tiny_course()  # 进入 微课页面
                if self.tiny.wait_check_page():

                    self.save_operation()  # 保存 按钮具体操作

                    if self.tiny.wait_check_page():
                        self.shoot_video_operation()  # 视频拍摄 具体操作
                        if self.tiny.wait_check_page():
                            self.tiny.save_button()  # 点击 保存按钮

                            self.tiny.judge_save_result(name_data[-1]['name'])  # 验证保存结果
                else:
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def save_operation(self):
        """保存 按钮具体操作"""
        print('--------------------------------------------------')
        print('保存 按钮具体操作:')
        self.tiny.save_button()  # 不操作，直接点击 保存按钮
        Toast().find_toast('课程名不能为空')

        if self.user.wait_check_page(3):
            print('★★★ Error - 不操作，直接点击 保存按钮，保存成功')
        else:
            print('不操作，直接点击 保存按钮，未保存成功')
            print('------------------')

            self.tiny.edit_course_name(name_data[-1]['name'])  # 编辑课程名称
            Toast().find_toast('视频不能为空')

            if self.user.wait_check_page(3):
                print('★★★ Error - 未插入视频内容，保存成功')
            else:
                print('未插入视频内容，未保存成功')
            print('--------------------------------------------------')

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
                    self.video.shoot_button()  # 拍摄按钮
                    if self.video.wait_check_suspend_page():
                        time1 = self.video.shoot_time()  # 拍摄时长
                        time.sleep(5)  # 验证拍摄时长是否增加

                        if self.video.wait_check_suspend_page():
                            self.video.suspend_button()  # 暂停按钮
                            if self.video.wait_check_done_page():
                                time2 = self.video.shoot_time()  # 拍摄时长
                                self.time_operation(time1, time2)  # 时长比较
                                self.video.done_button()  # 完成 按钮
                                print('---------------------------------------')
                    else:
                        print('!!!未进入视频拍摄暂停页面')
                else:
                    print('!!!未进入视频拍摄页面')
            else:
                print('!!!未进入微课页面')

    @teststeps
    def time_operation(self, time1, time2):
        """时长比较"""
        item = self.tiny.video_duration_deal(time1)
        item2 = self.tiny.video_duration_deal(time2)
        print(item, item2)
        if item2 < item:
            print('★★★ Error - 拍摄时长无增加', time1, time2)
        else:
            print('拍摄时长有增加，展示无误')
        print('-----------------------------')


