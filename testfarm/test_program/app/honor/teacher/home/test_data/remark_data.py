#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 班级名称由1~30位中英文及数字组成，可以包含符号
remark_data = (
    {'name': '', 'count': '0', 'status': 'false'},  # 为空
    {'name': '1', 'count': '1', 'status': 'true'},  # 1个字符
    {'name': 'D', 'count': '1', 'status': 'true'},  # 1个字符  区分大小写
    {'name': "van在线教育12", 'count': '10', 'status': 'true'},
    {'name': 'van在线教育12', 'count': '10', 'status': 'true'},
    {'name': 'v@在线$123', 'count': '8', 'status': 'true'},  # 特殊字符
    {'name': '2VANTHNKvan1ink以数字studeVANTH7INKr', 'count': '34', 'status': 'false'},   # 多于30个字符 - 34个
    {'name': '8VANTH7INK4v     nkstu在线', 'count': '20', 'status': 'true'},   # 24个字符  5个连续空格
    {'name': '180q azws123xQA ZWS XEUY19在线教育', 'count': '30', 'status': 'true'},  # 30个字符  空格
    {'name': 'YB字体', 'count': '5', 'status': 'true', 'assert': '班级名 已存在'}  # 不可重名
)
