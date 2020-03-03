#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time


class GetVariable(object):
    """test_cases/test_cases 发布作业 - 作业名"""
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())   # 生成当前时间

    VAN_HW_ASSIGN = '班级作业编辑assign' + str(now_time)  # test004

