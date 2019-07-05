from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from testfarm.test_program.app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from testfarm.test_program.app.honor.student.word_book.object_page.sql_data.data_action import DataActionPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.utils.toast_find import Toast
from testfarm.test_program.conf.base_config import GetVariable as gv


class CleanDataPage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.common = DataActionPage()
        self.user_center = UserCenterPage()
        self.user_info = UserInfoPage()

    @teststep
    def wait_check_set_up_page(self):
        """以“设置” text 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_cache_page(self):
        """以“设置” text 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'清除缓存')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def wait_check_grade_page(self):
        """以“请选择你所处的年级” text为依据"""
        locator =(By.XPATH, "//android.widget.TextView[contains(@text,'请选择你所处年级')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def select_setting_up(self):
        """点击设置"""
        self.driver.\
            find_element_by_xpath("//android.widget.TextView[contains(@text,'设置')]")\
            .click()

    @teststep
    def select_clear_cache(self):
        """清除缓存"""
        self.driver. \
            find_element_by_xpath("//android.widget.TextView[contains(@text,'清除缓存')]") \
            .click()

    @teststep
    def grade_btn(self):
        """点击年级"""
        self.driver. \
            find_element_by_xpath("//android.widget.TextView[contains(@text,'年级')]") \
            .click()

    @teststep
    def grade_options(self):
        """年级选项"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_grade')
        return ele

    @teststep
    def select_another_grade(self):
        """选择倒数第一个年级（只要此次年级和指定年级不一样都可以）"""
        grades = self.grade_options()
        grades[-1].click()

    @teststep
    def select_certain_grade(self):
        """选择指定年级 """
        xpath_ele = "//android.widget.TextView[contains(@text,'{}')]".format(gv.GRADE)
        self.driver. \
            find_element_by_xpath(xpath_ele).click()

    @teststep
    def reset_grade(self):
        """重新选择年级"""
        self.clean_cache()  # 清除缓存
        self.grade_btn()   # 年级按钮
        if self.wait_check_grade_page():
            self.select_another_grade()  # 选择最后一个年级
            if self.user_center.wait_check_page():
                self.grade_btn()
                if self.wait_check_grade_page():
                    self.select_certain_grade()  # 重新选择三年级
        if self.user_center.wait_check_page():
            self.home.click_tab_hw()

    @teststep
    def clean_cache(self):
        """清除缓存"""
        if self.wait_check_set_up_page():
            self.select_setting_up()    # 设置按钮
            if self.wait_check_clear_cache_page():
                self.select_clear_cache()  # 清空缓存
                Toast().find_toast("清除缓存成功")
            self.home.click_back_up_button()
            if self.user_center.wait_check_page():
                pass

    @teststep
    def clean_cache_back_to_home(self):
        self.home.click_tab_profile()
        self.clean_cache()
        self.home.click_tab_hw()
        if self.home.wait_check_home_page():
            pass

    @teststep
    def clear_user_all_data(self):
        """清除数据库所有相关数据"""
        if self.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            self.common.get_student_id()  # 获取用户id
            self.common.delete_all_word()    # 删除所有单词
            self.common.delete_all_record()  # 删除去重记录
            self.common.delete_all_fluency_flag()  # 删除标星标熟记录
            self.common.change_play_times(0)  # 更改练习组数
            self.common.change_today_new_count(0)  # 更改今日新词个数
            self.common.change_today_word_count(0)  # 更改今日已练词数
            self.common.delete_all_star()   # 删除所有星星
            self.common.delete_all_score()  # 删除所有分数
            self.home.click_back_up_button()
            if self.user_center.wait_check_page():
                self.reset_grade()  # 重置年级







