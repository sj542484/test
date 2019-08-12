#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:48
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.games.game_public_element import PublicPage
from testfarm.test_program.conf.decorator import teststep


class CompleteArticleGame(PublicPage):
    @teststep
    def wait_check_complete_article_page(self):
        """补全文章页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False
