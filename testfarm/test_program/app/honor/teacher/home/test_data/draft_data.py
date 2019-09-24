#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random


class GetVariable(object):
    """test_cases/assign_other_script 发布作业 - 作业名"""
    HW_TIME = '测试timing一年级三班2019年9月xx日 练习作业_定时' + str(random.randint(100, 999))  # test001
    HW_MODIFY = 'MODIFY' + str(random.randint(100, 999))  # test003

    HW_ASSIGN = 'hw assign' + str(random.randint(100, 999))  # test004
    SPOKEN_ASSIGN = 'spoken assign' + str(random.randint(100, 999))  # test005

    DRAFT_MODIFY = '测试draft' + str(random.randint(100, 999))  # test007

