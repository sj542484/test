import time
from functools import wraps
from selenium.common.exceptions import WebDriverException
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.report_path import ReportPath

def _screenshot(name):
    '''错误的页面截屏'''
    date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    screenshot = name + '-' + date_time + '.png'
    path = ReportPath().get_path() + '\\' + screenshot
    driver = BasePage().get_driver()
    driver.save_screenshot(path)
    return screenshot

def teststep(func: object) -> object:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except WebDriverException as e:
            raise WebDriverException(e)
        except AssertionError as e:
            raise AssertionError(e)
        except Exception as e:
            raise Exception(e)
    return wrapper


def teststeps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except WebDriverException as e:
            raise WebDriverException(e)
        except AssertionError as e:
            raise AssertionError(e)
        except Exception as e:
            raise Exception(e)
    return wrapper


def _wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except WebDriverException as e:
            raise WebDriverException(e)
        except AssertionError as e:
            raise AssertionError(e)
        except Exception as e:
            raise Exception(e)
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