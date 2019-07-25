#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.teacher.login.object_page import TloginPage
from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.home.object_page.adjust_vanclass_page import AdjustVanOrderPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class Vanclass(unittest.TestCase):
    """班级 列表"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.adjust = AdjustVanOrderPage()
        cls.get = GetAttribute()
  
    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_list(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            if self.home.wait_check_van_page():  # 已有班级
                print('----------------班级列表----------------')
                van = self.vanclass_order()  # 班级 列表

                if self.home.wait_check_page():  # 页面检查点
                    self.home.class_sort_button()  # 班级排序 按钮
                    self.adjust.adjust_vanclass_order()  # 调整班级顺序 具体操作
                    self.adjust.confirm_button()  # 确定按钮

                    van2 = self.vanclass_order()  # 班级 列表

                    count = 0
                    for i in range(len(van2)):
                        if van2 != van:
                            count += 1

                    if count == 0:
                        print('★★★ Error- 班级顺序未调整')
                    else:
                        print('调整班级顺序保存成功')
            else:
                print('暂无班级')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def list_swipe_operation(self, content):
        """班级列表 滑屏 操作"""
        var = self.vanclass_statistic_operation(content)  # 获取 班级列表信息
        SwipeFun().swipe_vertical(0.5, 0.75, 0.25)

        if self.home.wait_check_van_page():
            title = []
            item = self.home.item_detail()  # 班级条目
            for i in range(len(item)):
                name = self.home.vanclass_name(item[i].text)  # name
                title.append(name)
            last = item[-1].text  # 最后一个班级的title

            index = []
            if len(title) != 10:  # 到底部
                if var in title:  # todo 列表中可能有多个相同
                    if last != var:  # 滑动了
                        # print('滑动后到底部')
                        for i in range(len(title)):
                            if title[i] == var:
                                index.append(i + 1)
                                break
                    else:
                        # print('到底了')
                        index.append(len(title))

                    self.vanclass_statistic_operation(content, index[0])  # 获取 班级列表信息
            else:
                # print('滑动后未到底部')
                if var in title:  # 未滑够一页
                    # print('未滑够一页')
                    for i in range(len(title)):
                        if title[i] == var:
                            index.append(i + 1)
                            break
                else:
                    index.append(0)

                return self.list_swipe_operation(content, index[0])

    @teststeps
    def vanclass_statistic_operation(self, content, index=0):
        """获取班级列表 及 页面内最后一个name"""
        if self.home.wait_check_van_page():
            name = self.home.item_detail()  # 班号+班级名
            count = self.home.st_count()  # 学生人数

            if len(name) != len(count):  # 滑屏后
                length = min(len(name), len(count))
            else:
                length = len(count)

            for i in range(index, length):
                num = self.home.vanclass_no(name[i].text)  # 班号
                van = self.home.vanclass_name(name[i].text)  # 班级名
                print(van, '  班号:', num, '  学生人数:', count[i].text)
                content.append(van)
            last = self.home.vanclass_name(name[-1].text)  # 最后一个作业的title

            return last

    @teststeps
    def vanclass_order(self):
        """班级 列表"""
        van = []
        self.list_swipe_operation(van)  # 已有班级数 统计

        print('--------------------------------------')
        content = []
        for i in range(len(van)):
            for j in range(len(van[i])):
                content.append(van[i][j])

        return content
