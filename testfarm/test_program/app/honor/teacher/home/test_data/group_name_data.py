#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 班级名称由1~30位中英文及数字组成，可以包含符号
group_data = (
    {'name': '', 'count': '0', 'status': 'false'},  # 为空
    {'name': '   ', 'count': '3', 'status': 'true', 'assert': '组名 不能为空'},  # 为3个空格
    {'name': '1', 'count': '1', 'status': 'true'},  # 1个字符
    {'name': 'D', 'count': '1', 'status': 'true'},  # 1个字符  区分大小写
    {'name': "van在线教育124", 'count': '10', 'status': 'true'},
    {'name': 'v@在线$123', 'count': '8', 'status': 'true'},  # 特殊字符
    {'name': '2VANTHNKvan1ink以数字studeVANTH7INKr', 'count': '34', 'status': 'false'},   # 多于30个字符 - 34个
    {'name': '8VANTH7INK4v     nkstu在线', 'count': '20', 'status': 'true'},   # 24个字符  5个连续空格
    {'name': '180q azws1werQA ZWS XEUY19在线教育', 'count': '30', 'status': 'true'},  # 30个字符  空格
    {'name': 'D', 'count': '4', 'status': 'true', 'assert': '同一班级 组名不能重复'}  # 不可重名
)
