#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 班级名称由1~10位中英文及数字组成，可以包含符号
class_data = (
    {'name': '', 'count': '0'},  # 为空
    {'name': '   ', 'count': '3', 'assert': '(C306)班级名称由1-10位中英文及数字组成'},  # 为3个空格
    {'name': '1', 'count': '1'},  # 1个字符
    {'name': 'D', 'count': '1'},  # 1个字符  区分大小写
    {'name': "van在线教育124", 'count': '10'},  # 10个字符
    {'name': "  van在1  ", 'count': '9'},  # 10个字符  空格
    {'name': '2VANvan数字g', 'count': '10'},  # 10个汉字和字母组合
    # {'name': 'V4v     在', 'count': '9'},  # 9个字符  5个连续空格
    {'name': 'v@在线$123', 'count': '8'},  # 特殊字符
    {'name': '18 aA X9万在8', 'count': '11'},  # 11个字符  空格    （自动截断）
    {'name': "万星在线教育有限公司天", 'count': '11'},  # 11个汉字

    {'name': 'block', 'count': '5'},  # 恢复测试数据
    {'name': 'YB字体', 'count': '4', 'assert': '(C306)班级名 已经存在'}  # 不可重名
)
