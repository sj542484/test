#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium import webdriver

from app.honor.pc_operation.my_resource.object_page.game_list_detail import GameDetailPage
from app.honor.pc_operation.my_resource.object_page.login_page import LoginPage
from app.honor.pc_operation.my_resource.object_page.my_recommend_page import ManageRecommendPage
from app.honor.pc_operation.my_resource.object_page.pc_home_page import HomePage
from app.honor.pc_operation.test_bank.object_page.pc_test_bank_page import TestBankPage
from conf.decorator_pc import teststeps
from conf.base_config import GetVariable as gv


class Delete(object):
    """删除微课"""

    def __init__(self):
        driver = webdriver.Chrome('E:/480179/Tools/chromedriver_win32/71/chromedriver.exe')
        driver.maximize_window()
        driver.get(gv.URL)

        self.login = LoginPage(driver)
        self.home = HomePage(driver)
        self.detail = GameDetailPage(driver)
        self.manage = ManageRecommendPage(driver)
        self.bank =TestBankPage(driver)

    @teststeps
    def delete_recommend_operation(self):
        self.login.login_operation()  # 登录操作
        print('------删除推荐 具体操作-----')
        if self.home.wait_check_page():
            self.home.test_bank_tab()  # 进入 题库
            if self.bank.wait_check_page():
                self.bank.our_school_button()  # 本校 按钮
                if self.bank.wait_check_page():

                    var = ['大题', '题单', '试卷']
                    for i in range(len(var)):
                        if i == 0:
                            if self.bank.wait_check_no_page():
                                print('暂无数据')
                            elif self.bank.wait_check_menu_list_page():
                                self.bank.choose_button()
                                self.bank.out_bank_button()
                                self.bank.menu_tips_content()  # 删除具体操作
                        elif i == 1:
                            self.bank.games()
                            if self.bank.wait_check_no_page():
                                print('暂无数据')
                            elif self.bank.wait_check_games_list_page():
                                self.bank.choose_button()
                                self.bank.out_bank_button()
                                self.bank.games_tips_content()  # 删除具体操作
                        elif i == 2:
                            self.bank.paper()
                            if self.bank.wait_check_no_page():
                                print('暂无数据')
                            elif self.bank.wait_check_paper_list_page():
                                self.bank.choose_button()
                                self.bank.out_bank_button()

                                self.bank.menu_tips_content()  # 删除具体操作
            else:
                print('未进入题库')
        else:
            print('未进入主界面')
