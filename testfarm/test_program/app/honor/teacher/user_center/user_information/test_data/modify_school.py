#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 学校老师不可修改，会提示“没有权限修改学校信息！”；
# 自由老师可以修改成任意学校名称，字符数量限制在40位，可以是中文、数字、字母
school_data = [
    {'sch': ''},  # 为空
    {'sch': '  '},  # 2个空格
    {'sch': '#￥%#？@'},  # 特殊字符  - 6个字符
    {'sch': '万星在线'},  # 中文 - 4个字符
    {'sch': '123456342423443213423'},  # 数字 - 21个字符
    {'sch': 'VANTHINKvanthinkstudesdfs'},  # 字母  - 21个字符
    {'sch': '123456sfsfwrzdf但是d1sa'},  # 中文、数字、字母组合  - 21个字符
    {'sch': 'sdfs123456sfsfwrzdf但是d1sa万星在线VANTHINKvanw'},  # 多于40个字符 - 41个
]
