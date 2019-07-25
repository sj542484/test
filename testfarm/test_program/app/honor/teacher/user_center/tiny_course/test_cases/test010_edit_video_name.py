# coding=utf-8
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center import \
    MineTestBankPage
from app.honor.teacher.user_center import CreateTinyCourse
from app.honor.teacher.user_center import VideoPage
from app.honor.teacher.user_center import name_data
from app.honor.teacher.user_center import TuserCenterPage
from conf.decorator import testcase, teststeps, setup, teardown
from utils.toast_find import Toast


class TinyCourse(unittest.TestCase):
    """微课 本地视频 课程名"""
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
        cls.mine = MineTestBankPage()
        cls.question = TestBankPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

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
                    print("未进入 微课页面")

                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def choice_local_video(self):
        """选择本地视频 操作"""
        print('---------------选择本地视频 操作----------------')
        self.tiny.create_tiny_course()  # + 微课内容
        if self.video.wait_check_local_page():
            if self.video.wait_check_local_list_page():
                self.video.click_video_item(0)  # 选择视频

                if self.video.wait_check_cut_page():
                    self.video.rule_hint()
                    self.video.control_button()
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
                        if not Toast().find_toast(name_data[i]['assert']):
                            print('★★★ Error - 未弹toast:', name_data[i]['assert'])
                        print('=============================================================')
                    else:
                        self.tiny.judge_upload_operation(2)  # 判断视频 是否 正在上传中
                        self.home.tips_content_commit()  # 提示 页面信息

                        if not Toast().find_toast('加入成功'):
                            print('★★★ Error - 未弹toast：加入成功')
                        else:
                            print('加入成功')

                        if self.game.wait_check_page():  # 游戏详情页
                            self.home.back_up_button()

                            if self.user.wait_check_page():
                                self.tiny.judge_save_result(name_data[i]['name'])  # 验证视频保存结果

                                if i != len(name_data)-1:
                                    print('=============================================================')
                                    if self.user.wait_check_page():  # 页面检查点
                                        self.user.click_tiny_course()  # 进入 微课页面
                                        if self.tiny.wait_check_page():
                                            self.choice_local_video()  # 选择视频 具体操作
