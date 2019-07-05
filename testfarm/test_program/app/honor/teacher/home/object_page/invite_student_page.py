#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.wait_element import WaitElement


class InviteStPage(BasePage):
    """ 邀请学生 详情页面"""
    wechat_friend_value = gv.PACKAGE_ID + "weixin"  # 微信好友

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self, var):
        """以“title: 班级名称/ 作业名称/本班卷子/口语作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststep
    def vanclass_name(self):
        """班级名"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "class_name").text
        print(item)
        return item

    @teststep
    def vanclass_num(self):
        """班号"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "class_num").text
        print(item)
        return item

    @teststep
    def hint_content(self):
        """提示 具体内容"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "invite_class_no").text
        print(item)
        return item

    @teststep
    def share_button(self):
        """分享按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "share") \
            .click()

    @teststep
    def copy_link_button(self):
        """复制链接 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "copy_link") \
            .click()

    @teststep
    def copy_no_button(self):
        """复制班号 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "copy_class_num") \
            .click()

    # 分享控件
    @teststeps
    def wait_check_share_page(self):
        """以“微信好友”为依据"""
        locator = (By.ID, self.wechat_friend_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def wechat_friend(self):
        """微信好友"""
        item = self.driver \
            .find_element_by_id(self.wechat_friend_value)
        return item

    @teststep
    def wechat_friends(self):
        """朋友圈 """
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "weixin_friends")
        return item

    @teststeps
    def wait_check_share_wechat_page(self, var=5):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'微信号/QQ/邮箱登录')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def wechat_back_button(self):
        """微信好友 返回"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView").click()

    @teststeps
    def wait_check_share_not_login_page(self, var=5):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'由于登录过期，请重新登录。无法分享到微信')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def back_up_button(self):
        """微信好友 返回"""
        self.driver \
            .find_element_by_class_name("android.widget.Button").click()
