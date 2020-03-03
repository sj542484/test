#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time


class GetVariable(object):
    """test_cases/test_cases 发布作业 - 作业名"""
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())   # 生成当前时间

    HW_TIME = '定时作业' + str(now_time)  # test002
    HW_TIME_MUL = '作业_多定时' + str(now_time)  # test003

    HW_ASSIGN = '作业 assign' + str(now_time)  # test006
    SPOKEN_ASSIGN = '口语作业 assign' + str(now_time)  # test0057
