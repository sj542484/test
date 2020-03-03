#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
from conf.base_config import GetVariable as gv


class GetVariable(object):
    """班级 -- 作业、试卷、口语参数化数据"""
    # test_cases
    VANCLASS = '自动化测试'

    HW_TITLE = "口语/习题·{}"  # 习题作业 分析、奖杯等
    SPOKEN = '口语作业(口语)'
    SPOKEN_MERGE = '习题口语合并(口语)'

    PAPER_TITLE = "卷子·{}"  # 卷子作业 分析

    SPOKEN_EDIT = '口语测试' + str(random.randint(100, 999))  # 编辑
    HW_TEST = '编辑测试' + str(random.randint(100, 999))  # 编辑

    DETAIL = gv.ACCOUNT[-4:]  # 班级成员 学生详情页

    APPLY = 'class one'  # 入班申请/ 小组管理
    INVITE = '邀请学生-{}'  # 邀请学生

    FREE_TEACHER = '18711111236'  # 学校名称 自由老师
    FREE_PWD = '456789'  # 学校名称
