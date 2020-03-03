#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI


class TipsData(object):
    """提示信息 参数化数据"""
    # 布置作业
    timing_hw = '1. 无定时，作业将立即布置。\n' \
                '2. 有定时，作业将存入“首页” - “定时作业”中，会在您设定的时间自动布置。\n' \
                '3. 可以选择多个时间重复布置作业，最多可选择7个时间。\n' \
                '4. 定时作业发布时，如果当天已有同名作业，作业名称后会自动加数字以示区别。'

    timing_success = '作业已存入定时作业，点击“首页”右上角图标可查看'  # 定时作业 保存成功
    hw_only_daily = '作业名称不能与当天布置的其他作业相同'  # 每天不重复
    # can_not_spoken = '达标模式不能包含口语题'  # 达标模式不能包含口语题

    # 请输入作业名称
    no_hw_name = '请输入作业名称'
    # 请选择学生
    no_choose_st = '请选择学生'

    no_student = '布置学生不能为空'

    assign_success = '布置成功'
