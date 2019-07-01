#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import HTMLTestRunner
import re
import time
import os
from testfarm.test_program.conf.base_config import GetVariable as gv


class RunCases:
    def __init__(self, device_info,test_side):

        self.device = device_info
        if not os.path.exists(gv.REPORT_ROOT):
            os.makedirs(gv.REPORT_ROOT)
        date_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        # 过滤掉deviceName中的':'（因为文件夹名称不能包含':'）
        device_name = re.sub('[:]', '-', '%s' % self.device['deviceName']).replace(' ','')
        plv = self.device['platformVersion'].replace('.','_') if '.' in self.device['platformVersion'] else self.device['platformVersion'] + '_0'
        self.test_report_path = gv.REPORT_ROOT + '/' + test_side + '/' + device_name + '/' + plv + '/' + date_time + '/'
        if not os.path.exists(self.test_report_path):
            os.makedirs(self.test_report_path)
        self.file_name = self.test_report_path + 'TestReport_' + date_time + '.html'  # 这个filename是生成的自动化测试报告的文件名

    def get_path(self):
        return self.test_report_path

    def get_device(self):
        return self.device

    def run(self, cases):
        desc = '用例执行情况统计：'
        report_title = '测试用例执行报告'
        fp = open(self.file_name, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title=report_title,
                description=desc)
        runner.run(cases)
        fp.close()
