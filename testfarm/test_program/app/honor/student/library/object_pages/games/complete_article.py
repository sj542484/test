# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/10 9:35
# -------------------------------------------
import re

from testfarm.test_program.app.honor.student.games.article_complete import CompleteArticleGame
from testfarm.test_program.app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from testfarm.test_program.app.honor.student.library.object_pages.games.select_word_blank import SelectWordBlank
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class CompleteArticle(CompleteArticleGame):

    def __init__(self):
        self.common = LibraryPubicPage()
        self.home = HomePage()

    @teststep
    def result_opt_char(self, opt_text):
        """结果页的选项"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{}")]/preceding-sibling::'
                                                'android.widget.TextView'.format(opt_text))
        return ele

    @teststep
    def click_opt_by_text(self, opt_text):
        """根据选项内容进行点击"""
        ele = self.driver.find_element_by_xpath('//*[contains(@text,"{}")]'.format(opt_text))
        ele.click()

    @teststeps
    def complete_article_operate(self, fq, sec_answer, half_exit):
        """补全文章游戏过程"""
        timer = []
        mine_answers = {}
        if self.wait_check_complete_article_page():
            total_num = self.common.rest_bank_num()
            article = self.rich_text()
            print(article.text)
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
            self.next_btn_judge('false', self.fab_next_btn)  # 下一步按钮状态校验

            if fq == 1:
                for i in range(0, total_num):
                    self.common.rate_judge(total_num, i)
                    self.opt_char()[i].click()
                    mine_answers[i] = self.opt_text()[i].text
                    timer.append(self.common.bank_time())
            else:
                for i, ans in enumerate(list(sec_answer.values())):
                    self.click_opt_by_text(ans)
                    mine_answers[i] = ans
                    timer.append(self.common.bank_time())

            if half_exit:
                self.click_back_up_button()
                return

            self.common.judge_timer(timer)

            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, self.get_window_size()[1] - 20)  # 拖拽至最上方
            SelectWordBlank().check_position_change()
            self.next_btn_operate('true', self.fab_next_btn)  # 下一步按钮状态校验
            answer = mine_answers if fq == 1 else sec_answer
            print('我的答案：', answer)
            return answer, total_num

    @teststeps
    def complete_article_result_operate(self, mine_answer):
        """补全文章查看答案页处理"""
        right_answer = {}
        right, wrong = [], []
        index = 0
        if ResultPage().wait_check_answer_page():
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方
            desc = self.rich_text().get_attribute('contentDescription')
            desc_right_answer = re.findall(r' (.*?) \(.*?\) .*?', desc.split('##')[1])
            result_right_answer = [x.strip() for x in desc_right_answer]

            for i, ans in enumerate(result_right_answer):
                right_error_desc = self.result_opt_char(ans).get_attribute('contentDescription')
                print('我的答案：', mine_answer[i])
                print('正确答案', ans)
                if mine_answer[i][:-1] != ans:
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








