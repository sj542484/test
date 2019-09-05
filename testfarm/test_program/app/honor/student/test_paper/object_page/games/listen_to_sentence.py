import random
import re
import time

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
    def mine_answers(self, explain):
        """我的答案"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '{}')]/"
                                                "preceding-sibling::android.widget.TextView".format(explain))
        return ele.text

    @teststep
    def right_answer(self, explain):
        """解释"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '{}')]/preceding-sibling::"
                                                "android.widget.LinearLayout/android.widget.TextView"
                                                .format(explain))
        return ele.text

    @teststep
    def result_icon(self, explain):
        """结果图标"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'{}')]/../"
                                                "following-sibling::android.widget.ImageView"
                                                .format(explain))
        return ele

    @teststep
    def voices(self, explain):
        """声音按钮"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '{}')]/preceding-sibling::"
                                                "android.widget.LinearLayout/android.widget.ImageView"
                                                .format(explain))
        return ele


    @teststeps
    def play_listen_sentence_game(self, num, exam_json):
        """听音连句"""
        exam_json['听音连句'] = bank_json = {}
        for i in range(num):
            if self.wait_check_listen_sentence_page():
                self.next_btn_judge("false", self.listen_link_clear_btn)          # 清除按钮状态判断
                word_num = self.get_rich_text_input_count()  # 获取需要填补文本的个数
                print(word_num)
                for j in range(word_num):
                    random.choice(self.text_for_select()).click()

                self.next_btn_judge("true", self.listen_link_clear_btn)    # 清除按钮
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
        while len(tips) < len(bank_info):
            result_explain = self.sentence_explain()
            for explain in result_explain:
                if explain.text in tips:
                    continue
                else:
                    input_answer = bank_info[str(len(tips))]
                    tips.append(explain.text)
                    self.result_check(explain.text, input_answer)
            self.home.screen_swipe_up(0.5, 0.8, 0.3,  1000)
            time.sleep(1)

    @teststeps
    def result_check(self, explain, input_answer):
        print(explain)
        mine_answer = self.mine_answers(explain)
        right_answer = self.right_answer(explain)
        print(right_answer)
        print(mine_answer)
        print('记录答案：', input_answer)
        voice = self.voices(explain)
        voice.click()
        result_icon = self.result_icon(explain)

        if input_answer != mine_answer.split(": ")[1].strip().replace(',', ''):
            print('★★★ 输入答案与页面展示不一致！')
        else:
            if mine_answer.split(": ")[1] == explain.split(": ")[1]:
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










