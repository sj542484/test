#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium import webdriver

from app.honor.pc_operation.my_resource.object_page.game_list_detail import GameDetailPage
from app.honor.pc_operation.my_resource.object_page.login_page import LoginPage
from app.honor.pc_operation.my_resource.object_page.my_resource_page import MyResourcePage
from app.honor.pc_operation.my_resource.object_page.pc_home_page import HomePage
from conf.decorator import teststeps
from conf.base_config import GetVariable as gv


class Delete(object):
    """删除微课"""

    def __init__(self):
        self.driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get(gv.URL)

        self.login = LoginPage(self.driver)
        self.home = HomePage(self.driver)
        self.my = MyResourcePage(self.driver)
        self.detail = GameDetailPage(self.driver)

    @teststeps
    def delete_tiny(self):
        self.login.login_operation()  # 登录操作

        if self.home.wait_check_page():
            self.home.my_resource()  # 进入 我的题库
            if self.my.wait_check_page():

                self.my.game_list_tab()  # 大题tab
                if self.my.wait_menu_name_not():

                    self.my.mine_tab()  # 我的 tab按钮
                    if self.my.wait_upload_not():
                        self.delete_operation()  # 删除具体操作
            self.driver.close()  # 关闭浏览器

    @teststeps
    def delete_operation(self):
        """删除具体操作"""
        names = self.my.hw_name()  # 名称
        modes = self.my.hw_type()  # 类型
        print('---------------删除微课具体操作-------------')

        for k in range(20):
            if self.my.wait_check_mine_game_page():  # 大题tab + 我的tab
                name = names[k].text
                mode = modes[k].text
                if mode == '微课':
                    print('-------------------------')
                    print(name, mode)
                    names[k].click()
                    if self.detail.wait_check_switch_page():
                        self.detail.switch_iframe()
                        if self.detail.wait_check_page():
                            self.detail.delete_question_btn()  # 删除题目 按钮

                            self.detail.switch_back()
                            self.detail.commit_button()  # 删除题目 二次确认
                        else:
                            print('未打开iframe')
                            self.detail.switch_back()
                            self.detail.close_operation()
                else:
                    break
