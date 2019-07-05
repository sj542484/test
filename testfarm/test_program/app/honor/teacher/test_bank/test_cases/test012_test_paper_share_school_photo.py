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
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.screen_shot import ScreenShot
from testfarm.test_program.utils.swipe_screen import SwipeFun


class PaperShare(unittest.TestCase):
    """试卷分享 -拍照上传"""

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
        cls.filter = FilterPage()
        cls.screen_shot = ScreenShot()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_share_school_photo(self):
        self.login.app_status()  # 判断APP当前状态

        self.share.into_paper_share_page()  # 进入试卷分享页面

        if self.share.wait_check_share_page():
            if self.share.wait_check_share_list_page():

                self.share.share_page_info()  # 分享页面 信息

                self.share.help_button()  # ?按钮
                if self.share.wait_check_help_page():
                    i = 0
                    while i < 2:
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
                        i += 1
                    SwipeFun().swipe_vertical(0.5, 0.2, 0.9)

                    self.home.back_up_button()  # 返回按钮

                if self.share.wait_check_share_page():  # 页面检查点
                    if self.share.wait_check_share_list_page():  # 页面检查点
                        ele = self.share.school_upload_img()  # 学校徽标
                        avatar = self.screen_shot.get_screenshot(ele)  # 获取截图
                        ele.click()
                        if self.share.wait_check_change_page():
                            print('=================学校徽标- 拍照=================')
                            self.share.click_photograph()  # 拍照
                            self.share.upload_img_save_operation(avatar)  # save 上传图片操作

                if self.share.wait_check_share_list_page():  # 页面检查点
                    self.home.back_up_button()  # 返回 试卷详情页
                    if self.paper.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回题库页面
                        if self.question.wait_check_page('试卷'):
                            self.home.click_tab_hw()
