import os,json,subprocess
from conf.base_config import GetVariable as gv
from testfarm.models import EquipmentList, SideType, ItemType
from django.db import close_old_connections


class Utils:
    _con = {
        'capabilities':
            [
                {
                    "platformName": "Android",
                    "platformVersion": "8.0",
                    "deviceName": "honor2",
                    "app": "./test_program/app_folder/student_env_devDebug_1.3.4(2).apk",
                    # "appPackage": "com.vanthink.student0.debug",
                    "automationName": "uiautomator2",
                    # "appActivity": "com.tencent.mm.ui.LauncherUI",
                    "udid": "MKJNW18524003878",
                    "systemPort": 5500,
                    "resetKeyboard": True,
                    "unicodeKeyboard": True,
                    "noReset": True
                }
            ],
            'configuration':
                {
                    'url': 'http://127.0.0.1:%s/wd/hub/',
                    'host': '127.0.0.1',
                    'port': '',
                    'cleanUpCycle': 2000,
                    'timeout': 30000,
                    'proxy': 'org.openqa.grid.selenium.proxy.DefaultRemoteProxy',
                    'maxSession': 1,
                    'register': True,
                    'registerCycle': 5000,
                    'hubPort': 4444,
                    'hubHost': '',
                    'hubProtocol': 'http'
                }
    }

    def __init__(self, port):
        print('_ports', port)
        '''存放已用端口 防止启动多次'''
        self._port = port

    def is_using(self, port):
        """判断端口号是否被占用"""
        # Mac OS
        cmd = "lsof -i:%s" % port
        print(cmd)
        res = os.popen(cmd).readlines()
        if res:
            return res
        else:
            return False

    def get_ports(self,port, count):
        """获得4723端口后一系列free port"""
        port_list = []
        while True:
            if len(port_list) == count:
                break
            if not self.is_using(port) and (port not in port_list) and (port not in self._port):
                port_list.append(port)
            else:
                port += 2
        return port_list

    def appium_node_info(self, hubHost, port, device_name, udid, platversion, systemPort, side):
        self._con['configuration']['url'] = 'http://127.0.0.1:%s/wd/hub/' % port
        self._con['configuration']['port'] = '%s' % port
        self._con['configuration']['hubHost'] = hubHost
        self._con['capabilities'][0]['platformVersion'] = platversion
        self._con['capabilities'][0]['deviceName'] = device_name
        self._con['capabilities'][0]['udid'] = udid
        self._con['capabilities'][0]['systemPort'] = systemPort
        if side == 'student': # 学生
            self._con['capabilities'][0]['app'] = gv.STU_PACKAGE
        elif side == 'teacher_01':
            self._con['capabilities'][0]['app'] = gv.TEA_PACKAGE
        node_path = './test_program/nodeconfig/%s/%s/'%(device_name,platversion)
        if not os.path.exists(node_path):
            os.makedirs(node_path)
        print('app路径：',self._con['capabilities'][0]['app'])
        fp = open('%smobile.json' % (node_path),'w')
        fp.write(json.dumps(self._con))
        fp.close()

    def start_appium(self, mutex, dn, udid, plv, file_name, port, bp, systemPort, side):
        hubHost = gv.HUBHOST
        self.appium_node_info(hubHost=hubHost, port=port, device_name=dn, udid=udid, platversion=plv, systemPort=systemPort, side=side)

        CMD = 'appium -p {port} -bp {bp} -U {udid} --nodeconfig ./test_program/nodeconfig/{devicename}/{platformversion}/mobile.json > {portPath}appium_server.log'.format(port=port, bp=bp, udid=udid, devicename=dn, platformversion=plv, portPath=file_name)
        res = subprocess.Popen(CMD, shell=True)
        print('appium_pid:', res.pid)
        print(res.terminate())
        print('cmd:', CMD)
        # 将进程号存入数据库
        mutex.acquire()
        close_old_connections()
        EquipmentList.objects.filter(equipment_uuid=udid).update(node_pid=res.pid)
        mutex.release()
        return int(port), systemPort

    def clear_port(self,*port):
        for i in port:
            self._port.remove(i)
        return self._port


if __name__ == '__main__':
    a = Utils()
    res = a.is_using(port='4733')
    if res:
        print(res,len(res))
    else:
        print(res)
