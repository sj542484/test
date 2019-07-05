# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/8 13:18
# -------------------------------------------
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep
from testfarm.test_program.utils.get_attribute import GetAttribute


class ListenLinkSentence(BasePage):
    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_listen_sentence_page(self):
        """听音连句页面检查点"""
        locator = (By.ID, '{}rich'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_btn_page(self):
        """检查是否存在清除按钮"""
        locator = (By.ID, '{}clear'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def blank_text(self):
        """待填补的"""
        ele = self.driver.find_element_by_id(self.id_type() + "rich")
        return ele

    @teststep
    def text_for_select(self):
        """下方可点击的文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + "text")
        return [x for x in ele if x.text != '']

    @teststep
    def click_voice(self):
        """声音按钮"""
        self.driver.find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_right')
        return ele.text

    @teststep
    def explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele.text

    @teststep
    def result_explain(self):
        """结果页答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_explain')
        return ele

    @teststep
    def clear_btn_judge(self, var):
        """清除按钮状态判断"""
        ele = self.driver.find_element_by_id(self.id_type() + 'clear')
        attr = ele.get_attribute('enabled')
        if attr != var:
            print('★★★ 清除按钮 状态Error', attr)

    @teststep
    def result_answer(self, explain):
        """结果页答案"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(explain))
        mine_answer = ele.find_element_by_xpath('.//android.widget.TextView[contains(@resource-id,"{}tv_mine")]'
                                                .format(self.id_type())).text.strip()
        right_answer = ele.find_element_by_xpath('.//android.widget.TextView[contains(@resource-id,"{}tv_right")]'
                                                 .format(self.id_type())).text.strip()
        return mine_answer, right_answer

    def result_voice(self, explain):
        """结果页声音按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(explain))
        voice_btn = ele.find_element_by_xpath('.//android.widget.ImageView[contains(@resource-id, "{}iv_speak")]'
                                              .format(self.id_type()))
        return voice_btn

    def mine_icon(self, explain):
        """结果图标"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../..'.format(explain))
        icon = ele.find_element_by_xpath('.//android.widget.ImageView[contains(@resource-id, "{}iv_mine")]'
                                         .format(self.id_type()))
        return icon

    @teststep
    def listen_to_sentence_operate(self, fq, sec_answer, half_exit):
        """听音连句游戏过程"""
        timer = []
        mine_answers = {}
        total_num = self.common.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_listen_sentence_page():
                self.common.judge_next_is_true_false('false')     # 下一步按钮状态校验
                self.clear_btn_judge('false')                     # 清除按钮状态校验
                self.click_voice()
                self.common.rate_judge(total_num, i)              # 剩余题数校验
                if fq == 1:                                       # 第一轮，按下方单词或词组顺序依次点击
                    while True:
                        if GetAttribute().enabled(self.common.next_btn()) == 'true':
                            break
                        self.text_for_select()[0].click()
                else:                                            # 第二轮，依次点击正确答案拆分后的顺序
                    right_answer = sec_answer[i].split(' ')
                    print('正确答案：', right_answer)
                    index = 0
                    while True:
                        if GetAttribute().enabled(self.common.next_btn()) == 'true':
                            break
                        for x in self.text_for_select():       # 每次只点击一个（与答案相同的词组）
                            if x.text == right_answer[index]:
                                index += 1
                                x.click()
                                break

                self.common.judge_next_is_true_false('true')
                self.clear_btn_judge('true')
                self.common.next_btn().click()

                if self.wait_check_clear_btn_page():
                    print('★★★ 点击下一步后，清除按钮依然存在')

                rich_content = self.blank_text().get_attribute('contentDescription')  # 获取完成句子的desc
                finish_answer = ' '.join(re.findall(r'\[(.*?)\]', rich_content)[0].split(', '))
                right_answer = self.right_answer().replace('\n', ': ')
                explain = self.explain().replace('\n', ': ')
                print('我的答案: ', finish_answer.strip())
                print(right_answer)
                print(explain)
                mine_answers[i] = finish_answer.strip()
                timer.append(self.common.bank_time())
                print('-'*20, '\n')

                if i == 2:
                    if half_exit:
                        self.click_back_up_button()
                        break
                self.common.next_btn().click()

        self.common.judge_timer(timer)
        answer = mine_answers if fq == 1 else sec_answer
        return answer, total_num

    @teststep
    def listen_to_sentence_result_operate(self, mine_answer):
        right_answer = {}
        right, wrong = [], []
        index = 0
        while True:
            if ResultPage().wait_check_answer_page():
                explains = self.result_explain()
                for j, x in enumerate(explains):
                    result_answer = self.result_answer(x.text)
                    self.result_voice(x.text).click()
                    print('explain:', x.text)
                    print('right:', result_answer[1])
                    print('mine:', result_answer[0].split(': ')[1])
                    print('done:', mine_answer[j])

                    if result_answer[0].split(': ')[1] != mine_answer[j]:
                        print('★★★ 输入的答案与页面展示的不一致！')

                    mine_icon = self.mine_icon(x.text)
                    if result_answer[0] != result_answer[1]:
                        if GetAttribute().selected(mine_icon) == 'true':
                            print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                        else:
                            print('图标验证正确')
                        wrong.append(x.text)
                        right_answer[index] = result_answer[1].split(': ')[1]
                    else:
                        if GetAttribute().selected(mine_icon) == 'false':
                            print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                        else:
                            print('图标验证正确')
                        right.append(x.text)

                    index += 1
                    print('-' * 20, '\n')
                if index == len(mine_answer):
                    break
                else:
                    self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
        print(right_answer)
        self.click_back_up_button()
        return wrong, right, right_answer
