from selenium.webdriver.remote.webdriver import WebDriver as Remotewebdriver
import time

import subprocess
from appium import webdriver
from conf.run_cases import RunCases

from conf.base_page import BasePage

from conf.case_strategy import CaseStrategy
from utils.st_appium_server import Utils
from utils.sql import SqlDb
from conf.base_config import GetVariable as gv
from conf.log import Log
from conf.report_path import ReportPath


class Driver:

    def __init__(self, udid, platformVersion, deviceName, ports, test_side, test_items):
        print(udid, platformVersion, deviceName,ports, test_side, test_items, '===============-=')
        self.udid = udid
        self.platformVersion = platformVersion
        self.deviceName = deviceName
        self.ports = ports
        self.test_side = test_side
        self.test_items = test_items

    def remote_info(self, systemport=8200):
        desired_caps = {
             "platformName": "Android",
             "platformVersion": self.platformVersion,
             "deviceName": self.deviceName,
             "app": "",
             "automationName": "uiautomator2",
             "udid": self.udid,
             "resetKeyboard": True,
             # "unicodeKeyboard":True,
             "noReset": True,
             "systemPort": systemport
        }
        if self.test_side == 'student':
            desired_caps['app'] = gv.STU_PACKAGE
        elif self.test_side == 'teacher':
            desired_caps['app'] = gv.TEA_PACKAGE
        print('desired:', desired_caps)
        return desired_caps

    def run_cases(self, appium_port, sysport, mutex):
        # 收集用例 根据测试端 和 测试项
        cs = CaseStrategy(self.test_side,self.test_items)
        cases = cs.collect_cases(suite=False)
        # 返回 存放报告的文件夹路径
        run_case = RunCases(self.remote_info(), self.test_side)
        file_name = run_case.file_name
        file_path = run_case.get_path()
        # 设置报告路径
        path = ReportPath()
        path.set_path(file_path)
        # 开启appium服务
        Utils(port=self.ports).start_appium(mutex, dn=self.deviceName, udid=self.udid, plv=self.platformVersion, file_name=file_path, port=appium_port, bp=int(appium_port)+1000, systemPort=sysport, side=self.test_side)
        # hub地址
        addr = 'http://%s:4444/wd/hub' % gv.HUBHOST

        # 清楚应用缓存
        cmd = 'adb -s {} shell pm clear com.vanthink.student.debug'.format(self.udid)
        res = subprocess.Popen(cmd, shell=True)
        # 取保端口已经启动apiumm服务
        while True:
            print('opopopp', appium_port)
            res = Utils(port=self.ports).is_using(appium_port)
            if res:
                if 'node' in str(res):
                    print('节点启动成功')
                    time.sleep(5)
                    driver = webdriver.Remote(addr, self.remote_info(sysport))
                    break
            time.sleep(0.3)

        # 实例化log
        log = Log()
        log.set_logger(self.deviceName, file_path + '/' + 'client.log')

        # 实例化base类
        base_page = BasePage()
        # 连接数据库
        mysql = SqlDb()
        mysql.start_db()    # 启动数据库
        # 设置driver
        base_page.set_driver(driver)
        base_page.set_db(mysql)
        base_page.set_user(deviceName=self.deviceName)
        base_page.set_path(path=file_path)
        base_page.set_window_size(uuid=self.udid)
        try:
            time.sleep(5)
            print('start cases')
            run_case.run(cases)
            print('end')
            sta = 0
        except Exception as e:
            print('异常：',e)
            sta = 2

        driver.quit()
        # kill掉node服务
        # Utils(port=self.ports).clear_port(appium_port,sysport)
        # killPid().kill_pid(appium_port)
        return file_name,sta
