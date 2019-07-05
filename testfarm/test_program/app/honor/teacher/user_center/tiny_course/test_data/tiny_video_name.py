#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 1~50字符 ，包含空格
name_data = (
    {'name': '', 'assert': '课程名不能为空'},  # 为空
    {'name': '  '},  # 2 个空格
    {'name': '2'},  # 1个字符
    {'name': '万1'},  # 2个字符
    {'name': '重  点 ew'},  # 3个空格
    {'name': '45Qvip'},  # 6个字符
    {'name': 'QiE 4万6'},  # 7个字符
    {'name': '重点'},  # 2跟个字符
    {'name': '我的题库 -  万星在线_Test1万星在线test1万星在线_test1万星在线_test1万星在线', 'assert': '1~50字符 ，包含空格'},  # 51个字符
    {'name': '万星在线_Test'},  # 9个字符
)
