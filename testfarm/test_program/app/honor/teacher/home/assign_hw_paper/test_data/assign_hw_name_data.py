#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
# 作业名称必填，字符限制在1~50，可以输入英文、字母、中文、符号；多于50自动截断
from app.honor.teacher.home.assign_hw_paper.test_data.hw_name_data import GetVariable as gv
from app.honor.teacher.home.assign_hw_paper.test_data.tips_data import TipsData

hw_data = (
    {'name': '{}_题筐为空'.format(gv.HW_TIME),
     'mode': '题筐为空',
     'assert': '{}'.format(TipsData().timing_success)},  # 题筐为空
    #
    # {'name': '{}_题筐为空'.format(gv.HW_TIME),
    #  'mode': '题筐为空',
    #  'assert': '{}'.format(TipsData().timing_success)},  # 作业名称重复/发布时间一致 todo 发布时间一致

    {'name': '{}_题筐不为空'.format(gv.HW_TIME),
     'mode': '题筐不为空',
     'assert': '{}'.format(TipsData().timing_success)},  # 题筐不为空

    {'name': '{}_题筐不为空'.format(gv.HW_TIME),
     'mode': '作业名称重复',
     'assert': '{}'.format(TipsData().timing_success)}  # 作业名称重复/发布时间不一致
)
