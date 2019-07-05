# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/10 15:53
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.cloze import Cloze
from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class ReadUnderstand(BasePage):

    def __init__(self):
        self.common = CommonPage()
        self.cloze = Cloze()

    @teststep
    def wait_check_ss_content_page(self):
        locator = (By.ID, self.id_type() + "ss_view")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def article(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() +'ss_view')
        return ele

    @teststep
    def check_position_change(self, content):
        if GetAttribute().checked(self.common.font_large()) == 'false':  # 查看页面是否默认选择第二个Aa
            print('★★★ 页面未默认选择中等字体')

        large_hg = self.article().size['height']
        print('large',self.article().size)

        self.common.font_middle().click()
        time.sleep(1)
        middle_hg = self.article().size['height']
        print('middle', self.article().size)

        self.common.font_great().click()
        time.sleep(1)
        great_hg = self.article().size['height']
        print('great', self.article().size)

        print(middle_hg, large_hg, great_hg)
        if not large_hg > middle_hg:
            print('★★★ 大字体变中等字体未发生变化')

        if not great_hg > large_hg:
            print('★★★ 超大字变大字体未发生变化')

        self.common.font_large().click()
        time.sleep(2)

    @teststep
    def read_understand_operate(self, fq, sec_answer, half_exit):
        if self.wait_check_ss_content_page():
            total_num = self.common.bank_time()
            article = self.article()
            print(article.text)
            # self.check_position_change(article)  # 校验字体大小是否发生变化
            self.common.judge_next_is_true_false('false')
            loc = self.get_element_location(self.cloze.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)     # 拖拽至最上方
            ques_info = []
            timer = []
            mine_answer = {}
            flag = False
            while True:
                if flag or self.common.rest_bank_num() == 0:
                    break
                questions = self.cloze.result_question()
                for i, ques in enumerate(questions):
                    if ques.text in ques_info:
                        continue
                    else:
                        if i == len(questions) - 1:
                            self.screen_swipe_up(0.5, 0.8, 0.5, 1000)
                        ques_text = ques.text
                        print('问题：', ques_text)

                        self.common.rate_judge(total_num, len(ques_info))
                        ques_info.append(ques_text)
                        if fq == 1:
                            for x, opt in enumerate(self.cloze.result_opt_text(ques_text)):
                                print(self.cloze.result_opt_char(ques_text)[x].text, opt.text)
                            random_index = random.randint(0, len(self.cloze.result_opt_char(ques_text)) -1)
                            random_text = self.cloze.result_opt_text(ques_text)[random_index].text
                            mine_answer[ques_text] = random_text
                            print('我的答案：', random_text)
                            self.cloze.result_opt_char(ques_text)[random_index].click()
                        else:
                            right_answer = sec_answer[ques_text]
                            for x, opt in enumerate(self.cloze.result_opt_text(ques_text)):
                                print(self.cloze.result_opt_char(ques_text)[x].text, opt.text)
                                if opt.text == right_answer:
                                    self.cloze.result_opt_char(ques_text)[x].click()
                            print('我的答案：', right_answer)

                        print('-'*20, '\n')

                        timer.append(self.common.bank_time())
                        if i == 2:
                            if half_exit:
                                self.click_back_up_button()
                                flag = True
                                break
                self.screen_swipe_up(0.5, 0.9, 0.3, 1000)

            self.common.judge_next_is_true_false('true')
            self.common.judge_timer(timer)
            self.common.next_btn().click()
            answer = mine_answer if fq == 1 else sec_answer
            print(answer)
            return answer, total_num