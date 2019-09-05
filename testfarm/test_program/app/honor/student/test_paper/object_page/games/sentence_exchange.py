import random
from app.honor.student.games.sentence_exchange import SentenceExchangeGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class SentenceExchange(SentenceExchangeGame):

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()

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
            question = self.sentence_question()[0].text
            print(question)
            self.next_btn_judge('false', self.clear_btn)
            print('提示词序：', ' '.join([x.text for x in self.text_bottom()]))

            answer_parts = self.text_bottom()
            for x in range(len(answer_parts)):
                random.choice(self.text_bottom()).click()
            mine_answer = ' '.join([x.text for x in self.input_text()])
            print('我的答案：', mine_answer)
            self.next_btn_judge('true', self.clear_btn)
            bank_json[question] = mine_answer
            self.answer.skip_operator(i, num, "句型转换", self.wait_check_exchange_sentence_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        answer_array = [x.text for x in self.input_text()]
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









