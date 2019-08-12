import random
import time
from app.honor.student.games.choice_listen import ListenChoiceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class ListenSelect(ListenChoiceGame):

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()

    # 详情页 元素
    @teststep
    def voice_play(self):
        """详情页 音频播放按钮"""
        self.driver.\
            find_element_by_id(self.id_type() + 'iv_play')\
            .click()

    @teststep
    def first_content(self):
        """第一行文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fs_content')
        print(ele.text)

    @teststeps
    def option_button(self, var):
        """选项"""
        opt_char = self.driver \
            .find_elements_by_xpath(
                            '//android.widget.TextView[contains(@text, "{0}")]'
                            '/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout'
                            '/android.widget.LinearLayout/android.widget.TextView'
                            '[contains(@resource-id,"{1}tv_char")]'.format(var, self.id_type()))

        opt_text = self.driver \
            .find_elements_by_xpath(
                            '//android.widget.TextView[contains(@text, "{0}")]'
                            '/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout'
                            '/android.widget.LinearLayout/android.widget.TextView'
                            '[contains(@resource-id,"{1}tv_item")]'.format(var, self.id_type()))
        return opt_char, opt_text

    @teststep
    def print_options(self, options):
        for i in range(len(options[0])):
            print(options[0][i].text, '  ', options[1][i].text)

    @teststeps
    def play_listening_select_game(self, num, exam_json):
        """听力选择 """
        if self.wait_check_listen_select_page():
            print(self.red_hint())
            self.voice_button().click()
            time.sleep(2)
            if self.wait_check_listen_select_page():
                print('★★★ Error-- 红色标识未消失')

            if self.voice_button().get_attribute('enabled') == 'true':
                print('★★★ Error-- 喇叭点击后未置灰')

            else:
                exam_json['听后选择'] = bank_json = {}
                self.select_operate(num, '听后选择', bank_json)

    @teststeps
    def select_operate(self, num, name, bank_json):
        """滑动操作"""
        tips = []
        while True:
            questions = self.questions()
            for j in range(len(questions)):
                ques = questions[j].text
                if ques in tips:
                    continue
                else:
                    tips.append(ques)
                    print(ques)
                    options = self.option_button(ques)
                    self.print_options(options)
                    index = random.randint(0, len(options[0]) - 1)
                    select_text = options[1][index].text
                    options[1][index].click()
                    print('选择选项：', select_text)
                    bank_json[ques] = select_text

                if len(tips) == 1 and name == "听后选择":
                    while True:
                        if self.answer.answer_check_button().get_attribute('enabled') == 'true':
                            break
                        else:
                            time.sleep(3)
                opt_text = tips[-1]
                self.answer.skip_operator(len(tips) - 1, num, name, self.wait_check_listen_select_page,
                                          self.judge_tip_status, opt_text, next_page=1)

            if len(tips) == num:
                break

    @teststep
    def judge_tip_status(self, opt_text):
        opt_chars = self.option_button(opt_text)
        selected_char = [x for x in opt_chars[0] if x.get_attribute('selected') == 'true']
        if len(selected_char) == 0:
            print('★★★ Error-- 跳转回来后题目完成状态发生变化')
        elif len(selected_char) == 1:
            print('题目跳转后题目状态未改变：已完成')

    @teststep
    def check_result_detail_operate(self, bank_info, quote_type=1):
        tips = []
        while True:
            questions = self.questions()
            for i in range(len(questions)):
                ques = questions[i].text
                mine_answer = bank_info[ques]
                if ques in tips:
                    continue
                else:
                    tips.append(ques)
                    print(ques)
                    if i != len(questions) - 1:
                        options = self.option_button(ques)
                        self.print_options(options)
                        self.check_answer(options, mine_answer)
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.42, 1000)
                        options = self.option_button(ques)
                        self.print_options(options)
                        self.check_answer(options, mine_answer)
            if len(tips) < len(bank_info):
                if quote_type == 1:
                    self.screen_swipe_up(0.5, 0.8, 0.25, 1500)
                else:
                    self.screen_swipe_up(0.5, 0.8, 0.4, 1500)
            else:
                break

    @teststep
    def check_answer(self, options, mine_answer):
        right_answer = [options[1][x].text for x in range(len(options[0]))
                        if options[0][x].get_attribute("contentDescription") == 'right']
        error_answer = [options[1][x].text for x in range(len(options[0]))
                        if options[0][x].get_attribute("contentDescription") == 'error']

        if len(right_answer) == 0:
            print('★★★ 未发现正确答案提示')
        else:
            print('正确答案：', right_answer[0])
            print("我的答案：", mine_answer)
            if len(error_answer) == 0:
                print('所选答案：', right_answer[0])
                if mine_answer != right_answer[0]:
                    print("★★★ 所选答案与页面显示不一致！\n")
                else:
                    print("答案核实正确\n")
            else:
                print("所选答案：", error_answer[0])
                if mine_answer != error_answer[0]:
                    print('★★★ 所选答案与页面显示不一致！\n')
                else:
                    print("答案核实正确\n")
