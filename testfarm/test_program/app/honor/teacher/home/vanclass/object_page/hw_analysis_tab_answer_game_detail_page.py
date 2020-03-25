#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from app.honor.teacher.home.vanclass.object_page.hw_analysis_tab_games_result_detail_page import *
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.dynamic_info.object_page.hw_spoken_detail_page import HwDetailPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.assert_package import MyAssert
from utils.click_bounds import ClickBounds
from utils.vue_context import VueContext
from utils.wait_element_vue import WaitElement


class VanclassGameDetailPage(BasePage):
    """ 作业详情 页面"""
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'  # 标识正确
    drop_down_menu_value = '//div[@class="dialog-content"]'  # 下拉菜单 内容
    detail_tips = '★★★ Error- 未进入答题分析情况 详情页面'

    def __init__(self):
        self.wait = WaitElement()
        self.v_hw = VanclassHwPage()
        self.vue = VueContext()
        self.detail = HwDetailPage()
        self.listen_form = ListenFormSentenceResult()  # 听音连句
        self.trans = SentenceTransResult()  # 句型转换
        self.picture = PictureDictationResult()  # 听音选图
        self.listen_dic = ListenDictationResult()  # 听后选择
        self.complete = CompleteArticleResult()  # 补全文章
        self.cloze = ClozeTestResult()  # 完型填空
        self.read = ReadingArticleResult()  # 阅读理解
        self.choose_cloze = ChooseClozeResult()  # 选词填空
        self.ear = EarsResult()  # 磨耳朵
        self.word_read = WordReadingResult()  # 单词跟读
        self.single = SingleChooseResult()  # 单项选择
        self.strength = StrengthenSentenceResult()  # 强化炼句

    @teststeps
    def wait_check_page(self, var):
        """以“title:  ”为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis" and text()="%s"]' % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_list_page(self):
        """以“答案 元素”为依据"""
        locator = (By.XPATH, '//div[@class="game-cell van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_ear_page(self):
        """以class="pl-reports-content" 元素为依据"""
        locator = (By.XPATH, '//div[@class="pl-reports-content"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def result_voice(self):
        """语音按钮"""
        locator = (By.XPATH, '//div[@class="audio-icon-horn-default audio-icon-horn-stop"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_img(self):
        """图片"""
        locator = (By.XPATH, '//img[@class="van-image__img"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_answer(self):
        """单词"""
        locator = (By.XPATH, '//div[@class="van-cell__title"]/div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_explain(self):
        """解释"""
        locator = (By.XPATH, '//div[@class="van-cell__label"]/div[@class="game-cell-content"]')
        return self.wait.wait_find_elements(locator)

    @teststep
    def result_mine(self):
        """我的"""
        locator = (By.XPATH, '//div[@class="game-cell van-cell"]/i')
        return self.wait.wait_find_elements(locator)

    @teststep
    def game_title(self):
        """游戏title"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis"]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait \
            .wait_find_element(locator).click()

    @teststeps
    def verify_drop_down_content(self, var=15):
        """验证 正确选项后答对率 下拉菜单 是否存在"""
        locator = (By.XPATH, self.drop_down_menu_value)
        return self.wait.wait_check_element(locator, var)

    @teststep
    def drop_down_content(self):
        """x% 下拉菜单 内容"""
        locator = (By.XPATH, self.drop_down_menu_value)
        ele = self.wait.wait_find_elements(locator)

        content = []
        for i in ele:
            content.append(i.find_element_by_xpath('.//div/div[@class="van-cell-group__title"]').text)
            content.append(i.find_element_by_xpath('.//div/div/div/div/span').text)

        print('答题错误详情：', content)
        return ele, content

    @teststeps
    def click_block(self):
        """点击 空白处"""
        ClickBounds().click_bounds(540, 200)

    @teststeps
    def rm_bracket(self, var):
        """ 去掉括号及其中的内容"""
        st = []
        ret = []
        for x in var:
            if x == '(':
                st.append(x)
            elif x == ')':
                st.pop()
            else:
                if len(st) == 0:
                    ret.append(x)  # 没有'('
        return ''.join(ret)

    @teststeps
    def word_reading_operation(self):
        """单词跟读游戏 所有题目内容
        """
        if self.word_read.wait_check_page():
            self.word_read.st_name()  # 学生姓名

            question = self.word_read.result_word_explain()
            voice = self.word_read.result_voice()

            for i in range(0, len(question), 2):
                print(question[i].text, question[i+1].text)
                print('-----------------------------')
                index = (i + 1) // 2
                voice[index].click()

    @teststeps
    def single_choose_operation(self, content):
        """单项选择 查看 题目 答题内容"""
        if self.single.wait_check_list_page():
            ques = self.single.question_items()  # 条目
            rate = self.single.drop_down_rate()  # 答对率

            for i in range(len(ques)):
                print(ques[i].text)

                self.single.option_element(ques[i])
                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容
                print('---------------------------------')

    @teststeps
    def listen_choose_operation(self, content):
        """听后选择 查看 题目 答题内容"""
        if self.listen_dic.wait_check_list_page():
            self.listen_dic.sound_operation()  # 音频 操作

            ques = self.listen_dic.question_items()  # 条目
            rate = self.listen_dic.drop_down_rate()  # 答对率

            for i in range(len(ques)):
                print(ques[i].text)

                option = self.listen_dic.option_element(ques[i])
                for j in range(0, len(option[0]), 2):
                    print(option[1][j], option[1][j+1])

                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容
                print('---------------------------------')

    @teststeps
    def strength_sentence_operation(self, content):
        """强化炼句 所有题目内容
        """
        if self.strength.wait_check_page():
            question = self.strength.question()
            explain = self.strength.explain()

            rate = self.strength.drop_down_rate()  # 答对率
            for i in range(len(question)):
                print(question[i].text, explain[i].text)
                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容
                print('-----------------------------')

    @teststeps
    def ears_ergodic_list(self, content):
        """磨耳朵 遍历列表
        :param content :遍历
        """
        icon = self.detail.st_icon()  # 学生icon
        name = self.detail.st_name()  # 学生名字
        status = self.detail.st_finish_status()  # 答题情况

        for z in range(len(status)):
            content.append(status[z].text)
            print(name[z].text, ': ', status[z].text, '\n', icon[z].text)

        print('----------------------------')

    @teststeps
    def cloze_test_list_operation(self, content):
        """完型填空游戏 所有内容
         :param content: 答对的题目
        """
        if self.cloze.wait_check_list_page():
            self.cloze.cloze_article_content()  # 文章元素
            question = self.cloze.question_item()  # 题目
            options = self.cloze.option_items()
            rate = self.cloze.drop_down_rate()  # 答对率

            for i in range(len(question)):
                print(question[i].text)
                print(options[1])
                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容
                print('-----------------------------')

    @teststeps
    def reading_article_list_operation(self, content):
        """阅读理解游戏 所有内容
         :param content: 答对的题目
        """
        if self.read.wait_check_list_page():
            self.read.reading_article_content()  # 文章元素
            question = self.read.question_item()  # 题目
            options = self.read.option_items()
            rate = self.read.drop_down_rate()  # 答对率

            for i in range(len(question)):
                print(question[i].text)
                print(options[1])
                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容
                print('-----------------------------')

    @teststeps
    def choose_vocabulary_block(self, content):
        """选词填空"""
        if self.choose_cloze.verify_hint_word():  # 有提示词
            self.choose_cloze.hint_word()  # 提示词：
            self.choose_cloze.prompt_word()  # 提示的内容

        self.choose_cloze.choice_vocabulary_content()  # 内容
        rate = self.choose_cloze.drop_down_rate()  # 答对率
        for i in range(len(rate)):
            content.append(rate[0][i])  # 答对率
            self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容

    @teststeps
    def complete_article_operation(self, content):
        """补全文章"""
        if self.complete.wait_check_list_page():
            self.complete.complete_article_content()  # 文章元素
            self.v_hw.swipe_vertical_web(0.5, 0.95, 0.1)

            if self.complete.wait_check_list_page():
                options = self.complete.option_char()  # 选项 A B C D
                options_content = self.complete.option_content()
                rate = self.complete.drop_down_rate()  # 答对率

                for i in range(len(options)):
                    print('-------------------------------')
                    print(options[i].text, options_content[i].text)
                    content.append(rate[0][i])  # 答对率
                    self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容

    @teststeps
    def listen_ergodic_list(self, content):
        """听音连句 遍历列表
        :param content:答对题数
        """
        if self.listen_form.wait_check_page():
            answer = self.listen_form.sentence()  # 答案
            explain = self.listen_form.explain()  # 解释
            voice = self.listen_form.result_voice()  # 喇叭按钮
            rate = self.listen_form.drop_down_rate()  # 答对率

            for i in range(len(answer)):
                print('-----------------------------------------')
                print(explain[i].text, '\n', answer[i].text)
                voice[i].click()  # 点击发音按钮

                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容

    @teststeps
    def sentence_trans_ergodic_list(self, content):
        """句型转换 遍历列表
        :param content:答对题数
        """
        if self.trans.wait_check_list_page():
            explain = self.trans.result_question()  # 题目
            mine = self.trans.result_mine()  # 我的答案
            answer = self.trans.result_answer()  # 正确答案

            rate = self.trans.drop_down_rate()  # 答对率
            count = 0  # 小题数
            for i in range(len(answer)):
                count += 1
                print(explain[i].text, '\n', mine[i].text, '\n', answer[i].text)
                content.append(rate[0][i])  # 答对率
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容

                print('-----------------------------------------')

    @teststeps
    def picture_list_operation(self, content):
        """听音选图 答题内容"""
        if self.picture.wait_check_list_page():
            self.picture.sound_operation()  # 音频 操作

            ques = self.picture.result_sentence()  # 题目
            items = self.picture.result_options()  # 选项
            rate = self.picture.drop_down_rate()  # 答对率

            for i in range(len(ques)):
                print(ques[i].text)
                print(items[1][i])

                content.append(rate[0][i])  # 答对率
                print(rate[0][i])
                self.drop_down_operation(rate[0][i], rate[1][i])  # 下拉菜单内容
                print('---------------------------------')

    @teststeps
    def drop_down_operation(self, var, button):
        """下拉按钮"""
        rate_text = re.sub("\D", "", var)  # 准确率

        if len(rate_text) == 0 and '未作答' in var:
            print('该题还没有学生完成')
        else:
            if int(rate_text) < 100:
                button.click()
                self.vue.app_web_switch()  # 切到apk 再切到vue

                MyAssert().assertTrue(self.verify_drop_down_content())
                self.drop_down_content()  # 下拉菜单内容
                self.click_block()  # 点击空白处
                self.vue.app_web_switch()  # 切到apk 再切到vue
            elif int(rate_text) == 100:
                print('该题正确率为100%')
            else:
                print('★★★ Error -该题正确率', rate_text)
