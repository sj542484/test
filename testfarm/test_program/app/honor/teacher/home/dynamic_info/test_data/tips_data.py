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
    hw_success = '作业已经成功布置，学生现在可以查看并且作答！'  # 作业 保存成功
    hw_only_daily = '作业名称不能与当天布置的其他作业相同'  # 每天不重复
    # can_not_spoken = '达标模式不能包含口语题'  # 达标模式不能包含口语题

    # 完成情况及答题分析
    no_report = '无需答题报告，答对即可'

    # 删除习题/口语
    delete_success = '操作成功'

    add_basket_success = '成功加入题筐'

