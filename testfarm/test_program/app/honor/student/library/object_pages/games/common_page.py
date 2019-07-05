# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 11:30
# -------------------------------------------
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class CommonPage(BasePage):
    @teststep
    def wait_check_next_btn_page(self):
        """听音选图页面检查点 以题目索引id作为依据"""
        locator = (By.ID, self.id_type() + "fab_next")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def rest_bank_num(self):
        """待完成题数"""
        ele = self.driver.find_element_by_id('{}rate'.format(self.id_type()))
        return int(ele.text)

    @teststep
    def bank_time(self):
        """题目时间"""
        ele = self.driver.find_element_by_id('{}time'.format(self.id_type()))
        time_str = re.findall(r'\d', ele.text)
        return int(time_str[0]) * 3600 + int(time_str[1]) * 60 + int(time_str[2]) * 10 + int(time_str[3])

    @teststep
    def rate_judge(self, total, i):
        """待完成数校验"""
        current_rate = self.rest_bank_num()
        if int(current_rate) != total - i:
            print('★★★ 待完成数不正确', current_rate, '应为：', total - i)

    @teststep
    def font_middle(self):
        """第一个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_middle")
        return ele

    @teststep
    def font_large(self):
        """第二个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_large")
        return ele

    @teststep
    def font_great(self):
        """第三个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_great")
        return ele

    @teststep
    def next_btn(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_next')
        return ele

    @teststep
    def judge_next_is_true_false(self, var):
        attr = GetAttribute().enabled(self.next_btn())
        if attr != var:
            print('★★★ 下一步按钮状态错误', attr)

    @teststep
    def judge_timer(self, timer):
        if len(timer) > 1:
            if any(timer[i + 1] > timer[i] for i in range(0, len(timer) - 1)):
                print('计时功能无误:', timer, '\n')
                return True
            else:
                print('★★★ Error - 计时错误:', timer, '\n')
        else:  # 只有一道题
            print('只有一道题，时间为:', timer[0], '\n')
            return True
