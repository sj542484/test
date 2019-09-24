#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.login.object_page.login_page import TloginPage
from conf.decorator import setup, teardown, testcase
from utils.toast_find import Toast


class PollImg(unittest.TestCase):
    """轮播图 and 单词本&每日一听 提示信息"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.speak = SpokenDetailPage()
        cls.van = VanclassPage()
        cls.release = ReleasePage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_word_book_daily_listen(self):
        """单词本 & 每日一听 提示信息"""
        self.login.app_status()  # 判断APP当前状态

        self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
        if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
            if self.van.wait_check_list_page():
                print('==================单词本================')
                self.van.word_book()  # 单词本icon
                Toast().toast_operation('请去电脑端使用单词本,移动端即将上线。')  # 获取toast

                print('================每日一听================')
                self.van.daily_listen()  # 每日一听icon
                Toast().toast_operation('功能开发中,敬请期待!')  # 获取toast

                if self.van.wait_check_list_page():
                    self.home.back_up_button()
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")
