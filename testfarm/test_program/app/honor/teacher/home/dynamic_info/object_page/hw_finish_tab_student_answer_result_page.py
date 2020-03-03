#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from app.honor.teacher.home.vanclass.object_page.vanclass_hw_spoken_page import VanclassHwPage
from app.honor.teacher.home.vanclass.object_page.finish_tab_games_result_detail_page import *
from conf.base_page import BasePage
from conf.decorator_vue import teststep, teststeps
from utils.assert_package import MyAssert
from utils.vue_context import VueContext
from utils.wait_element_vue import WaitElement


class ResultDetailPage(BasePage):
    """结果 详情页
    单词听写/ 词汇选择/ 猜词游戏/ 连连看(文字模式)/ 单词拼写/ 闪卡(单词抄写&学习)/ 还原单词/ """
    result_right_value = 'van-icon van-icon-cross game-cell-right-icon-right'  # 标识正确

    result_tips = '★★★ Error- 未进入结果 详情页面'
    result_vue_tips = '★★★ Error- 未进入结果 详情vue页面'

    def __init__(self):
        self.wait = WaitElement()
        self.v_hw = VanclassHwPage()
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
        self.word_form = WordFormSentenceResult()  # 连词成句
        self.match = MatchExerciseResult()  # 连连看
        self.single = SingleChooseResult()  # 单项选择
        self.strength = StrengthenSentenceResult()  # 强化炼句
        self.flash_sent = FlashSentenceResult()  # 闪卡 句子学习
        self.vue = VueContext()

    @teststeps
    def wait_check_app_page(self, var):
        """以“title: 小游戏名”的ID为依据"""
        locator = (By.XPATH, "//android.view.View[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_page(self, var=10):
        """以“title: 学生名”的ID为依据"""
        locator = (By.XPATH, '//div[@class="van-nav-bar__title van-ellipsis"]')
        return self.wait.wait_check_element(locator, var)

    @teststeps
    def wait_check_list_page(self):
        """以“答案 元素”的ID为依据"""
        locator = (By.XPATH, '//div[@class="game-cell van-cell"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def first_report(self):
        """首次正答率"""
        locator = (By.XPATH, '//span[contains(text(),"首次正答")]')
        item = self.wait.wait_find_element(locator).text
        print(item)
        return item

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

    @teststeps
    def judge_voice(self):
        """判断是否存在 发音按钮"""
        locator = (By.XPATH, '//audio[@class="audio-icon-detail-audio"]')
        return self.wait.wait_check_element(locator)

    @teststep
    def back_up_button(self):
        """返回按钮"""
        locator = (By.XPATH, '//div[@class="vt-page-left"]/img[@class="vt-page-left-img-Android"]')
        self.wait\
            .wait_find_element(locator).click()

    @teststeps
    def hw_detail_operation(self, index, score=None):
        """答题情况 详情页
        :param index:游戏编号
        :param score:成绩
        """
        MyAssert().assertTrue_new(self.wait_check_page(), self.result_vue_tips)  # 页面检查点
        content = []  # 答对的 小题数
        value = self.report_score_compare(score)  # 验证 首次成绩 与首次正答
        # var = value.split('/')
        # ques_num = int(re.sub("\D", "", var[0]))  # 首次正答题数

        if index == 1:  # 听后选择
            self.listen_choose_operation(content)  # 具体操作
        elif index == 2:  # 单项选择
            self.single_choose_operation(content)  # 具体操作
        elif index == 6:  # 阅读理解
            self.reading_article_list_operation(content)  # 具体操作
        elif index == 7:  # 完形填空
            self.cloze_test_list_operation(content)  # 具体操作
        elif index == 15:  # 听音选图
            self.picture_list_operation(content)  # 选图题滑屏及具体操作
        elif index == 8:  # 补全文章
            self.complete_article_operation(content)
        elif index == 9:  # 选词填空
            if self.choose_cloze.verify_hint_word():  # 有提示词
                self.choose_cloze.hint_word()  # 提示词：
                self.choose_cloze.prompt_word()  # 提示的内容

            self.choose_cloze.choice_vocabulary_content()  # 内容
            if self.choose_cloze.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()
        elif index == 19:  # 连词成句
            self.word_form_sentence_operation(content)
        elif index == 3:  # 强化炼句
            self.strength_sentence_operation(content)
        elif index == 4:  # 听音连句
            self.listen_ergodic_list(content)
        elif index == 5:  # 句型转换
            self.sentence_trans_ergodic_list(content)
        else:  # /11单词拼写/单词听写/12猜词游戏/13词汇选择/14闪卡练习(单词抄写&学习)/20还原单词/
            self.list_operation(content)

        # if index not in (18, 15, 9):
        #     if len(content) != ques_num:
        #         print("★★★ Error- 首次正答 与答题情况不匹配", ques_num, content)
        #     else:
        #         print('答对{}题，答错{}题'.format(len(content), int(var[1]) - len(content)))

    @teststeps
    def word_reading_operation(self, score):
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

            if self.word_read.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def single_choose_operation(self, content):
        """单项选择 查看 题目 答题内容"""
        if self.single.wait_check_list_page():
            ques = self.single.question_items()  # 条目
            for i in range(len(ques)):
                print(ques[i].text)

                option = self.single.option_element(ques[i])
                for j in range(len(option[0])):
                    # print(option[1][j])
                    if option[0][j].get_attribute("class") == self.single.result_right_value:
                        content.append(option[1][j])
                    # print('-----------------------')
                print('---------------------------------')

            if self.single.wait_check_list_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def listen_choose_operation(self, content):
        """听后选择 查看 题目 答题内容"""
        if self.listen_dic.wait_check_list_page():
            self.listen_dic.sound_operation()  # 音频 操作

            ques = self.listen_dic.question_items()  # 条目
            for i in range(len(ques)):
                print(ques[i].text)

                option = self.listen_dic.option_element(ques[i])
                for j in range(0, len(option[0]), 2):
                    print(option[1][j], option[1][j+1])
                    if option[0][j].get_attribute("class") == self.listen_dic.result_right_value:
                        content.append(option[1][j])
                print('---------------------------------')

            if self.listen_dic.wait_check_list_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def strength_sentence_operation(self, content):
        """强化炼句 所有题目内容
        """
        if self.strength.wait_check_page():
            question = self.strength.question()  # 题目
            explain = self.strength.explain()  # 解释
            mine = self.strength.status()  # 答题情况

            for i in range(len(question)):
                print(question[i].text, explain[i].text)
                if mine[i].get_attribute("class") == self.strength.result_right_value:
                    content.append(mine[i])
                print('-----------------------------')
            if self.strength.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def flash_sentence_operation(self, content, score):
        """闪卡 句子学习游戏 所有题目内容
        """
        if self.flash_sent.wait_check_page():
            self.report_score_compare(score)  # 验证 首次成绩 与首次正答

            question = self.flash_sent.sentence()
            explain = self.flash_sent.explain()
            mine = self.flash_sent.status()

            for i in range(len(question)):
                print(question[i].text, explain[i].text)
                if mine[i].get_attribute("class") == self.flash_sent.result_right_value:
                    content.append(mine[i])
                print('-----------------------------')
            if self.flash_sent.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def word_form_sentence_operation(self, content):
        """连词成句 所有题目内容
        """
        if self.word_form.wait_check_page():
            question = self.word_form.question()
            explain = self.word_form.explain()
            mine = self.word_form.status()

            for i in range(len(question)):
                print(question[i].text, explain[i].text)
                if mine[i].get_attribute("class") == self.word_form.result_right_value:
                    content.append(mine[i])
                print('-----------------------------')
            if self.word_form.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def match_img_operation(self, content, score):
        """连连看 （图片模式）游戏 所有题目内容
        """
        if self.match.wait_check_page():
            self.report_score_compare(score)  # 验证 首次成绩 与首次正答

            question = self.match.word()
            img = self.match.img()
            mine = self.match.status()

            for i in range(len(question)):
                print(question[i].text, img[i].get_attribute("src"))
                if mine[i].get_attribute("class") == self.match.result_right_value:
                    content.append(mine[i])
                print('-----------------------------')
            if self.match.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def list_operation(self, content):
        """/11单词拼写/单词听写/12猜词游戏/13词汇选择/14闪卡练习(单词抄写&学习)/20还原单词/连连看(文字模式)
        """
        if self.wait_check_list_page():
            question = self.result_answer()
            explain = self.result_explain()
            mine = self.result_mine()
            voice = self.result_voice()  # 喇叭按钮

            for i in range(len(question)):
                print(question[i].text, explain[i].text)
                if mine[i].get_attribute("class") == self.result_right_value:
                    content.append(mine[i])

                voice[i].click()
                print('-----------------------------')

            if self.wait_check_page():
                self.back_up_button()  # 返回 游戏列表
                self.vue.app_web_switch()

    @teststeps
    def flash_card_list_operation(self, content, score):
        """14闪卡练习(单词抄写&学习)
        """
        if self.wait_check_list_page():
            self.report_score_compare(score)  # 验证 首次成绩 与首次正答

            img = self.result_img()
            question = self.result_answer()
            explain = self.result_explain()
            mine = self.result_mine()
            voice = self.result_voice()  # 喇叭按钮

            for i in range(len(question)):
                print(question[i].text, explain[i].text, '\n', img[i])
                if mine[i].get_attribute("class") == self.result_right_value:
                    content.append(mine[i])

                voice[i].click()
                print('-----------------------------')

            if self.wait_check_page():
                self.back_up_button()  # 返回 游戏列表
                self.vue.app_web_switch()

    @teststeps
    def cloze_test_list_operation(self, content):
        """完型填空游戏 所有内容
         :param content: 首次正答数
        """
        if self.cloze.wait_check_list_page():
            self.cloze.cloze_article_content()  # 文章元素
            question = self.cloze.question_item()  # 题目
            options = self.cloze.option_items()
            for i in range(len(question)):
                print(question[i].text)
                print(options[1])
                if options[0][i].get_attribute('class') == self.cloze.result_right_value:
                    content.append(i)
                print('-----------------------------')

            if self.cloze.wait_check_list_page():
                self.back_up_button()  # 返回 游戏列表
                self.vue.app_web_switch()

    @teststeps
    def reading_article_list_operation(self, content):
        """阅读理解游戏 所有内容
         :param content: 首次正答数
        """
        if self.read.wait_check_list_page():
            self.read.reading_article_content()  # 文章元素
            question = self.read.question_item()  # 题目
            options = self.read.option_items()
            for i in range(len(question)):
                print(question[i].text)
                print(options[1])
                if options[0][i].get_attribute('class') == self.read.result_right_value:
                    content.append(i)
                print('-----------------------------')

            if self.read.wait_check_list_page():
                self.back_up_button()  # 返回 游戏列表
                self.vue.app_web_switch()

    @teststeps
    def complete_article_operation(self, content):
        """补全文章
        :param content: 首次正答数
        """
        if self.complete.wait_check_list_page():
            self.complete.complete_article_content()  # 文章元素
            self.v_hw.swipe_vertical_web(0.5, 0.95, 0.1)

            if self.complete.wait_check_list_page():
                options = self.complete.option_char()  # 选项 A B C D
                options_content = self.complete.option_content()
                for i in range(len(options)):
                    print('-------------------------------')
                    print(options[i].text, options_content[i].text)
                    if options[i].get_attribute('class') == self.complete.result_right_value:
                        content.append(i)

                if self.complete.wait_check_list_page():
                    self.back_up_button()  # 返回 游戏列表
                    self.vue.app_web_switch()

    @teststeps
    def listen_ergodic_list(self, content):
        """听音连句 遍历列表
        :param content:答对题数
        """
        if self.listen_form.wait_check_page():
            items = self.listen_form.question_items()  # 题数

            status = self.listen_form.result_mine()  # 对错标识
            voice = self.listen_form.result_voice()  # 喇叭按钮
            for i in range(len(items)):
                var = items[i].find_elements_by_xpath('.//div')
                if var[1].text != '':
                    result = self.listen_form.correct_detail(var[0])
                    mine = self.listen_form.correct_detail(var[1])  # 我的
                    print(var[0].text, result, '\n',
                          var[1].text, mine, '\n',
                          var[2].text)
                else:
                    MyAssert().assertEqual(status[i].get_attribute('class'), self.listen_form.result_right_value)
                    content.append(i)
                    print(var[0].text, '\n',
                          var[2].text)

                print('-----------------------------------------')
                voice[i].click()  # 点击发音按钮

        if self.listen_form.wait_check_page():
            self.back_up_button()  # 返回 游戏列表
            self.vue.app_web_switch()

    @teststeps
    def sentence_trans_ergodic_list(self, content):
        """句型转换 遍历列表
        :param content:答对题数
        """
        if self.trans.wait_check_list_page():
            explain = self.trans.result_question()  # 题目
            mine = self.trans.result_mine()  # 我的答案
            answer = self.trans.result_answer()  # 正确答案
            status = self.trans.result_mine_state()  # 对错标识

            count = 0  # 小题数
            for i in range(len(answer)):
                count += 1
                print(explain[i].text, '\n', mine[i].text, '\n', answer[i].text)
                if status[i].get_attribute('class') == self.trans.result_right_value:
                    content.append(i)

                print('-----------------------------------------')
            if self.trans.wait_check_list_page():
                self.back_up_button()  # 返回 游戏列表
            self.vue.app_web_switch()

    @teststeps
    def ears_ergodic_list(self):
        """磨耳朵 列表"""
        if self.ear.wait_check_page():
            sentence = self.ear.ears_sentence()  # 小题
            explain = self.ear.ears_explain()  # 解释
            img = self.ear.ears_img()  # 图片
            if len(img) != len(sentence):
                print('★★★ Error- 图片个数与小题数不一致', len(img), len(sentence))

            count = 0  # 小题数
            for i in range(len(explain)):
                count += 1
                print(sentence[i].text)
                print(explain[i].text)
                print('--------------------------------')
            if self.ear.wait_check_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def picture_list_operation(self, content):
        """听音选图 答题内容"""
        if self.picture.wait_check_list_page():
            self.picture.sound_operation()  # 音频 操作

            ques = self.picture.result_sentence()
            items = self.picture.result_options()  # 选项
            for i in range(len(ques)):
                print(ques[i].text)
                print(items[1][i])
                for j in range(len(items[1])):
                    if items[0][j].get_attribute('class') == self.picture.result_right_value:
                        content.append(items[0][j])
                print('---------------------------------')
            if self.picture.wait_check_list_page():
                self.back_up_button()  # 返回  游戏列表
                self.vue.app_web_switch()

    @teststeps
    def judge_first_achieve(self, achieve, report):
        """验证 首次成绩 与 首次正答
        :param achieve: 首次成绩
        :param report: 首次正答
        """
        item = report.split('/')
        value = int(re.sub("\D", "", item[0]))
        if int(item[1]) != 0:
            answer_num = int(value / int(item[1]) * 100)
        else:
            answer_num = 0
        if achieve != answer_num:
            var = achieve - answer_num
            if var < 0:
                var = -var

            if var > 1:
                print(achieve, answer_num)
                print('★★★ Error- 首次成绩 与首次正答 不匹配:', achieve, report)

        return item

    @teststeps
    def report_score_compare(self, score):
        """验证 首次成绩 与首次正答"""
        value = self.first_report()  # 首次正答
        if score is not None:
            self.judge_first_achieve(int(score), value)  # 验证 首次成绩 与首次正答
            print('-------------------------')
        return value
