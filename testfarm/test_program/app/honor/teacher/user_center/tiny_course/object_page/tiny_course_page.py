#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_bank_page import QuestionBankPage
from testfarm.test_program.app.honor.teacher.user_center.mine_collection.object_page.mine_question_bank_page import \
    MineQuestionBankPage
from testfarm.test_program.app.honor.teacher.user_center.user_information.object_page.user_center_page import TuserCenterPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.base_config import GetVariable as gv
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.wait_element import WaitElement


class TinyCoursePage(BasePage):
    """微课页面"""
    course_value = gv.PACKAGE_ID + 'name'  # 微课名称
    play_value = gv.PACKAGE_ID + 'play'  # 添加视频后，微课主页面 视频播放 按钮

    menu_value = gv.PACKAGE_ID + "md_title"  # 菜单条目

    exo_pause_value = gv.PACKAGE_ID + 'exo_pause'  # 视频播放页面 暂停 按钮
    exo_play_value = gv.PACKAGE_ID + 'exo_play'  # 视频播放页面 播放 按钮
    exo_rotate_value = gv.PACKAGE_ID + 'rotate'  # 视频播放页面 横竖屏切换 按钮

    def __init__(self):
        self.wait = WaitElement()
        self.user = TuserCenterPage()
        self.mine = MineQuestionBankPage()
        self.question = QuestionBankPage()

    @teststeps
    def wait_check_page(self):
        """以“title:创建微课”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'创建微课')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“微课名称”的id为依据"""
        locator = (By.ID, self.course_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def course_name(self):
        """以“微课名称”的id为依据"""
        ele = self.driver \
            .find_element_by_id(self.course_value)
        return ele

    @teststep
    def create_tiny_course(self):
        """以“+ 微课内容”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'create_tiny_course') \
            .click()

    @teststep
    def delete_tiny_course_button(self):
        """以“删除按钮”的id为依据"""
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'delete') \
            .click()

    @teststep
    def save_button(self):
        """以“保存 按钮”的id为依据"""
        self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "save")\
            .click()

    # 创建页面
    @teststeps
    def wait_check_menu_page(self):
        """以“md_title”的id为依据"""
        locator = (By.ID, self.menu_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def menu_item(self):
        """以“拍摄视频/本地视频”的id为依据"""
        ele = self.driver\
            .find_elements_by_id(self.menu_value)
        return ele

    # 选择视频后
    @teststeps
    def play_button(self):
        """播放按钮"""
        print('点击 播放按钮')
        self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "play") \
            .click()

    @teststeps
    def wait_check_play_page(self):
        """以“横竖屏切换”的id为依据"""
        locator = (By.ID, self.exo_rotate_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def back_up_button(self):
        """返回 按钮"""
        self.driver \
            .find_element_by_class_name('android.widget.ImageButton').click()

    @teststeps
    def screen_switch_button(self):
        """横竖屏切换 按钮"""
        self.driver \
            .find_element_by_id(self.exo_rotate_value).click()

    @teststeps
    def exo_play_button(self):
        """播放键"""
        print('点击播放按钮')
        self.driver \
            .find_element_by_id(self.exo_play_value).click()

    @teststeps
    def exo_pause_button(self):
        """暂停键"""
        self.driver\
            .find_element_by_id(self.exo_pause_value).click()

    @teststeps
    def exo_position(self):
        """播放到的位置"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + 'exo_position').text
        return ele

    @teststeps
    def exo_progress(self):
        """进度条 description == exo_position的text值"""
        ele = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + 'exo_progress')
        return ele

    @teststeps
    def exo_duration(self):
        """视频时长"""
        ele = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + 'exo_duration').text
        return ele

    @teststeps
    def video_duration_deal(self, duration):
        """视频时长处理"""
        value = duration.split(':')
        return 10*int(value[0])+int(value[1])

    @teststeps
    def judge_delete(self):
        """以“删除按钮删除后页面”的id为依据"""
        locator = (By.ID, self.play_value)
        return self.wait.judge_is_exists(locator)

    @teststeps
    def edit_course_name(self, name):
        """编辑课程名称 操作"""
        if self.wait_check_list_page():
            var = self.course_name()  # 微课名称
            var.send_keys(name)
            print('输入微课名称：', var.text)
            self.save_button()  # 点击保存按钮

    @teststeps
    def judge_save_result(self, var):
        """
        验证视频保存结果
        :param var: 视频名称
        """
        if self.user.wait_check_page():
            nick = self.user.nickname()  # 昵称

            print('--------------验证视频拍摄保存结果-------------')
            self.user.click_mine_bank()  # 我的题库
            if self.mine.wait_check_page():
                if self.mine.wait_check_list_page():
                    name = self.question.question_name()  # 名称
                    type = self.question.question_type()  # 类型
                    author = self.question.question_author()  # 创建人
                    print(name[0], type[0], author[0])
                    if type[0] != '微课':
                        print('★★★ Error - 视频保存失败，我的题库题型有误', type[0])
                    else:
                        if name[0] != var:
                            print('★★★ Error - 视频保存失败，我的题库视频名称有误', name[0], var)
                        else:
                            if author[0] != nick:
                                print('★★★ Error - 视频保存失败，我的题库视频作者有误', author[0], nick)
                            else:
                                print('视频拍摄保存成功')

                    ThomePage().back_up_button()  # 返回个人中心页面
