import random
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.student.login.object_page.home_page import HomePage
from app.student.homework.object_page.homework_page import Homework
from app.student.test_paper.object_page.answer_page import AnswerPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class ListenSentence(BasePage):
    """听音连句"""

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_listen_sentence_page(self):
        """听音连句页面检查点"""
        locator = (By.ID, '{}clear'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
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
        return ele

    @teststep
    def click_voice(self):
        """声音按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice")\
            .click()

    @teststep
    def clear_button_operate(self, var):
        self.click_clear_btn()
        self.clear_btn_judge(var)

    @teststep
    def click_clear_btn(self):
        """点击清除按钮"""
        self.driver.\
            find_element_by_id(self.id_type() + "clear")\
            .click()

    @teststep
    def clear_btn_judge(self, var):
        """清除按钮状态判断"""
        ele = self.driver.find_element_by_id(self.id_type() + "clear")
        attr = ele.get_attribute("enabled")
        if attr != var:
            print("★★★ 清除按钮 状态Error", attr)

    @teststep
    def right_answers(self):
        """正确答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + "tv_right")
        return ele

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
                self.click_voice()
                self.homework.next_button_operate("false")  # 下一步按钮状态判断
                self.clear_button_operate("false")          # 清除按钮状态判断
                blank_text = self.blank_text()              # 待填补的文本
                word_num = len(re.findall(r"{}", blank_text.text))  # 获取需要填补文本的个数
                for j in range(word_num):
                    select_option = self.text_for_select()    # 可点击的文本
                    options = [x for x in select_option if x.text != '']  # 获取不为空的文本
                    options[random.randint(0, len(options)-1)].click()   # 随机点击

                self.clear_btn_judge("true")    # 清除按钮
                self.homework.next_button_judge("true")  # 下一步
                finish_text = self.blank_text().get_attribute("contentDescription")  # 完成答案
                finish_sentence = re.findall(r"\[(.*?)\]", finish_text)[0]
                mine_answer = finish_sentence.replace(",", "")
                print("我的答案：", mine_answer)
                bank_json[i] = mine_answer

                self.answer.skip_operator(i, num, '听音连句', self.wait_check_listen_sentence_page,
                                          self.judge_tip_status, finish_sentence)

    @teststeps
    def judge_tip_status(self, finish_sentence):
        cont_desc = self.blank_text().get_attribute("contentDescription")
        if finish_sentence == re.findall(r'\[(.*?)\]', cont_desc)[0]:
            print('跳转后填空文本未发生变化')
        else:
            print('★★★ Error-- 跳转回来填空内容发生改变')

    @teststeps
    def listen_form_sentence_detail(self, bank_info):
        tips = []
        while True:
            right_answers = self.right_answers()
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










