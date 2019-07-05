# coding=utf-8
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.user_center.setting_center.object_page.setting_page import SettingPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.test_data.modify_school import school_data
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.screen_shot import ScreenShot
from testfarm.test_program.utils.toast_find import Toast


class School(unittest.TestCase):
    """修改我的学校"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.user = TuserCenterPage()
        cls.user_info = UserInfoPage()
        cls.screen_shot = ScreenShot()
        cls.set = SettingPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_modify_school(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if self.user.wait_check_page():  # 页面检查点
                self.user.click_avatar_profile()  # 点击登录头像按钮，进入个人信息页面

                if self.user_info.wait_check_page():  # 页面检查点
                    self.user_info.click_school()  # 点击学校条目，进入设置页面

                    school = self.school_teacher()  # 在校老师
                    self.free_teacher(school)  # 自由老师

                    self.restore_test_data()
                else:
                    print('未进入个人信息页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def school_teacher(self):
        """在校老师"""
        if Toast().find_toast('没有权限修改学校信息'):
            print('=========================在校老师==========================\n',
                  '  没有权限修改学校信息')
            self.home.back_up_button()  # 返回 个人中心 页面
            if self.user.wait_check_page():  # 页面检查点
                self.set.logout_operation()  # 退出登录 操作

                if self.login.wait_check_page():  # 页面检查点
                    phone = self.login.input_username()
                    pwd = self.login.input_password()

                    phone.click()  # 激活phone输入框
                    phone.send_keys('18711111134')  # 输入手机号

                    pwd.click()  # 激活pwd输入框
                    pwd.send_keys('456789')  # 输入密码

                    self.login.login_button()  # 登录按钮
                    if self.home.wait_check_page():
                        self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮
                        if self.user.wait_check_page():  # 页面检查点
                            self.user.click_avatar_profile()  # 点击登录头像按钮，进入个人信息页面

                            if self.user_info.wait_check_page():  # 页面检查点
                                school = self.user_info.school().text  # 目前学校信息
                                self.user_info.click_school()  # 点击学校条目，进入设置页面

                                return school

    @teststeps
    def free_teacher(self, school):
        """自由老师"""
        print('=========================自由老师==========================')
        for i in range(len(school_data)):
            if self.home.wait_check_tips_page():  # 页面检查点
                print('-------------------------------------')
                name = self.user_info.input()  # 找到要修改的EditText元素
                name.send_keys(r'' + school_data[i]['sch'])  # 输入
                if i == 0:
                    print('修改为:', school_data[i]['sch'])
                else:
                    print('修改为:', name.text)
                self.home.character_num()  # 字符数
                self.user_info.click_positive_button()  # 确定 按钮

                if self.user_info.wait_check_page():  # 页面检查点
                    school2 = self.user_info.school().text  # 修改手机号
                    self.user_info.click_school()  # 点击学校条目，进入设置页面

                    if school2 == school:
                        print('我的学校修改成功')
                    else:
                        print('★★★ Error - 我的学校修改失败')
                elif self.home.wait_check_tips_page():
                    self.user_info.click_negative_button()  # 取消 按钮 返回个人信息页面

    @teststeps
    def restore_test_data(self):
        """恢复测试数据"""
        if self.user_info.wait_check_page():  # 页面检查点
            self.home.back_up_button()  # 返回 个人中心 页面
            if self.user.wait_check_page():  # 页面检查点
                self.set.logout_operation()  # 退出登录 操作
                if self.login.wait_check_page():  # 页面检查点
                    phone = self.login.input_username()
                    pwd = self.login.input_password()

                    phone.click()  # 激活phone输入框
                    phone.send_keys('18711111234')  # 输入手机号

                    pwd.click()  # 激活pwd输入框
                    pwd.send_keys('456789')  # 输入密码

                    self.login.login_button()  # 登录按钮
                    if not self.home.wait_check_page():  # 页面检查点
                        print('★★★ Error- 18711111234 登录失败')
