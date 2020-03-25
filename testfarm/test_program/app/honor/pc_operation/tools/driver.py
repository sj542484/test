#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium import webdriver
from conf.base_config import GetVariable as gv


class Driver:

    def run_case(self):
        driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        driver.get(gv.URL)

        driver.quit()
