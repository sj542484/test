#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from app.honor.teacher.test_bank.object_page.test_paper_share_page import PaperSharePage
from app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class PaperShare(unittest.TestCase):
    """试卷分享 -修改"""

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

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_paper_share_edittext(self):
        self.login.app_status()  # 判断APP当前状态

        self.share.into_paper_share_page()  # 进入试卷分享页面
        if self.share.wait_check_share_page():
            if self.share.wait_check_share_list_page():
                print('------------------------------------------')
                name = self.share.share_name_edit()  # 编辑框
                print(name.text)
                name.clear()
                name.send_keys('123')
                print('修改为:', '123')
                print('------------------')

                if self.share.wait_check_share_list_page():
                    school = self.share.share_school_edit()  # 学校
                    print(school.text)
                    school.clear()
                    school.send_keys('school')
                    print('修改为:', 'school')
                    print('------------------')

                if self.share.wait_check_share_list_page():
                    contact = self.share.share_contact_edit()  # 联系方式
                    print(contact.text)
                    contact.clear()
                    contact.send_keys('1234')
                    print('修改为:', '1234')
                    print('------------------')

                self.share_control_operation()  # 分享控件

                if self.share.wait_check_share_list_page():
                    self.home.back_up_button()  # 返回 试卷详情页

        if self.paper.wait_check_page():  # 页面检查点
            self.home.back_up_button()  # 返回题库页面

        if self.question.wait_check_page('试卷'):
            self.question.filter_button()  # 筛选按钮
            if self.filter.wait_check_page():  # 页面检查点
                self.filter.click_question_menu()  # 点击 题单
                self.filter.commit_button()  # 确定按钮
                if self.question.wait_check_page('题单'):
                    self.home.click_tab_hw()


    @teststeps
    def share_control_operation(self):
        """分享控件 选择操作"""
        if self.share.wait_check_share_list_page():
            SwipeFun().swipe_vertical(0.5, 0.7, 0.2)

            if self.share.wait_check_share_list_page():
                print('------------------------------------------')
                self.share.wechat_friend().click()  # 微信好友
                print('微信好友')
                if self.share.wait_check_toast_page(5):  # 该校分享额度已用完 or 非合作校
                    self.home.tips_title()  # 提示
                    self.home.tips_content()  # 提示的内容
                    self.home.commit_button().click()  # 确定按钮

                    if self.share.wait_check_share_list_page():
                        print('------------------')
                        self.share.wechat_circle().click()  # 微信朋友圈
                        print('微信朋友圈')
                        if self.share.wait_check_toast_page(5):  # 该校分享额度已用完 or 非合作校
                            self.home.tips_title()  # 提示
                            self.home.tips_content()  # 提示的内容
                            self.home.commit_button().click()  # 确定按钮
                else:  # 可分享
                    if self.share.wait_check_share_wechat_page(5):  # 说明 手机安装了微信且未登录
                        self.share.wechat_back_button()

                        if self.share.wait_check_share_list_page():
                            print('------------------')
                            self.share.wechat_circle().click()  # 微信朋友圈
                            print('微信朋友圈')
                            if self.share.wait_check_share_wechat_page():
                                self.share.wechat_back_button()
                            elif self.share.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                                self.share.back_up_button()
                    elif self.share.wait_check_share_not_login_page(): # 由于登录过期，请重新登录。无法分享到微信
                        self.share.back_up_button()
                        if self.share.wait_check_share_list_page():
                            print('------------------')
                            self.share.wechat_circle().click()  # 微信朋友圈
                            print('微信朋友圈')
                            if self.share.wait_check_share_wechat_page(5):
                                self.share.wechat_back_button()
                            elif self.share.wait_check_share_not_login_page():  # 由于登录过期，请重新登录。无法分享到微信
                                self.share.back_up_button()
                    elif self.share.wait_check_share_list_page():
                        print(' 手机未安装微信')
                        print('------------------')
                        self.share.wechat_circle().click()  # 微信朋友圈
                        print('微信朋友圈')
                        print(' 手机未安装微信')

            if self.share.wait_check_share_list_page():
                print('------------------')
                self.share.copy_link().click()  # 复制链接
                print('复制链接')
                if self.share.wait_check_share_list_page():
                    if not Toast().find_toast('已经复制到粘贴板'):
                        print('★★★ Error- 未弹toast: 已经复制到粘贴板')
                    else:
                        print('已经复制到粘贴板')
                    print('------------------')
                elif self.share.wait_check_toast_page(5):  # 该校分享额度已用完 or 非合作校
                        self.home.tips_title()  # 提示
                        self.home.tips_content()  # 提示的内容
                        self.home.commit_button().click()  # 确定按钮
