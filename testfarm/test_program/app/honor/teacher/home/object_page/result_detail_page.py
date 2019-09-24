#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
from selenium.webdriver.common.by import By

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page.complete_article_page import CompleteArticle
from app.honor.teacher.play_games.object_page.listening_form_sentence import ListenFormSentence
from app.honor.teacher.play_games.object_page.picture_dictation_page import PictureDictation
from app.honor.teacher.play_games.object_page.sentence_transform_page import SentenceTrans
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.conf.base_page import BasePage
from conf.base_config import GetVariable as gv
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.get_element_bounds import ElementBounds
from utils.swipe_screen import SwipeFun
from utils.wait_element import WaitElement


class ResultDetailPage(BasePage):
    """结果 详情页"""
    result_answer_value = gv.PACKAGE_ID + "tv_answer"  # 单词
    voice_value = gv.PACKAGE_ID + "iv_speak"  # 发音按钮
    char_value = gv.PACKAGE_ID + "tv_char"  # 选项元素 ABCD
    question_value = gv.PACKAGE_ID + "tv_question"  # 题目

    article_question_value = gv.PACKAGE_ID + "question"  # 题目

    def __init__(self):
        self.wait = WaitElement()
        self.game = GamesPage()
        self.listen = ListenFormSentence()
        self.trans = SentenceTrans()

    @teststeps
    def wait_check_page(self, var):
        """以“title: 小游戏名”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_answer_list_page(self):
        """以“答案 元素”的ID为依据"""
        locator = (By.ID, self.result_answer_value)
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_match_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "explain")
        return self.wait.wait_check_element(locator)

    @teststep
    def game_name(self):
        """游戏名"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "first_report").text
        print(item)

    @teststep
    def first_report(self):
        """首次正答率"""
        item = self.driver\
            .find_element_by_id(gv.PACKAGE_ID + "first_report").text
        print(item)
        return item

    @teststep
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(self.voice_value)[index] \
            .click()

    @teststep
    def result_answer(self):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(self.result_answer_value)
        return ele

    @teststep
    def result_explain(self):
        """解释"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_hint")
        return ele

    @teststep
    def result_mine(self):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "iv_mine")
        return ele

    @teststeps
    def judge_voice(self):
        """判断是否存在 发音按钮"""
        return self.wait.wait_check_element(self.voice_value)

    @teststeps
    def game_mode(self, item):
        """小游戏模式--匹配小括号内游戏模式"""
        m = re.match(".*\（(.*)\）.*", item)  # title中有一个括号
        print(m.group(1))
        return m.group(1)

    # 听音连句
    @teststeps
    def question_item(self):
        """题目数"""
        item = self.driver \
            .find_elements_by_xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout')
        return item

    # 补全文章
    @teststeps
    def complete_article_content(self):
        """文章元素"""
        locator = (By.ID, gv.PACKAGE_ID + "ss_view")
        if self.wait.wait_check_element(locator):
            print(self.wait.wait_find_element(locator).text)
        else:
            print('★★★ Error- 文章元素不存在')

    # 完形填空/阅读理解
    @teststeps
    def cloze_read_content(self):
        """文章元素"""
        locator = (By.ID, gv.PACKAGE_ID + "cl_content")
        if self.wait.wait_check_element(locator):
            print(self.wait.wait_find_element(locator).text)
        else:
            print('★★★ Error- 文章元素不存在')

    @teststep
    def dragger_button(self):
        """拖动按钮"""
        num = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "dragger")
        return num

    @teststeps
    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(gv.PACKAGE_ID + "option_container")
        var = num.size
        return var['height']

    @teststeps
    def drag_operation(self, var='up'):
        """完形填空  拖拽按钮 拖拽操作"""
        drag = self.dragger_button()  # 拖拽 拖动按钮
        loc = ElementBounds().get_element_bounds(drag)  # 获取按钮坐标
        size = self.options_view_size()  # 获取整个选项页面大小
        if var == 'up':
            y = loc[3] - size * 4 / 3
            if loc[3] - size * 4 / 3 < 0:
                y = 0
            self.driver.swipe(loc[2], loc[3], loc[2], y, 1000)  # 向上拖拽
        else:
            self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size - 10, 1000)  # 向下拖拽按钮

    @teststep
    def choice_vocabulary_content(self):
        """选词填空的文章"""
        item = self.driver \
            .find_element_by_id(gv.PACKAGE_ID + "tb_content").text
        print(item)
        print('-----------------------------------')

    @teststep
    def ears_item(self):
        """磨耳朵"""
        ele = self.driver \
            .find_elements_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout")
        return ele

    # 磨耳朵
    @teststeps
    def wait_check_ears_page(self):
        """以“spend_time”的ID为依据"""
        locator = (By.ID, gv.PACKAGE_ID + "img")
        return self.wait.wait_check_element(locator)

    @teststep
    def all_ears_item(self):
        """磨耳朵"""
        ele = self.driver \
            .find_elements_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout/descendant::")

        item = []  # 当前页面中所有题目
        var = []  # 每个题目的内容
        count = []  # 题号元素index
        for i in range(len(ele)):
            if GetAttribute().resource_id(ele[i]) == gv.PACKAGE_ID + 'num':
                count.append(i)
        count.append(len(ele))  # 多余 只为最后一题

        for i in range(len(count) - 1):
            for j in range(count[i], count[i + 1]):
                var.append(ele[j])
            item.append(var)

        return item

    # 单选
    @teststeps
    def wait_check_option_list_page(self):
        """以“选项 元素”的ID为依据"""
        locator = (By.ID, self.char_value)
        return self.wait.wait_check_element(locator)

    @teststep
    def single_question(self):
        """题目"""
        item = self.driver \
            .find_elements_by_id(self.question_value)
        return item

    @teststep
    def option_char(self):
        """选项 A BCD"""
        item = self.driver \
            .find_elements_by_id(self.char_value)
        return item

    @teststep
    def option_item(self):
        """选项 内容"""
        item = self.driver \
            .find_elements_by_id(gv.PACKAGE_ID + "tv_item")
        return item

    @teststeps
    def option_element(self):
        """当前页面中所有题目的选项"""
        ele = self.driver.find_elements_by_xpath(
            "//android.widget.TextView[contains(@resource-id,'%s')]"
            "/parent::android.widget.LinearLayout"
            "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView"
            % self.question_value)
        return ele

    @teststeps
    def article_option_element(self):
        """文章类的 当前页面中所有题目的选项"""
        ele = self.driver.find_elements_by_xpath(
            "//android.widget.TextView[contains(@resource-id,'%s')]"
            "/parent::android.widget.LinearLayout"
            "/android.widget.RadioGroup/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView"
            % self.article_question_value)
        return ele

    @teststeps
    def option_button(self, ele):
        """当前页面中所有题目的选项"""
        result = ele
        item = []  # 当前页面中所有题目的选项
        var = []  # 所有题目的正确选项
        count = []  # text为A的元素index

        for i in range(0, len(result), 2):
            if result[i].text == 'A':
                count.append(i)
        count.append(len(result))  # 多余 只为最后一题

        for i in range(len(count) - 1):
            options = []  # 每个题目的选项
            for j in range(count[i], count[i + 1], 2):
                if j + 1 == count[-1] and (j + 1) % 2 != 0:  # len(ele)为奇数 去掉
                    break

                options.append(result[j + 1].text)  # 选项内容
                if GetAttribute().selected(result[j]) == 'true':
                    var.append(result[j + 1])  # ABCD元素
            item.append(options)

        return item, var

    @teststep
    def question_judge(self, var):
        """元素 resource-id属性值是否为题目"""
        value = GetAttribute().resource_id(var)
        if value == self.question_value:
            return True
        else:
            return False

    @teststeps
    def get_first_num(self, var):
        """获取 当前页面第一个题号"""
        item = var[0].text.split(".")[0]
        return item

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1]

    @teststep
    def article_question(self):
        """文章类游戏  题目"""
        item = self.driver \
            .find_elements_by_id(self.article_question_value)
        return item

    @teststeps
    def article_swipe_operation(self, swipe_num):
        """文章类游戏 滑屏 获取所有题目内容
        :param swipe_num:小题数
        """
        ques_last_index = 0  # 每个页面最后操作过的题号

        if self.wait_check_option_list_page():
            for i in range(swipe_num):
                if ques_last_index < swipe_num:
                    ques_num = self.article_question()  # 题目
                    ques_first_index = int(ques_num[0].text.split(".")[0])

                    if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                        for step in range(0, 10):
                            SwipeFun().swipe_vertical(0.5, 0.5, 0.62)
                            index = int(self.get_first_num(self.article_question()))

                            if index == ques_last_index + 1:  # 正好
                                ques_num = self.article_question()
                                break
                            elif index < ques_last_index + 1:  # 下拉拉过了
                                SwipeFun().swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                                if int(self.get_first_num(self.article_question())) == ques_last_index + 1:  # 正好
                                    ques_num = self.article_question()
                                    break
                            # else:
                            #     print('再下拉一次:', int(self.get_first_num(self.article_question())), ques_last_index)

                    last_one = self.get_last_element()  # 页面中最后一个元素

                    if self.question_judge(last_one):  # 判断最后一项是否为题目
                        options = self.option_button(self.article_option_element())  # 当前页面中所有题目的选项
                        for j in range(len(ques_num) - 1):
                            current_index = int(ques_num[j].text.split(".")[0])
                            if current_index > ques_last_index:
                                print('-----------------------------------------')
                                print(ques_num[j].text, '\n',
                                      '选项:', options[0][j])
                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                    else:  # 判断最后一题是否为选项
                        options = self.option_button(self.article_option_element())  # 当前页面中所有题目的选项
                        for k in range(len(ques_num)):
                            if k < len(ques_num) - 1:  # 前面的题目照常点击
                                current_index = int(ques_num[k].text.split(".")[0])
                                if current_index > ques_last_index:
                                    print('-----------------------------------------')
                                    print(ques_num[k].text, '\n',
                                          '选项:', options[0][k])
                                    if k == len(ques_num) - 2:
                                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                            elif k == len(ques_num) - 1:  # 最后一个题目上滑一部分再进行选择
                                SwipeFun().swipe_vertical(0.5, 0.76, 0.60)
                                ques_num = self.article_question()
                                options = self.option_button(self.article_option_element())  # 当前页面中所有题目的选项
                                for z in range(len(ques_num)):
                                    current_index = int(ques_num[z].text.split(".")[0])
                                    if current_index > ques_last_index:
                                        print('-----------------------------------------')
                                        print(ques_num[z].text, '\n',
                                              '选项:', options[0][z])
                                        ques_last_index = int(ques_num[z].text.split(".")[0])
                                        break

                    if i != swipe_num - 1:
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
                else:
                    break

    @teststeps
    def word_swipe_operation(self, swipe_num):
        """单项选择/听后选择     滑屏 获取所有题目内容"""
        ques_last_index = 0  # 每个页面最后操作过的题号

        if self.wait_check_option_list_page():
            for i in range(swipe_num):
                if ques_last_index < swipe_num:
                    ques_num = self.single_question()  # 题目
                    ques_first_index = int(ques_num[0].text.split(".")[0])

                    if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                        for step in range(0, 10):
                            SwipeFun().swipe_vertical(0.5, 0.5, 0.62)
                            index = int(self.get_first_num(self.single_question()))
                            if index == ques_last_index + 1:  # 正好
                                ques_num = self.single_question()
                                break
                            elif index < ques_last_index + 1:  # 下拉拉过了
                                SwipeFun().swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                                if int(self.get_first_num(self.single_question())) == ques_last_index + 1:  # 正好
                                    ques_num = self.single_question()
                                    break
                            # else:
                            #     print('再下拉一次:', int(self.get_first_num(self.single_question())), ques_last_index)

                    last_one = self.get_last_element()  # 页面中最后一个元素

                    if self.question_judge(last_one):  # 判断最后一项是否为题目
                        options = self.option_button(self.option_element())  # 当前页面中所有题目的选项
                        for j in range(len(ques_num) - 1):
                            current_index = int(ques_num[j].text.split(".")[0])
                            if current_index > ques_last_index:
                                print('-----------------------------------------')
                                print(ques_num[j].text, '\n',
                                      '选项:', options[0][j])
                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                    else:  # 判断最后一题是否为选项
                        options = self.option_button(self.option_element())  # 当前页面中所有题目的选项
                        for k in range(len(ques_num)):
                            if k < len(ques_num) - 1:  # 前面的题目照常点击
                                current_index = int(ques_num[k].text.split(".")[0])
                                if current_index > ques_last_index:
                                    print('-----------------------------------------')
                                    print(ques_num[k].text, '\n',
                                          '选项:', options[0][k])
                                    if k == len(ques_num) - 2:
                                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                            elif k == len(ques_num) - 1:  # 最后一个题目上滑一部分再进行选择
                                SwipeFun().swipe_vertical(0.5, 0.76, 0.60)
                                ques_num = self.single_question()
                                options = self.option_button(self.option_element())  # 当前页面中所有题目的选项
                                for z in range(len(ques_num)):
                                    current_index = int(ques_num[z].text.split(".")[0])
                                    if current_index > ques_last_index:
                                        print('-----------------------------------------')
                                        print(ques_num[z].text, '\n',
                                              '选项:', options[0][z])
                                        ques_last_index = int(ques_num[z].text.split(".")[0])
                                        break

                    if i != swipe_num - 1:
                        SwipeFun().swipe_vertical(0.5, 0.9, 0.27)  # 滑屏
                else:
                    break

    @teststeps
    def hw_detail_operation(self, index, num, achieve=None):
        """答题情况 详情页
        :param index:游戏编号
        :param num:小题数
        :param achieve:成绩
        """
        content = []  # 答对的 小题数
        value = self.first_report()  # 首次正答
        if achieve is not None:
            self.judge_first_achieve(int(achieve), value)  # 验证 首次成绩 与首次正答
            print('-------------------------')

        var = value.split('/')
        if num != int(var[1]):  # 验证 小题数
            print('★★★ Error- 小题数不匹配', var[1], num)
        ques_num = int(re.sub("\D", "", var[0]))  # 首次正答题数

        if index in (1, 2, 10):  # 单项选择/听后选择/单词听写
            if index == 1 and self.game.verify_voice_button():  # 听后选择
                self.game.play_button()  # 播音按钮
            self.word_swipe_operation(num)  #
        elif index in (6, 7):  # 有选项
            self.cloze_read_content()  # 文章元素
            self.drag_operation()  # 向上拖拽按钮操作
            self.article_swipe_operation(num)  # 单选题滑屏及具体操作
        elif index == 15:  # 听音选图
            PictureDictation().swipe_operation(num)  # 选图题滑屏及具体操作
        elif index == 8:  # 补全文章
            self.complete_article(ques_num)
        elif index == 9:  # 选词填空
            if self.game.verify_hint_word():  # 有提示词
                self.game.hint_word()  # 提示词：
                self.game.prompt_word()  # 提示的内容

            self.choice_vocabulary_content()  # 文章
        elif index == 21:
            print('口语')  # todo
            ThomePage().back_up_button()
        elif index == 22:
            print('口语')  # todo
            ThomePage().back_up_button()
        elif index == 4:  # 听音连句
            if self.listen.wait_check_correct_page():
                self.answer_explain_type(content, self.listen_ergodic_list, self.question_item)
        elif index == 5:  # 句型转换
            if self.wait_check_answer_list_page():
                self.answer_explain_type(content, self.sentence_trans_ergodic_list, self.trans.result_question)
        elif index == 16:  # 连连看
            self.answer_explain_type(content, self.ergodic_list, self.result_answer)  # 不需要统计答对的小题
        elif index == 18:  # 磨耳朵
            if self.wait_check_ears_page():
                self.answer_explain_type(ques_num, self.ears_ergodic_list, self.ears_item)
        else:  # 3强化炼句/11单词拼写/12猜词游戏/13词汇选择/14闪卡练习/19连词成句/20还原单词
            if self.wait_check_answer_list_page():
                self.answer_explain_type(content, self.ergodic_list, self.result_explain)

        if index in (3, 4, 5, 11, 12, 13, 14, 19, 20):
            if len(content) != ques_num:
                print('★★★ Error- 首次正答 与答题情况不匹配', ques_num, content)
            else:
                print('答对{}题，答错{}题'.format(len(content), num - len(content)))
        print('==========================================================')

    @teststeps
    def complete_article(self, content):
        """补全文章
        :param content: 首次正答数
        """
        self.complete_article_content()  # 文章元素
        CompleteArticle().drag_operation()  # 向上拖拽按钮操作

        count = 0  # 小题数
        options = self.option_char()  # 选项 A B C D
        for i in range(len(options)):
            print('-------------------------------')
            print(options[i].text)
            if GetAttribute().selected(options[i]) == 'true':
                count += 1
                status = GetAttribute().description(options[i])
                print(status)
                if status == 'right':
                    content.append(i)

    @teststeps
    def answer_explain_type(self, num, func, element, content=None):
        """答案/解释类型
        :param num: 首次正答数
        :param func: 遍历方法
        :param element: 获取length值
        :param content: 翻页
        """
        if content is None:
            content = []

        item = 0
        if self.judge_voice():  # 判断存在 发音按钮
            item = 1

        hint = element()  # 解释
        if len(hint) > 4 and not content:
            if item == 0:
                func(num, len(hint) - 1)
            else:
                func(num, len(hint) - 1, 0, item)
            content = [hint[-2].text]

            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_explain_type(num, func, element, content)
        else:
            var = 0
            if content:
                for k in range(len(hint)):
                    if content[0] == hint[k].text:
                        var += k + 1
                        break

            if item == 0:
                func(num, len(hint), var)
            else:
                func(num, len(hint), var, item)

    @teststeps
    def ergodic_list(self, content, length, var=0, item=0):
        """遍历列表
        :param item: 是否有发音按钮
        :param content:答对题数
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        explain = self.result_explain()  # 解释
        answer = self.result_answer()  # 答案
        mine = self.result_mine()  # 对错标识

        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            print('解释:', explain[i].text)  # 解释
            print('单词:', answer[i].text)  # 正确word
            mode = GetAttribute().selected(mine[i])
            print(mode)

            if mode == 'true':
                content.append(i)

            print('-----------------------------------------')
            if item == 1:
                self.result_voice(i)  # 点击发音按钮

    @teststeps
    def listen_ergodic_list(self, content, length, var=0):
        """听音连句 遍历列表
        :param content:答对题数
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        answer = self.listen.correct()  # 答案
        mine = self.listen.result_answer()  # 我的
        explain = self.listen.explain()  # 解释
        status = self.listen.result_mine()  # 对错标识

        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            print(explain[i].text, '\n', mine[i].text, '\n', answer[i].text)
            mode = GetAttribute().selected(status[i])
            print(mode)
            if mode == 'true':
                content.append(i)

            print('-----------------------------------------')
            self.listen.result_voice(i)  # 点击发音按钮

    @teststeps
    def sentence_trans_ergodic_list(self, content,  length, var=0):
        """句型转换 遍历列表
        :param content:答对题数
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        explain = self.trans.result_question()  # 题目
        mine = self.trans.result_mine()  # 我的答案
        answer = self.trans.result_answer()  # 正确答案
        status = self.trans.result_mine_state()  # 对错标识

        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            print(explain[i], '\n', mine[0][i], '\n', answer[i])
            mode = GetAttribute().selected(status[i])
            print(mode)
            if mode == 'true':
                content.append(i)

            print('-----------------------------------------')

    @teststeps
    def ears_ergodic_list(self, ques_num, length, var=0):
        """磨耳朵 遍历列表
        :param ques_num:答对题数
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        print(ques_num)
        item = self.all_ears_item()

        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            for j in range(len(item[i])):
                print(item[i].text)
                print('--------------------------------')

    @teststeps
    def judge_first_achieve(self, achieve, report):
        """验证 首次成绩 与 首次正答
        :param achieve: 首次成绩
        :param report: 首次正答
        """
        item = report.split('/')
        value = int(re.sub("\D", "", item[0]))

        answer_num = int(value / int(item[1]) * 100)
        if achieve != answer_num:
            var = achieve - answer_num
            if var < 0:
                var = -var

            if var > 1:
                print(achieve, answer_num)
                print('★★★ Error- 首次成绩 与首次正答 不匹配:', achieve, report)
