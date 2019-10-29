# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/2 8:28
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.library_sql import LibrarySql
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.word_book.object_page.wordbook_sql import WordBookSql
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep


class UserCenterPage(BasePage):
    @teststep
    def wait_check_user_center_page(self):
        """以“设置”业务的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学校')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_buy_page(self):
        """购买页面检查点"""
        locator = (By.ID, self.id_type() + "goToCustomerService")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_logout_page(self):
        """退出登录页面检查点"""
        locator = (By.ID, self.id_type() + "logout")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def nickname(self):
        """昵称"""
        ele = self.driver.find_element_by_id(self.id_type() + 'name')
        return ele.text

    @teststep
    def school_name(self):
        """学校名称"""
        ele = self.driver.find_element_by_id(self.id_type() + 'school_name')
        return ele.text

    @teststep
    def purchase(self):
        """购买"""
        ele = self.driver.find_element_by_id(self.id_type() + 'study_card')
        print('点击 购买')
        return ele

    @teststep
    def phone(self):
        """学生的手机号"""
        ele = self.driver.find_element_by_id(self.id_type() + 'phone')
        return ele.text

    @teststep
    def setting_up(self):
        """设置"""
        ele = self.driver.find_element_by_id(self.id_type() + 'setting')
        return ele

    @teststep
    def clear_cache(self):
        """清除缓存"""
        ele = self.driver.find_element_by_id(self.id_type() + 'clear_cache')
        return ele


    @teststep
    def get_user_info(self):
        """:return 学生id、学校名称、学校id、昵称"""
        HomePage().click_tab_profile()                         # 点击个人中心
        if self.wait_check_user_center_page():                 # 个人中心页面检查点
            self.screen_swipe_up(0.5, 0.2, 0.8, 1000)
            nickname = self.nickname()  # 昵称
            self.screen_swipe_up(0.5, 0.8, 0.2, 1000)
            self.purchase().click()                            # 点击购买
            if self.wait_check_buy_page():                     # 购买页面检查点
                phone = self.phone()                           # 手机号
                stu_id = WordBookSql().find_student_id(phone)[0][0]   # 根据手机号获取学生ID
                self.click_back_up_button()
                if self.wait_check_user_center_page():
                    school_name = self.school_name()           # 学习名称
                    school_id = 0
                    if school_name:
                        id1 = LibrarySql().find_school_id(school_name)
                        id2 = LibrarySql().find_school_id_by_short_name(school_name)
                        if id1:
                            school_id = id1[0][0]
                        else:
                            school_id = id2[0][0]

                    self.setting_up().click()
                    if self.wait_check_logout_page():          # 清除缓存
                        self.clear_cache().click()
                        time.sleep(2)

                    self.click_back_up_button()                # 返回个人中心
                    if self.wait_check_user_center_page():
                        HomePage().click_tab_hw()             # 点击学习返回主页面

                    print('学生昵称：', nickname, '\n',
                          '学校名称：', school_name, '\n',
                          '学校id：', school_id, '\n',
                          '学生id：', stu_id, '\n'
                          )
                    return stu_id, school_name, school_id, nickname

