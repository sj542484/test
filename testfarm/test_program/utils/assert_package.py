#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import os
import sys
import time
import unittest

from conf.base_page import BasePage
from conf.report_path import ReportPath
from testfarm.test_program.utils.validate_file_name import validate_name


class MyToast(unittest.TestCase):
    """提示信息 错误获取"""
    errors = []

    def get_error(self):
        return self.errors

    def except_error(self, msg):
        print('except_error:', msg)
        self.errors.append(msg)

    # 重写断言方法
    def toast_assert(self, func, first, second=True, msg=None):
        try:
            super().assertEqual(first, second, msg)
        except Exception as msg:
            nowTime = time.strftime("%Y%m%d%H%M%S")
            MyToast().except_error(sys.exc_info())
            info = validate_name(str(msg).split('\n')[0])
            file = 'Fail--{}'.format(func) + info + '_' + nowTime + '.png'
            file_path = ReportPath().get_path() + "/image"

            if not os.path.exists(file_path):  # 判断文件夹是否存在
                os.mkdir(file_path)
            file = os.path.join(file_path, file)
            driver = BasePage().get_driver()
            driver.get_screenshot_as_file(file)

            pass
            # raise msg  # 加上下面这句，断言不通过时，测试用例也不能通过


class MyAssert(unittest.TestCase):
    """提示信息 错误获取"""

    def assertEqual_new(self, first, second, msg=None):
        super().assertEqual(first, second, msg=msg)

    def assertTrue_new(self, first, msg=None):
        super().assertTrue(first, msg=msg)
