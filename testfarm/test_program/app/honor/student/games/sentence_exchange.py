#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:46
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.game_public_element import PublicPage
from conf.decorator import teststep


class SentenceExchangeGame(PublicPage):

    @teststep
    def wait_check_exchange_sentence_page(self):
        """句型转换页面检查点，以输入答案的id作为依据"""
        locator = (By.ID, self.id_type() + "rv_answer")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def text_bottom(self):
        """下方后补选择文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv_hint')
        return ele.find_elements_by_xpath('.//android.widget.TextView')

    @teststep
    def input_text(self):
        """需要填空的文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv_answer')
        return ele.find_elements_by_xpath('.//android.widget.TextView')

    @teststep
    def sentence_question(self):
        """问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_question')
        return ele

    @teststep
    def sentence_answer(self):
        """提交后的答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return ele.text

    @teststep
    def finish_answer_list(self):
        """已完成的句子"""
        ele = self.driver.find_elements_by_xpath('//android.support.v7.widget.RecyclerView/following-sibling::'
                                                 'android.widget.LinearLayout/android.widget.TextView')
        answer_array = [x.text for x in ele]
        return answer_array