# coding=utf-8
import re, os, hashlib
import subprocess
import time
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from testfarm.models import EquipmentList, SideType, ItemType
from testfarm.test_program.run import Driver
from testfarm.test_program.utils.st_appium_server import Utils
from django.contrib.auth.decorators import login_required
from testfarm.test_program.utils.kill_pid import killPid
from django.db import close_old_connections
from multiprocessing import Process
import threading

_port = []


def show_index(request):
    return render(request, 'testproject/login.html')


@login_required
def index(request):
    """首页"""
    return render(request, 'testproject/index.html')


def do_login(request):
    user = request.POST.get('username')
    pwd = request.POST.get('pwd')
    print(pwd, 'login', 'user:', user)
    pwd = encryption(pwd=pwd)
    print(pwd, 'login', 'user:', user)

    user = authenticate(username=user, password=pwd)
    print(user)
    # if user:
    '''登陆成功'''
    if user:
        login(request, user=user)
        return HttpResponse('<script>location.href="/"</script>')
    else:
        err_msg = '用户名或密码错误'
        return render(request, 'testproject/login.html', {'err_msg': err_msg})


def register(request):
    return render(request, 'testproject/register.html')


def do_register(request):
    user = request.POST.get('username')
    pwd = request.POST.get('pwd')
    pwd = encryption(pwd=pwd)
    print('zhuce:', pwd)
    try:
        # 使用django提供的认证系统
        close_old_connections()
        db = User.objects.create_user(username=user, password=pwd)
        db.save()
        print('数据保存成功')
        return HttpResponse('<script>alert("注册成功,请进行登陆");location.href="/"</script>')
    except Exception as e:
        print('数据存储异常')
        print(e)
        return HttpResponse('<script>alert("注册失败，请重新尝试")</script>')


@login_required
def do_logout(request):
    logout(request)
    return HttpResponse('<script>alert("退出登陆");location.href="/"</script>')


@login_required
def show_devices(request):
    """连接设备展示到页面中"""
    content = get_show_phone()
    print(content)
    return render(request, 'testproject/show_devices.html', content)


@login_required
def inputInfo(request):
    """获取设备信息并展示到页面进行设备信息录入"""
    dev_list_info = get_phone_online()
    pat = re.compile('(.*?) .*?model:(.*?) ')
    res = pat.findall(dev_list_info[0])
    if res:
        content = {'devices_model': res[0][1], 'devices_uuid': res[0][0]}
    else:
        content = {'devices_model': None}
    return render(request, '{}'.format('testproject/input_info.html'), content)


@login_required
def saveInfo(request):
    """保存数据"""
    devices_model = request.POST.get('devices_model')
    devices_uuid = request.POST.get('devices_uuid')
    devices_name = request.POST.get('devices_name')
    platformVersion = request.POST.get('platformVersion')
    try:
        db = EquipmentList(equipment_name=devices_name, equipment_model=devices_model, equipment_uuid=devices_uuid,
                           platform_verion=platformVersion)
        db.save()
        return HttpResponse('<script>alert("数据添加成功");location.href="/inputinfo"</script>')
    except Exception as e:
        print(e)
        return HttpResponse('<script>alert("设备已经存在 请更换设备录入");location.href="/inputinfo"</script>')


@login_required
def startservice(request):
    """开始测试"""
    e_uuid = request.POST.get('e_uuid')
    test_side = request.POST.get('parent')
    test_items = request.POST.get('child')
    print('设备uuid:', e_uuid, '测试端:', test_side, type(test_side), '测试项:', test_items)
    if test_side == '0' or test_items == '0':
        return HttpResponse('<script>alert("没有选择测试项/测试端，请先进行勾选！！！");location.href="/devices"</script>')
    # close_old_connections()
    # test_sides = SideType.objects.filter(id=int(test_side))[0].side_eng
    # print(test_sides)
    # test_item = ItemType.objects.filter(side=str(int(test_side)))[int(test_items) - 1].item_eng
    # print(test_item)
    # print('设备uuid:', e_uuid, '测试端:', test_sides, '测试项:', test_item)

    # p = Utils(port=_port)
    # appium_port = p.get_ports(port=4723, count=1)[0]
    # _port.append(appium_port)
    # sysport = p.get_ports(port=8200, count=1)[0]
    # _port.append(sysport)
    t = Process(target=st, args=(e_uuid, _port, test_side, test_items))
    t.start()
    time.sleep(0.3)
    content = get_show_phone()
    return render(request, 'testproject/show_devices.html', content)


