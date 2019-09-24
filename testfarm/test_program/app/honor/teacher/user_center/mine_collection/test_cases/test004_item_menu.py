#!/usr/bin/env python
# encoding:UTF-8
import unittest
import time

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.question_basket_page import QuestionBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center.mine_collection.object_page.mine_collect_page import CollectionPage
from app.honor.teacher.user_center.mine_recommend.object_page.mine_recommend_page import RecommendPage
from app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Collection(unittest.TestCase):
    """我的收藏 -- 题单条目右侧菜单"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.filter = FilterPage()
        cls.collect = CollectionPage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()

        cls.recommend = RecommendPage()
        cls.basket = QuestionBasketPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_collection_menu_operation(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user.wait_check_page():  # 页面检查点
                self.user.click_mine_collection()  # 点击 我的收藏
                if self.collect.wait_check_page():  # 页面检查点
                    if self.home.wait_check_empty_tips_page():
                        print('暂无 题单收藏')
                        self.add_collection_operation()  # 添加收藏

                    if self.collect.wait_check_list_page():  # 是否有收藏
                        print('-----------------我的收藏 题单-------------------')
                        var = self.item_operation()  # 具体操作
                        self.judge_basket_result(var)  # 加入题筐结果 验证
                        self.cancel_collection_operation()  # 恢复测试数据 - 取消收藏
                        self.judge_recommend_result(var)  # 加入我的推荐结果 验证
                else:
                    print('未进入 我的收藏 页面')
            else:
                print('未进入个人中心页面')
            if self.user.wait_check_page():  # 页面检查点
                self.home.click_tab_hw()  # 回首页
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def item_operation(self):
        """收藏条目 的右端菜单具体操作"""
        name = self.question.question_name()  # 题单
        author = self.question.question_author()  # 老师
        item = author[0].text
        print(name[1][0], '  ', item)
        name[0][0].click()  # 进入题单详情页

        content = []
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():
                title = self.question.question_name()  # 获取 小游戏名
                if len(title[0]) > 1:
                    content.append(title[1][-2])  # 页面中倒数第二道题
                else:
                    content.append(title[1][0])  #
                self.home.back_up_button()  # 返回 我的收藏 页面

                if self.collect.wait_check_page():
                    if self.collect.wait_check_list_page():  # 是否有收藏
                        self.collect.menu_button(0)  # 右侧菜单按钮
                        time.sleep(1)
                        self.collect.recommend_to_school()  # 推荐到学校
                        self.filter.choose_school_label()  # 选择本校标签

                        print('推荐到学校:')
                        if Toast().find_toast('加入成功'):
                            print(' 推荐成功')
                        print('----------------')

                        self.collect.menu_button(0)  # 右侧菜单按钮
                        time.sleep(1)
                        print('加入题筐:')
                        self.collect.put_to_basket()  # 加入题筐
                        if Toast().find_toast('添加成功'):
                            print(' 添加题筐成功')
                        print('----------------')

                        self.collect.menu_button(0)  # 右侧菜单按钮
                        time.sleep(1)
                        print('贴标签：')
                        self.collect.stick_label()  # 贴标签

                        if self.collect.wait_check_label_page():
                            self.collect.check_box(0)  # 选择标签
                            self.collect.save_button()  # 保存按钮
                            if Toast().find_toast('贴标签成功'):
                                print(' 贴标签成功')
                        return content[0], item, name[1][0]

    @teststeps
    def add_collection_operation(self):
        """添加收藏- 题单"""
        self.home.back_up_button()  # 返回 个人中心页面
        if self.user.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单'):  # 页面检查点
                print('添加收藏- 题单')
                SwipeFun().swipe_vertical(0.5, 0.9, 0.2)

                for i in range(1, 3):  # 加2道题
                    if self.question.wait_check_page('题单'):  # 页面检查点
                        item = self.question.question_name()  # 获取
                        item[0][i].click()  # 点击第X道题单

                        if self.detail.wait_check_page():  # 页面检查点
                            if self.detail.wait_check_list_page():  # 题单信息加载完成
                                self.detail.collect_button()  # 收藏按钮
                                if self.detail.wait_check_page():  # 页面检查点
                                    self.home.back_up_button()

                if self.question.wait_check_page('搜索'):  # 页面检查点
                    self.home.click_tab_profile()  # 个人中心
                    if self.user.wait_check_page():  # 页面检查点
                        self.user.click_mine_collection()  # 点击 我的收藏

                        if self.collect.wait_check_page():  # 页面检查点
                            if not self.collect.wait_check_list_page():  # 是否有收藏
                                if self.home.wait_check_empty_tips_page():
                                    print('★★★ Error- 添加收藏失败')

    @teststeps
    def judge_basket_result(self, var):
        """验证 加入题筐结果"""
        if self.collect.wait_check_page():  # 页面检查点
            print('----------------验证 加入题筐结果---------------')
            print(var[0])
            self.question.question_basket()  # 题筐 按钮
            if self.basket.wait_check_page():  # 页面检查点
                name = self.question.question_name()  # 获取 小游戏名
                check = self.basket.check_button()  # 单选框

                for i in range(len(name[0])):
                    if name[1][i] == var[0]:
                        print('加入题筐成功')
                        check[i].click()
                        break

                if self.basket.wait_check_page():  # 页面检查点
                    if self.basket.wait_check_list_page():
                        self.basket.out_basket_button()  # 移出题筐 按钮
                        if self.basket.wait_check_page():  # 页面检查点
                            self.home.back_up_button()  # 返回 我的收藏 页面

    @teststeps
    def cancel_collection_operation(self):
        """恢复测试数据 - 取消收藏"""
        if self.collect.wait_check_page():  # 页面检查点
            if self.collect.wait_check_list_page():
                print('-------------恢复测试数据 - 取消收藏------------')
                item = self.question.question_name()  # 获取
                for z in range(len(item[0])):
                    if self.collect.wait_check_list_page():
                        name = self.question.question_name()  # 获取
                        print(name[1][0])
                        self.collect.menu_button(0)  # 为了保证脚本每次都可以运行，故将加入收藏的题单取消收藏

                        if self.home.wait_check_tips_page():
                            self.collect.cancel_collection()  # 取消收藏
                            print('确定取消收藏')
                            print('------------------')

    @teststeps
    def judge_recommend_result(self, var):
        """验证 加入我的推荐 结果"""
        if self.collect.wait_check_page():
            print('--------------验证 加入我的推荐 结果------------')
            self.home.back_up_button()  # 返回个人中心 页面
            if self.user.wait_check_page():
                self.user.click_mine_recommend()  # 我的推荐

                if self.recommend.wait_check_page():
                    if self.recommend.wait_check_list_page():
                        title = self.question.question_name()  # 题单
                        author = self.question.question_author()  # 老师

                        if var[2] != title[1][0] or var[1] != author[0].text:
                            print('★★★ Error- 加入我的推荐 失败', var[2], title[1][0])
                        else:
                            print(var[2], '  ', var[1])
                            print('加入 我的推荐成功')

                        self.recommend.menu_button(0)
                        self.home.tips_commit()  # 温馨提示 -- 确定
                        print('确定删除')
                    elif self.home.wait_check_empty_tips_page():
                        print('暂无数据')
                        print('★★★ Error- 加入我的推荐 失败')

                    if self.recommend.wait_check_page():
                        self.home.back_up_button()  # 返回 个人中心 页面

