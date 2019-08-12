#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:49
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class SelectBlankGame(PublicPage):
    """选词填空"""
    @teststep
    def wait_check_select_blank_page(self):
        """选词填空页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    def wait_check_hint_btn_page(self):
        """检测是否存在提示按钮"""
        locator = (By.ID, '{}prompt'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_hint_content_page(self):
        """提示词页面检查点"""
        locator = (By.ID, '{}md_titleFrame'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def hint_answer(self):
        """提示答案"""
        ele = self.driver.find_element_by_xpath('//*[@resource-id="{}md_customViewFrame"]/'
                                                'android.widget.ScrollView/android.widget.TextView'
                                                .format(self.id_type()))
        return ele.text

    @teststep
    def hint_btn(self):
        """提示词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'prompt')
        return ele

