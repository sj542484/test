#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
# 作业名称必填，字符限制在1~50，可以输入英文、字母、中文、符号；多于50自动截断

hw_data = (
    {'name': '',
     'mode': 'reach',
     'assert_name': '请输入作业名称'},  # 为空

    {'name': '   ',
     'mode': 'free',
     'assert_name': '请输入作业名称'},  # 为3个空格

    {'name': '2VANvan数字g2VANvan数字g2VANvan数字g2VANvan数字g2VANvan数字g我', 'mode': 'reach'},   # 51个汉字和字母组合

    {'name': '1', 'mode': 'reach'},  # 1个字符

    {'name': 'D', 'mode': 'free'},  # 1个字符  区分大小写

    {'name': '作业1234567890', 'mode': 'reach'},  # 为空

    {'name': '一年级三班2019年9月xx日 练习作业_定时', 'mode': 'free'},  # 为3个空格

    {'name': "v育9", 'mode': 'reach'},  # 3个字

    {'name': "  van在1  ", 'mode': 'free'},  # 10个字符  空格

    {'name': 'V4v     在V4v     在',
     'mode': 'reach',
     'date': '3',
     'dire': 'up'},   # 18个字符  5个连续空格

    {'name': 'v@在_$(3)',
     'mode': 'free',
     'date': '3',
     'dire': 'down'},  # 特殊字符

    {'name': '18 aA X9万在118 aA X9万在12345618 aA X9万在118 aA X9万在12',
     'mode': 'reach',
     'date': '4',
     'dire': 'down'},  # 50个字符  空格

    {'name': "小升初首字母填空——“形容词”专练，赶快练起来！", 'mode': 'free'},  # 11个汉字
)
