#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.home.object_page import DraftPage
from app.honor.teacher.home.object_page.vanclass_hw_detail_page import HwDetailPage
from app.honor.teacher.home.object_page import ReleasePage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page import VanclassPage
from app.honor.teacher.home.test_data.draft_data import GetVariable as gv
from app.honor.teacher.login.object_page import TloginPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class DraftBox(unittest.TestCase):
    """草稿箱 - 修改草稿"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = HwDetailPage()
        cls.van = VanclassPage()
        cls.release = ReleasePage()
        cls.get = GetAttribute()
        cls.draft = DraftPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_draft_box_assign(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.timing_button()  # 定时作业 按钮

            if self.draft.wait_check_page():  # 页面检查点
                self.draft.draft_box_button()  # 草稿箱 按钮

                if self.draft.wait_check_draft_page():  # 页面检查点
                    if self.draft.wait_check_draft_list_page():
                        content = self.draft_box_operation()  # 草稿箱
                        self.draft_detail_operation(content)  # 草稿详情页具体操作

                        self.judge_draft_operation(content)  # 验证 草稿箱
                        # self.judge_result_operation(van)  # 验证 班级 习题列表

                    elif self.home.wait_check_empty_tips_page():
                        print('草稿箱 暂无数据')
                else:
                    print('未进入草稿箱')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def draft_box_operation(self):
        """草稿 列表"""
        print('---------------------草稿 列表-------------------')
        content = []  # 草稿名 元素
        name = []  # 草稿名 text
        draft = self.draft.draft_name()  # 草稿名 元素
        create = self.draft.draft_time()  # 创建时间
        num = self.draft.draft_count()  # 题数

        for i in range(len(num)):
            print(draft[i].text, '\n',
                  create[i].text, '\n',
                  num[i].text)
            print('------------------')
            content.append(draft[i])
            name.append(draft[i].text)
        return content, name

    @teststeps
    def draft_detail_operation(self, content):
        """草稿 详情页"""
        if self.home.wait_check_empty_tips_page():
            print('暂无草稿')
            self.home.back_up_button()  # 返回按钮
            self.home.click_tab_hw()  # 返回首页
        else:
            content[0][0].click()  # 随机进去一个草稿
            print('------------草稿 %s 详情页:--------------' % content[1][0])
            self.home.tips_content_commit()  # 温馨提示 页面

            if self.release.wait_check_release_page():  # 页面检查点
                if self.release.wait_check_release_list_page():
                    name = self.release.hw_name_edit()  # 作业名称 编辑框
                    if name.text != content[1][0]:
                        print('★★★ Error- 详情页草稿名与草稿箱不一致', name.text, content[1][0])

                    name.send_keys(r'' + gv.DRAFT_MODIFY)
                    print(self.release.hw_title(), ":", name.text)  # 打印元素 作业名称

                    print(self.release.hw_list(), ":", self.release.hw_list_tips())  # 打印元素 题目列表
                    self.release.hw_mode_operation()  # 作业模式 操作
                    self.release.hw_vanclass_list()  # 班级列表
                    self.release.choose_class_operation()  # 选择班级 学生

                    if self.release.wait_check_release_page():  # 页面检查点
                        self.release.hw_adjust_order()  # 调整题目顺序

                        if self.release.wait_check_release_page():  # 页面检查点
                            # self.release.assign_button()  # 不发布！！！ 因为草稿箱只有一个测试数据了
                            self.home.back_up_button()
                            if self.draft.wait_check_draft_list_page():
                                print('-----------------------------------------')
                                print('取消编辑')
                                self.home.back_up_button()  # 返回 定时作业 页面
                                if self.draft.wait_check_page():
                                    self.home.back_up_button()  # 返回 主界面
                        else:
                            print('选择班级学生后，未返回 发布作业 页面')
                    else:
                        print('调整题目顺序后，未返回 发布作业 页面')
            else:
                print('未进入 发布作业 页面')

    @teststeps
    def judge_draft_operation(self, content):
        """草稿箱 验证"""
        if self.home.wait_check_page():  # 主页面检查点
            print('----------------验证布置结果 草稿箱----------------')
            self.home.timing_button()  # 定时作业 按钮

            if self.draft.wait_check_page():  # 页面检查点
                self.draft.draft_box_button()  # 草稿箱 按钮
                if self.draft.wait_check_draft_page():  # 页面检查点
                    if self.draft.wait_check_draft_list_page():

                        name1 = self.draft.draft_name()  # 草稿名
                        if content[1][0] != name1[0].text:
                            print('★★★ Error- 取消编辑草稿失败')
                        else:
                            print('取消编辑成功')
                    elif self.home.wait_check_empty_tips_page():
                        print('取消编辑成功')

                    self.home.back_up_button()  # 返回 定时作业
                    if self.draft.wait_check_page():  # 页面检查点
                        self.home.back_up_button()  # 返回主界面
                else:
                    print('未再次进入 草稿箱')

    @teststeps
    def judge_result_operation(self, van):
        """验证布置结果 班级习题列表"""
        if self.home.wait_check_page():  # 页面检查点
            print('-------------验证布置结果 班级习题列表-------------')
            SwipeFun().swipe_vertical(0.5, 0.8, 0.2)
            name = self.home.item_detail()  # 条目名称
            for i in range(len(name)):
                var = self.home.vanclass_name(name[i].text)  # 班级名
                if var == van:
                    name[i].click()  # 进入班级

                    if self.van.wait_check_page(var):  # 页面检查点
                        if self.van.wait_check_list_page():
                            hw = self.van.hw_name()  # 作业名
                            title = self.home.vanclass_name(hw[0].text)
                            if title != gv.DRAFT_MODIFY:
                                print('★★★ Error- 布置作业失败', gv.DRAFT_MODIFY, title)
                            else:  # 恢复测试数据
                                print('布置作业成功')
                                hw[0].click()
                                if self.detail.wait_check_page():  # 页面检查点
                                    self.detail.delete_commit_operation()  # 删除作业 具体操作
                        elif self.home.wait_check_empty_tips_page():
                            print('★★★ Error-草稿箱为空, 布置作业失败')

                        if self.van.wait_check_page(van):
                            self.home.back_up_button()  # 返回 主界面
                    else:
                        print('未进入班级:', van)
                    break
