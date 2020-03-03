#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time


class GetVariable(object):
    """test_cases/test_cases 发布作业 - 作业名"""
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())   # 生成当前时间

    HW_MODIFY = '定时作业MODIFY' + str(now_time)  # test004

    DRAFT_MODIFY = '测试draft' + str(now_time)  # test001

    VAN_HW_ASSIGN = '班级作业编辑assign' + str(now_time)  # test004
    
    ASSIGN_AGAIN = '再次发布作业' + str(now_time)
