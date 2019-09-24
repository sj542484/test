#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFE
from selenium.webdriver.common.by import By

from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_page import BasePage
from utils.click_bounds import ClickBounds
from utils.get_element_bounds import ElementBounds
from utils.wait_element import WaitElement


class VideoPage(BasePage):
    """视频"""
    video_button_value = gv.PACKAGE_ID + 'video'  # 拍摄按钮
    time_value = gv.PACKAGE_ID + 'time'  # 拍摄时长
    delete_button_value = gv.PACKAGE_ID + 'delete'  # 删除按钮

    permission_title_value = "com.android.packageinstaller:id/permission_message"  # 权限问询 title

    video_item_value = 'com.android.documentsui:id/mz_text_container'  # 视频条目

    def __init__(self):
        self.wait = WaitElement()
        self.tiny = CreateTinyCourse()

    # 权限询问页面
    @teststeps
    def wait_check_permission_page(self, var=3):
        """ 权限title的id为依据"""
        locator = (By.ID, self.permission_title_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def permission_title(self):
        """权限title"""
        ele = self.driver \
            .find_element_by_id(self.permission_title_value).text
        print(ele)

    @teststeps
    def allow_button(self):
        """允许 按钮"""
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'允许')]") \
            .click()

    @teststeps
    def permission_allow(self):
        """ 拍照权限"""
        if self.wait_check_permission_page():
            self.permission_title()  # 权限title
            self.allow_button()  # 允许 按钮
            print('-----------')

    # 拍摄
    @teststeps
    def wait_check_shoot_page(self):
        """拍摄视频 的为依据"""
        locator = (By.ID, self.video_button_value)
        return self.wait.wait_check_element(locator)

    # 第一页面
    @teststeps
    def shoot_button(self):
        """'拍摄'按钮"""
        print('点击拍摄按钮')
        self.driver \
            .find_element_by_id(self.video_button_value).click()

    @teststeps
    def rotate_button(self):
        """切换前后摄像头"""
        print('点击切换前后摄像头')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "rotate") \
            .click()

    @teststeps
    def shoot_button_location(self):
        """'拍摄 按钮坐标"""
        ele = self.driver\
            .find_element_by_id(self.video_button_value)
        return ElementBounds().get_element_location(ele)

    # 第二页面
    @teststeps
    def wait_check_suspend_page(self, var=10):
        """暂停拍摄按钮 为依据"""
        locator = (By.ID, self.time_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def suspend_button(self, loc):
        """'暂停'按钮  由于拿不到元素信息，因为暂停 和 开始 是同一个view，故用坐标点击"""
        print('点击暂停按钮')
        ClickBounds().click_bounds(loc[0], loc[1])

    # 第三页面
    @teststeps
    def wait_check_done_page(self, var=10):
        """时间 为依据"""
        locator = (By.ID, self.delete_button_value)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def retake_button(self):
        """'拍摄'按钮"""
        print('点击拍摄按钮')
        self.driver \
            .find_element_by_id(self.video_button_value).click()

    @teststeps
    def shoot_time(self):
        """拍摄时长"""
        ele = self.driver \
            .find_element_by_id(self.time_value).text
        return ele

    @teststeps
    def shoot_progress(self):
        """拍摄进度条"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "progress")
        return ele

    @teststeps
    def delete_button(self):
        """'删除'按钮"""
        print('点击删除按钮')
        self.driver \
            .find_element_by_id(self.delete_button_value) \
            .click()

    @teststeps
    def done_button(self):
        """完成按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "done") \
            .click()

    # 本地视频 有视频/无视频

    @teststeps
    def wait_check_local_page(self, var=10):
        """title:最近 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'最近')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def menu_button(self):
        """左上角"""
        self.driver \
            .find_element_by_id("com.android.documentsui:id/mz_toolbar_nav_button") \
            .click()

    @teststeps
    def wait_check_video_file_page(self, item, var=10):
        """title:下载 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % item)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def order_menu_button(self):
        """视频排序"""
        self.driver \
            .find_element_by_id("com.android.documentsui:id/menu_sort") \
            .click()

    @teststeps
    def wait_check_order_page(self, var=10):
        """条目元素 为依据"""
        locator = (By.ID, "com.android.documentsui:id/title")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def order_item_button(self):
        """排序方式"""
        self.driver \
            .find_elements_by_id("com.android.documentsui:id/title")[0] \
            .click()

    @teststeps
    def video_file_button(self):
        """"""
        self.driver \
            .find_element_by_id("com.android.documentsui:id/title")[1] \
            .click()


    @teststeps
    def album_button(self):
        """视频"""
        ele = self.driver.find_elements_by_id("android:id/text1")
        print(len(ele))
        return ele

    @teststeps
    def video_file_button(self):
        """视频"""
        print('点击 视频按钮')
        self.driver \
            .find_elements_by_id("android:id/title")[1] \
            .click()

    # 本地视频 有视频 进入视频列表
    @teststeps
    def wait_check_local_list_page(self, var=10):
        """视频条目列表 为依据"""
        locator = (By.ID, self.video_item_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def click_video_item(self, index):
        """点击 视频 条目"""
        self.driver \
            .find_elements_by_id(self.video_item_value)[index].click()

    @teststeps
    def video(self, name):
        """选择视频"""
        ele = self.driver \
            .find_elements_by_id("android:id/text1")

        content = []
        index = 0
        for i in range(len(ele)):
           if ele[i].text == name:
               content.append(ele[i])
               ele[i].click()
               index += 1
               break
        return content, index

    @teststeps
    def video_item(self):
        """视频信息"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.RelativeLayout/descendant::*")

        content = []
        item = []
        for i in range(len(ele)):
            if ele[i].text != '':
                content.append(ele[i].text)

        return content, item

    # 视频裁剪
    @teststeps
    def wait_check_cut_page(self, var=10):
        """title:视频裁剪 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'视频裁剪')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def finish_button(self):
        """完成按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "finish") \
            .click()

    @teststeps
    def control_button(self):
        """control按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "control") \
            .click()

    @teststeps
    def rule_hint(self):
        """裁剪视频规则"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "rule").text
        print(ele)

    # @teststeps
    # def play_video_operation(self):
    #     """视频播放 操作"""
    #     if self.tiny.wait_check_page():
    #         print('---------视频播放 操作--------')
    #         self.tiny.play_button()  # 播放 按钮
    #
    #         if self.tiny.wait_check_play_page():
    #             time.sleep(3)
    #             if self.tiny.wait_check_play_page():
    #                 time_str = self.tiny.exo_position()
    #                 var = self.tiny.exo_progress()  # 进度条
    #
    #                 if time_str != GetAttribute().description(var):
    #                     print('★★★ Error - 视频时长展示有误', time_str, var)
    #                 else:
    #                     print('--播放视频时长展示无误--')
    #
    #                 if self.tiny.wait_check_play_page():
    #                     location = Element().get_element_location(self.tiny.exo_progress())
    #
    #                     self.tiny.screen_switch_button()  # 横竖屏切换 按钮  竖屏切横屏
    #                     if self.tiny.wait_check_play_page():
    #
    #                         location1 = Element().get_element_location(self.tiny.exo_progress())
    #                         if location[0] <= location1[0] or location[1] >= location1[1]:
    #                             print('★★★ Error - 竖屏切横屏有误', location, location1)
    #                         else:
    #                             print('--横竖屏切换 按钮  竖屏切横屏--')
    #
    #                         self.tiny.screen_switch_button()  # 横竖屏切换 按钮 横屏切竖屏
    #                         if self.tiny.wait_check_play_page():
    #                             self.tiny.exo_play_button()  # 再次点击播放键
    #                             location2 = Element().get_element_location(self.tiny.exo_progress())
    #
    #                             if location1[0] >= location2[0] or location1[1] <= location2[1]:
    #                                 print('★★★ Error - 横屏切竖屏有误', location1, location2)
    #                             else:
    #                                 print('--横竖屏切换 按钮 横屏切竖屏--')
    #         else:
    #             print('!!!未进入视频播放页面')
    #
    #         if self.tiny.wait_check_play_page():
    #             self.tiny.back_up_button()  # 返回按钮
