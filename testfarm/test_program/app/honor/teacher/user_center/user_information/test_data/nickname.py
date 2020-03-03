#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

# 昵称：由2~20位中文、数字及英文组成，数字不能做首位；可以允许有字符【.】【@】【空格】
nickname_data = (
    {'nick': ''},  # 为空
    {'nick': 'VANTHINKvanthinkstude'},   # 多于20个字符 - 21个
    {'nick': 'VANTH7INK4vanthink8stude'},   # 多于20个字符 - 24个

    {'nick': '180qazwsx', 'assert': '昵称不能以数字开头'},  # 数字为首位
    {'nick': '4212345678909876543', 'assert': '昵称不能以数字开头'},  # 数字  19个字符
    {'nick': 'q#*azw180sx', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 其他特殊字符
    {'nick': '  ', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 两个空格
    {'nick': '          ', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 多个空格 -10个
    {'nick': 'q', 'assert': '昵称由2~20位中文，数字，英文组成'},   # 少于2个字符 - 1个

    {'nick': 'We'},    # 2个字符
    {'nick': '.@'},    # 2个字符
    {'nick': 'VANTHINKVANTHINKVANT'},   # 20个字符 -大写字母
    {'nick': 'vanthinkvanthink'},   # 纯小写字母 - 16个
    {'nick': '你好万星在线教育平台教师端'},  # 纯中文 -13个
    {'nick': '你好2018world'},  # 中文、数字、英文字符组合
    {'nick': 'f学生2018 z@WSx'},   # 中文、数字、英文、大写字母、空格、@字符组合
    {'nick': 'q12a z.w@S勿x'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
    {'nick': 'sff'},  # 改回原来昵称
    )
