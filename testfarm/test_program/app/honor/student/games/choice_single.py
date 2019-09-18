#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:47
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class SingleChoiceGame(PublicPage):
    @teststep
    def wait_check_single_choice_page(self):
        """单项选择页面检查点"""
        locator = (By.ID, "{}question".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def right_choice(self):
        """正确选项内容"""
        ele = self.driver.find_element_by_xpath('//*[@content-desc="right"]/following-sibling::android.widget.TextView')
        return ele.text