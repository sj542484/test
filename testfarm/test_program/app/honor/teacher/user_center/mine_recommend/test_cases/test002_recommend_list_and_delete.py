#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


class Recommend(unittest.TestCase):
    """我的推荐 -- 列表"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()

        cls.recommend = RecommendPage()
        cls.question = TestBankPage()
        cls.basket = QuestionBasketPage()
        cls.detail = QuestionDetailPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_recommend_list(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_recommend()  # 点击 我的推荐
                if self.recommend.wait_check_page():  # 页面检查点
                    if self.home.wait_check_empty_tips_page():
                        print('暂无 题单推荐')
                        self.add_recommend_operation()  # 添加 题单推荐

                    if self.recommend.wait_check_list_page():  # 页面检查点
                        print('-----------------我的推荐 题单-------------------')
                        self.item_operation()  # 具体操作
                        self.cancel_recommend_operation()  # 恢复测试数据 - 删除推荐

                    if self.recommend.wait_check_page():  # 页面检查点
                        self.question.question_basket()  # 题筐 按钮
                        if self.basket.wait_check_page():  # 页面检查点
                            self.home.back_up_button()

                    if self.recommend.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 点击 返回按钮
                else:
                    print('未进入 我的推荐 页面')
                if self.user.wait_check_page():  # 页面检查点
                    self.home.click_tab_hw()  # 回首页
            else:
                print('未进入个人中心页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def add_recommend_operation(self):
        """添加推荐 题单"""
        self.home.back_up_button()  # 返回 个人中心页面
        if self.user.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                print('添加推荐- 题单')
                SwipeFun().swipe_vertical(0.5, 0.9, 0.2)
                for i in range(1, 3):  # 加2道题
                    if self.question.wait_check_page('题单'):  # 页面检查点
                        item = self.question.question_name()  # 获取
                        item[0][i].click()  # 点击第X道题单

                        if self.detail.wait_check_page():  # 页面检查点
                            if self.detail.wait_check_list_page():  # 题单信息加载完成
                                self.detail.recommend_button()  # 推荐按钮
                                if not Toast().find_toast('推荐成功'):  # 获取toast
                                    print(' ★★★ Error- 未弹toast：推荐失败')

                                if self.detail.wait_check_page():  # 页面检查点
                                    self.home.back_up_button()

                if self.question.wait_check_page('搜索'):  # 页面检查点
                    self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

                    if self.user.wait_check_page():  # 页面检查点
                        self.user.click_mine_recommend()  # 点击 我的推荐
                        if self.recommend.wait_check_page():  # 页面检查点
                            if not self.recommend.wait_check_list_page():  # 是否有推荐列表
                                if self.home.wait_check_empty_tips_page():
                                    print('★★★ Error- 添加推荐失败')

    @teststeps
    def item_operation(self):
        """收藏条目 的右端菜单具体操作"""
        name = self.question.question_name()  # 题单
        author = self.question.question_author()  # 老师
        for i in range(len(author)):
            mode = self.question.question_type(i)
            num = self.question.question_num(i)
            print(mode, '\n', name[1][i], '\n', num, '\n', author[i].text)
            print('------------------------------------')

        print(name[1][0], '  ', author[0].text)
        name[0][0].click()  # 进入题单详情页

        if self.detail.wait_check_page():
            self.home.back_up_button()  # 返回 我的推荐 页面

    @teststeps
    def cancel_recommend_operation(self):
        """删除推荐"""
        if self.recommend.wait_check_page():  # 页面检查点
            if self.recommend.wait_check_list_page():
                print('-----------------删除推荐-----------------')
                item = self.question.question_name()  # 获取
                var = 0
                for z in range(len(item[0])):
                    if self.recommend.wait_check_list_page():
                        name = self.question.question_name()  # 获取
                        print(name[1][0])
                        if self.recommend.wait_check_page():
                            self.recommend.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入收藏的题单取消收藏

                            self.home.tips_commit()  # 温馨提示 -- 确定
                            print('确定删除')
                            var += 1

                self.judge_delete(item, var)  # 验证 删除推荐 结果

    @teststeps
    def judge_delete(self, item, var):
        """验证 删除推荐 结果"""
        print('-------------验证 删除推荐 结果------------')
        if self.recommend.wait_check_list_page():
            name = self.question.question_name()  # 题单
            if len(name[0]) != len(item[0]) - var:
                print('★★★ Error- 取消推荐失败', item[1][0])
            else:
                print('取消推荐成功')
        elif self.home.wait_check_empty_tips_page():
            print('取消推荐成功')
