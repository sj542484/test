#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.test_paper_detail_page import PaperDetailPage
from app.honor.teacher.user_center.user_information.object_page.change_image_page import ChangeImage
from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.screen_shot import ScreenShot
from utils.wait_element import WaitElement


class PaperSharePage(BasePage):
    """试卷 分享页面"""

    def __init__(self):
        self.wait = WaitElement()
        self.change_image = ChangeImage()
        self.paper = PaperDetailPage()
        self.filter = FilterPage()
        self.home = ThomePage()
        self.question = TestBankPage()

    # 分享 功能
    @teststeps
    def wait_check_share_page(self):
        """以“title:分享”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'分享')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_share_list_page(self):
        """以“”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学校')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def defined_school_info(self):
        """自定义学校信息"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'自定义学校信息')]").text
        return item

    @teststep
    def help_button(self):
        """? 按钮 """
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "question") \
            .click()

    @teststeps
    def school_upload_title(self):
        """上传学校微标"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'上传学校微标')]").text
        return item

    @teststep
    def school_upload_img(self):
        """学校徽标 图片上传 按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "upload_img")
        return ele

    @teststeps
    def qr_upload_title(self):
        """上传二维码"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'上传二维码')]").text
        return item

    @teststep
    def qr_upload_img(self):
        """二维码 图片上传 按钮"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "upload_img_qr")
        return ele

    @teststeps
    def share_name(self):
        """页面名称"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_name").text
        return item

    @teststeps
    def share_name_edit(self):
        """页面名称 编辑框"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "name")
        return item

    @teststeps
    def share_school(self):
        """学校"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_school").text
        return item

    @teststeps
    def share_school_edit(self):
        """学校 编辑框"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "school")
        return item

    @teststeps
    def share_contact(self):
        """联系方式"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_contact_information").text
        return item

    @teststeps
    def share_contact_edit(self):
        """联系方式 编辑框"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "contact_information")
        return item

    @teststeps
    def send_title(self):
        """选择发送至"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'选择发送至')]").text
        return item

    @teststep
    def wechat_friend(self):
        """微信好友"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "weixin")
        return ele

    @teststep
    def wechat_circle(self):
        """微信朋友圈"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "weixin_friends")
        return ele

    @teststep
    def copy_link(self):
        """复制链接"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "copylink")
        return ele

    @teststeps
    def judge_loading_tips(self):
        """正在加载…"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'正在加载…')]")
        return self.wait.judge_is_exists(locator)

    # 微信 登录界面
    @teststeps
    def wait_check_share_wechat_page(self, var=10):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'微信号/QQ/邮箱登录')]")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def wechat_back_button(self):
        """微信好友 返回"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView") \
            .click()

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

    # 该校h5分享次数已用完
    @teststeps
    def wait_check_toast_page(self, var=20):
        """以“title:提示”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "md_title")
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def share_page_info(self):
        """试卷详情页 分享页面信息"""
        if self.wait_check_share_page():
            if self.wait_check_share_list_page():
                name = self.share_name_edit()  # 页面名称
                school = self.share_school_edit()  # 学校
                contact = self.share_contact_edit()  # 联系方式

                print('--------------------试卷分享页面----------------------')
                print(self.defined_school_info(), '\n',
                      self.school_upload_title(), '\n',
                      self.qr_upload_title(), '\n',
                      self.share_name(), ':', name.text, '\n',
                      self.share_school(), ':', school.text, '\n',
                      self.share_contact(), ':', contact.text, '\n',
                      self.send_title(), ':', self.wechat_friend().text,self.wechat_circle().text, self.copy_link().text)
                print('----------------------------------------------------')

    # 使用说明
    @teststeps
    def wait_check_help_page(self):
        """以“title:使用说明”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'Vanthink Online')]")
        return self.wait.wait_check_element(locator)

    # 上传图片
    @teststeps
    def wait_check_change_page(self):
        """以“title:更改学校图标”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'更改学校图标')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_exchange_page(self):
        """以“title:更改二维码”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'更改二维码')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def click_photograph(self):
        """以“拍照”的xpath @index为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'拍照')]") \
            .click()

    @teststep
    def click_album(self):
        """以“从相册选择”的xpath @index为依据"""
        time.sleep(2)
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'从相册选择')]") \
            .click()

    @teststeps
    def upload_img_cancel_operation(self, img, var='school'):
        """拍照 上传照片"""
        self.change_image.permission_allow()  # 拍照权限

        if self.change_image.photo_upload_cancel():  # 上传照片具体操作
            if self.wait_check_share_page():  # 页面检查点
                ele = self.school_upload_img()  # 学校徽标
                if var == 'qr':
                    ele = self.qr_upload_img()  # 二维码

                if ScreenShot().same_as_screenshot(ele, img):  # 获取修改取消后的头像截图
                    print('取消修改成功')
                else:
                    print('★★★ Error - 取消修改失败')

        print('----------------------')

    @teststeps
    def upload_img_save_operation(self, img, var='school'):
        """拍照 上传照片"""
        self.change_image.permission_allow()  # 拍照权限

        if self.change_image.photo_upload_save():
            if self.wait_check_share_page():
                ele = self.school_upload_img()  # 学校徽标
                if var == 'qr':
                    ele = self.qr_upload_img()  # 二维码

                if not ScreenShot().same_as_screenshot(ele, img):  # 获取修改后的截图, 截图不相同时
                    print('修改成功')
                else:
                    print('★★★ Error - 修改失败')

        print('---------------------------')

    @teststeps
    def upload_img_retake_operation(self, img, var='school'):
        """拍照 上传照片"""
        self.change_image.permission_allow()  # 拍照权限

        if self.change_image.photo_upload_retake():
            if self.wait_check_share_page():
                ele = self.school_upload_img()  # 学校徽标
                if var == 'qr':
                    ele = self.qr_upload_img()  # 二维码

                if not ScreenShot().same_as_screenshot(ele, img):  # 获取修改后的截图, 截图不相同时
                    print('修改成功')
                else:
                    print('★★★ Error - 修改失败')

        print('---------------------------')

    @teststeps
    def album_cancel_operation(self, img, var='school'):
        """相册 上传照片"""
        self.change_image.album_upload_cancel()  # 上传照片具体操作
        if self.wait_check_share_page():  # 页面检查点
            ele = self.school_upload_img()  # 学校徽标
            if var == 'qr':
                ele = self.qr_upload_img()  # 二维码

            if ScreenShot().same_as_screenshot(ele, img):  # 获取修改取消后的头像截图
                print('取消修改成功')
            else:
                print('★★★ Error - 取消修改失败')
        print('----------------------')

    @teststeps
    def album_save_operation(self, img, var='school'):
        """相册 上传照片"""
        self.change_image.album_upload_save()  # 上传照片具体操作
        if self.wait_check_share_page():  # 页面检查点
            ele = self.school_upload_img()  # 学校徽标
            if var == 'qr':
                ele = self.qr_upload_img()  # 二维码

            if not ScreenShot().same_as_screenshot(ele, img):  # 获取修改后的截图, 截图不相同时
                print('修改成功')
            else:
                print('★★★ Error - 修改失败')
        print('----------------------')

    @teststeps
    def into_paper_share_page(self):
        """进入试卷分享页面"""
        if self.home.wait_check_page():  # 页面检查点
            self.question.judge_into_tab_question()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page('题单', 5):  # 页面检查点
                self.question.filter_button()  # 筛选按钮

                if self.filter.wait_check_page():
                    paper = self.filter.test_paper()
                    if GetAttribute().selected(paper) == 'false':
                        self.filter.click_test_paper()  # 点击 试卷
                        self.filter.commit_button()  # 确定按钮
                    else:
                        self.filter.commit_button()  # 确定按钮

            if self.question.wait_check_page('试卷', 5):  # 页面检查点
                item = self.question.question_name()  # 获取name
                print('试卷:', item[1][2])
                item[0][2].click()  # 点击第X个试卷

                if self.paper.wait_check_page():  # 页面检查点
                    self.paper.share_button()  # 分享 按钮

    @teststeps
    def judge_app_status(self):
        """判断应用当前状态"""
        if self.home.wait_check_page():  # 在主界面
            self.into_paper_share_page()
        elif self.wait_check_share_page():  # 在分享界面
            print('在分享页面')
        else:
            print('在其他页面,重启app')
            TloginPage().close_app()  # 关闭APP
            TloginPage().launch_app()  # 重启APP
            if self.home.wait_check_page():  # 在主界面
                self.into_paper_share_page()
