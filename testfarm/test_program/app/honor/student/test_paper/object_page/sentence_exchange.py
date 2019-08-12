import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class SentenceExchange(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_exchange_answer_page(self):
        """句型转换页面检查点，以输入答案的id作为依据"""
        locator = (By.ID, self.id_type() + "rv_answer")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def input_answer_array(self):
        ele = self.driver.find_elements_by_xpath('//android.support.v7.widget.RecyclerView/following-sibling::'
                                                 'android.widget.LinearLayout/android.widget.TextView')
        answer_array = [x.text for x in ele]
        return answer_array

    @teststep
    def question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_question')
        return ele.text

    @teststep
    def question_hint(self):
        """提示部分"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv_hint')
        return ele

    @teststep
    def hint_part(self):
        """句子 拆分的部分"""
        ele = self.question_hint().find_elements(By.CLASS_NAME, 'android.widget.TextView')
        return ele

    @teststep
    def answer_ele(self):
        """答案整体"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv_answer')
        return ele

    @teststep
    def answer_part(self):
        """答案 部分"""
        ele = self.answer_ele().find_elements(By.CLASS_NAME, 'android.widget.TextView')
        return ele

    @teststep
    def clear_button_operate(self, var):
        """清除操作"""
        self.click_clear_btn()
        self.clear_btn_judge(var)

    @teststep
    def click_clear_btn(self):
        """点击清除按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'bt_clear') \
            .click()

    @teststep
    def clear_btn_judge(self, var):
        """清除按钮状态判断"""
        ele = self.driver.find_element_by_id(self.id_type() + 'bt_clear')
        attr = ele.get_attribute('enabled')
        if attr != var:
            print('★★★ 清除按钮 状态Error', attr)

    @teststep
    def get_all_text(self):
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def mine_icon(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'iv_mine')
        return ele

    @teststep
    def result_question(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_question')
        return ele

    @teststep
    def detail_answer(self, question):
        """单个结果信息"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,'
                                                '"{0}")]/../following-sibling::android.widget.LinearLayout/'
                                                'android.widget.TextView[@resource-id="{1}tv_answer"]'
                                                .format(question, self.id_type()))
        return ele.text

    @teststep
    def mine_answer(self, question):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,'
                                                '"{0}")]/../following-sibling::android.widget.LinearLayout/'
                                                'android.widget.TextView[@resource-id="{1}tv_mine"]'
                                                .format(question, self.id_type()))

        return ele.text

    @teststep
    def result_icon(self, question):
        ele = self.driver \
            .find_element_by_xpath(
                '//android.widget.TextView[contains(@text, "%s")]/../../'
                'following-sibling::android.widget.ImageView' % question)
        return ele

    @teststeps
    def play_sentence_exchange_game(self, num, exam_json):
        """句型转换"""
        exam_json['句型转换'] = bank_json = {}
        for i in range(num):
            question = self.question()
            print(question)
            self.clear_button_operate('false')
            self.homework.next_button_operate('false')

            hint_parts = self.hint_part()
            hint = []
            for k in range(len(hint_parts)):
                hint.append(hint_parts[k].text)
            print('提示词序：', ' '.join(hint))

            answer_parts = self.answer_part()
            for j in range(len(answer_parts)):
                hint_parts = self.hint_part()
                hint_parts[random.randint(0, len(hint_parts)-1)].click()

            answer = []
            final_answer_part = self.answer_part()
            for k in range(len(final_answer_part)):
                answer.append(final_answer_part[k].text)
            print('我的答案：', ' '.join(answer))
            bank_json[question] = ' '.join(answer)
            self.clear_btn_judge('true')
            self.homework.next_button_judge('true')
            self.answer.skip_operator(i, num, "句型转换", self.wait_check_exchange_answer_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        answer_array = self.input_answer_array()
        if '' in answer_array or None in answer_array:
            print('★★★ Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')

    @teststeps
    def sentence_exchange_detail(self, bank_info):
        """强化炼句 详情页处理"""
        tips = []
        while True:
            questions = self.result_question()
            for i in range(len(questions)):
                if questions[i].text in tips:
                    continue
                else:
                    if i != len(questions) - 1:
                        tips.append(questions[i].text)
                        self.check_result(questions[i].text, bank_info)
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        tips.append(questions[i].text)
                        self.check_result(questions[i].text, bank_info)
                        self.home.screen_swipe_down(0.5, 0.6, 0.75, 1000)

            if len(tips) < len(bank_info):
                self.screen_swipe_up(0.5, 0.9, 0.2, 2000)
            else:
                break

    @teststep
    def check_result(self, question, bank_info):
        answer = self.detail_answer(question)
        mine_answer = self.mine_answer(question)
        icon = self.result_icon(question)
        input_answer = bank_info[question]

        print('问题：', question)
        print('答案：', answer)
        print('我的：', mine_answer)
        print('记录答案：', input_answer)

        if input_answer != mine_answer:
            print("★★★ 输入答案与页面展示不一致！")
        else:
            if mine_answer == answer:
                if icon.get_attribute('selected') == 'true':
                    print('结果核实正确')
                else:
                    print('★★★ 答案正确图标显示错误！')
            else:
                if icon.get_attribute('selected') == 'false':
                    print('结果核实正确')
                else:
                    print('★★★ 答案错误图标显示正确！')
        print('-'*20, '\n')









