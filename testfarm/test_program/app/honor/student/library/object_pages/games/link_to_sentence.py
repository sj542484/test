# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/9 13:38
# -------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.games.restore_word import RestoreWord
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class LinkToSentence(BasePage):

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_link_sentence_page(self):
        """连词成句页面检查点"""
        locator = (By.ID, '{}tv_prompt'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_right_answer_page(self):
        """检查是否出现正确答案"""
        locator = (By.ID, '{}tv_prompt'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele.text

    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_sentence')
        return ele.text

    @teststep
    def result_explain(self):
        """正确答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_hint')
        return ele

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def result_answer_by_explain(self, explain):
        """结果页句子"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/preceding-sibling::android.widget.TextView'.format(explain))
        return ele.text

    @teststep
    def mine_icon_by_sentence(self, explain):
        """对错图标"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../following-sibling::android.widget.ImageView'
                                                .format(explain))
        return ele

    @teststep
    def get_sentence_size(self, explain):
        """获取句子的大小"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../..'.format(explain))
        return ele.size


    @teststeps
    def link_sentence_operate(self, fq, sec_answer):
        """连词成句操作"""
        timer = []
        mine_answer = {}
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_link_sentence_page():
                self.common.judge_next_is_true_false('false')              # 判断下一步状态
                self.common.rate_judge(total_num, i)
                explain = self.explain().strip()
                print('解释：', explain)
                if fq == 1:
                    RestoreWord().drag_operate(self.word_alpha()[-1], self.word_alpha()[0])
                    self.common.next_btn().click()
                else:
                    right_answer = sec_answer[explain]
                    self.do_right_operate(right_answer)

                if not self.wait_check_right_answer_page():
                    print('★★★ 点击下一步后未发现正确答案')
                else:
                    right_answer = self.right_answer()
                    print(right_answer)
                mine = ' '.join([x.text for x in self.word_alpha()])
                mine_answer[explain] = mine
                print('我的答案：', mine)
                print('-' * 20, '\n')
                timer.append(self.common.bank_time())
                self.common.next_btn().click()

        self.common.judge_timer(timer)
        done_answer = mine_answer if fq == 1 else sec_answer
        return done_answer, total_num

    @teststeps
    def link_sentence_result_operate(self, mine_answer):
        """连词成句结果页处理"""
        if ResultPage().wait_check_answer_page():
            right_answer = {}
            right, wrong = [], []
            answer_info = []
            sentence_size = self.get_sentence_size(self.result_explain()[0].text)
            sentence_scale = sentence_size['height'] / self.get_window_size()[1]
            print('===== 查看结果页 =====\n')
            while len(answer_info) < len(mine_answer):
                result_explains = self.result_explain()
                for i, exp in enumerate(result_explains):
                    if exp.text in answer_info:
                        continue
                    else:                                           # 倒数第一道题，向上滑出一道题的距离
                        if i == len(result_explains) - 1:
                            self.screen_swipe_up(0.5, 0.9, 0.9 - sentence_scale, 1000)

                        result_explain = exp.text.strip()
                        print('解释：', result_explain)
                        answer_info.append(exp.text)
                        result_answer = self.result_answer_by_explain(exp.text)
                        print('答案：', result_answer)

                        mine_icon = self.mine_icon_by_sentence(exp.text)
                        if mine_answer[result_explain] != result_answer:
                            if GetAttribute().selected(mine_icon) == 'true':       # 校验图标是否正确
                                print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                            else:
                                print('图标验证正确')
                            wrong.append(result_explain)

                        else:
                            if GetAttribute().selected(mine_icon) == 'false':
                                print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                            else:
                                print('图标验证正确')
                            right.append(result_explain)
                        right_answer[result_explain] = result_answer

                    print('-'*30, '\n ')

            print('正确题：', right)
            print('错误题：', wrong)
            self.click_back_up_button()
            return wrong, right, right_answer

    @teststep
    def do_right_operate(self, right_answer):
        """连词成绩做对操作"""
        right_word_list = right_answer.split(' ')
        index = 0
        print('初始句子：', ' '.join([x.text for x in self.word_alpha()]).strip())
        for i in range(index, len(right_word_list)):
            alpha_list = self.word_alpha()
            for j in range(len(alpha_list)):
                if alpha_list[j].text == right_word_list[i]:
                    if alpha_list[j].text != alpha_list[index].text:
                        RestoreWord().drag_operate(alpha_list[j], alpha_list[index])
                    index += 1
                    break
            if ' '.join([x.text for x in self.word_alpha()]).strip() == right_answer:
                break