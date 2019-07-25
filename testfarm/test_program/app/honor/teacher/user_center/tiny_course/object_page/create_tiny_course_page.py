#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.test_bank.object_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.user_center import CollectionPage
from app.honor.teacher.user_center import MineTestBankPage
from app.honor.teacher.user_center import name_data
from app.honor.teacher.user_center import TuserCenterPage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.connect_db import ConnectDB
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class CreateTinyCourse(BasePage):
    """创建微课页面"""
    course_value = gv.PACKAGE_ID + 'name'  # 微课名称
    video_value = gv.PACKAGE_ID + 'video'  # 添加视频后，微课主页面 视频 按钮

    menu_value = gv.PACKAGE_ID + "md_title"  # 菜单条目

    def __init__(self):
        self.wait = WaitElement()
        self.user = TuserCenterPage()
        self.mine = MineTestBankPage()
        self.question = TestBankPage()
        self.filter = FilterPage()
        self.collect = CollectionPage()

    @teststeps
    def wait_check_page(self):
        """以“title:创建微课”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'创建微课')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“微课名称”的id为依据"""
        locator = (By.ID, self.course_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def course_name(self):
        """以“微课名称”的id为依据"""
        ele = self.driver \
            .find_element_by_id(self.course_value)
        return ele

    @teststep
    def create_tiny_course(self):
        """以“+ 微课内容”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'create_tiny_course') \
            .click()

    @teststep
    def delete_tiny_course_button(self):
        """以“删除按钮”的id为依据"""
        print('点击删除按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'delete') \
            .click()

    @teststeps
    def hint(self):
        """说明:一道微课题目中包含一个视频"""
        ele = self.driver \
            .find_element_by_xpath('说明:一道微课题目中包含一个视频').text
        return ele

    @teststep
    def save_button(self):
        """以“保存 按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "save")\
            .click()

    # 创建页面
    @teststeps
    def wait_check_menu_page(self):
        """以“md_title”的id为依据"""
        locator = (By.ID, self.menu_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def menu_item(self):
        """以“拍摄视频/本地视频”的id为依据"""
        ele = self.driver\
            .find_elements_by_id(self.menu_value)
        return ele

    @teststeps
    def judge_video_exist(self):
        """以“删除按钮删除后页面”的id为依据"""
        locator = (By.ID, self.video_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def play_video(self):
        """以“视频”的id为依据"""
        print('点击视频')
        self.driver \
            .find_element_by_id(self.video_value).click()

    # 上传中....
    @teststeps
    def wait_check_upload_page(self, var=10):
        """以“上传中  进度条”的id为依据"""
        locator = (By.ID, "android:id/progress")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def upload_rate(self):
        """上传百分率"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'md_label').text
        return ele

    @teststeps
    def upload_num(self):
        """上传数量"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'md_minMax').text
        return ele

    @teststeps
    def edit_course_name(self, name=None):
        """编辑课程名称 操作"""
        print('---编辑课程名称---')
        if name is None:
            var = 0
            length = len(name_data)
            name = name_data[var]['name']
        else:
            length = 1

        item = 0  # 微课名称
        for i in range(length):
            if self.wait_check_list_page():
                var = self.course_name()  # 微课名称
                var.send_keys(name)
                item = var.text
                print('输入微课名称：', item)
                self.save_button()  # 点击保存按钮

                if self.wait_check_upload_page(3):  # 上传中....
                    self.judge_upload_operation()  # 判断视频 是否 正在上传中
                    ThomePage().tips_content_commit()  # 提示 页面信息

                if not Toast().find_toast('加入成功'):
                    print('★★★ Error - 未弹toast：加入成功')
                    break
                else:
                    continue
        print('-----------------')
        return item

    @teststeps
    def judge_upload_operation(self, var=5):
        """判断视频 是否 正在上传中"""
        if self.wait_check_upload_page(var):  # 上传中....
            # self.upload_rate()  # 上传百分率
            # self.upload_num()  # 上传数量

            while True:
                locator = (By.ID, "android:id/progress")
                if self.wait.judge_is_exists(locator):  # 上传中....
                    time.sleep(1)
                else:
                    break

    @teststeps
    def judge_save_result(self, video):
        """
        验证视频保存结果
        :param video: 视频名称
        """
        if self.user.wait_check_page():
            nick = self.user.nickname()  # 昵称

            print('--------------验证微课作业保存结果-------------')
            self.user.click_mine_bank()  # 我的题库
            if self.mine.wait_check_page():
                self.user.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                    self.user.click_game_list()  # 点击 大题
                    self.filter.commit_button()  # 点击 确定按钮

                if self.mine.wait_check_page():  # 页面检查点
                    if self.mine.wait_check_list_page():
                        name = self.question.question_name()  # 名称
                        type = self.question.question_type(0)  # 类型
                        author = self.question.question_author()  # 创建人
                        print(name[1][0], type, author[0].text)

                        if type != '微课':
                            print('★★★ Error - 视频保存失败，我的题库题型有误', type)
                        else:
                            if name[1][0] != video:
                                print('★★★ Error - 视频保存失败，我的题库视频名称有误', name[1][0], video)
                            else:
                                if author[0].text != nick:
                                    print('★★★ Error - 视频保存失败，我的题库视频作者有误', author[0].text, nick)
                                else:
                                    print('视频拍摄保存成功')

                        # self.recovery_data(video)  # 恢复测试数据

            ThomePage().back_up_button()  # 返回个人中心页面

    @teststeps
    def recovery_data(self, name, number=None):
        """ 恢复测试数据
        :param number: limit 取值数量
        :param name:   视频名称
        :param created_date:  创建日期
        """
        print('------恢复测试数据-----')
        if number is None:
            number = 1000

        if name.find('&') != -1:
            name = name.replace('&', '&amp;')

        sql = "DELETE FROM `testbank` WHERE (`account_id` = '51869' AND `name`='{}') LIMIT {}" \
            .format(name, number)
        print(sql)
        ConnectDB().operate_mysql(sql)
