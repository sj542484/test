#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.common.by import By

from testfarm.test_program.conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from conf.base_config import GetVariable as gv
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class QuestionDetailPage(BasePage):
    """题单详情 页面"""
    game_value = gv.PACKAGE_ID + "test_bank_name"  # 小游戏名
    game_type_value = gv.PACKAGE_ID + "type"  # 小游戏类型
    num_value = gv.PACKAGE_ID + "exercise_num"  # 共X题

    def __init__(self):
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title:题单详情”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'题单详情')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“题单详情页面  列表是否已加载出来”的id为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "test_bank_name")
        return self.wait.wait_check_element(locator)

    @teststep
    def recommend_button(self):
        """推荐到学校 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "recommend") \
            .click()
        time.sleep(2)

    @teststep
    def collect_button(self):
        """收藏/取消收藏 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "collect") \
            .click()
        time.sleep(1)

    @teststep
    def put_to_basket_button(self):
        """加入题筐 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "add_pool") \
            .click()

    @teststep
    def all_check_button(self):
        """全选/全不选 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "all_check") \
            .click()

    @teststep
    def check_button(self):
        """单选 按钮"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "cb_add")
        return ele

    @teststeps
    def game_item(self):
        """小游戏条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@resource-id, %s)]"
                                    "/parent::android.widget.LinearLayout"
                                    "/parent::android.widget.LinearLayout/parent::android.widget.LinearLayout"
                                    "/descendant::android.widget.TextView" % self.game_value)
        count = []  # 名称
        game_type = []
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:  # 类型
                count.append(i)
                game_type.append(ele[i].text)

        count.append(len(ele) - 1)

        content = []  # 页面内所有条目 元素text
        name = []  # 页面内所有条目元素
        num = []  # 共X题
        for j in range(len(count) - 1):
            item = []  # 每一个条目的所有元素k
            if count[j + 1] - count[j] in (4, 5):
                for k in range(count[j], count[j + 1]):
                    item.append(ele[k].text)
                    if GetAttribute().resource_id(ele[k]) == self.num_value:  # 共X题
                        num.append(ele[k])
                    elif GetAttribute().resource_id(ele[k]) == self.game_value:  # 题目名称
                        name.append(ele[k].text)

                content.append(item)

        return content, name, num, game_type

    @teststeps
    def game_mode(self, var):
        """小游戏模式--匹配小括号内游戏模式
        :param var: 名称
        """
        m = re.match(".*\（(.*)\）.*", var)  # title中有一个括号
        return m.group(1)
