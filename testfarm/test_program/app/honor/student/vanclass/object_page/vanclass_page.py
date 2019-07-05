#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class VanclassPage(BasePage):
    """ 班级 页面"""

    @teststeps
    def wait_check_page(self, var=10):
        """以“班级列表页面 添加班级 按钮”为依据"""
        locator = (By.ID, "{}add".format(self.id_type()))
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_quit_vanclass(self, class_name):
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'{}')]".format(class_name))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def empty_tips(self):
        """暂时没有数据"""
        try:
            self.driver\
                .find_element_by_id(self.id_type() + "load_empty")
            return True
        except Exception:
            return False

    @teststeps
    def swp(self):
        self.screen_swipe_up(0.5, 0.8, 0.2, 1000)

    @teststep
    def vanclass_name(self):
        """班级名称"""
        item = self.driver \
            .find_elements_by_id("{}class_name".format(self.id_type()))
        return item

    @teststep
    def vanclass_no(self):
        """班号"""
        item = self.driver \
            .find_elements_by_id("{}class_no".format(self.id_type()))
        return item

    @teststep
    def st_count(self):
        """学生人数"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "count")
        return item

    @teststep
    def add_class_button(self):
        """以“添加班级 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + "add") \
            .click()

    # 申请入班
    @teststeps
    def wait_check_apply_page(self, var=20):
        """以“title: 添加班级”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'添加班级')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_no_class_page(self):
        locator = (By.ID, self.id_type() + "status_error_hint_view")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def all_element(self):
        """页面内所有class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        content = []
        for i in range(len(ele)):
            # print(ele[i].text)
            content.append(ele[i].text)
        # print('++++++++++++++++')
        return ele, content


    @teststep
    def apply_teacher_name(self):
        """老师名称"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_teacher_name").text
        return ele

    @teststep
    def apply_vanclass_no(self):
        """班号"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "tv_class_no").text
        return item

    @teststep
    def remark_name_modify(self):
        """备注名称 输入框"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "et_remark_name")
        return ele

    @teststep
    def apply_class_button(self):
        """以“申请入班 按钮”的id为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + "tv_apply") \
            .click()
        time.sleep(2)

    # 班级 详情页
    @teststeps
    def wait_check_vanclass_page(self, var):
        """以“title: 班级名称”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def teacher_name(self):
        """老师名称 title"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "tv_teacher_title") \
            .text
        return item

    @teststep
    def teacher_name_modify(self):
        """老师名称"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_teacher").text
        return ele

    @teststep
    def class_name(self):
        """班级名称 title"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "tv_class_name_title") \
            .text
        return item

    @teststep
    def class_name_modify(self):
        """班级名称 编辑"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_class_name").text
        return ele

    @teststep
    def school_name(self):
        """学校名称"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "tv_school_title") \
            .text
        return item

    @teststep
    def school_name_modify(self):
        """学校名称 编辑"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_school").text
        return ele

    @teststep
    def score_ranking(self):
        """积分排行榜"""
        self.driver \
            .find_element_by_id(self.id_type() + "rl_score_ranking") \
            .click()

    @teststep
    def star_ranking(self):
        """星星排行榜"""
        self.driver \
            .find_element_by_id(self.id_type() + "rl_star_ranking") \
            .click()

    @teststep
    def vanclass_hw(self):
        """本班作业"""
        self.driver \
            .find_element_by_id(self.id_type() + "rl_homework") \
            .click()

    @teststep
    def quit_vanclass(self):
        """退出班级 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "tv_quit_class") \
            .click()

    # 退出班级
    @teststeps
    def wait_check_quit_page(self):
        """以“title: 退出班级”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'退出班级')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def phone_name(self):
        """手机号"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_phone").text
        print(ele)

    @teststep
    def code_input(self):
        """验证码 输入框"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "code")
        return ele

    @teststep
    def get_code_button(self):
        """获取 验证码"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "count_time")
        return ele

    @teststep
    def sonic_code_judge(self):
        """语音验证码"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "tv_sonic_code")
            return True
        except:
            return False

    @teststep
    def sonic_code(self):
        """语音验证码"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_sonic_code").text
        print(ele)

    @teststep
    def quit_button(self):
        """退出班级 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "quit") \
            .click()
