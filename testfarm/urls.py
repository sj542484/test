"""vanthink_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from . import views
urlpatterns = [
    # 操作首页
    path('', views.index, name='show'),
    # 登陆页面
    path('index',views.show_index,name='index'),
    # 执行登陆
    path('login',views.do_login,name='login'),
    # 注册页面
    path('register',views.register,name='register'),
    # 执行注册
    path('doregister',views.do_register,name='do_register'),
    # 退出登陆
    path('logout',views.do_logout,name='do_logout'),
    # 信息录入页
    path(r'inputinfo',views.inputInfo,name='inputinfo'),
    # 连接设备页
    path(r'devices',views.show_devices,name='showDevices'),
    # 保存数据
    path(r'saveinfo', views.saveInfo, name='saveinfo'),
    # 开始
    path(r'startservices/$',views.startservice,name='startserver'),
    # 停止
    path(r'stopservices/<path:gid>/<path:e_uuid>/',views.stopservice, name='stopserver'),
    # 展示报告
    path(r'showreport/<path:file_name>', views.showreport, name='showreport'),
    # 测试模块编辑
    path(r'testmodeledit',views.testmodeledit,name='testmodeledit'),
    # 展示所有添加的设备信息
    path(r'showalldevices',views.showalldevices,name='showalldevices'),
    # 删除设备信息
    path(r'deldata<path:e_uuid>',views.del_data,name='del_data'),
    # 展示要修改的设备信息
    path(r'updatedata<path:e_uuid>',views.update_show,name='update_show'),
    # 更新设备信息
    path(r'updatedata',views.update_data,name='update_data'),
    # 增加测试模块
    path(r'addtest',views.addtest,name='addtest'),
    # 教师端传数据
    path(r'tea',views.tea,name='tea'),
    path(r'exectea', views.tea_do_data, name='tea_do_data')
]
