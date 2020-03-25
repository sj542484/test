#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import sys
import os
import time
import subprocess
from functools import wraps
from PIL import ImageGrab
from selenium.common.exceptions import WebDriverException

from conf.report_path import ReportPath
from conf.log import Log

flag = 'IMAGE:'
log = Log()


def _screenshot(error_type):
    path = ReportPath().get_path() + 'image/'
    if not os.path.exists(path):
        os.makedirs(path)

    date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    img_name = error_type + "--" + date_time + '.png'
    var = path + img_name
    im = ImageGrab.grab()
    im.save(var)
    return img_name

def saveComputer(cmd):  #将截图保存到电脑
    screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = screenExecute.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    # 输出执行命令结果结果
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    print(stdout)
    print(stderr)


def teststep(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('\t--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            return ret
        except WebDriverException as e:
            log.e('WebDriverException, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'WebDriverException', 'Error')

            if flag in str(e):
                raise WebDriverException(e)
            else:
                raise WebDriverException(flag + _screenshot('Error--' + sys._getframe().f_code.co_name + func.__qualname__))
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + _screenshot('Fail--' + sys._getframe().f_code.co_name + func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + _screenshot('Error--' + sys._getframe().f_code.co_name + func.__qualname__))

    return wrapper


def teststeps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('  --> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.i('  <-- %s, %s', func.__qualname__, 'Success')
            return ret
        except WebDriverException as e:
            log.e('WebDriverException, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'WebDriverException', 'Error')

            if flag in str(e):
                raise WebDriverException(e)
            else:
                raise WebDriverException(flag + _screenshot('Error--' + sys._getframe().f_code.co_name + func.__qualname__))
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + _screenshot('Fail--' + sys._getframe().f_code.co_name + func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + _screenshot('Error--' + sys._getframe().f_code.co_name + func.__qualname__))

    return wrapper


def _wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.i('<-- %s, %s\n', func.__qualname__, 'Success')
            return ret
        except WebDriverException as e:
            log.e('WebDriverException, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'WebDriverException', 'Error')

            if flag in str(e):
                raise WebDriverException(e)
            else:
                raise WebDriverException(flag + _screenshot('Error--' + sys._getframe().f_code.co_name + func.__qualname__))
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + _screenshot('Fail--' + sys._getframe().f_code.co_name + func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + _screenshot('Error--' + sys._getframe().f_code.co_name + func.__qualname__))

    return wrapper


def testcase(func):
    return _wrapper(func)


def setup(func):
    return _wrapper(func)


def teardown(func):
    return _wrapper(func)


def setupclass(func):
    return _wrapper(func)


def teardownclass(func):
    return _wrapper(func)
