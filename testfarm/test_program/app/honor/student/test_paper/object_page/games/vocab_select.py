import random
import time
from app.honor.student.games.choice_vocab import VocabChoiceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.test_paper.object_page.exam_data_handle import DataPage
from conf.decorator import teststep, teststeps


class VocabSelect(VocabChoiceGame):

    def __init__(self):
        self.home = HomePage()
        self.common = DataPage()
        self.answer = AnswerPage()

    @teststep
    def text_views(self):
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def answers(self):
        """单词"""
        ele = self.driver.find_elements_by_id('{}tv_answer'.format(self.id_type()))
        return ele

    @teststep
    def voices(self, var):
        """声音图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/'
                                                'preceding-sibling::android.widget.ImageView' % var)
        return ele

    @teststep
    def explain(self, var):
        """解释"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/../'
                                                'following-sibling::android.widget.TextView' % var)
        return ele.text

    @teststep
    def mine_result(self, var):
        """我的结果图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/../'
                                                'following-sibling::android.widget.ImageView' % var)
        return ele



    @teststeps
    def play_vocab_select_game(self, num, exam_json):
        """词汇选择 """
        exam_json['词汇选择'] = bank_json = {}
        # self.click_voice()
        for i in range(num):
            if self.wait_check_head_page():
                word = self.vocab_question()
                print('题目：', word)

                options = self.vocab_options()
                print('选项如下：')
                for opt in options:
                    print(opt.text)
                opt_index = random.randint(0, len(options)-1)
                print('选择选项：', options[opt_index].text)
                bank_json[word] = options[opt_index].text
                options[opt_index].click()
                self.answer.skip_operator(i, num, '词汇选择', self.wait_check_head_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        select_char = self.vocab_right_answer()
        if len(select_char) == 0:
            print('★★★ Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')

    @teststeps
    def game_detail(self, bank_info, game_type=1):
        """试卷题型详情"""
        all_text = self.text_views()
        print(all_text[3].text, '\t', all_text[4].text, '\t', all_text[5].text)
        tips = []
        while True:
            answers = self.answers()
            for i in range(len(answers)):
                right_word = answers[i].text
                if right_word in tips:
                    continue
                else:
                    self.result_check(right_word, bank_info, tips, game_type)
                    tips.append(right_word)

            if len(tips) < len(bank_info):
                self.home.screen_swipe_up(0.5, 0.9, 0.3, 2000)
            else:
                break

    @teststeps
    def result_check(self, right_word, bank_info, tips, game_type):
        """结果比对"""
        explain = self.explain(right_word)
        mine_icon = self.mine_result(right_word)
        self.voices(right_word).click()
        time.sleep(1)

        if game_type != 2:
            if game_type == 1:
                mine_answer = bank_info[explain]
            else:
                mine_answer = bank_info[list(bank_info.keys())[len(tips)]]

            if right_word == mine_answer:
                if mine_icon.get_attribute('selected') == 'true':
                    print("单词：", right_word + '\n解释：', explain, '\n图标显示为正确')
                    print("我的答案：", mine_answer)
                    print('结果核实正确\n')

                else:
                    print("单词：", right_word + '\n解释：', explain, '\n图标显示为错误')
                    print("我的答案：", mine_answer)
                    print('★★★ Error--结果一致我的图标显示错误！\n')
            else:
                if mine_icon.get_attribute('selected') == 'false':
                    print("单词：", right_word + '\n解释：', explain, '\n图标显示为错误')
                    print('我的答案：', mine_answer)
                    print('结果核实正确\n')
                else:
                    print("单词：", right_word + '\n解释：', explain, '\n图标显示为正确')
                    print('我的答案：', mine_answer)
                    print('★★★ Error-- 答案有误但是图标显示正确！\n')
        else:
            print('单词：', right_word, '\t解释：', explain, '\t正确')
            if mine_icon.get_attribute('selected') == "false":
                print("★★★ Error-- 答案正确但是图标显示错误！\n")









