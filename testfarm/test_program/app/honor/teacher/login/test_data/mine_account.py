#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

# 11位手机号
phone_data = [
    {'username': '18011111897', 'password': '456789', 'assert': '手机号未注册，请先注册'},  # 未注册手机号
    {'username': '81011111112', 'password': '456789'},  # 11位数字 - 非手机号
    {'username': '132345', 'password': '456789'},  # 少于11个数字  是否报错
    {'username': '', 'password': '456789'},  # 手机号为空
    {'username': '           ', 'password': '456789'},  # 11个空格
    {'username': '130你好8world', 'password': '456789'},  # 中文、数字、英文字符组合 -11位
    {'username': '180q2.w@S勿x', 'password': '456789'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
    {'username': '18711111119', 'password': '456789'},  # 已注册有学生身份
    {'username': '187111112347348', 'password': '456789'},  # 15位数字  大于11位输入是否截断  # 已注册有老师身份又有学生身份
    ]

# 6-20位非空字符；只允许设置数字、英文字母（英文字母区分大小写）
pwd_data = [
    {'username': '18711111234', 'password': ''},   # 为空
    {'username': '18711111234', 'password': '      ', 'assert': '手机号或密码错误'},   # 6个空格
    {'username': '18711111134', 'password': '12rdh6W89', 'assert': '手机号或密码错误'},  # 数字 字母组合 区分大小写 正确密码为：123eWr78  9位
    {'username': '18711111234', 'password': '3$#3r@#7r', 'assert': '手机号或密码错误'},  # 输入特殊字符
    {'username': '18711111234', 'password': '1D2a4', 'assert': '手机号或密码错误'},   # 少于6位 数字、字母组合
    {'username': '18711111234', 'password': '12345WE42dlui43213423123', 'assert': '手机号或密码错误'},   # 多于20位  数字、字母组合
    {'username': '', 'password': ''},  # 手机号和密码均不输入
    {'username': '18711111232', 'password': '123eWr78'},  # 正确密码 字母、数字组合 8位
    {'username': '18711111234', 'password': '456789'},  # 正确密码 数字 6位
    ]
