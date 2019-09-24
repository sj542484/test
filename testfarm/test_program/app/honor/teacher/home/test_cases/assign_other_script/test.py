#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import re

hw =[ "作业详情(习题)","青少版新概念(习题) 1A Unit 3 Lesson 5 单词-2（引用1）"]

for i in range(len(hw)):
    # value = re.match(r".*\（(.*)\）.*|.*\((.*)\).*", hw[i])
    # print(value)
    # print(value.group(1))

    a = re.sub(u"\\(.*?\\)$|\\（.*?\\）$", "", hw[i])
    print(a)
