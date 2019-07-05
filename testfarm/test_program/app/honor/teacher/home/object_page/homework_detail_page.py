#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.utils.click_bounds import ClickBounds
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.get_element_bounds import Element
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.wait_element import WaitElement


class HwDetailPage(BasePage):
    """ 作业详情 页面"""

    more_button_item_value = gv.PACKAGE_ID + "title"  # 更多按钮 -条目元素
    drop_down_menu_value = gv.PACKAGE_ID + "report_content"  # 下拉菜单 内容
    game_type_value = gv.PACKAGE_ID + 'type'  # 小游戏类型

    def __init__(self):
        self.game = GamesPage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_page(self):
        """以“title: 答题分析”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'答题分析')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def all_element(self):
        """页面内所有class name为android.widgetFen.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        # for i in range(len(ele)):
        #     print(ele[i].text)
        return ele

    @teststep
    def finished_tab(self):
        """完成情况"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'完成情况')]")
        return ele

    @teststep
    def analysis_tab(self):
        """答题分析"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'答题分析')]")
        return ele

    @teststep
    def answer_detail_button(self):
        """答题详情 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "details") \
            .click()

    @teststep
    def more_button(self):
        """更多 按钮"""
        self.driver \
            .find_element_by_class_name("android.widget.ImageView")\
            .click()

    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.ID, self.more_button_item_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def edit_delete_button(self, index):
        """编辑& 删除 按钮"""
        self.driver \
            .find_elements_by_id(self.more_button_item_value)[index] \
            .click()

    # 完成情况tab 学生列表
    @teststeps
    def wait_check_st_list_page(self):
        """以“学生完成情况 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "status")
        return self.wait.wait_check_element(locator)

    @teststep
    def st_item(self):
        """学生 条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.RelativeLayout/android.widget.LinearLayout"
                                    "/child::*")

        count = []
        for i in range(0, len(ele), 5):
            if GetAttribute().resource_id(ele[i]) == gv.PACKAGE_ID + 'name':
                count.append(i)
        count.append(len(ele))
        print(count)

        content = []  # 页面内所有学生
        for j in range(len(count) - 1):
            item = []  # 每一个学生
            for k in range(count[j], count[j + 1]):
                if ele[k].text != '':
                    item.append(ele[k].text)
            content.append(item)
        return content

    @teststep
    def st_type(self):
        """基础班/提分版学生"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "type")
        return ele

    @teststep
    def st_finish_status(self):
        """学生 完成与否"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "status")
        return ele

    @teststep
    def st_name(self):
        """学生 昵称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "name")
        return ele

    @teststep
    def st_icon(self):
        """学生 头像"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "head")
        return ele

    # 答题分析tab 页面
    @teststeps
    def wait_check_hw_list_page(self):
        """以“cup 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "iv_cup")
        return self.wait.wait_check_element(locator)

    @teststep
    def game_item(self):
        """游戏 条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/child::*")

        count = []
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:
                count.append(i)
        count.append(len(ele))

        content = []  # 页面内所有game
        for j in range(len(count)-1):
            item = []  # 每一个game
            for k in range(count[j], count[j+1]):
                if ele[k].text != '':
                    item.append(ele[k].text)
                elif GetAttribute().resource_id(ele[k]) == gv.PACKAGE_ID + 'iv_cup':
                    item.append(ele[k])
            content.append(item)
        return content

    @teststep
    def game_type(self):
        """游戏类型"""
        ele = self.driver \
            .find_elements_by_id(self.game_type_value)
        return ele

    @teststep
    def game_level(self):
        """提分"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "level")
        return ele

    @teststep
    def game_num(self):
        """共x题"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "exercise_num")
        return ele
        
    @teststep
    def game_name(self):
        """游戏 名称"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "test_bank_name")
        return ele

    @teststep
    def average_achievement(self):
        """全班首轮平均成绩x%"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_testbank_status")
        return ele

    @teststep
    def cup_icon(self):
        """奖杯 icon"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_cup")
        return ele
    
    # 游戏详情页
    @teststep
    def drop_down_button(self, var):
        """正确选项后答对率 下拉按钮"""
        loc = Element().get_element_bounds(var)
        self.driver.tap([(loc[2], loc[5] - 10)])

    @teststeps
    def verify_drop_down_content(self, var=5):
        """验证 正确选项后答对率 下拉菜单 是否存在"""
        locator = (By.ID, self.drop_down_menu_value)
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def drop_down_content(self):
        """x% 下拉菜单 内容"""
        item = self.driver \
            .find_element_by_id(self.drop_down_menu_value).text
        print('答题错误详情：', item)
        return item

    @teststeps
    def click_block(self):
        """点击 空白处"""
        ClickBounds().click_bounds(540, 200)

    # 学生个人答题情况页 特有元素
    @teststeps
    def wait_check_per_detail_page(self, var=20):
        """以“最优成绩 元素”为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_testbank_status")
        return self.wait.wait_check_element(locator, var)

    @teststep
    def per_game_item(self):
        """个人答题情况页面 -游戏 条目"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.LinearLayout/"
                                    "child::*/android.widget.TextView")

        count = []  # 每个游戏条目第一个元素为游戏类型
        var = []  # 游戏类型
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == self.game_type_value:
                count.append(i)
                var.append(ele[i])
        count.append(len(ele))

        content = []  # 页面内所有game
        for j in range(len(count) - 1):
            item = []  # 每一个game
            for k in range(count[j], count[j + 1]):
                if ele[k].text != '':
                    item.append(ele[k].text)
            content.append(item)
        return var, content

    @teststep
    def optimal_achievement(self):
        """最优成绩-"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_testbank_status")
        return ele

    @teststep
    def first_achievement(self):
        """首次成绩-"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_spend_time")
        return ele

    # 编辑作业 页面
    @teststeps
    def wait_check_edit_page(self):
        """以“title:编辑作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'编辑作业')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def assign_button(self):
        """发布作业 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "action_first")\
            .click()

    # 删除作业tips 页面
    @teststeps
    def wait_check_tips_page(self):
        """以“title:删除作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'删除作业')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def delete_cancel_operation(self):
        """删除作业 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.edit_delete_button(1)  # 删除按钮

            if self.wait_check_tips_page():
                print('---------删除作业---------')
                ThomePage().tips_title()
                ThomePage().tips_content()
                ThomePage().cancel_button()  # 取消按钮
                print('---------------')
                print('取消删除')
                # ThomePage().commit_button()  # 确定按钮
                # print('确定删除')
            else:
                print('★★★ Error- 无删除提示框')

    @teststeps
    def delete_commit_operation(self):
        """删除作业 具体操作"""
        self.more_button()  # 更多 按钮
        if self.wait_check_more_page():
            self.edit_delete_button(1)  # 删除按钮

            if self.wait_check_tips_page():
                print('---------删除作业---------')
                ThomePage().commit_button()  # 确定按钮
                print('确定删除')

    @teststeps
    def swipe_operation(self, swipe_num):
        """滑屏 获取所有题目内容"""
        ques_last_index = 0

        for i in range(swipe_num):
            if ques_last_index < swipe_num:
                ques_first_index = self.game.get_num()  # 当前页面中第一题 题号

                if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                    for step in range(0, 10):
                        SwipeFun().swipe_vertical(0.5, 0.5, 0.62)
                        if self.game.get_num() == ques_last_index + 1:  # 正好
                            break
                        elif self.game.get_num() < ques_last_index + 1:  # 下拉拉过了
                            SwipeFun().swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                            if self.game.get_num() == ques_last_index + 1:  # 正好
                                break

                last_one = self.game.get_last_element()  # 页面最后一个元素
                quesnum = self.game.single_question()  # 题目

                if self.game.question_judge(last_one):  # 判断最后一项是否为题目
                    for j in range(len(quesnum) - 1):
                        current_index = self.game.get_num(j)  # 当前页面中题号

                        if current_index > ques_last_index:
                            print('-----------------------------')
                            print(quesnum[j].text)
                            self.drop_down_operation(j)  # 选项内容及下拉按钮是否可点击
                            ques_last_index = self.game.get_num(j)  # 当前页面中 做过的最后一题 题号
                else:  # 判断最后一题是否为选项
                    for k in range(len(quesnum)):
                        if k < len(quesnum) - 1:  # 前面的题目照常点击
                            current_index = self.game.get_num(k)  # 当前页面中题号

                            if current_index > ques_last_index:
                                print('-----------------------------')
                                print(quesnum[k].text)
                                self.drop_down_operation(k)  # 选项内容及下拉按钮是否可点击

                                ques_last_index = self.game.get_num(k)  # 当前页面中 做过的最后一题 题号
                        elif k == len(quesnum) - 1:  # 最后一个题目上滑一部分再进行选择
                            SwipeFun().swipe_vertical(0.5, 0.8, 0.55)
                            quesnum = self.game.single_question()  # 题目
                            for z in range(len(quesnum)):
                                current_index = self.game.get_num(z)  # 当前页面中题号

                                if current_index > ques_last_index:
                                    print('-----------------------------')
                                    print(quesnum[z].text)
                                    self.drop_down_operation(z)  # 选项内容及下拉按钮是否可点击
                                    ques_last_index = self.game.get_num(z)  # 当前页面中 做过的最后一题 题号
                                    break

                if i != swipe_num - 1:
                    SwipeFun().swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
            else:
                break

    @teststeps
    def rm_bracket(self, var):
        """ 去掉括号及其中的内容"""
        st = []
        ret = []
        for x in var:
            if x == '(':
                st.append(x)
            elif x == ')':
                st.pop()
            else:
                if len(st) == 0:
                    ret.append(x)  # 没有'('
        return ''.join(ret)

    @teststeps
    def drop_down_operation(self, k):
        """下拉按钮"""
        options = self.game.option_button()  # 选项
        print('选项:', options[0][k])
        rate = re.sub("\D", "", options[2][k].split()[-1])  # 准确率

        if rate == '' and options[2][k].split()[-1] == '未作答':
            print('该题还没有学生完成')
        else:
            if int(rate) < 100:
                self.drop_down_button(options[1][k])
                if self.verify_drop_down_content():
                    content = self.drop_down_content()
                    self.click_block()

                    item = self.rm_bracket(content)  # 去掉括号及其中的内容
                    var = item.split('\n')  # 以'\n'分割字符串

                    for i in range(0, len(var) - 1, 2):  # len()-1是为了去掉最后一个换行符分割出的空元素
                        if var[i] not in options[0][k]:
                            print('★★★ Error -下拉菜单内容不是本题选项', options[0][k], var[i])
            elif int(rate) == 100:
                print('该题正确率100%')
            else:
                print('★★★ Error -该题正确率', rate)
