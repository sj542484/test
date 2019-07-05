# coding=utf-8
import time
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.test_data.nickname import nickname_data
from testfarm.test_program.conf.decorator import setup, teardown, testcase
from testfarm.test_program.utils.screen_shot import ScreenShot
from testfarm.test_program.utils.toast_find import Toast


class NickName(unittest.TestCase):
    """修改昵称"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.screen_shot = ScreenShot()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_nickname(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点

                self.user.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作
                if self.user_info.wait_check_page():  # 页面检查点
                    for i in range(len(nickname_data)):
                        if self.user_info.wait_check_page():  # 页面检查点
                            name1 = self.user_info.nickname()

                            self.user_info.click_nickname()  # 点击昵称条目，进入设置页面
                            if self.home.wait_check_tips_page():
                                if i == 0:
                                    self.home.tips_title()
                                    print('---------------')
                                nick = self.user_info.input()  # 找到要修改的文本 EditText元素
                                print('原昵称:', nick.text)
                                nick.send_keys(r'' + nickname_data[i]['nick'])  # 输入昵称
                                if i == 0:
                                    print('修改为：', nickname_data[0]['nick'])
                                else:
                                    print('修改为：', nick.text)

                                if i == len(nickname_data) - 2:
                                    print('----------不保存修改----------')
                                    self.user_info.click_negative_button()  # 取消按钮

                                    if self.user_info.wait_check_page():
                                        name2 = self.user_info.nickname()  # 昵称条目
                                        if name2 == name1:
                                            print('cancel change nickname success')
                                        else:
                                            print('cancel change nickname failed')
                                else:
                                    if self.user_info.positive_button() == 'true':
                                        self.user_info.click_positive_button()  # 确定按钮

                                        if len(nickname_data[i]) == 2:
                                            if Toast().find_toast(nickname_data[i]['assert']):
                                                print(nickname_data[i]['assert'])

                                            if self.user_info.wait_check_page():  # 页面检查点
                                                name2 = self.user_info.nickname()
                                                if name2 == name1:
                                                    print('昵称没有修改成功')
                                                else:
                                                    print('★★★ Error- 昵称被修改', nickname_data[i]['nick'], name2)
                                        else:
                                            if self.user_info.wait_check_page():  # 页面检查点
                                                time.sleep(2)
                                                name2 = self.user_info.nickname()
                                                if name2 != name1:
                                                    print('昵称修改成功')
                                                else:
                                                    print('★★★ Error- 昵称修改失败', nickname_data[i]['nick'], name2)
                                    else:
                                        self.user_info.click_negative_button()  # 取消按钮

                                        if self.user_info.wait_check_page():  # 页面检查点
                                            name2 = self.user_info.nickname()
                                            if name2 == name1:
                                                print('取消修改成功')
                                            else:
                                                print('★★★ Error- 取消修改失败', nickname_data[i]['nickname'], name2)
                                        else:
                                            print('未返回个人信息页面')

                        print('-----------------------------------')
                else:
                    print('未进入个人信息页面')
                self.user_info.back_up()  # 返回
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")
