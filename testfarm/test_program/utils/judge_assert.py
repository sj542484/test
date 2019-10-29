#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI

import unittest


class JudgeAssert(unittest.TestCase):

    def judgeEqual(self, first, second, msg=None):
        """判断a==b"""
        self.assertEqual(first, second, msg)
        print('\t✅数据验证成功，预期：%s, 实际：%s')

    def judgeNotEqual(self, first, second, msg=None):
        """判断a！=b"""
        self.assertNotEqual(first, second, msg)

    def judgeTrue(self, expr, msg=None):
        """bool(expr) is True"""
        self.assertTrue(expr, msg)

    def judgeFalse(self, expr, msg=None):
        """bool(expr) is True"""
        self.assertFalse(expr, msg)

    def judgeIn(self, member, container, msg=None):
        """a in b"""
        self.assertIn(member, container, msg)

    def assertNotIn(self, member, container, msg=None):
        """a not in b"""
        self.assertNotIn(member, container, msg)

    def judgeLess(self, a, b, msg=None):
        """Just like self.assertTrue(a < b), but with a nicer default message."""
        self.assertLess(a, b, msg)

    def judgeAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        """"""
        self.assertAlmostEqual(first, second, places, msg, delta)
