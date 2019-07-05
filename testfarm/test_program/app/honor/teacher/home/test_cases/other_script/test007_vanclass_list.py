#!/usr/bin/env python
# encoding:UTF-8
import unittest

from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.home.object_page.adjust_vanclass_page import AdjustVanOrderPage
from testfarm.test_program.app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


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
                self.list_swipe_operation()  # 已有班级数 统计
            else:
                print('暂无班级')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def list_swipe_operation(self):
        """班级列表 滑屏 操作"""
        var = self.vanclass_statistic_operation()  # 获取 班级列表信息
        SwipeFun().swipe_vertical(0.5, 0.75, 0.25)

        title = []
        item = self.home.item_detail()  # 班级条目
        for i in range(len(item)):
            name = self.home.vanclass_name(item[i].text)  # name
            title.append(name)
        last = item[-1].text  # 最后一个作业的title

        index = []
        if len(title) != 10:  # 到底部
            if var in title:  # todo 列表中可能有多个相同作业名
                if last != var:  # 滑动了
                    # print('滑动后到底部')
                    for i in range(len(title)):
                        if title[i] == var:
                            index.append(i + 1)
                            break
                else:
                    # print('到底了')
                    index.append(len(title))

                self.vanclass_statistic_operation(index[0])  # 获取 班级列表信息
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

            return self.list_swipe_operation(index[0])

    @teststeps
    def vanclass_statistic_operation(self, index=0):
        """获取班级列表 及 页面内最后一个name"""
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
        last = self.home.vanclass_name(name[-1].text)  # 最后一个作业的title

        return last

