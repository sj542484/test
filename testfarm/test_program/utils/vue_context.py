#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import time
from appium.webdriver.mobilecommand import MobileCommand

from conf.base_config import GetVariable
from conf.base_page import BasePage
from conf.decorator import teststeps


class VueContext(BasePage):

    @teststeps
    def context(self):
        time.sleep(2)
        print(self.driver.contexts)

    @teststeps
    def switch_h5(self):
        """切换到web"""
        # time.sleep(2)
        # self.context()
        # context = self.driver.contexts
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": GetVariable().CONTEXT})

        # for value in context:
        #     if 'WEBVIEW_com.vanthink.vanthinkteacher' in value:
        #         self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": value})
        #         break
        # self.current_context()

    @teststeps
    def switch_app(self):
        """切换到apk"""
        # time.sleep(2)
        self.driver.execute(MobileCommand.SWITCH_TO_CONTEXT, {"name": "NATIVE_APP"})
        # self.current_context()

    @teststeps
    def current_context(self):
        """首页口语/习题 班级口语/习题和下方作业列表 ,其中除用户指南 作业编辑 再次发布跳转到原生 , 其余全是网页"""
        print(self.driver.current_context)

    @teststeps
    def app_web_switch(self):
        """app 和 web页面切换"""
        self.switch_app()  # 切到apk
        self.switch_h5()  # 切到web

    @teststeps
    def current_activity(self):
        """首页口语/习题 班级口语/习题和下方作业列表 ,其中除用户指南 作业编辑 再次发布跳转到原生 , 其余全是网页"""
        self.driver.background_app(2)
        print('ACTIVITY:',self.driver.current_context)
