import random
import re

from app.honor.student.games.sentence_listen_link import ListenLinkSentenceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class ListenSentence(ListenLinkSentenceGame):
    """听音连句"""

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()


    @teststep
    def mine_answers(self, right_answer):
        """我的答案"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,"
                                                "'{0}')]/../following-sibling::android.widget.TextView"
                                                "[@resource-id='{1}tv_mine']".format(right_answer, self.id_type()))
        return ele.text

    @teststep
    def explain(self, right_answer):
        """解释"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,"
                                                "'{0}')]/../following-sibling::android.widget.TextView"
                                                "[@resource-id='{1}tv_explain']".format(right_answer, self.id_type()))
        return ele.text

    @teststep
    def voices(self, right_answer):
        """声音按钮"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'%s')]/"
                                                "preceding-sibling::android.widget.ImageView" % right_answer)
        return ele

    @teststep
    def result_icon(self, right_answer):
        """结果图标"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'%s')]/../"
                                                "../following-sibling::android.widget.ImageView" % right_answer)
        return ele

    @teststep
    def text_views(self):
        """页面所有text"""
        ele = self.driver.find_elements_by_class_name("android.widget.TextView")
        return ele

    @teststeps
    def play_listen_sentence_game(self, num, exam_json):
        """听音连句"""
        exam_json['听音连句'] = bank_json = {}
        for i in range(num):
            if self.wait_check_listen_sentence_page():
                self.next_btn_judge("false", self.clear_btn)          # 清除按钮状态判断
                word_num = self.get_rich_text_input_count() # 获取需要填补文本的个数
                for j in range(word_num):
                    select_option = self.text_for_select()    # 可点击的文本
                    random.choice(select_option).click()

                self.next_btn_judge("true", self.clear_btn)    # 清除按钮
                finish_answer = ' '.join(self.rich_text().text.split())
                print("我的答案：", finish_answer)
                bank_json[i] = finish_answer

                self.answer.skip_operator(i, num, '听音连句', self.wait_check_listen_sentence_page,
                                          self.judge_tip_status, finish_answer)

    @teststeps
    def judge_tip_status(self, finish_sentence):
        page_finish_answer = ' '.join(self.rich_text().text.split())
        if finish_sentence == page_finish_answer:
            print('跳转后填空文本未发生变化')
        else:
            print('★★★ Error-- 跳转回来填空内容发生改变')

    @teststeps
    def listen_form_sentence_detail(self, bank_info):
        tips = []
        while True:
            right_answers = self.right_sentence_answer()
            for i in range(len(right_answers)):
                if right_answers[i].text in tips:
                    continue
                else:
                    input_answer = bank_info[str(len(tips))]
                    if i != len(right_answers) - 1:
                        tips.append(right_answers[i].text)
                        self.result_check(right_answers[i].text, input_answer)
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        tips.append(right_answers[i].text)
                        self.result_check(right_answers[i].text, input_answer)
                        self.home.screen_swipe_up(0.5, 0.6, 0.75, 1000)

            if len(tips) < len(bank_info):
                self.screen_swipe_up(0.5, 0.9, 0.2, 1000)
            else:
                break

    @teststeps
    def result_check(self, right_answer, input_answer):
        voice = self.voices(right_answer)
        voice.click()
        mine_answer = self.mine_answers(right_answer)
        explain = self.explain(right_answer)
        result_icon = self.result_icon(right_answer)

        print(explain + '\n' + right_answer + '\n' + mine_answer)
        print('记录答案：', input_answer)

        if input_answer != mine_answer.split(": ")[1].strip().replace(',', ''):
            print('★★★ 输入答案与页面展示不一致！')
        else:
            if mine_answer.split(": ")[1] == right_answer.split(": ")[1]:
                if result_icon.get_attribute("selected") == "true":
                    print("结果核实正确")
                else:
                    print("★★★ 结果正确 图标显示错误！")
            else:
                if result_icon.get_attribute("selected") == "false":
                    print("结果核实正确")
                else:
                    print("★★★ 结果错误 图标显示正确！")

        print("-"*20, '\n')










