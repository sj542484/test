import os
import random
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.word_book.object_page.sql_data.data_action import DataActionPage
from testfarm.test_program.app.honor.student.word_book.object_page.sql_data.mysql_data import MysqlData
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps,teststep
from testfarm.test_program.utils.get_attribute import GetAttribute

PATH = os.path.dirname(os.path.dirname(__file__))


class VocabularyChoose(BasePage):
    """词汇选择"""
    def __init__(self):
        self.attr = GetAttribute()
        self.homework = Homework()
        self.mysql = MysqlData()
        self.common = DataActionPage()

    @teststeps
    def wait_check_head_page(self):
        """以“词汇选择 -选单词模式”的 发音按钮 为依据"""
        locator = (By.ID, self.id_type() + "tv_head")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_sentence_page(self):
        """以“词汇选择 -句子选单词模式”的 提示按钮 为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@resource-id,'{}hint')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_explain_page(self):
        """以“词汇选择 -句子选单词模式”的 提示按钮 为依据"""
        locator = (By.ID, self.id_type() + "explain")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_voice_page(self):
        """以“词汇选择 -句子选单词模式”的 提示按钮 为依据"""
        locator = (By.ID, self.id_type() + "fab_sound")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "fab_sound") \
            .click()

    @teststep
    def question_content(self):
        """获取题目内容"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_head").text
        return ele

    @teststep
    def option_button(self):
        """获取四个选项"""
        ele = self.driver.find_elements_by_id(self.id_type() + "option")
        return ele

    # 听音选词
    @teststep
    def explain(self):
        """选择答案后，出现中文解释"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "explain")
        return word.text

    # 句子选单词
    @teststep
    def click_hint_button(self):
        """提示按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "hint").click()
        time.sleep(2)

    @teststep
    def sentence_explain(self):
        """点击 提示按钮后，出现中文解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        print('explain：', explain)
        return explain

    @teststep
    def hint_button_judge(self, var):
        """‘提示’按钮 状态判断"""
        item = self.driver.find_element_by_id(self.id_type() + "hint").get_attribute("enabled")  # ‘下一题’按钮
        if item != var:  # 测试 提示 按钮 状态
            print('★★★ 提示按钮 状态Error', item)

    @teststeps
    def vocab_select_choice_explain(self, i):
        """《词汇选择》 - 选解释模式"""
        if i == 0:
            print('\n词汇选择 - 根据单词选解释模式（复习）\n')
        self.homework.next_button_operate('false')  # 下一题 按钮 判断加 点击操作

        self.click_voice()  # 点击发音按钮
        word = self.question_content()  # 题目
        print('题目:', word)

        options = self.option_button()  # 遍历选项，点击和word一样的单词
        for j in range(0, len(options)):
            find_word = self.common.get_word_by_explain(options[j].text)
            if word in find_word:
                print('选项解释：', options[j].text)
                options[j].click()
                break
        self.homework.next_button_operate('true')  # 下一题 按钮 状态判断 加点击
        print('----------------------------------')

    @teststeps
    def vocab_select_choice_word(self, i):
        """《词汇选择》 - 根据解释选单词"""
        if i == 0:
            print('\n词汇选择-选单词模式（复习）\n')

        self.homework.next_button_operate('false')  # 下一题 按钮 判断加 点击操作

        item = self.question_content()  # 题目
        print('题目:', item)
        word = self.common.get_word_by_explain(item)  # 根据解释获取单词

        options = self.option_button()  # 遍历选项，点击和word一样的单词
        for j in range(0, len(options)):
            if options[j].text in word:
                options[j].click()
                break
        if self.wait_check_voice_page():
            self.click_voice()
            self.homework.next_button_operate('true')  # 下一题 按钮 状态判断 加点击
        else:
            print('★★★ Error-- 声音按钮未出现')
        print('----------------------------------')

    @teststeps
    def vocab_select_listen_choice(self, answer, lc,fc, ws,star,familiar):
        """《词汇选择》 - 听音选词模式 具体操作"""
        if lc == 0:
            self.start_familiar_count_compare(fc, ws, star, familiar)
            print('\n词汇选择-听音选词模式(新词)\n')

        self.homework.next_button_operate('false')  # 下一题 按钮 判断加 点击操作

        self.click_voice()  # 点击发音按钮
        options = self.option_button()  # 获取当前页面所有选项

        if answer[0] == '':  # 若answer为0，则说明上一选项为正确选项，随机选择
            opt_index = random.randint(0, len(options)-1)
            opt_text = options[opt_index].text
            options[opt_index].click()
            print('选择答案为：', opt_text)

            if self.wait_check_explain_page():
                explain = self.explain()
                word = self.common.get_word_by_explain(explain)
                if opt_text in word:
                    print('选项正确:', opt_text)
                    print('解释:', explain)
                    print('-------------------------------------')
                else:
                    print('选项不正确,正确选项为:', word, '\n')
                    answer[0] = word
            else:
                print('★★★ Error-- 解释文本未出现')

        else:  # 若answer为其他，则说明上一选项为错误选项，这一次需定向选择
            for i in range(0, len(options)):
                if options[i].text in answer[0]:
                    options[i].click()
                    if self.wait_check_explain_page():
                        exp = self.explain()
                        print('答案正确：%s\n解释：%s' % (answer[0], exp))
                    else:
                        print('★★★ Error-- 解释文本未出现')
                    break
            answer[0] = ''
            print('-------------------------------------\n')
        self.homework.next_button_operate("true")  # 下一题 按钮 状态判断 加点击

    @teststep
    def start_familiar_count_compare(self, fc, ws,star,familiar):
        """标星和标熟个数的判断"""
        # 对上一游戏的标熟和标星进行个数验证
        if len(star) == fc:
            print('\n标星单词：', star)
            print('标星个数与闪卡抄写个数一致')
        else:
            print('标星单词：', star)
            print("★★★ Error--标星个数与闪卡抄写个数不一致!")

        if len(familiar) == ws:
            print('标熟单词', familiar)
            print('标熟个数与单词默写个数一致\n')
        else:
            print('标熟单词：', familiar)
            print('★★★ Error--熟个数与单词默写个数不一致!')
        print('------------------------------------')

    @teststeps
    def vocab_apply(self, i):
        if i == 0:
            # 词汇选择分组

            # 单词拼写分组
            print('\n 词汇运用 --句子选单词模式(复习)\n')
        self.homework.next_button_operate('false')
        item = self.question_content()  # 题目
        print('题目：%s' % item)

        self.click_hint_button()  # 点击提示按钮
        self.hint_button_judge('false')  # 提示按钮 状态判断

        explain = self.sentence_explain()
        word = self.common.get_word_by_sentence(explain)  # 根据中文获取缺少单词
        print('word：', word)

        options = self.option_button()  # 四个选项
        if i == 1 or i == 2:
            for j in range(0, len(options)):
                if options[j].text not in word:
                    options[j].click()
                    break
        else:
            for j in range(0, len(options)):
                if options[j].text in word:
                    options[j].click()
                    break
        # self.click_voice()
        self.homework.next_button_operate('true')
        print('----------------------------------')


