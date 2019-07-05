#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_paper_share_page import PaperSharePage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from testfarm.test_program.conf.decorator import setup, teardownclass, testcase
from testfarm.test_program.utils.screen_shot import ScreenShot


class PaperShare(unittest.TestCase):
    """试卷分享- 相册上传"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.question = TestBankPage()
        cls.paper = PaperDetailPage()
        cls.share = PaperSharePage()
        cls.game = GamesPage()
        cls.change_image = ChangeImage()
        cls.filter = FilterPage()

    @teardownclass
    def tearDown(self):
        if self.share.wait_check_share_list_page():
            self.home.back_up_button()  # 返回 试卷详情页
            if self.paper.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回题库页面
                if self.question.wait_check_page('试卷'):
                    self.home.click_tab_hw()

    @testcase
    def test_001_paper_share_qr_album(self):
        self.login.app_status()  # 判断APP当前状态

        self.share.into_paper_share_page()  # 进入试卷分享页面

        if self.share.wait_check_share_page():
            if self.share.wait_check_share_list_page():
                ele = self.share.qr_upload_img()  # 二维码
                avatar = ScreenShot().get_screenshot(ele)  # 获取截图
                ele.click()
                if self.share.wait_check_exchange_page():
                    print('=================二维码- 相册=================')
                    self.share.click_album()  # 相册上传
                    self.share.album_save_operation(avatar, 'qr')  # save 上传图片操作

    @testcase
    def test_002_paper_share_qr_album_cancel(self):
        self.share.judge_app_status()  # 判断应用当前状态，并进入分享界面

        if self.share.wait_check_share_page():
            if self.share.wait_check_share_list_page():
                ele = self.share.qr_upload_img()  # 二维码
                avatar = ScreenShot().get_screenshot(ele)  # 获取截图
                ele.click()
                if self.share.wait_check_exchange_page():
                    print('=================二维码- 相册=================')
                    self.share.click_album()  # 相册上传
                    self.share.album_cancel_operation(avatar, 'qr')  # cancel 上传图片操作
