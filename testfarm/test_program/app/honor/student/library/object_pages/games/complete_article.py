# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/10 9:35
# -------------------------------------------
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.games.select_word_blank import SelectWordBlank
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class CompleteArticle(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_complete_article_page(self):
        """补全文章页面检查点"""
        locator = (By.ID, '{}ss_view'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def drag_btn(self):
        """拖拽按钮"""
        ele = self.driver.find_element_by_id('{}dragger'.format(self.id_type()))
        return ele

    @teststep
    def article(self):
        """文章"""
        ele = self.driver.find_element_by_id('{}ss_view'.format(self.id_type()))
        return ele

    @teststep
    def opt_char(self):
        """选项 字母 ABCD"""
        ele = self.driver.find_elements_by_id('{}tv_char'.format(self.id_type()))
        return ele

    @teststep
    def opt_text(self):
        """选项 文本"""
        ele = self.driver.find_elements_by_id('{}tv_item'.format(self.id_type()))
        return ele

    @teststep
    def result_opt_char(self, opt_text):
        """结果页的选项"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/preceding-sibling::android.widget.TextView'
                                                .format(opt_text))

        return ele

    @teststeps
    def complete_article_operate(self, fq, sec_answer, half_exit):
        """补全文章游戏过程"""
        timer = []
        mine_answers = {}
        if self.wait_check_complete_article_page():
            total_num = self.common.rest_bank_num()
            article = self.article()
            print(article.text)
            SelectWordBlank().check_position_change(article)

            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
            self.common.judge_next_is_true_false('false')  # 下一步按钮状态校验

            index = 0
            if fq == 1:
                for i in range(0, total_num):
                    self.common.rate_judge(total_num, i)
                    self.opt_char()[i].click()
                    mine_answers[i] = self.opt_text()[i].text
                    timer.append(self.common.bank_time())
            else:
                while True:
                    if self.common.rest_bank_num() == 0:
                        break
                    for i, opt in enumerate(self.opt_text()):
                        if opt.text == sec_answer[index]:
                            self.opt_char()[i].click()
                            break
                    index += 1
                    timer.append(self.common.bank_time())

            if half_exit:
                self.click_back_up_button()
                return

            self.common.judge_next_is_true_false('true')  # 下一步按钮状态校验
            self.common.judge_timer(timer)
            self.common.next_btn().click()

            answer = mine_answers if fq == 1 else sec_answer
            print('我的答案：', answer)
            return answer, total_num

    @teststeps
    def complete_article_result_operate(self, mine_answer):
        right_answer = {}
        right, wrong = [], []
        index = 0
        if ResultPage().wait_check_answer_page():
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
            desc = self.article().get_attribute('contentDescription')
            right_ans = re.findall(r'\[(.*?)\]', desc)[0].split(', ')

            for i, ans in enumerate(right_ans):
                right_error_desc = self.result_opt_char(ans).get_attribute('contentDescription')
                print('我的答案：', mine_answer[i])
                print('正确答案', ans)
                if mine_answer[i] != ans:
                    if right_error_desc == 'right':
                        print('★★★ 选择结果不正确，页面却显示正确')
                    elif right_error_desc == 'error':
                        print('选项校验正确')
                    right_answer[index] = ans
                    wrong.append(ans)
                    index += 1
                else:
                    if right_error_desc == 'error':
                        print('★★★ 选择结果正确，页面却显示不正确')
                    elif right_error_desc == 'right':
                        print('选项校验正确')
                    right.append(ans)
                print('\n')

        self.click_back_up_button()
        print('错题答案：', right_answer)
        return wrong, right, right_answer








