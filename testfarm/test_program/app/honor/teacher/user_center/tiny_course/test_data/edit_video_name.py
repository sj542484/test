#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

# 1~30字符 ，包含空格
name_data = (
    {'name': '  ', 'assert': '课程名不能为空'},  # 2 个空格
    {'name': '2'},  # 1个字符
    {'name': '星'},  # 1个字符
    {'name': '万1'},  # 2个字符
    {'name': '重  点 ew'},  # 3个空格
    {'name': '45Qvip'},  # 6个字符
    {'name': 'QiE 4万6'},  # 7个字符
    {'name': '重点'},  # 2个字符
    {'name': '!万@星￥(重&点)*'},  # 特殊字符
    {'name': '我的题11库 -  万星在线_Test1万星在线test1'},  # 30个字符
    {'name': 'wan万星在线_Test1万星在线test2我题库342-的W'},  # 31个字符
    {'name': '万星在线_Test'},  # 9个字符
    {'name': '万星在线_Test', 'assert': '题目名称已存在'},  # 9个字符
)
