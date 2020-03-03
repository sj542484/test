#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 名字由2-20位中文、英文组成
remark_dict = (
    {'name': '', 'count': '0', 'status': 'false'},  # 为空
    {'name': '1', 'count': '1', 'status': 'true', 'assert': '名字由2-20位中文、英文组成'},  # 1个字符
    {'name': 'D', 'count': '1', 'status': 'true', 'assert': '名字由2-20位中文、英文组成'},  # 1个字符  区分大小写
    {'name': "van在线教育12", 'count': '10', 'status': 'true'},
    {'name': 'van在线教育12', 'count': '10', 'status': 'true'},
    {'name': 'v@在线$123', 'count': '8', 'status': 'true', 'assert': '名字由2-20位中文、英文组成'},  # 特殊字符
    {'name': '2VANTHNKvan1ink以数字studeVANTH7INKr', 'count': '34', 'status': 'false'},   # 多于30个字符 - 34个
    {'name': '8VANTH7INK4v     nkstu在线', 'count': '20', 'status': 'true', 'assert': '名字由2-20位中文、英文组成'},   # 24个字符  5个连续空格
    {'name': '180q azws123xQA ZWS XEUY19在线教育', 'count': '30', 'status': 'true', 'assert': '名字由2-20位中文、英文组成'},  # 30个字符  空格
    {'name': 'YB字体', 'count': '5', 'status': 'true'}  # 不可重名
)
