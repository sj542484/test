#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from conf.base_page import BasePage


class Vanclass(BasePage):
    """本班习题 - 完成情况tab 二级详情"""

    def __init__(self):
        self.home = ThomePage()
        self.v_hw = VanclassHwPage()

    def vanclass_hw(self):
        if self.v_hw.wait_check_list_page():
            name = self.v_hw.hw_name()  # 作业name
            count = []
            for i in range(len(name)):
                text = name[i].text
                if self.v_hw.wait_check_list_page():
                    if self.home.brackets_text_in(text) == '习题':
                        count.append(i)
            return count


menu = Vanclass().vanclass_hw()
