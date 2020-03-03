#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from conf.base_page import BasePage
from conf.decorator import teststeps


class JudgeType(BasePage):
    """判断元素类型"""

    @teststeps
    def is_chinese(self, item):
        """判断一个unicode是否是汉字"""
        if u'\u4e00' <= item <= u'\u9fa5':
            return True
        else:
            return False

    @teststeps
    def is_alphabet(self, item):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= item <= u'\u005a') or (u'\u0061' <= item <= u'\u007a'):
            return True
        else:
            return False

    @teststeps
    def is_number(self, item):
        """判断一个unicode是否是数字"""
        if item >= u'\u0030' and item <= u'\u0039':
            return True
        else:
            return False