# @login_required
def st(e_uuid, ports, test_side, test_items):
    # 获取进程 id
    gid = os.getpid()
    print('gid:', gid)
    # 变更该设备的 运行状态
    EquipmentList.objects.filter(equipment_uuid=e_uuid).update(start_but_statue=1, statue_statue=1, gid=gid)

    test_sides = SideType.objects.filter(id=int(test_side))[0].side_eng
    print(test_sides)
    test_item = ItemType.objects.filter(side=str(int(test_side)))[int(test_items) - 1].item_eng
    print(test_item)
    print('设备uuid:', e_uuid, '测试端:', test_sides, '测试项:', test_item)

    p = Utils(port=_port)
    appium_port = p.get_ports(port=4723, count=1)[0]
    _port.append(appium_port)
    sysport = p.get_ports(port=8200, count=1)[0]
    _port.append(sysport)

    # 根据设别uuid 获取设备的详情
    close_old_connections()
    device = EquipmentList.objects.get(equipment_uuid=e_uuid)
    e_name = device.equipment_name
    plat_verion = device.platform_verion

    # 实例化 driver类，开始进行测试
    dr = Driver(udid=e_uuid, platformVersion=plat_verion, deviceName=e_name, ports=ports, test_side=test_sides,
                test_items=test_item)
    file_name, sta = dr.run_cases(appium_port, sysport)  # 测试程序入口

    # 返回报告路径
    file_name = file_name.split('/templates/')[1]
    print('存储报告路径：', file_name)

    # 跟新设备运行状态
    close_old_connections()
    device = EquipmentList.objects.get(equipment_uuid=e_uuid)
    node_pid = device.node_pid
    EquipmentList.objects.filter(equipment_uuid=e_uuid).update(start_but_statue=0, statue_statue=0, gid=None,
                                                               report=file_name)
    # 清除端口占用
    pp = Utils(_port).clear_port(appium_port, sysport)
    print(_port, pp, '端口占用情况')

    # kill掉 node
    killPid().kill_pid(appium_port, node_pid)


@login_required
def stopservice(request, gid, e_uuid):
    """关闭进程 结束测试"""
    CMD = 'kill -9 {}'.format(gid)
    os.popen(CMD)
    print('kill进程:', CMD)
    close_old_connections()
    EquipmentList.objects.filter(equipment_uuid=e_uuid).update(start_but_statue=0, statue_statue=0, gid=None,
                                                               report=None)
    content = get_show_phone()
    return render(request, 'testproject/show_devices.html', content)


def get_phone_online():
    """获取连接的设备信息"""
    res = subprocess.Popen('adb devices -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    result, err = res.communicate()
    result = result.decode().replace('List of devices attached\n', '').replace('\n\n', '')
    dev_list_info = result.split('\n')
    return dev_list_info


def get_show_phone():
    """获取设备列表页展示的设备/信息"""
    dev_list_info = get_phone_online()
    dev_list = []
    if dev_list_info[0]:
        for i in dev_list_info:
            pat = re.compile('(.*?) .*?model:(.*?) ')
            res = pat.findall(i)
            res = EquipmentList.objects.filter(equipment_uuid=res[0][0])
            if res:
                dev_list.append(res[0])
        if dev_list:
            content = {'devices': dev_list, 'len': len(dev_list)}
        else:
            content = {'devices': 0}
    else:
        content = {'devices': 1}
    return content


@login_required
def showreport(request, file_name):
    print(file_name, '=============\n\n')
    return render(request, file_name)


@login_required
def testmodeledit(request):
    try:
        db = SideType.objects.all()
        print([i.id for i in db])
        content = {'sides': db}
        print('success')
    except Exception as e:
        print(e)
        print('=======数据库异常-------')
    return render(request, 'testproject/test_model.html', content)


@login_required
def showalldevices(request):
    # 分页
    devices = EquipmentList.objects.all()
    paginator = Paginator(devices, 5)
    content = {'content': devices}
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    content['contacts'] = contacts

    return render(request, 'testproject/show_all_devices.html', content)


@login_required
def update_show(request, e_uuid):
    content = {}
    res = EquipmentList.objects.filter(equipment_uuid=e_uuid)
    content['content'] = res
    return render(request, 'testproject/update_data.html', content)


@login_required
def update_data(request):
    e_uuid = request.POST.get('devices_uuid')
    plv = request.POST.get('platformVersion')
    device_name = request.POST.get('devices_name')
    devices_model = request.POST.get('devices_model')
    EquipmentList.objects.filter(equipment_uuid=e_uuid).update(platform_verion=plv, equipment_name=device_name,
                                                               equipment_model=devices_model)
    return HttpResponse('<script>alert("更新成功！！！");location.href="/showalldevices"</script>')


@login_required
def del_data(request, e_uuid):
    EquipmentList.objects.filter(equipment_uuid=e_uuid).delete()
    return HttpResponse('<script>alert("删除成功！！！");location.href="/showalldevices"</script>')


def encryption(pwd):
    # 1.创建一个hash对象
    h = hashlib.sha256()
    # 2.填充要加密的数据
    h.update(bytes(pwd, encoding='utf-8'))
    # 3.获取加密结果
    pawd_result = h.hexdigest()
    return pawd_result


def addtest(request):
    SideType(side='学生端')
    # test_side = request.POST.get('pro')
    # test_model = request.POST.get('')


def tea(request):
    return render(request, 'testproject/tea_data.html')


def tea_do_data(request):
    start_dir = request.POST.get('folder_path')
    start_num = request.POST.get('number')
    start_tea_account = request.POST.get('tea_account')
    print(start_dir)
    print(start_num)
    print(start_tea_account)

    return HttpResponse('<script>alert("开始上传！！！");location.href="/"</script>')
