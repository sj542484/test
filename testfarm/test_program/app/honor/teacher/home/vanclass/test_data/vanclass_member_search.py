#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

#
search_data = [
    {'search': ''},  # 为空
    {'search': '    '},  # 4个空格
    {'search': '万w'},  # 2位 字母汉字
    {'search': 'zaqwsx'},  # 6位字母
    {'search': '12你2hldw4512你2hldw45'},   # 中文、数字、英文字符组合 - 20位
    {'search': "'1q.w@S勿2:"},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合 - 9位
    {'search': 'yueg!##@%)56231sadyueg!##@%)56231sadyueg!##@%)56231sadyueg!##@%)56231sadyueg!##@%)56231sadyueg!##@%)56231sadyueg!##@%)56231sadyueg!##@%)56231sad'},  # 中文、数字、英文字符组合 - 104位

    {'search': '1'},  # 1位 数字
    {'search': '810111111'},  # 9位数字
    {'search': '11111111111'},  # 11位 数字
    {'search': '18711111111'},  # 手机号

    {'search': '18711111234'},  # 手机号
    {'search': 'sff'},  #
    ]
