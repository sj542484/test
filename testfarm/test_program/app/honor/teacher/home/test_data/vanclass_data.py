#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random


class GetVariable(object):
    """班级 -- 作业、试卷、口语参数化数据"""
    # dynamic_info_script
    DY_HW_TITLE = '口语/习题'
    DY_PAPER_TITLE = '卷子'

    # vanclass_script
    MODIFY_VAN = 'block'  # 修改班级

    VANCLASS= '自动化测试'

    HW_TITLE = "口语/习题·{}"  # 习题作业 分析、奖杯等
    HW = "作业详情"
    SPOKEN = '口语作业(口语)'
    SPOKEN_MERGE = '习题口语合并(口语)'

    PAPER_TITLE = "卷子·{}"  # 卷子作业 分析
    PAPER = "译林牛津三起点六上 Unit6 单元测试卷"

    SPOKEN_EDIT = '口语测试' + str(random.randint(100, 999))  # 编辑
    HW_TEST = '编辑测试' + str(random.randint(100, 999))  # 编辑

    MEMBER = 'class one'  # 班级成员
    PHONE = '1134'  # 班级成员 修改备注名  18711111134
    DETAIL = '1234'  # 班级成员 学生详情页 18711111234

    GROUP = 'YB字体'  # 小组管理
    INVITE = '邀请学生-YB字体'  # 邀请学生

    APPLY = 'class one'  # 入班申请
    vanclass_num = '9257'  # 学生端申请 班号 9257

    FREE_TEACHER = '18711111237'  # 学校名称 自由老师
    FREE_PWD = '456789'  # 学校名称

    # 提示信息 参数化数据
    timing_success = '作业已存入定时作业，点击“首页”右上角图标可查看'  # 定时作业 保存成功
    hw_success = '作业已经成功布置，学生现在可以查看并且作答！'  # 作业 保存成功

    no_report = '无需答题报告，答对即可'

