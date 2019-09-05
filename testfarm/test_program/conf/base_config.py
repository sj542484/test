#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI

class GetVariable(object):
    """参数化"""
    # ==== DEV ====
    HOST = '172.17.0.200'
    USER_NAME = 'director'
    PASSWORD = 'r0#pX8^V'
    DB = "b_vanthink_core"

    # ==== Test =====
    # HOST = '172.17.0.16'
    # USER_NAME = 'tmp'
    # PASSWORD = 'mysql#0056'
    # DB = "b_vanthink_online"

    REPORT_ROOT = r'./testfarm/templates/test_report'  # 测试报告存放路径

    ID_TYPE = 'com.vanthink.student.debug:id/'
    PACKAGE_ID = 'com.vanthink.vanthinkteacher.debug:id/'

    # case统计 配置信息
    SUIT_PATH = 'testfarm'

    # case 目录
    CASE_PATH = 'testfarm/test_program/app/'
    CASE_PATTERN = 'test*.py'

    # 做题情况统计 Excel表格存放路径
    EXCEL_PATH = './storges/test_report/games_result_info.xlsx'

    # 教师web端
    TEA_URL = 'http://dev.vanthink.cn/accounts/#/login'

    # 安装包
    # 教师端
    TEA_PACKAGE = "./test_program/app_folder/teacher_env_devDebug_1.2.2(9).apk"
    # 学生端
    STU_PACKAGE = "./test_program/app_folder/student_env_devDebug_1.4.0-3(1).apk"

    # hub地址
    HUBHOST = '192.168.222.67'

    # 学生的ID
    STU_ID = 0
    # 需要测试的单词熟练度
    LEVEL = 1
    # 需改动的时间数
    TIME_COUNT = 0
    # 年级
    GRADE = '四年级'
    # 试卷的索引
    EXAM_INDEX = -1
