#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

from conf.base_page import BasePage
from conf.decorator import teststeps


class ConnectDB(BasePage):

    @teststeps
    def __init__(self):
        self.connect = pymysql.\
            connect(host='172.17.0.200', user='director', passwd='AZ*vkTJj', db='b_vanthink_core')

        self.cursor = self.connect.cursor()

    @teststeps
    def operate_mysql(self,mysql):
        self.cursor.execute(mysql)
        return self.cursor.fetchall()
