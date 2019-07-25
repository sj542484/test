# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/10 11:53
# -------------------------------------------
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.games.select_word_blank import SelectWordBlank
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class Cloze(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_cl_content_page(self):
        """完形填空页面检查点"""
        locator = (By.ID, self.id_type() + "cl_content")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_dragger_btn(self):
        """检查页面是否存在拖拽按钮"""
        locator = (By.ID, self.id_type() + "dragger")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def article(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'cl_content')
        return ele

    @teststep
    def drag_btn(self):
        """拖拽按钮"""
        ele = self.driver.find_element_by_id('{}dragger'.format(self.id_type()))
        return ele

    @teststep
    def question(self):
        """问题 """
        ele = self.driver.find_element_by_id(self.id_type() + 'question')
        return ele.text

    @teststep
    def opt_text(self):
        """选项 文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_item')
        return ele

    @teststep
    def opt_char(self):
        """选项 字母 ABCD"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_char')
        return ele


    @teststep
    def result_question(self):
        """结果页的问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'question')
        return ele

    @teststep
    def result_opt_char(self, ques):
        """结果页每个题目对应的选项"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(ques))

        chars = ele.find_elements_by_id('{}tv_char'.format(self.id_type()))
        return chars

    @teststep
    def result_opt_text(self, ques):
        """结果页问题对应的选项内容"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(ques))
        texts = ele.find_elements_by_id('{}tv_item'.format(self.id_type()))
        return texts

    @teststep
    def get_ques_size(self, ques):
        """获取包含题目的大小"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(ques))
        return ele.size

    @teststep
    def get_opt_size(self, ques):
        """获取只有选项的大小"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/following-sibling::android.widget.LinearLayout'.format(ques))
        return ele.size

    @teststep
    def get_last_textview_type(self):
        """获取最后一个文本的属性"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        if 'question' in ele[-1].get_attribute('resourceId'):
            return 'ques'
        else:
            return 'opt'

    @teststep
    def swipe_operate(self, last_text_attr):
        """获取问题、选项的屏幕占比"""
        ques_size = self.get_ques_size(self.result_question()[0].text)
        opt_size = self.get_opt_size(self.result_question()[0].text)
        ques_scale = ques_size['height'] / self.get_window_size()[1]  # 获取一道题所占整个屏幕的大小
        opt_scale = opt_size['height'] / self.get_window_size()[1]  # 获取一道题的选项所占整个屏幕的大小

        if last_text_attr == 'ques':
            self.screen_swipe_up(0.5, 0.9, 0.9 - ques_scale, 1000)
        elif last_text_attr == 'opt':
            self.screen_swipe_up(0.5, 0.9, 0.9 - opt_scale, 1000)

    @teststeps
    def cloze_operate(self, fq, sec_answer):
        """完形填空操作"""
        timer = []
        mine_answers = {}
        if self.wait_check_cl_content_page():
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 100)  # 拖拽至最上方
            total_num = self.common.rest_bank_num()
            article = self.article()
            print(article.text)
            # SelectWordBlank().check_position_change(article)      # 校验字体大小是否发生变化

            for i in range(total_num):
                question = self.question().strip()
                print('问题：', question)
                self.common.judge_next_is_true_false('false')     # 判断下一题状态
                self.common.rate_judge(total_num, i)              # 剩余题数校验
                if fq == 1:
                    for j, char in enumerate(self.opt_char()):
                        print(char.text, self.opt_text()[j].text)

                    random_index = random.randint(0, len(self.opt_char()) - 1)
                    random_opt = self.opt_text()[random_index]
                    mine_answers[i+1] = random_opt.text
                    print('我的选项：', random_opt.text)
                    self.opt_char()[random_index].click()
                else:
                    right_answer = sec_answer[i+1]
                    for j, opt in enumerate(self.opt_text()):
                        print(self.opt_char()[j].text, opt.text)
                        if opt.text == right_answer:
                            self.opt_char()[j].click()

                    print('我的选项：', right_answer)
                timer.append(self.common.bank_time())
                if i != total_num - 1:
                    self.screen_swipe_left(0.9, 0.7, 0.2, 1000)
                print('-'*20, '\n')

            self.common.judge_next_is_true_false('true')
            self.common.judge_timer(timer)
            self.common.next_btn().click()
            answer = mine_answers if fq == 1 else sec_answer
            print('我的答案', answer)
            print('------ 游戏结束  -----\n')
            return answer, total_num

    @teststeps
    def cloze_result_operate(self, mine_answer, store_key):
        """完形填空、阅读理解、单项选择结果页处理"""
        right_answer = {}
        right, wrong = [], []
        if ResultPage().wait_check_answer_page():
            if self.wait_check_dragger_btn():
                loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
                self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
            ques_info = []
            index = 0
            while len(ques_info) < len(mine_answer):
                questions = self.result_question()
                last_text_attr = self.get_last_textview_type()
                for i, ques in enumerate(questions):
                    if ques.text in ques_info:
                        continue
                    else:
                        if i == len(questions) - 1:
                            self.swipe_operate(last_text_attr)

                        ques_info.append(ques.text)
                        print('问题：', ques.text, '\n')
                        for y, opt in enumerate(self.result_opt_text(ques.text)):
                            char = self.result_opt_char(ques.text)[y]
                            mine_ans = mine_answer[ques.text] if store_key else mine_answer[len(ques_info)]
                            if opt.text == mine_ans:
                                if char.get_attribute('contentDescription') == 'right':
                                    right.append(opt.text)
                                    print('我的：', mine_ans)
                                    print('答案正确：', opt.text)
                                    if store_key:
                                        right_answer[ques.text] = opt.text

                                elif char.get_attribute('contentDescription') == 'error':
                                    wrong.append(opt.text)
                                    print('我的答案错误', opt.text)
                                else:
                                    print('★★★ 选择的选项未标识对错信息！')
                            else:
                                if char.get_attribute('contentDescription') == 'right':
                                    if store_key:
                                        right_answer[ques.text] = opt.text
                                    else:
                                        index += 1
                                        right_answer[index] = opt.text
                                    print('正确答案：', opt.text)
                        print('-'*30, '\n')

            print('结果页答案:', right_answer)
            self.click_back_up_button()
            return wrong, right, right_answer


    # @teststeps
    # def check_result_opt_answer_operate(self, ques_info, ques, mine_answer, store_key, right, wrong,
    #                                     right_answer, index ):
    #     """查看结果页选项答案操作"""
    #     ques_info.append(ques.text)
    #     print('问题：', ques.text, '\n')
    #     for y, opt in enumerate(self.result_opt_text(ques.text)):
    #         char = self.result_opt_char(ques.text)[y]
    #         mine_ans = mine_answer[ques.text] if store_key else mine_answer[len(ques_info)]
    #         if opt.text == mine_ans:
    #             if char.get_attribute('contentDescription') == 'right':
    #                 right.append(opt.text)
    #                 print('我的：', mine_ans)
    #                 print('答案正确：', opt.text)
    #                 if store_key:  # 存储正确答案
    #                     right_answer[ques.text] = opt.text
    #                 else:  # 完形填空越位存储答案，保证个数与做题个数一致
    #                     right_answer[index + len(mine_answer)] = opt.text
    #
    #             elif char.get_attribute('contentDescription') == 'error':
    #                 wrong.append(opt.text)
    #                 print('我的答案错误', opt.text)
    #             else:
    #                 print('★★★ 选择的选项未标识对错信息！')
    #         else:
    #             if char.get_attribute('contentDescription') == 'right':
    #                 if store_key:
    #                     right_answer[ques.text] = opt.text
    #                 else:
    #                     index += 1
    #                     right_answer[index] = opt.text
    #                 print('正确答案：', opt.text)