#!/usr/bin/env python
# encoding:UTF-8

# 验证当前密码、新密码与确认密码输入要一致；密码由6~20位英文及数字组成
reset_pwd = (
    {'old': '456789', 'new': '', 'commit': '', 'assert': ''},  # 为空
    {'old': '456789', 'new': '      ', 'commit': '      ', 'assert': ''},  # 多个空格 -6个
    {'old': '456789', 'new': '180we', 'commit': '180we', 'assert': '密码 格式不正确'},   # 少于6个字符 - 5位
    {'old': '456789', 'new': '456789sfsfwrzxcsad1sa', 'commit': '456789sfsfwrzxcsad1sa', 'assert': '密码 格式不正确'},  # 多于20个字符 - 21个数字、字母组合
    {'old': '456789', 'new': 'q12a z.w@S勿x', 'commit': 'q12a z.w@S勿x', 'assert': '密码 格式不正确'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合

    {'old': '123qwe', 'new': '你好2018world', 'commit': '你好2018world', 'assert': '旧密码未通过认证'},   # 原密码验证不通过

    {'old': '456789', 'new': 'We2018', 'commit': 'We2018'},  # 6个字符 - 字母、数字
    {'old': 'We2018', 'new': '201801', 'commit': '201801'},  # 6个字符 - 数字
    {'old': '201801', 'new': 'VAnthi', 'commit': 'VAnthi'},  # 6个字符 - 大、小写字母
    {'old': 'VAnthi', 'new': 'VANTHINK201801vanTHK', 'commit': 'VANTHINK201801vanTHK'},  # 20个字符
    {'old': 'VANTHINK201801vanTHK', 'new': '123321', 'commit': '123321'},  # 数字、英文字符组合
    {'old': '123321', 'new': '456789', 'commit': '456789'},  # 改回原来密码
)
