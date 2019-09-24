#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import unittest
from app.honor.teacher.home.object_page.dynamic_info_page import DynamicPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.object_page.spoken_detail_page import SpokenDetailPage
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
        cls.info = DynamicPage()
        cls.release = ReleasePage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_001_poll_img(self):
        """轮播图"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_image_page():  # 轮播图 检查点
                print('================轮播图================')
                button = self.home.poll_button()  # 轮播按钮
                index = random.randint(1, len(button) - 1)
                button[index].click()

                if index in (0, 1):
                    if self.home.wait_check_poll_img_page(3):  # 班级年报 页面检查点
                        print('第{}张轮播图, 班级年报' .format(index))
                else:  # 页面检查点
                    print('第{}张轮播图' .format(index))
                self.home.back_up_button()  # 返回首页

                print('======================================')
                self.home.poll_img()  # 点击 轮播图
                if self.home.wait_check_poll_img_page(3):  # 班级年报 页面检查点
                    print('班级年报')
                self.home.back_up_button()  # 返回首页
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")

    @testcase
    def test_002_word_book_daily_listen(self):
        """单词本 & 每日一听 提示信息"""
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            print('==================单词本================')
            self.home.word_icon()  # 单词本icon
            if not Toast().find_toast('请去电脑端使用单词本,移动端即将上线。'):  # 获取toast
                print('★★★ Error- 未弹toast:请去电脑端使用单词本,移动端即将上线。')
            else:
                print('请去电脑端使用单词本,移动端即将上线。')

            print('================每日一听================')
            self.home.listen_icon()  # 每日一听icon
            if not Toast().find_toast('功能开发中,敬请期待!'):  # 获取toast
                print('★★★ Error- 未弹toast:功能开发中,敬请期待!')
            else:
                print('功能开发中,敬请期待!')
        else:
            Toast().get_toast()  # 获取toast
            print("!!!未进入主界面")
