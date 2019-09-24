#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import random
import unittest
import re

from app.honor.teacher.home.object_page.home_page import ThomePage
from app.honor.teacher.play_games.object_page.complete_article_page import CompleteArticle
from app.honor.teacher.home.object_page.result_detail_page import ResultDetailPage
from app.honor.teacher.home.test_data.paper_detail_data import game_type_operation
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.home.object_page.paper_detail_page import PaperPage
from app.honor.teacher.home.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.teacher.home.object_page.vanclass_page import VanclassPage
from app.honor.teacher.home.test_data.vanclass_data import GetVariable as gv
from app.honor.teacher.play_games.object_page.listening_form_sentence import ListenFormSentence
from app.honor.teacher.play_games.object_page.matching_exercises_page import MatchingExercises
from app.honor.teacher.play_games.object_page.sentence_transform_page import SentenceTrans
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.get_attribute import GetAttribute
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class VanclassPaper(unittest.TestCase):
    """本班试卷 -完成情况tab 二级详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.paper = PaperPage()
        cls.get = GetAttribute()
        cls.result = ResultDetailPage()

        cls.game = GamesPage()
        cls.listen = ListenFormSentence()
        cls.trans = SentenceTrans()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vanclass_paper_game_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.home.into_vanclass_operation(gv.VANCLASS)  # 进入 班级详情页
            if self.van.wait_check_page(gv.VANCLASS):  # 页面检查点
                if self.van.wait_check_list_page():  # 加载完成

                    self.van.vanclass_paper()  # 进入 本班卷子
                    title = gv.PAPER_TITLE.format(gv.VANCLASS)
                    if self.detail.wait_check_page(title):  # 页面检查点
                        if self.detail.wait_check_empty_tips_page():  # 无卷子时
                            self.detail.no_data()  # 暂无数据
                            # self.detail.goto_paper_pool()  # 点击 去题库 按钮
                        elif self.detail.wait_check_list_page():  # 有卷子
                            print('本班试卷:')
                            name = self.detail.hw_name()  # 试卷name
                            count = []
                            for i in range(len(name)):
                                if self.detail.wait_check_list_page():  # 有卷子
                                    name = self.detail.hw_name()  # 试卷name
                                    progress = self.detail.progress()  # 进度
                                    text = name[i].text
                                    pro = progress[i].text  # int(re.sub("\D", "", progress[i].text))
                                    if int(pro[3]) != 0 and self.home.brackets_text_in(text) == '试卷':
                                        count.append(i)
                            if len(count) == 0:
                                print('暂无习题作业包')
                            else:
                                index = random.randint(0, len(count) - 1)
                                text = name[count[index]].text
                                name[count[index]].click()  # 进入试卷
                                if self.paper.wait_check_page():  # 页面检查点
                                    print('###########################################################')
                                    print(text)
                                    self.finish_situation_operation()  # 具体操作

                                    if self.paper.wait_check_st_list_page():
                                        self.home.back_up_button()  # 返回 试卷列表
                            if self.paper.wait_check_page():  # 页面检查点
                                self.home.back_up_button()
                    else:
                        print('★★★ Error- 未进入 本班试卷页面')
                    if self.van.wait_check_page(title):  # 本班卷子 页面检查点
                        self.home.back_up_button()  # 返回 班级页面
            else:
                print('★★★ Error- 未进入班级:', gv.VANCLASS)
            if self.van.wait_check_page(gv.VANCLASS):  # 班级 页面检查点
                self.home.back_up_button()  # 返回 主界面
        else:
            Toast().get_toast()  # 获取toast
            print("★★★ Error- 未进入主界面")

    @teststeps
    def finish_situation_operation(self):
        """完成情况tab 具体操作"""
        complete = self.paper.finished_tab()  # 完成情况 tab
        if self.get.selected(complete) is False:
            print('★★★ Error- 未默认在 完成情况 tab页')
        else:
            print('---------------------完成情况tab---------------------')
            if self.paper.wait_check_st_list_page():
                status = self.paper.st_score()  # 学生完成与否

                for i in range(len(status)):
                    if self.paper.wait_check_st_list_page():
                        name = self.paper.st_name()  # 学生name
                        status = self.paper.st_score()  # 学生完成与否
                        if status[i].text == '未完成':
                            print('-------------------------------------------')
                            print('学生 %s 还未完成该试卷' % name[i].text)
                        else:
                            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            text = name[i].text
                            name[i].click()  # 进入学生的答题情况页

                            if self.detail.wait_check_page(text):  # 页面检查点
                                print('学生 %s 答题情况:' % text)
                                self.paper_detail_operation(text)  # 试卷 详情页

                                if self.detail.wait_check_page(text):
                                    self.home.back_up_button()  # 返回 试卷列表
            elif self.home.wait_check_empty_tips_page():
                print('暂无数据')

    @teststeps
    def paper_detail_operation(self, st, content=None):
        """答题具体信息 页面"""
        if content is None:
            content = []

        if self.paper.wait_check_paper_list_page():
            mode = self.paper.game_title()  # 游戏类型 元素
            info = self.paper.game_desc()  # 共x题 xx分

            if len(info) > 4 and not content:
                content = [mode[len(info)-2].text, info[-2].text]

                self.result_detail_operation(0, len(info)-1, st)  # 答题详情页

                if self.detail.wait_check_page(st):  # 页面检查点
                    SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
                    self.paper_detail_operation(st, content)
            else:
                var = 0
                if content:
                    for k in range(len(mode)):
                        if content[0] == mode[k].text and content[1] == info[k].text:
                            var += k + 1
                            break

                self.result_detail_operation(var, len(info), st)  # 答题详情页

    @teststeps
    def result_detail_operation(self, var, length, st):
        """答题 详情页"""
        for i in range(var, length):
            if self.detail.wait_check_page(st):  # 页面检查点
                if self.paper.wait_check_paper_list_page():
                    mode = self.paper.game_title()  # 游戏类型 元素
                    mine = self.paper.game_score()[i+1].text  # 我的得分
                    info = self.paper.game_desc()[i].text  # 共x题 xx分

                    if self.detail.wait_check_page(st):  # 页面检查点
                        text = mode[i].text.split(' ')[0]  # 游戏类型
                        print(text)
                        print(mine)
                        mine = int(re.sub("\D", "", mine))  # 我的得分

                        var = info.split(' ')
                        count = int(re.sub("\D", "", var[0]))  # 小题数
                        score = int(re.sub("\D", "", var[1]))  # 总分数

                        value = game_type_operation(text)
                        mode[i].click()  # 进入游戏 详情页
                        if self.paper.wait_check_per_detail_page(text):
                            if self.paper.wait_check_per_answer_page():
                                print(info)
                                self.hw_detail_operation(value, count, score, mine)  # 答题情况

                                if self.paper.wait_check_per_detail_page(text):
                                    self.home.back_up_button()  # 返回 st答题详情页

    @teststeps
    def hw_detail_operation(self, index, num, score, achieve=None):
        """答题情况 详情页
        :param index:游戏编号
        :param num:小题数
        :param score: 总分数
        :param achieve:我的成绩
        """
        content = []  # 答对的 小题数
        value = self.result.first_report()  # 首次正答

        if achieve is not None:
            self.judge_first_achieve(value, score, achieve)  # 验证 成绩 与首次正答
            print('-------------------------')

        var = value.split('/')
        if num != int(var[1]):  # 验证 小题数
            print('★★★ Error- 小题数不匹配', var[1], num)
        ques_num = int(re.sub("\D", "", var[0]))  # 首次正答题数

        if index in (1, 2, 10):  # 单项选择/听后选择/单词听写
            if index == 1 and self.game.verify_voice_button():  # 听后选择
                self.game.play_button()  # 播音按钮
            self.word_swipe_operation(num)  #
        elif index in (6, 7,):  # 有选项
            if index in (6, 7,):  # 完形填空/阅读理解
                self.result.cloze_read_content()  # 文章元素
                self.result.drag_operation()  # 向上拖拽按钮操作

            self.result.article_swipe_operation(num)  # 单选题滑屏及具体操作
        elif index == 16:  # 连连看
            if self.result.wait_check_match_detail_page():
                self.answer_explain_type(MatchingExercises().explain_ergodic_list, MatchingExercises().result_word(), 9)
            else:
                self.answer_explain_type(MatchingExercises().img_ergodic_list, MatchingExercises().result_word(), 9)
        elif index == 8:  # 补全文章
            self.complete_article(ques_num)
        elif index == 9:  # 选词填空
            if self.game.verify_hint_word():  # 有提示词
                self.game.hint_word()  # 提示词：
                self.game.prompt_word()  # 提示的内容

            self.result.choice_vocabulary_content()  # 文章
        elif index == 4:  # 听音连句
            if self.listen.wait_check_correct_page():
                self.answer_explain_type(content, self.listen_ergodic_list, self.result.question_item)
        elif index == 5:  # 句型转换
            if self.result.wait_check_answer_list_page():
                self.answer_explain_type(content, self.sentence_trans_ergodic_list, self.trans.result_question)
        else:  # 3强化炼句/11单词拼写/12猜词游戏/13词汇选择/15连词成句/14还原单词
            if self.result.wait_check_answer_list_page():
                max_len = 4
                if index == 3:
                    max_len = 3
                self.answer_explain_type(content, self.ergodic_list, self.result.result_explain, max_len)

        print('==========================================================')

    @teststeps
    def complete_article(self, content):
        """补全文章
        :param content: 首次正答数
        """
        self.result.complete_article_content()  # 文章元素
        CompleteArticle().drag_operation()  # 向上拖拽按钮操作

        count = 0  # 小题数
        options = self.result.option_char()  # 选项 A B C D
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
    def answer_explain_type(self, num, func, element, max_len=4, content=None):
        """答案/解释类型
        :param max_len:  最大值
        :param num: 首次正答数
        :param func: 遍历方法
        :param element: 获取length值
        :param content: 翻页
        """
        if content is None:
            content = []

        item = 0
        if self.result.judge_voice():  # 判断存在 发音按钮
            item = 1

        hint = element()  # 解释
        if len(hint) > 4 and not content:
            if item == 0:
                func(num, len(hint) - 1)
            else:
                func(num, len(hint) - 1, 0, item)
            content = [hint[-2].text]

            SwipeFun().swipe_vertical(0.5, 0.85, 0.1)
            self.answer_explain_type(num, func, element, max_len, content)
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
        explain = self.result.result_explain()  # 解释
        answer = self.result.result_answer()  # 答案
        mine = self.result.result_mine()  # 对错标识

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
                self.result.result_voice(i)  # 点击发音按钮

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
    def sentence_trans_ergodic_list(self, content, length, var=0):
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
    def ears_ergodic_list(self, content, length, var=0):
        """磨耳朵 遍历列表
        :param content:答对题数
        :param length: 遍历的最大值
        :param var:遍历的最小值
        """
        print(content)
        item = self.result.all_ears_item()

        count = 0  # 小题数
        for i in range(var, length):
            count += 1
            for j in range(len(item[i])):
                print(item[i].text)
                print('--------------------------------')

    @teststeps
    def judge_first_achieve(self, report, game_score, game_achieve):
        """验证 首次成绩 与 首次正答
        :param report: 首次正答
        :param game_score: 总分数（17分）
        :param game_achieve: 我的成绩 （获得0分）
        """
        item = report.split('/')  # 首次正答
        count = int(re.sub("\D", "", item[0]))
        num = int(re.sub("\D", "", item[1]))

        achieve = self.paper.game_score()[0].text  # 得分X分/共x分
        var = achieve.split('/')
        mine = int(re.sub("\D", "", var[0]))
        score = int(re.sub("\D", "", var[1]))

        if game_score != score:
            print('★★★ Error- 总题数不一致', game_score, score)
        if game_achieve != mine:
            print('★★★ Error- 我的得分不一致', game_achieve, mine)

        answer_num = round(count / num, 1)  # 题数（小数）
        mine_achieve = round(mine / score, 1)  # 分数（小数）

        if mine_achieve != answer_num:
            var = mine_achieve - answer_num
            if var < 0:
                print(mine_achieve, answer_num)
                print('★★★ Error- 成绩 小于 首次正答:', achieve, report)

    @teststeps
    def word_swipe_operation(self, swipe_num):
        """单项选择/听后选择     滑屏 获取所有题目内容"""
        ques_last_index = 0  # 每个页面最后操作过的题号

        if self.result.wait_check_option_list_page():
            for i in range(swipe_num):
                if ques_last_index < swipe_num:
                    ques_num = self.result.single_question()  # 题目
                    ques_first_index = int(ques_num[0].text.split(".")[0])

                    if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                        for step in range(0, 10):
                            SwipeFun().swipe_vertical(0.5, 0.5, 0.62)
                            index = int(self.result.get_first_num(self.result.single_question()))
                            if index == ques_last_index + 1:  # 正好
                                ques_num = self.result.single_question()
                                break
                            elif index < ques_last_index + 1:  # 下拉拉过了
                                SwipeFun().swipe_vertical(0.5, 0.6, 0.27)  # 滑屏
                                if int(self.result.get_first_num(self.result.single_question())) == ques_last_index + 1:  # 正好
                                    ques_num = self.result.single_question()
                                    break
                            # else:
                            #     print('再下拉一次:', int(self.get_first_num(self.single_question())), ques_last_index)

                    last_one = self.result.get_last_element()  # 页面中最后一个元素

                    if self.result.question_judge(last_one):  # 判断最后一项是否为题目
                        options = self.result.option_button(self.result.option_element())  # 当前页面中所有题目的选项
                        for j in range(len(ques_num) - 1):
                            current_index = int(ques_num[j].text.split(".")[0])
                            if current_index > ques_last_index:
                                print('-----------------------------------------')
                                print(ques_num[j].text, '\n',
                                      '选项:', options[0][j])
                        ques_last_index = int(ques_num[-2].text.split(".")[0])
                    else:  # 判断最后一题是否为选项
                        options = self.result.option_button(self.result.option_element())  # 当前页面中所有题目的选项
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
                                ques_num = self.result.single_question()
                                options = self.result.option_button(self.result.option_element())  # 当前页面中所有题目的选项
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
