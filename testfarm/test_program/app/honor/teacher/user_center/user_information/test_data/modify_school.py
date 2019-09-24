#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 学校老师不可修改，会提示“没有权限修改学校信息！”；
# 自由老师可以修改成任意学校名称，字符数量限制在30位，可以是中文、数字、字母
school_data = [
    {'sch': '', 'status': 'true'},  # 为空
    {'sch': '  ', 'status': 'true'},  # 2个空格
    {'sch': '万wW', 'status': 'true'},  # 3位 字母汉字
    {'sch': 'zaqwsx', 'status': 'true'},  # 6位字母
    {'sch': '12你2hldW4512你2hldw45', 'status': 'true'},  # 中文、数字、英文字符组合 - 20位
    # {'sch': "'1q.w@S勿2:", 'status': 'true'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合 - 9位
    # {'sch': 'yueg!##@%)56231s    eg!##@%)56231sa yueg!', 'status': 'true'},  # 中文、数字、英文字符组合 - 41位

    {'sch': '11111111111', 'status': 'true'},  # 11位 数字
    {'sch': '18711111111', 'status': 'true'},  # 手机号
    {'sch': 'W万星  在线@x 123W万星  在—线x 123W万星 在', 'status': 'false'},  # 31位
    # {'sch': '#￥%#？@', 'status': 'true'},  # 特殊字符  - 6个字符
    {'sch': '万星在线', 'status': 'true'},  # 中文 - 4个字符
]
