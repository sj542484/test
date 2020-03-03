#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import pexpect, sys, subprocess
from uiautomator import Device
from time import sleep
import threading


def install_apk(device, path_to_apk):
    print('Installing apk: {0} to device: {1}'.format(path_to_apk, device))
    P = subprocess.Popen("adb -s {0} install {1}".format(device, path_to_apk), stdout=subprocess.PIPE, shell=True)
    data = P.stdout.read()
    if "Success" in str(data):
        print('Installing apk: {0} for device: {1} Success'.format(path_to_apk, device))
        exit(1)
    if "Failure" in str(data):
        print('Installing apk: {0} for device: {1} Failure'.format(path_to_apk, device))
        exit(0)


def uninstall_apk(device, package):
    print('Uninstalling apk: {0} for device: {1}'.format(package, device))

    result = str(pexpect.run('adb -s {0} uninstall {1}'.format(device, package))).strip().lower()

    if 'failure' == result:
        print('WARN: Uninstall apk: {0} for device: {1} has error, maybe not exists.'.format(package, device))
        exit(0)

    if 'success' != result:
        print('Uninstall apk: {0} for device: {1} failed, msg: {2}'.format(package, device, result))
        exit(1)


def protect(nub, device):
    sleep(2)
    for i in range(nub):
        d = Device(device)
        el1 = d(text="安装")
        el2 = d(text="确定")
        if el1.exists:
            el1.click()
        if el2.exists:
            el2.click()
        sleep(2)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Arguments error, usage: python install_app <install | uninstall> <device> <apk | package>')
        exit(1)

    op = sys.argv[1]
    device = sys.argv[2]
    apk = sys.argv[3]

    if op == 'install':
        threads = []
        install = threading.Thread(target=install_apk, args=(device, apk))
        protect = threading.Thread(target=protect, args=(30, device))
        threads.append(install)
        threads.append(protect)
        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()
    else:
        package = sys.argv[3]
        uninstall_apk(device, package)
