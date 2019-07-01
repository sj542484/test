#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI

import os
class GetVariable(object):
    """参数化"""
    HOST = '172.17.0.200'
    USER_NAME = 'director'
    PASSWORD = 'AZ*vkTJj'
    DB = "b_vanthink_core"

    REPORT_ROOT = r'./testfarm/templates/test_report'  # 测试报告存放路径

    ID_TYPE = 'com.vanthink.student.debug:id/'

    # case统计 配置信息
    SUIT_PATH = 'testfarm'
    print(os.getcwd(),'==============')
    # CASE_PATH = 'app/student/homework/test_001_all_game'
    # CASE_PATH = 'app/student/homework/test_002_paper/test_case'
    # CASE_PATH = 'app/student/homework/test_class_cases'
    # CASE_PATH = 'app/student/user_center/test_cases'
    # CASE_PATH = 'app/student/login/test_cases'
    # CASE_PATH = 'testfarm/test_program/app/honor/weixin/test_cases/test_000_account'

    CASE_PATH = 'testfarm/test_program/app/'
    CASE_PATTERN = 'test*.py'

    # 以下为 appiumserver.py 配置信息
    CMD = "appium -a 127.0.0.1 -p %s -bp 4728 --no-reset"
    SERVER_URL = 'http://127.0.0.1:%s/wd/hub/status'
    SERVER_LOG = 'appium_server_port_%s.log'
    KILL = 'taskkill /PID %d /F'

    # 做题情况统计 Excel表格存放路径
    EXCEL_PATH = './storges/test_report/games_result_info.xlsx'

    # 教师web端
    TEA_URL = 'http://dev.vanthink.cn/accounts/#/login'