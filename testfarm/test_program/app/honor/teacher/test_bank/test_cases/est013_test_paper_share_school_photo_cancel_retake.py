#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from app.honor.teacher.test_bank.object_page.test_paper_share_page import PaperSharePage
from app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from conf.decorator import setupclass, teardownclass, testcase
from utils.screen_shot import ScreenShot


class PaperShare(unittest.TestCase):
    """试卷分享 -拍照上传"""

    @classmethod
    @setupclass
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
        cls.screen_shot = ScreenShot()

    @teardownclass
    def tearDown(self):
        if self.share.wait_check_share_list_page():  # 页面检查点
            self.home.back_up_button()  # 返回 试卷详情页
            if self.paper.wait_check_page():  # 页面检查点
                self.home.back_up_button()  # 返回题库页面
                if self.question.wait_check_page('试卷'):
                    self.home.click_tab_hw()

    @testcase
    def test_001_paper_share_school_photo_cancel(self):
        self.login.app_status()  # 判断APP当前状态

        self.share.into_paper_share_page()  # 进入试卷分享页面

        if self.share.wait_check_share_list_page():  # 页面检查点
            ele = self.share.school_upload_img()  # 学校徽标
            avatar = self.screen_shot.get_screenshot(ele)  # 获取截图
            ele.click()
            if self.share.wait_check_change_page():
                print('=================学校徽标- 拍照=================')
                self.share.click_photograph()  # 拍照
                self.share.upload_img_cancel_operation(avatar)  # cancel 上传图片操作

    @testcase
    def test_002_paper_share_school_photo_retake(self):
        self.share.judge_app_status()  # 判断应用当前状态，并进入分享界面

        if self.share.wait_check_share_list_page():  # 页面检查点
            ele = self.share.school_upload_img()  # 学校徽标
            avatar = self.screen_shot.get_screenshot(ele)  # 获取截图
            ele.click()
            if self.share.wait_check_change_page():
                print('=================学校徽标- 拍照=================')
                self.share.click_photograph()  # 拍照
                self.share.upload_img_retake_operation(avatar)  # retake 上传图片操作
