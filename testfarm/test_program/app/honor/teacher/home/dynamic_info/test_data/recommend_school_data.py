#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())   # 生成当前时间
tips_data = (
    {'name': '推荐到学校作业' + str(now_time), 'assert': '成功推荐到学校'},  #
    {'name': '推荐到学校作业—重复推荐' + str(now_time), 'assert': '(C10000)不可重复推荐'},
    {'name': '推荐到学校作业' + str(now_time), 'assert': '(C9052)名称已存在,请重新编辑'}  # 重复推荐
)
