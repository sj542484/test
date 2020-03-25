#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import time


class GetVariable(object):
    """test_cases/test_cases 发布作业 - 作业名"""
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())   # 生成当前时间
    VAN_HW_ASSIGN = '班级作业编辑assign' + str(now_time)  # test004
    RECOMMEND = '试卷推荐到学校' + str(now_time)

    SPOKEN_EDIT = '口语测试' + str(random.randint(100, 999))  # 编辑
    HW_TEST = '编辑测试' + str(random.randint(100, 999))  # 编辑
    ASSIGN_AGAIN = '再次发布作业' + str(now_time)
