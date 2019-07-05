from selenium.webdriver.remote.webdriver import WebDriver as Remotewebdriver
import time
from appium import webdriver
from testfarm.test_program.conf.run_cases import RunCases
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.case_strategy import CaseStrategy
from testfarm.test_program.utils.st_appium_server import Utils
from testfarm.test_program.app.honor.student.library.object_pages.data_action import DataAction

class Driver:

    def __init__(self,udid,platformVersion,deviceName,ports,test_side,test_items):
        self.udid = udid
        self.platformVersion = platformVersion
        self.deviceName = deviceName
        self.ports = ports
        self.test_side = test_side
        print(self.test_side,'-=-=-=-=-=-=')
        self.test_items = test_items

    def remote_info(self,systemport=8200):
        desired_caps = {
             "platformName": "Android",
             "platformVersion": self.platformVersion,
             "deviceName": self.deviceName,
             "app": "/Users/vanthink_test_ios/Woker/student_env_devDebug_1.3.4(2).apk",
             "automationName": "uiautomator2",
             "udid": self.udid,
             "resetKeyboard": True,
             "noReset": True,
             "systemPort": systemport
        }
        if self.test_side == 'student':
            desired_caps['app'] = "/Users/vanthink_test_ios/Woker/student_env_devDebug_1.3.4(2).apk"
        elif self.test_side == 'teacher':
            desired_caps['app'] = "/Users/vanthink_test_ios/Woker/teacher_env_devDebug_1.2.2.apk"
        print('desired:',desired_caps)
        return desired_caps

    def run_cases(self,appium_port,sysport):
        # 收集用例 根据测试端 和 测试项
        cs = CaseStrategy(self.test_side,self.test_items)
        cases = cs.collect_cases(suite=False)
        # 返回 存放报告的文件夹路径
        run_case = RunCases(self.remote_info(),self.test_side)
        file_name = run_case.file_name
        file_path = run_case.get_path()
        # 开启appium服务
        Utils(port=self.ports).start_appium(dn = self.deviceName, udid=self.udid, plv=self.platformVersion, file_name=file_path,port=appium_port,bp=int(appium_port)+1000,systemPort=sysport,side=self.test_side)
        # hub地址
        addr = 'http://192.168.8.124:4444/wd/hub'
        # 取保端口已经启动apiumm服务
        while True:
            res = Utils(port=self.ports).is_using(appium_port)
            if res:
                if 'node' in str(res):
                    print('节点启动成功')
                    time.sleep(5)
                    driver = webdriver.Remote(addr,self.remote_info(sysport))
                    break
            time.sleep(0.3)
        # 连接数据库
        mysql = DataAction()
        mysql.start_db()    # 启动数据库
        # 设置driver
        base_page = BasePage()
        base_page.set_driver(driver)
        base_page.set_db(mysql)
        base_page.set_user(username=self.deviceName)
        try:
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