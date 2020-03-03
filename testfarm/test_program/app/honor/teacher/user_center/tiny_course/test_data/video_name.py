#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI

# 1~30字符 ，包含空格
import datetime

nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")  # 生成当前时间
name_data = [{'name': 'autotest微课_' + "".join(str(nowTime))},
             {'name': 'autotest_拍摄' + "".join(str(nowTime))},
             ]
