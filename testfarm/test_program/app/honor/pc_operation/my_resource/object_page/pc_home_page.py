#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from pynput.mouse import Button, Controller

from conf.base_page import BasePage
from conf.decorator_pc import teststeps
from app.honor.pc_operation.tools.wait_element import WaitElement


class HomePage(BasePage):
    """主界面"""

    def __init__(self, driver):
        self.wait = WaitElement(driver)
        self.mouse = Controller()

    @teststeps
    def wait_check_page(self, var=15):
        """以 我的题库 元素 的xpath为依据"""
        locator = (By.XPATH, '//span[text()="班级"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_st_close(self):
        """x按钮"""
        locator = (By.XPATH, '//i[@class="iconfont icon-cross"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def st_close(self):
        """x按钮"""
        locator = (By.XPATH, '//i[@class="iconfont icon-cross"]')
        self.wait.wait_find_element(locator).click()

    # 顶部 菜单栏
    @teststeps
    def logo_icon(self):
        """左上角 logo图标"""
        locator = (By.ID, 'logo')
        return self.wait.wait_find_element(locator)

    @teststeps
    def home_tab(self):
        """顶部 首页tab"""
        locator = (By.XPATH, '//a[@href="#/master"]')
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def test_bank_tab(self):
        """顶部 题库tab"""
        locator = (By.XPATH, "//div[@class='nav']/a[contains(text(),'题库')]")
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def test_basket_tab(self):
        """顶部 题筐tab"""
        locator = (By.XPATH, '//i[@class="iconfont icon-cart"]')
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def test_basket_num(self):
        """题筐 数量"""
        locator = (By.XPATH, '//span[@class="highlight"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def message_icon(self):
        """顶部 消息icon"""
        locator = (By.XPATH, '//div[@id="user-center"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def avatar_icon(self):
        """顶部 右上角 头像"""
        locator = (By.XPATH, '//span[@class="avatar"]/img')
        return self.wait.wait_find_element(locator)

    @teststeps
    def nickname(self):
        """顶部 右上角 nickname"""
        locator = (By.XPATH, '//span[@class="name"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def user_center_item(self):
        """顶部 右上角 菜单-个人中心"""
        locator = (By.LINK_TEXT, '个人中心')
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def logout_button(self):
        """顶部 右上角 菜单-退出"""
        locator = (By.LINK_TEXT, '退出')
        return self.wait.wait_find_element(locator).click()

    # 左侧 菜单栏
    #  班级
    @teststeps
    def vanclass_title(self):
        """班级"""
        locator = (By.XPATH, '//div[@id="vanclass-list"]/span')
        return self.wait. wait_find_element(locator)

    @teststeps
    def vanclass_item(self):
        """班级 条目"""
        locator = (By.XPATH, '//div[@id="class-list"]/a/descendant::i')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def vanclass_adjust_button(self):
        """班级"""
        locator = (By.XPATH, '//div[@id="class-list"]/a/i[@title="拖拽调整顺序"]')
        return self.wait.wait_find_elements(locator).click()

    @teststeps
    def vanclass_name(self):
        """班级 名称"""
        locator = (By.XPATH, '//div[@id="class-list"]/a')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def vanclass_create_icon(self):
        """班级"""
        locator = (By.XPATH, '//a[@id="step1"]/i')
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def vanclass_create_button(self):
        """班级"""
        locator = (By.XPATH, '//a[@id="step1"  and @class="link-button"]')
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def toggle_button(self):
        """班级过多时，下拉wording"""
        locator = (By.XPATH, '//a[@class="toggle-link"]')
        return self.wait.wait_find_element(locator).click()

    @teststeps
    def toggle_icon(self):
        """班级过多时，下拉/收起icon"""
        locator = (By.XPATH, '//a[@class="toggle-link"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def drag_and_drop_operation(self, origin, target):
        """拖拽元素"""
        ActionChains(self.driver).drag_and_drop(origin, target).perform()

        start = origin.location
        print(start)
        self.mouse.position = (start['x'], start['y'])
        time.sleep(2)

        self.mouse.press(Button.left)
        target = target.location
        print(target)
        self.mouse.position = (target['x'], target['y'])
        time.sleep(2)

        # 松开鼠标
        self.mouse.release(Button.left)
        time.sleep(1)

    # 其他
    @teststeps
    def other_title(self):
        """其它"""
        locator = (By.XPATH, '//div[@class="group"]/span[text()=" 其它"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def my_library_icon(self):
        """图书馆icon"""
        locator = (By.XPATH, '//a[text()=" 图书馆"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def my_library(self):
        """图书馆"""
        locator = (By.XPATH, '//a[text()=" 图书馆"]')
        self.wait\
            .wait_find_element(locator).click()

    @teststeps
    def my_resource_icon(self):
        """我的题库icon"""
        locator = (By.XPATH, '//a[text()=" 我的题库"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def my_resource(self):
        """我的题库"""
        # time.sleep(2)
        locator = (By.XPATH, '//a[text()=" 我的题库"]')
        self.wait\
            .wait_find_element(locator).click()

    @teststeps
    def draft_icon(self):
        """草稿箱icon"""
        locator = (By.XPATH, '//a[text()=" 草稿箱"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def draft(self):
        """草稿箱"""
        locator = (By.XPATH, '//a[text()=" 草稿箱"]')
        self.wait\
            .wait_find_element(locator).click()

    @teststeps
    def timing_hw_icon(self):
        """定时作业icon"""
        locator = (By.XPATH, '//a[text()=" 定时作业"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def timing_hw(self):
        """定时作业"""
        locator = (By.XPATH, '//a[text()=" 定时作业"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststeps
    def my_share_icon(self):
        """我的分享icon"""
        locator = (By.XPATH, '//a[text()=" 我的分享"]/i')
        return self.wait.wait_find_element(locator)

    @teststeps
    def my_share(self):
        """我的分享"""
        locator = (By.XPATH, '//a[text()=" 我的分享"]')
        self.wait. \
            wait_find_element(locator).click()

    # 首页 主要内容
    # 轮播图
    @teststeps
    def carousel_img(self):
        """轮播图"""
        locator = (By.XPATH, '//div[@class="el-carousel"]/div')
        return self.wait.wait_find_element(locator)

    @teststeps
    def carousel_img_button(self):
        """轮播图 按钮"""
        locator = (By.XPATH, '//div[@class="el-carousel"]/ul/li')
        return self.wait.wait_find_element(locator)

    # 中部 tab
    @teststeps
    def primary_school_tab(self):
        """小学"""
        locator = (By.XPATH, '//div[text()="小学资源推荐"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststeps
    def junior_middle_school_tab(self):
        """初中"""
        locator = (By.XPATH, '//div[text()="初中资源推荐"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststeps
    def colloquial_picture_book_tab(self):
        """口语绘本"""
        locator = (By.XPATH, '//div[text()="口语绘本资源"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststeps
    def management_tab(self):
        """管理干货"""
        locator = (By.XPATH, '//div[text()="管理干货推荐"]')
        self.wait. \
            wait_find_element(locator).click()

    # 资源列表
    @teststeps
    def source_item(self):
        """资源条目"""
        locator = (By.XPATH, '//div[@class="el-tabs__content"]/a')
        return self.wait.wait_find_elements(locator)

    # 弹框窗口
    @teststeps
    def wait_check_dialog_page(self, var=15):
        """以 我的题库 元素 的xpath为依据"""
        locator = (By.XPATH, '//span[@class="el-dialog__title"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def dialog_title(self):
        """弹框title"""
        locator = (By.XPATH, '//span[@class="el-dialog__title"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def dialog_input_title(self):
        """弹框 输入框前的title"""
        locator = (By.XPATH, '//*[@id="new-vanclass-form"]/div/label')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def dialog_input(self):
        """弹框 输入框"""
        locator = (By.XPATH, '//*[@id="new-vanclass-form"]/div/div/div/input')
        return self.wait.wait_find_element(locator)

    @teststeps
    def dialog_tips_title(self):
        """弹框 提示信息title"""
        locator = (By.XPATH, '//label[@class="el-form-item__label"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def dialog_tips(self):
        """弹框 提示信息"""
        locator = (By.XPATH, '//span[@class="del-tip"]')
        return self.wait.wait_find_element(locator).text

    @teststeps
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//span[contains(text(), "取 消")]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//button[@class="el-button el-button--default el-button--primary "]')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def save_button(self):
        """保存 按钮"""
        locator = (By.XPATH, '//span[text()="保存"]/parent::button')
        self.wait.wait_find_element_visibility(locator).click()

    @teststeps
    def close_button(self):
        """X 按钮"""
        locator = (By.XPATH, '//button[@aria-label="Close"]')
        self.wait. \
            wait_find_element(locator).click()

    @teststeps
    def edit_button(self):
        """编辑 按钮"""
        locator = (By.XPATH, '//span[text()="编辑"]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def delete_button(self):
        """删除 按钮"""
        locator = (By.XPATH, '//span[text()="删除"]/parent::button')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def input_text(self):
        """输入的文本信息"""
        locator = (By.XPATH, '//span[@class="name"]')
        return self.wait.wait_find_element(locator)

    @teststeps
    def alert_info(self):
        """提示信息"""
        locator = (By.CLASS_NAME, 'el-message')
        return self.wait.wait_find_element(locator).text
