#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.user_center import ChangeImage
from conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class PaperDetailPage(BasePage):
    """试卷 详情页面"""

    def __init__(self):
        self.wait = WaitElement()
        self.change_image = ChangeImage()

    @teststeps
    def wait_check_page(self):
        """以“title:布置试卷”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'布置试卷')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def recommend_button(self):
        """推荐到学校 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "recommend") \
            .click()
        time.sleep(2)

    @teststeps
    def collect_button(self):
        """收藏/取消收藏 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "collect") \
            .click()
        time.sleep(1)

    @teststep
    def share_button(self):
        """分享 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "share") \
            .click()

    @teststep
    def paper_type(self):
        """试卷"""
        if self.driver.find_element_by_id(gv.PACKAGE_ID + "tv_paper"):
            return True
        else:
            return False

    @teststeps
    def paper_title(self):
        """title"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_paper_name") \
            .text
        print('试卷名称:', item)
        return item

    @teststeps
    def teacher(self):
        """作者"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_author") \
            .text
        print(item)

    # 测评模式 - 百分制/AB制
    @teststeps
    def score_type(self):
        """测评模式 - 百分制/AB制"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'模式')]") \
            .text
        return item

    @teststeps
    def score(self):
        """百分制"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_score") \
            .text
        return item

    @teststeps
    def score_unit(self):
        """百分制 单位"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "score") \
            .text
        return item

    # 考试时间
    @teststep
    def time_title(self):
        """测评模式 - 百分制/AB制"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'考试时间')]") \
            .text
        return item

    @teststep
    def time_unit(self):
        """考试时间 单位"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'分钟')]") \
            .text
        return item

    @teststep
    def time_str(self):
        """时间"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_time") \
            .text
        return item

    # 小题数
    @teststep
    def num_title(self):
        """小题数"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'小题数')]") \
            .text
        return item

    @teststep
    def num_unit(self):
        """小题数 单位"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'题')]") \
            .text
        return item

    @teststep
    def game_num(self):
        """小题数"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_exercise_num") \
            .text
        return item

    # 限制交卷
    @teststep
    def limit_type(self):
        """限制交卷"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'限制交卷')]") \
            .text
        return item

    @teststeps
    def limit_judge(self):
        """限制交卷: 限制"""
        locator = (By.ID, gv.PACKAGE_ID + "tv_limit_m")
        return self.wait.judge_is_exists(locator)

    @teststep
    def limit_hand(self):
        """限制交卷"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_limit") \
            .text
        return item

    @teststeps
    def limit_unit(self):
        """不限制交卷"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_limit_m") \
            .text
        return item

    # 题型
    @teststep
    def game_list_tile(self):
        """题型"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'题型')]") \
            .text
        return item

    @teststep
    def question_name(self):
        """小游戏名"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_name")
        return item

    @teststep
    def num(self, index):
        """每个小游戏 题数"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_desc")[index]
        return item

    @teststep
    def arrow(self, index):
        """箭头"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_arrow")[index]
        return item

    @teststep
    def assign_button(self):
        """布置试卷 按钮"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tv_assign") \
            .click()

    @teststep
    def sentence(self):
        """句子"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_answer")
        return item

    # 布置试卷 页面
    @teststeps
    def wait_check_assign_list_page(self):
        """以“title:”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选择班级')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def assign_title(self):
        """选择班级"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'选择班级')]")
        print(item.text)

    @teststep
    def assign_hint(self):
        """点击选择班级，暂无学生班级已经从列表中隐藏"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'点击选择班级，暂无学生班级已经从列表中隐藏')]")
        print(item.text)

    @teststeps
    def paper_detail_operation(self):
        """试卷 详情页"""
        if not self.paper_type():
            print('★★★ Error- 试卷详情页的试卷类型')
        var = self.paper_title()  # 返回值
        print('---------------------试卷详情页---------------------')

        if self.score() in ('100', '120'):
            title = self.score_type()
            score = self.score()  # 分值
            unit = self.score_unit()
            print(title, score, unit)
        else:  # A/B制
            print()

        # 考试时间
        title = self.time_title()
        timestr = self.time_str()
        unit = self.time_unit()
        print(title, timestr, unit)

        # 小题数
        title = self.num_title()
        num = self.game_num()
        unit = self.num_unit()
        print(title, num, unit)

        if self.limit_judge():  # 限制
            print(self.limit_type(), self.limit_hand(), self.limit_unit())
        else:
            print(self.limit_type(), self.limit_hand())

        print('----------------')
        self.game_list_tile()
        name = self.question_name()  # 小游戏名
        for i in range(len(name)):
            num = self.num(i)  # 每个小游戏 题数
            print(name[i].text, num.text)
        print('------------------------------------------')
        return var

    @teststeps
    def tips_page_info(self):
        """温馨提示 页面信息"""
        print('------------------------------------------', '\n',
              '温馨提示 页面:')

        if ThomePage().wait_check_tips_page():
            ThomePage().tips_title()
            ThomePage().tips_content()
            ThomePage().never_notify()  # 不再提醒
            ThomePage().cancel_button()  # 取消按钮

            self.assign_button()  # 布置试卷 按钮
            if ThomePage().wait_check_tips_page():
                ThomePage().commit_button()
        else:
            print('★★★ Error- 无icon')
