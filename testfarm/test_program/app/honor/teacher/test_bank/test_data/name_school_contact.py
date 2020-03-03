#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

# 试卷名称
name_data = (
    {'name': ''},  # 为空
    {'name': 'VANTHINKvanthinkstude'},   # 多于20个字符 - 21个
    {'name': 'VANTH7INK4vanthink8stude'},   # 多于20个字符 - 24个

    {'name': '180qazwsx', 'assert': '昵称不能以数字开头'},  # 数字为首位
    {'name': '4212345678909876543', 'assert': '昵称不能以数字开头'},  # 数字  19个字符
    {'name': 'q#*azw180sx', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 其他特殊字符
    {'name': '  ', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 两个空格
    {'name': '          ', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 多个空格 -10个
    {'name': 'q', 'assert': '昵称由2~20位中文，数字，英文组成'},   # 少于2个字符 - 1个

    {'name': 'We'},    # 2个字符
    {'name': '.@'},    # 2个字符
    {'name': 'VANTHINKVANTHINKVANT'},   # 20个字符 -大写字母
    {'name': 'vanthinkvanthink'},   # 纯小写字母 - 16个
    {'name': '你好万星在线教育平台学生端'},  # 纯中文 -13个
    {'name': '你好2018world'},  # 中文、数字、英文字符组合
    {'name': 'f学生2018 z@WSx'},   # 中文、数字、英文、大写字母、空格、@字符组合
    {'name': 'q12a z.w@S勿x'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
    {'name': 'sff'},  # 改回原来昵称
    )

# 学校 名称
school_data = (
    {'sch': ''},  # 为空
    {'sch': '  '},  # 2个空格
    {'sch': '#￥%#？@'},  # 特殊字符  - 6个字符
    {'sch': '万星在线'},  # 中文 - 4个字符
    {'sch': '123456342423443213423'},  # 数字 - 21个字符
    {'sch': 'VANTHINKvanthinkstudesdfs'},  # 字母  - 21个字符
    {'sch': '123456sfsfwrzdf但是d1sa'},  # 中文、数字、字母组合  - 21个字符
    {'sch': 'sdfs123456sfsfwrzdf但是d1sa万星在线VANTHINKvanw'},  # 多于40个字符 - 41个
    )

# 联系方式
contact_data = (
    {'contact': '13020670521'},  # 原手机号
    {'contact': '18011111112'},  # 已注册其他手机号
    {'contact': '  '},  # 两个空格
    {'contact': '           '},  # 11个空格
    {'contact': ''},  # 为空
    {'contact': '1'},  # 1个数字
    {'contact': '180111111112'},  # 12位数字
    {'contact': '81011111111'},  # 11位数字 - 非手机号
    {'contact': '你好万星在线教育学生端'},  # 中文、数字、英文字符组合 -11位
    {'contact': '20182018201'},  # 数字 -11位
    {'contact': 'WEhelloDCds'},  # 大小写英文字符-11位
    {'contact': '你好2018world'},  # 中文、数字、英文字符组合 -11位
    {'contact': 'q12 a.w@S勿x'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合

    {'contact': '18011115234'},  # 未注册手机号
    {'contact': '13020670521'},  # 改回原手机号
    )
