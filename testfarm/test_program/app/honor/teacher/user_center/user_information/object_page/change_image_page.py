#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.user_center.user_information.test_data.image import VALID_IMAGE
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.click_bounds import ClickBounds
from utils.wait_element import WaitElement

# 小米 6x 8.1  Mi6x
shutter_button_id = 'com.android.camera:id/v9_shutter_button_internal'  # 拍照键
switch_button_id = 'com.android.camera:id/v9_camera_picker'  # 切换前置后置摄像头
retake_button_id = 'com.android.camera:id/intent_done_retry'  # 重拍 按钮
done_button_id = 'com.android.camera:id/inten_done_apply'  # 完成 按钮


class MeizuPage(BasePage):
    """魅族5.1"""
    def __init__(self):
        self.wait = WaitElement()

    # 拍照 魅族5.1
    @teststeps
    def wait_check_camera_page(self, var=10):
        """以 “拍照键”的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.camera:id/shutter_btn")
        return self.wait.wait_check_element(locator, var)

    # 第一页面
    @teststeps
    def click_camera_button(self):
        """以相机拍照按钮"""
        time.sleep(2)
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/shutter_btn") \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.camera:id/btn_retake")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 保存按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/btn_done") \
            .click()

    @teststeps
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/btn_retake") \
            .click()

    # 第三页面
    @teststeps
    def wait_check_save_page(self):
        """取消 按钮 的为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '取消')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def click_save_button(self):
        """相机保存按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'完成')]") \
            .click()

    @teststeps
    def click_cancel_button(self):
        """相机取消按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消')]") \
            .click()

    # 相册 魅族5.1
    @teststeps
    def wait_check_album_page(self):
        """最新tab 的单个内容 的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.gallery:id/thumbnail")
        return self.wait.wait_check_element(locator)

    # 第一页面
    @teststeps
    def click_album(self):
        """进入相册tab"""
        print('进入相册列表页')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'相册')]") \
            .click()

    @teststeps
    def wait_check_all_picture_page(self):
        """所有图片 的为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '所有图片')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def open_album(self):
        """打开 第一个相册"""
        print('选择相册')
        self.driver \
            .find_elements_by_id("com.meizu.media.gallery:id/album_name")[0] \
            .click()

    # 第二页面  检查点用 wait_check_album_list_page()
    @teststeps
    def choose_image(self):
        """选择相册图片"""
        print('选择照片')
        ClickBounds().click_bounds(float(VALID_IMAGE.location_x()), float(VALID_IMAGE.location_y()))

    # 第三页面
    @teststeps
    def wait_check_photo_page(self):
        """ 确定 按钮 的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.gallery:id/action_get_multi_confirm")
        return self.wait.wait_check_element(locator)

    @teststeps
    def commit_button(self):
        """相册确定按钮"""
        print('点击 确定按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'确定')]") \
            .click()

    @teststep
    def back_up_button(self):
        """相册返回按钮"""
        self.driver \
            .find_element_by_id("android:id/home") \
            .click()


class HonorPage(BasePage):
    """华为7.0"""
    def __init__(self):
        self.wait = WaitElement()

    # 拍照 华为7.0
    @teststeps
    def wait_check_camera_page(self, var=10):
        """以 “拍照键”的resource-id为依据"""
        locator = (By.ID, "com.huawei.camera:id/shutter_button")
        return self.wait.wait_check_element(locator, var)

    # 第一页面
    @teststeps
    def click_camera_button(self):
        """以相机拍照按钮"""
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.huawei.camera:id/shutter_button") \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.huawei.camera:id/btn_cancel")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id("com.huawei.camera:id/btn_done") \
            .click()

    @teststeps
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.huawei.camera:id/btn_cancel") \
            .click()

    # 相册 华为7.0
    @teststeps
    def wait_check_album_page(self, var=10):
        """相册 的resource-id为依据"""
        locator = (By.ID, "com.android.gallery3d:id/album_name")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def open_album(self):
        """打开 第二个相册"""
        print('进入相册')
        self.driver \
            .find_elements_by_id("com.android.gallery3d:id/album_name")[1] \
            .click()

    @teststeps
    def wait_check_picture_page(self, var=10):
        """选择图片 的为依据"""
        locator = (By.ID, "com.android.gallery3d:id/head_actionmode_title")
        return self.wait.wait_check_element(locator, var)


class PixelPage(BasePage):
    """Pixel 8.1"""
    def __init__(self):
        self.wait = WaitElement()

    # 拍照
    @teststeps
    def wait_check_camera_page(self, var=10):
        """选择图片 的为依据"""
        locator = (By.ID, "com.google.android.GoogleCamera:id/camera_switch_button")
        return self.wait.wait_check_element(locator, var)

    # 第一页面
    @teststeps
    def click_retake_button(self):
        """相机'切换前置后置摄像头'按钮"""
        print('切换前后摄像头')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/camera_switch_button") \
            .click()

    @teststeps
    def click_camera_button(self):
        """以相机拍照按钮"""
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/center_placeholder") \
            .click()

    @teststeps
    def cancel_button(self):
        """以相机  左上角 取消按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_elements_by_class_name("android.view.View")[1] \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.google.android.GoogleCamera:id/retake_button")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/shutter_button") \
            .click()

    @teststeps
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/retake_button") \
            .click()

    # 相册
    @teststeps
    def wait_check_album_page(self, var=10):
        """相册 的resource-id为依据"""
        locator = (By.ID, "com.google.android.apps.photos:id/title")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def open_album(self):
        """打开 第二个相册"""
        print('选择相册')
        self.driver \
            .find_elements_by_id("com.google.android.apps.photos:id/title")[2] \
            .click()

    @teststeps
    def wait_check_picture_page(self):
        """图片 的class_name为依据"""
        locator = (By.CLASS_NAME, "android.view.ViewGroup")
        return self.wait.wait_check_element(locator)

    # 权限询问页面
    @teststeps
    def wait_check_permission_page(self):
        """ 的id为依据"""
        locator = (By.ID, "com.android.packageinstaller:id/permission_message")
        return self.wait.wait_check_element(locator, 3)

    @teststeps
    def permission_allow_button(self):
        """允许 按钮"""
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'允许')]") \
            .click()


