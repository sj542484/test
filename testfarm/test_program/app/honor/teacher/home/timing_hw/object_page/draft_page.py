#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import re
import sys
from selenium.webdriver.common.by import By

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.home.assign_hw_paper.object_page.release_hw_page import ReleasePage
from app.honor.teacher.home.vanclass.test_data.tips_data import TipsData
from app.honor.teacher.home.vanclass.test_data.vanclass_data import GetVariable
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.object_page.question_basket_page import TestBasketPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from conf.decorator_vue import teststep, teststeps
from conf.base_page import BasePage
from utils.assert_package import MyAssert, MyToast
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast
from utils.wait_element_vue import WaitElement


class DraftPage(BasePage):
    """定时作业+草稿箱 页面"""
    timing_tips = '★★★ Error- 未进入定时作业页面'
    timing_vue_tips = '★★★ Error- 未进入定时作业vue页面'
    timing_list_tips = '★★★ Error- 定时作业界面未加载成功'
    back_timing_tips = '★★★ Error- 未返回定时作业页面'

    draft_tips = '★★★ Error- 未进入草稿箱界面'
    draft_list_tips = '★★★ Error- 草稿界面未加载成功'
    back_draft_tips = '★★★ Error- 未返回草稿箱页面'
    van_choose_tips = '★★★ Error- 未进入班级选择界面'

    more_tips = '★★★ Error- 未进入更多按钮详情'
    edit_tips = '★★★ Error- 未进入编辑作业 详情页'
    edit_list_tips = '★★★ Error- 编辑作业 详情页未加载成功'

    def __init__(self):
        self.home = ThomePage()
        self.release = ReleasePage()
        self.detail = QuestionDetailPage()
        self.question = TestBankPage()
        self.basket = TestBasketPage()
        self.wait = WaitElement()
        self.my_assert = MyAssert()
        self.screen = self.get_window_size()

    @teststeps
    def wait_check_app_page(self, var=20):
        """以“title:定时作业”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="定时作业"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_page(self, var=20):
        """以“title:定时作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="定时作业"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_hw_list_page(self, var=20):
        """以“作业条目 元素”为依据"""
        locator = (By.XPATH, '//div[@class="time-content-list van-list"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_empty_tips_page(self, var=3):
        """暂时没有数据"""
        locator = (By.XPATH, '//div[@class="vt-loading-container__error"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def end_hint(self):
        """没有更多了"""
        locator = (By.XPATH, '//div[@class="van-list__finished-text"]')
        ele = self.wait.wait_find_element(locator).text
        print(ele)
        return ele

    @teststep
    def timing_name(self):
        """定时作业名称"""
        locator = (By.XPATH, '//div[@class="time-content-list-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def timing_time(self):
        """草稿创建时间"""
        locator = (By.XPATH, '//div[@class="time-content-list-label__send"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def more_button(self):
        """更多 按钮"""
        locator = (By.XPATH, '//i[@class="time-content-list-label__icon van-icon van-icon-ellipsis"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait\
            .wait_find_element(locator).click()

    # 更多 按钮
    @teststeps
    def wait_check_more_page(self):
        """以“更多按钮  条目元素”为依据"""
        locator = (By.XPATH, '//div[@class="van-popup van-popup--round van-popup--bottom van-action-sheet"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def more_edit_button(self):
        """编辑 按钮"""
        locator = (By.XPATH, '//span[text()="发布/编辑作业"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def more_delete_button(self):
        """删除 按钮"""
        locator = (By.XPATH, '//span[text()="删除"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def more_cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//div[@class="van-action-sheet__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def wait_check_tips_page(self, var=15):
        """以“title:删除作业”为依据"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        return self.wait.wait_check_element(locator, var)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.XPATH, '//div[@class="van-dialog__header"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def delete_tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.XPATH, '//div[@class="van-dialog__message van-dialog__message--has-title"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__cancel"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        locator = (By.XPATH, '//button[@class="van-button van-button--default van-button--large van-dialog__confirm van-hairline--left"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def all_vanclass(self):
        """全部班级 """
        locator = (By.XPATH, '//span[@class="van-dropdown-menu__title"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststep
    def all_time(self):
        """全部 """
        locator = (By.XPATH, '//span[@class="van-dropdown-menu__title"]')
        self.wait \
            .wait_find_elements(locator)[-1].click()

    # 下拉菜单
    @teststeps
    def wait_check_tab_page(self, var=20):
        """以“全部班级/全部 元素”为依据"""
        locator = (By.XPATH, '//div[@class="van-dropdown-item van-dropdown-item--down"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def van_check_text(self):
        """全部班级 菜单条目"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]/span')
        ele = self.wait.wait_find_elements(locator)  # 班级
        content = [i for i in ele if i.text != '']
        return ele

    @teststep
    def date_check_text(self):
        """全部 菜单条目"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]/span')
        ele = self.wait.wait_find_elements(locator)  # 日期
        content = [i for i in ele if i.text != '']
        return content

    @teststep
    def draft_box_button(self):
        """以“草稿箱 按钮”的id为依据"""
        locator = (By.XPATH, '//span[@class="nav-right" and text()= "草稿箱"]')
        self.wait \
            .wait_find_element(locator).click()

    # 草稿箱
    @teststeps
    def wait_check_draft_app_page(self, var=20):
        """以“title:草稿箱”为依据"""
        locator = (By.XPATH, '//android.view.View[@text="草稿箱"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_draft_page(self, var=10):
        """以“title:草稿箱”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="草稿箱"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_draft_list_page(self):
        """以“草稿list 名称”为依据"""
        locator = (By.XPATH, '//div[@id="time-content-list-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def draft_name(self):
        """草稿名称"""
        locator = (By.XPATH, '//div[@class="time-content-list-title"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def draft_time(self):
        """草稿创建时间"""
        locator = (By.XPATH, '//div[@class="time-content-list-label__send"]')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def swipe_vertical_web(self, ratio_x, start_y, end_y, steps=1000):
        """
        上/下滑动 x值不变
        :param ratio_x: x坐标系数
        :param start_y: 滑动起点y坐标系数
        :param end_y: 滑动终点y坐标系数
        :param steps: 持续时间ms
        :return: None
        """
        x = int(self.screen[0] * ratio_x)
        y1 = int(self.screen[1] * start_y)
        y2 = int(self.screen[1] * end_y)

        self.driver.swipe(x, y1, x, y2, steps)

    @teststeps
    def get_hw_list(self, name, date_list, content=None):
        """获取定时作业列表
        :param content:
        :param name: 定时作业名
        :param date_list:发布日期
        """
        if content is None:
            content = []

        hw = self.timing_name()  # 作业条目
        create = self.timing_time()  # 创建日期
        if len(hw) > 5 and not content:  # 多于5个
            self.hw_list(name, date_list, hw, create, len(hw)-1)
            content = [hw[-2].text, create[-2].text]

            self.swipe_vertical_web(0.5, 0.9, 0.2)
            if self.wait_check_hw_list_page():
                self.get_hw_list(name, date_list, content)
        else:
            index = 0
            if content:
                for k in range(len(hw)-1, 0, -1):  # 滑屏后 页面中是否有已操作过的元素
                    if hw[k].text == content[0] and create[k].text == content[1]:
                        index = k + 1
                        break
            self.hw_list(name, date_list, hw, create, len(hw), index)

    @teststeps
    def hw_list(self, name, date_list, hw, create, length, index=0):
        """定时作业列表
        :param hw: 作业名称
        :param create: 创建时间
        :param name: 作业名列表
        :param date_list: 发布时间列表
        :param length: 遍历最大值
        :param index: 遍历最小值
        """
        for i in range(index, length):
            print(hw[i].text, '\n',
                  create[i].text)
            print('----------------------')

            hw_name = hw[i].text
            name.append(re.sub(r'\(.*?\)', '', hw_name[4:]))  # name

            hw_create = create[i].text
            item = hw_create[6:].split()  # 发布时间
            var1 = item[0].split('/')
            var = item[2].split(':')
            content = [var1[0], var1[1], var[0], var[1]]

            date_list.append(content)

    @teststeps
    def add_to_basket(self):
        """加题进题筐"""
        print('=========加题进题筐=========')
        item = self.question.question_name()  # 获取
        item[0][1].click()  # 点击第一道题

        try:
            # print('----------题单详情页----------')
            self.detail.all_check_button()  # 全选按钮
            self.detail.put_to_basket_button()  # 点击加入题筐按钮
            # print('加题进题筐')
            self.home.back_up_button()  # 返回按钮

            self.question.question_basket()  # 题筐按钮
            if self.basket.wait_check_page():  # 页面检查点
                if self.basket.wait_check_list_page():
                    if self.question_bank_operation():
                        return True
                    else:
                        raise Exception('★★★ Error- 未进入发布作业页面')
                elif self.home.wait_check_empty_tips_page():  # 如果存在空白页元素
                    self.home.back_up_button()
                    self.home.click_tab_hw()  # 返回 主界面
                    raise Exception('★★★ Error- 加入题筐失败')
        except:
            raise Exception('★★★ Error- 未进入 题单详情页')

    @teststeps
    def question_bank_operation(self):
        """获取题筐所有题 并选择布置"""
        var = self.basket.question_name()[1]  # 所有题
        if len(var) > 1:
            for i in range(2):
                check = self.basket.check_button()  # 单选按钮
                check[i].click()
        elif len(var) == 1:
            self.basket.check_button()[0].click()
        else:
            print('题筐无题')
            return False

        self.basket.assign_button().click()  # 点击 布置作业 按钮
        self.home.tips_content_commit()  # 提示 页面

        if self.release.wait_check_release_page():  # 页面检查点
            if self.release.wait_check_release_list_page():
                return True
        else:
            self.home.back_up_button()
            return False

    @teststeps
    def time_types_exchange(self, time_text):
        """时间格式转换"""
        var = time_text[:-6].split('月')
        month = re.sub('\D', '', var[0])
        day = re.sub('\D', '', var[1])
        min_second = time_text[-5:].split(':')

        dates = [month, day, min_second[0], min_second[1]]
        return dates

    @teststeps
    def judge_time_setting(self, date):
        """验证 设定的时间"""
        print('------------------验证 设定的时间-------------------')
        timing = self.release.timing_show()  # 展示的时间
        dates_list = []
        for z in range(len(timing)):
            dates_list.append(self.time_types_exchange(timing[z].text))

        if len(dates_list) != len(date):
            print('★★★ Error- 展示的时间 个数与设定的不一致', dates_list, date)
        else:
            count = 0
            for i in range(len(dates_list)):  # 多个日期
                var = 0
                for j in range(len(dates_list[i])):  # 一个日期
                    if dates_list[i][j] != date[i][j]:
                        break  # 到下一个date
                    else:
                        var += 1

                if (var % 4 != 0) and (var != 0):
                    print('★★★ Error- 展示的时间与设定的不一致', dates_list[i], date[i])
                else:
                    count += var

            if count == len(date) * 4:
                print('保存定时作业成功\n'
                      '===========================================================================')
                return True
            else:
                print('★★★ Error -保存定时作业失败\n'
                      '===========================================================================')
                return False

    @teststeps
    def timing_operation(self):
        """布置定时作业 具体操作"""
        self.func_name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名
        self.my_assert.assertTrue_new(self.release.wait_check_release_page(), self.release.release_tips)  # 页面检查点
        self.my_assert.assertTrue_new(self.release.wait_check_release_list_page(), '★★★ Error- 编辑定时作业 详情页未加载成功')
        print('------------------布置定时作业------------------')
        name = self.release.hw_name_edit()  # 作业名称 编辑框
        hw = '练习作业_定时' + str(random.randint(1000, 9999))  # test001
        name.send_keys(hw)  # name
        print(name.text)

        self.my_assert.assertTrue_new(self.release.wait_check_release_list_page(), '★★★ Error- 编辑定时作业 详情页未加载成功')
        self.swipe_vertical_web(0.5, 0.9, 0.2)
        self.my_assert.assertTrue_new(self.release.wait_check_release_list_page(), '★★★ Error- 编辑定时作业 详情页未加载成功')

        button = self.release.choose_button()  # 单选框
        van = self.release.van_name()  # 班级 元素
        for k in range(len(button)):
            if all([GetAttribute().selected(button[k]) == 'false',
                    van[k].text != GetVariable().VANCLASS]):
                print('所选择的班级:', van[k].text)
                button[k].click()  # 选择 一个班
                break

        self.my_assert.assertTrue_new(self.release.wait_check_release_list_page(), '★★★ Error- 编辑定时作业 详情页未加载成功')
        self.release.add_time_button()  # 设定时间 元素
        if self.release.wait_check_time_list_page():
            date = self.release.get_assign_date()  # 设定时间
            print('设置发布时间为：', date)
            self.release.confirm_button()  # 点击 确定按钮

            self.my_assert.assertTrue_new(self.release.wait_check_release_list_page(), '★★★ Error- 编辑定时作业 详情页未加载成功')
            self.release.assign_button()  # 点击 发布作业 按钮
            if Toast().find_toast(TipsData().timing_success):  # 布置成功提示验证
                print('★★★ Error- 未弹toast: ', TipsData().timing_success)
            else:
                self.release.assign_button()  # 点击 发布作业 按钮
                MyToast().toast_assert(self.func_name, Toast().toast_operation(TipsData().hw_only_daily)) # 若当天布置的作业有重名，获取toast
                self.home.back_up_button()

    @teststeps
    def timing_hw_delete(self):
        """删除定时作业"""
        self.my_assert.assertTrue_new(self.wait_check_page(), self.back_timing_tips)  # 页面检查点
        if self.wait_check_empty_tips_page():
            print('暂无 定时作业')
            self.back_up_button()  # 返回主界面
            self.my_assert.assertTrue_new(self.wait_check_hw_list_page, self.timing_tips)
        else:
            self.my_assert.assertTrue_new(self.wait_check_hw_list_page, self.timing_tips)
            content = {}  # name:班级名

            name = self.draft_name()
            timestr = self.draft_time()
            # if len(name) > 2:  # 删除两个
            #     content[name[0].text] = timestr[0].text
            # self.delete_commit_operation()  # 删除作业

            self.my_assert.assertTrue_new(self.wait_check_hw_list_page, self.timing_tips)
            content[name[0].text] = timestr[0].text
            self.delete_commit_operation()  # 删除作业

            return content

    @teststeps
    def delete_cancel_operation(self, index=0):
        """删除作业 具体操作"""
        self.more_button()[index].click()  # 更多 按钮
        self.my_assert.assertTrue_new(self.wait_check_more_page(), self.more_tips)
        self.more_delete_button()  # 删除按钮

        self.my_assert.assertTrue_new(self.wait_check_tips_page(), '★★★ Error- 无删除提示框')
        print('---------删除作业---------')
        self.tips_title()
        self.delete_tips_content()
        self.cancel_button()  # 取消按钮
        print('---------------')

        if not self.wait_check_tips_page():
            print('取消删除')

    @teststeps
    def delete_commit_operation(self, index=0):
        """删除作业 具体操作"""
        self.func_name = self.__class__.__name__ + '_' + sys._getframe().f_code.co_name  # 文件名 + 类名

        self.more_button()[index].click()  # 更多 按钮
        self.my_assert.assertEqual(self.wait_check_more_page(), True, self.more_tips)
        self.more_delete_button()  # 删除按钮

        self.my_assert.assertTrue(self.wait_check_tips_page(), '★★★ Error- 无删除提示框')
        print('---------删除作业---------')
        self.commit_button()  # 确定按钮
        print('确定删除')
        MyToast().toast_assert(self.func_name, Toast().toast_vue_operation(TipsData().delete_success))  # 获取toast

    @teststeps
    def tips_content_commit(self, var=5):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page(var):  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.commit_button().click()  # 确定按钮
            print('--------------------------')
