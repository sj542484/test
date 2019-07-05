#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class Recommend(unittest.TestCase):
    """我的推荐 -- 筛选"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.question = TestBankPage()
        cls.filter = FilterPage()
        cls.recommend = RecommendPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_recommend_filter(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_recommend()  # 点击 我的推荐
                if self.recommend.wait_check_page():  # 页面检查点
                    self.recommend.filter_button()  # 筛选按钮

                    if self.filter.wait_check_page():  # 页面检查点
                        game = self.filter.game_list()  # 大题
                        if GetAttribute().selected(game) == 'false':  # 试卷
                            self.recommend.click_game_list()  # 点击 大题

                        if self.filter.wait_check_page():  # 页面检查点
                            self.recommend.source_type_selected()  # 具体操作

                            name = self.recommend.label_name()  # 所有标签
                            label = name[0].text  # 标签名
                            name[0].click()  # 选择一个标签
                            print('选择的标签为:', label)

                            if self.recommend.wait_check_page():  # 页面检查点
                                self.question.filter_button()  # 筛选按钮

                                if self.filter.wait_check_page():  # 页面检查点
                                    self.filter.reset_button()  # 重置按钮
                                    print('点击重置按钮')
                                    self.filter.commit_button()  # 确定按钮

                                    if self.recommend.wait_check_page():
                                        self.recommend.back_up_button()  # 点击 返回按钮
                                        if self.user.wait_check_page():  # 页面检查点
                                            self.home.click_tab_hw()  # 回首页
                else:
                    print('未进入 我的收藏 页面')
            else:
                print('未进入个人中心页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