class MeiZuMPage(BasePage):
    """MeiZu - M15  7.1"""
    def __init__(self):
        self.wait = WaitElement()

    # 拍照
    @teststeps
    def wait_check_camera_page(self, var=10):
        """拍照键 的为依据"""
        locator = (By.ID, "com.meizu.media.camera:id/shutter_button")
        return self.wait.wait_check_element(locator, var)

    # 第一页面
    @teststeps
    def click_retake_button(self):
        """相机'切换前置后置摄像头'按钮"""
        print('切换前置后置摄像头')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/switch_camera_btn") \
            .click()

    @teststeps
    def click_camera_button(self):
        """以相机拍照按钮"""
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/shutter_button") \
            .click()

    @teststeps
    def cancel_button(self):
        """以相机  左上角 取消按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_elements_by_class_name("android.view.View")[1] \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.camera:id/btn_retake")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/done_button") \
            .click()

    @teststeps
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/btn_retake") \
            .click()

    # 相册
    @teststeps
    def wait_check_album_page(self, var=10):
        """最近 的xpath 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '最近')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def open_album(self):
        """打开 图库"""
        print('选择相册')
        self.driver \
            .find_elements_by_id("android:id/title")[3] \
            .click()

    # 第一个页面
    @teststeps
    def wait_check_picture_page(self):
        """选择图片 的ID为依据"""
        locator = (By.ID, "com.meizu.media.gallery:id/action_bar_title")
        return self.wait.wait_check_element(locator)

    @teststeps
    def choose_image(self, index=0):
        """选择相册图片"""
        print('选择照片')
        if index == 0:
            index = random.randint(1, 10)

        self.driver \
            .find_elements_by_id("com.meizu.media.gallery:id/thumbnail")[index] \
            .click()

    # 第二个页面
    @teststeps
    def wait_check_commit_page(self):
        """确定 按钮 的为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '确定')]")
        return self.wait.wait_check_element(locator)

    # 第三个页面
    @teststeps
    def wait_check_save_page(self):
        """Ok 按钮 的为依据"""
        locator = (By.XPATH, "//android.widget.Button[contains(@text, 'Ok')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def commit_button(self):
        """相册 ok 按钮"""
        print('点击 OK按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'Ok')]") \
            .click()

    @teststeps
    def cancel_button(self):
        """相册Cancel按钮"""
        print('点击 Cancel按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'Cancel')]") \
            .click()


class Mi6x(BasePage):
    """小米 6x 8.1"""
    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def x_cancel_button(self):
        """相机'取消'按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_element_by_id('android:id/button1') \
            .click()

    # 拍照
    @teststeps
    def wait_check_camera_page(self, var=10):
        """拍照键 的为依据"""
        locator = (By.ID, shutter_button_id)
        return self.wait.wait_check_element(locator, var)

    # 第一页面
    @teststeps
    def click_retake_button(self):
        """相机'切换前置后置摄像头'按钮"""
        print('切换前置后置摄像头')
        self.driver \
            .find_element_by_id(switch_button_id) \
            .click()

    @teststeps
    def click_camera_button(self):
        """以相机拍照按钮"""
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id(shutter_button_id) \
            .click()

    @teststeps
    def cancel_button(self):
        """以相机  左上角 取消按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_elements_by_class_name("android.view.View")[3] \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, retake_button_id)
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id(done_button_id) \
            .click()

    @teststeps
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id(retake_button_id) \
            .click()

    # 相册
    @teststeps
    def wait_check_album_page(self, var=10):
        """最近 的xpath 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '最近')]")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def open_album(self):
        """打开 图库"""
        print('选择相册')
        self.driver \
            .find_elements_by_id("android:id/title")[3] \
            .click()

    # 第一个页面
    @teststeps
    def wait_check_picture_page(self):
        """选择图片 的ID为依据"""
        locator = (By.ID, "com.meizu.media.gallery:id/action_bar_title")
        return self.wait.wait_check_element(locator)

    @teststeps
    def choose_image(self, index=0):
        """选择相册图片"""
        print('选择照片')
        if index == 0:
            index = random.randint(1, 10)

        self.driver \
            .find_elements_by_id("com.meizu.media.gallery:id/thumbnail")[index] \
            .click()

    # 第二个页面
    @teststeps
    def wait_check_commit_page(self):
        """确定 按钮 的为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '确定')]")
        return self.wait.wait_check_element(locator)

    # 第三个页面
    @teststeps
    def wait_check_save_page(self):
        """Ok 按钮 的为依据"""
        locator = (By.XPATH, "//android.widget.Button[contains(@text, 'Ok')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def commit_button(self):
        """相册 ok 按钮"""
        print('点击 OK按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'Ok')]") \
            .click()

    @teststeps
    def cancel_button(self):
        """相册Cancel按钮"""
        print('点击 Cancel按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.Button[contains(@text,'Cancel')]") \
            .click()


class ChangeImage(BasePage):
    """更换头像功能所有控件信息
        之所以在这里定义,是为了避免每次调用click_bounds()时，再次计算坐标"""
    def __init__(self):
        self.meizu = MeizuPage()
        self.honor = HonorPage()
        self.pixel = PixelPage()
        self.meizu_m = MeiZuMPage()  # MeiZu - M15  7.1

    @teststeps
    def permission_allow(self):
        """ 拍照权限"""
        if self.pixel.wait_check_permission_page():
            self.pixel.permission_allow_button()  # 允许 按钮

    @teststeps
    def album_upload_save(self):
        """相册 上传照片 正常流程"""
        print('-------------相册修改 保存---------------')
        # if self.simu.wait_check_album_page():  # 5.1模拟器
        #     self.simu.choose_album_mul()  # 选择相册
        #     time.sleep(2)
        #     self.meizu.choose_image()  # 选择照片
        #     if self.meizu.wait_check_save_page():
        #         self.meizu.click_save_button()  # 完成 按钮
        # elif self.app.wait_check_album_page():  # 真机 华为7.0
        #     self.app.open_album()  # 进入某相册
        #     if self.app.wait_check_picture_page():
        #         self.meizu.choose_image()  # 选择照片
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_save_button()  # 完成按钮
        # elif self.meizu.wait_check_album_page():  # 真机 魅族5.1
        #         self.meizu.click_album()  # 进入相册列表页
        #         if self.meizu.wait_check_all_picture_page():
        #             self.meizu.open_album()  # 选择某相册
        #             if self.meizu.wait_check_album_page():
        #                 self.meizu.choose_image()  # 选择照片
        #                 if self.meizu.wait_check_photo_page():
        #                     self.meizu.commit_button()  # 确定按钮
        #                     if self.meizu.wait_check_save_page():
        #                         self.meizu.click_save_button()  # 完成按钮
        # elif self.pixel.wait_check_album_page():  # 真机 Pixel
        #     self.pixel.open_album()  # 进入某相册
        #     if self.pixel.wait_check_picture_page():
        #         self.meizu.choose_image()  # 选择照片
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_save_button()  # 完成按钮

        if self.meizu_m.wait_check_picture_page():  # 真机 MeiZu - M15  7.1
            self.meizu_m.choose_image()  # 选择照片
            if self.meizu_m.wait_check_commit_page():
                self.meizu.commit_button()  # 确定 按钮
                if self.meizu.wait_check_save_page():
                    self.meizu.click_save_button()  # 完成按钮
                    print('----------------------')

    @teststeps
    def album_upload_cancel(self):
        """相册 上传照片 - 取消"""
        print('------------取消相册修改--------------')
        # if self.simu.wait_check_album_page():  # 5.1模拟器
        #     self.simu.choose_album_mul()  # 选择相册
        #     time.sleep(2)
        #     self.meizu.choose_image()  # 选择照片
        #     if self.meizu.wait_check_save_page():
        #         self.meizu.click_cancel_button()  # 取消 按钮
        # elif self.app.wait_check_album_page():  # 真机 华为7.0
        #     self.app.open_album()  # 进入某相册
        #     if self.app.wait_check_picture_page():
        #         self.meizu.choose_image()  # 选择照片
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_cancel_button()  # 取消按钮
        # elif self.meizu.wait_check_album_page():  # 真机 魅族5.1
        #         self.meizu.click_album()   # 进入相册列表页
        #         if self.meizu.wait_check_all_picture_page():
        #             self.meizu.open_album()  # 选择某相册
        #             if self.meizu.wait_check_album_page():
        #                 self.meizu.choose_image()  # 选择照片
        #                 if self.meizu.wait_check_photo_page():
        #                     self.meizu.commit_button()  # 确定按钮
        #                     if self.meizu.wait_check_save_page():
        #                         self.meizu.click_cancel_button()  # 取消按钮
        # elif self.pixel.wait_check_album_page():  # 真机 Pixel
        #     self.pixel.open_album()  # 进入某相册
        #     if self.pixel.wait_check_picture_page():
        #         self.meizu.choose_image()  # 选择照片
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_cancel_button()  # 取消按钮

        if self.meizu_m.wait_check_picture_page():  # 真机 MeiZu - M15  7.1
            self.meizu_m.choose_image(random.randint(1, 10))  # 选择照片
            if self.meizu_m.wait_check_commit_page():
                self.meizu.commit_button()  # 确定 按钮
                if self.meizu.wait_check_save_page():
                    self.meizu.click_cancel_button()  # 取消按钮
                    print('----------------------')

    @teststeps
    def photo_upload_save(self):
        """拍照 上传照片 正常保存"""
        print('-------------拍照修改 保存---------------')
        # if self.meizu.wait_check_camera_page():  # 真机 魅族5.1
        #     self.meizu.click_camera_button()  # 拍照键
        #     if self.meizu.wait_check_retake_page():
        #         self.meizu.click_done_button()  # 完成按钮
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_save_button()  # 保存按钮
        #             return True
        # elif self.app.wait_check_camera_page():  # 真机 华为7.0
        #     self.app.click_camera_button()  # 拍照键
        #     if self.app.wait_check_retake_page():
        #         self.app.click_done_button()  # 完成按钮
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_save_button()  # 保存按钮
        #             return True
        # elif self.pixel.wait_check_camera_page():  # 真机 Pixel
        #     self.pixel.click_camera_button()  # 拍照键
        #     if self.pixel.wait_check_retake_page():
        #         self.pixel.click_done_button()  # 完成按钮
        #         return True
        if self.meizu_m.wait_check_camera_page():  # 真机 MeiZu - M15  7.1
            self.meizu_m.click_camera_button()  # 拍照键
            if self.meizu_m.wait_check_retake_page():
                self.meizu_m.click_done_button()  # 完成按钮

                if self.meizu.wait_check_save_page():
                    self.meizu.click_save_button()  # 完成按钮
                    print('----------------------')
                    return True
        # else:  # 模拟器 5.1
        #     return False

    @teststeps
    def photo_upload_cancel(self):
        """拍照 上传照片- 取消"""
        print('------------取消拍照修改--------------')
        # if self.meizu.wait_check_camera_page():  # 真机 魅族5.1
        #     self.meizu.click_camera_button()  # 拍照按钮
        #     if self.meizu.wait_check_retake_page():
        #         self.meizu.click_done_button()  # 完成按钮
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_cancel_button()  # 取消按钮
        #             return True
        # elif self.app.wait_check_camera_page():  # 真机 华为7.0
        #     self.app.click_camera_button()  # 拍照按钮
        #     if self.app.wait_check_retake_page():
        #         self.app.click_done_button()  # 完成按钮
        #         if self.meizu.wait_check_save_page():
        #             self.meizu.click_cancel_button()  # 取消按钮
        #             return True
        # elif self.pixel.wait_check_camera_page():  # 真机 Pixel
        #     self.pixel.cancel_button()  # 取消按钮
        #     return True
        if self.meizu_m.wait_check_camera_page():  # 真机 MeiZu - M15  7.1
            self.meizu_m.click_camera_button()  # 拍照键
            if self.meizu_m.wait_check_retake_page():
                self.meizu_m.click_done_button()  # 完成按钮

                if self.meizu.wait_check_save_page():
                    self.meizu.click_cancel_button()  # 取消按钮
                    print('----------------------')
                    return True
        # else:  # 模拟器 5.1
        #     return False

    @teststeps
    def photo_upload_retake(self):
        """拍照 上传照片 -重拍"""
        print('-------------重拍修改 保存---------------')
        # if self.meizu.wait_check_camera_page():  # 真机 魅族5.1
        #     self.meizu.click_camera_button()  # 拍照键
        #     if self.meizu.wait_check_retake_page():
        #         self.meizu.click_retake_button()  # 重拍 按钮
        #
        #         if self.meizu.wait_check_camera_page():
        #             self.meizu.click_camera_button()  # 拍照键
        #             if self.meizu.wait_check_retake_page():
        #                 self.meizu.click_done_button()  # 完成 按钮
        #                 if self.meizu.wait_check_save_page():
        #                     self.meizu.click_save_button()  # 保存 按钮
        #                     return True
        # elif self.app.wait_check_camera_page():  # 真机 华为7.0
        #     self.app.click_camera_button()  # 拍照按钮
        #     if self.app.wait_check_retake_page():
        #         self.app.click_retake_button()  # 重拍 按钮
        #
        #         if self.app.wait_check_camera_page():
        #             self.app.click_camera_button()  # 拍照按钮
        #             if self.app.wait_check_retake_page():
        #                 self.app.click_done_button()  # 完成 按钮
        #                 if self.meizu.wait_check_save_page():
        #                     self.meizu.click_save_button()  # 保存按钮
        #                     return True
        # elif self.pixel.wait_check_camera_page():  # 真机 Pixel
        #     self.pixel.click_camera_button()  # 拍照键
        #     if self.pixel.wait_check_retake_page():
        #         self.pixel.click_retake_button()  # 重拍按钮
        #
        #         if self.pixel.wait_check_camera_page():  # 真机 Pixel  8.1
        #             self.pixel.click_camera_button()  # 拍照按钮
        #             if self.pixel.wait_check_retake_page():
        #                 self.pixel.click_done_button()  # 完成按钮
        #         return True
        if self.meizu_m.wait_check_camera_page():  # 真机 MeiZu - M15  7.1
            self.meizu_m.click_camera_button()  # 拍照键
            if self.meizu_m.wait_check_retake_page():
                self.meizu_m.click_retake_button()  # 重拍按钮

                if self.meizu_m.wait_check_camera_page():  # 真机 MeiZu - M15  7.1
                    self.meizu_m.click_camera_button()  # 拍照键
                    if self.meizu_m.wait_check_retake_page():
                        self.meizu_m.click_done_button()  # 完成按钮
                        if self.meizu.wait_check_save_page():
                            self.meizu.click_save_button()  # 完成按钮
                    print('----------------------')
                    return True
        # else:  # 模拟器 5.1
        #     return False
