#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import json
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from conf.decorator import teststeps
from conf.base_config import GetVariable as gv
if gv.ENV == 'dev':  # ！！非Google浏览器
    tokens = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQ5NjI3LCJpc3MiOiJodHRwOi8vZGV2LmFwaXJlYnVpbGQubWFuYWdlLnZhbnRoaW5rLmNuL2FwaS9hdXRoL2xvZ2luIiwiaWF0IjoxNTgzMzk2MTQ2LCJleHAiOjE1ODQ2MDU3NDYsIm5iZiI6MTU4MzM5NjE0NiwianRpIjoia0JEWmJGY2VDTHBidk14ViJ9.8Eig1xj9crTPV7P33M6ZmOpyduP1Kubk1EtOgXnJWOM'
elif gv.ENV == '线上':
    tokens = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjk1MzE5LCJpc3MiOiJodHRwOi8vYXBpLm1hbmFnZS53eHp4emouY29tL2FwaS9hdXRoL2xvZ2luIiwiaWF0IjoxNTgzMzk2MzYzLCJleHAiOjE1ODQ2MDU5NjMsIm5iZiI6MTU4MzM5NjM2MywianRpIjoiS0pleHFmUWhBWmJSamh3biJ9.isyEW9FcAXFlU9Mtv7AzH1kLHo6ff0N2s-o9KCpV49I'
elif gv.ENV == 'test':
    tokens = ''


@teststeps
def get_verify(phone, var='editPhone', project_type='core'):
    """获取手机验证码
        action_type:register(用户注册) | resetPassword(忘记密码) | editPhone(修改手机) | quitClass(退出班级)
    """
    time.sleep(3)  # 管理端信息同步有时间延迟
    http = urllib3.PoolManager()

    urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
    header = {
        'Authorization': tokens,
        }
    var = "{}phone={}&project_type={}&action_type={}".format(gv.VERIFY_INF, phone, project_type, var)
    print(var)
    req = http.request('GET', var, headers=header)

    print(req._body.decode('utf-8'))
    value = json.loads(req._body.decode('utf-8'))['data']['captcha']
    return value


