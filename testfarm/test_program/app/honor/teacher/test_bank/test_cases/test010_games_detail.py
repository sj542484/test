#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
import unittest

from app.honor.teacher.home.vanclass.object_page.home_page import ThomePage
from app.honor.teacher.login.object_page.login_page import TloginPage
from app.honor.teacher.play_games.object_page.banked_cloze_page import BankedCloze
from app.honor.teacher.play_games.object_page.cloze_test_page import ClozePage
from app.honor.teacher.play_games.object_page.picture_dictation_page import PictureDictation
from app.honor.teacher.play_games.object_page.single_choice_page import SingleChoice
from app.honor.teacher.play_games.object_page.tiny_course_page import TinyCourse
from app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from app.honor.teacher.test_bank.test_data.game_type_data import game_type_operation
from app.honor.teacher.user_center.tiny_course.object_page.create_tiny_course_page import CreateTinyCourse
from conf.decorator import setup, teardown, testcase, teststeps
from utils.swipe_screen import SwipeFun
from utils.toast_find import Toast


class GameDetail(unittest.TestCase):
    """游戏详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = TloginPage()
        cls.home = ThomePage()
        cls.question = TestBankPage()
        cls.detail = QuestionDetailPage()
        cls.game = GamesPage()
        cls.filter = FilterPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_game_detail(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_page():  # 页面检查点
            self.question.search_operation()  # 进入首页后 点击 题库tab

            if self.question.wait_check_page():  # 页面检查点
                item = self.question.question_item()  # 题单名
                for i in range(len(item[0])):
                    if self.question.wait_check_page():  # 页面检查点
                        item = self.question.question_item()  # 题单条目
                        if 'autotest_' in item[0][i]:
                            print('##########################################################################')
                            print(item[0][i])
                            item[2][i].click()  # 点击进入该作业

                            self.game_detail_operation()  # 游戏详情页
                            if self.detail.wait_check_page():
                                self.home.back_up_button()  # 返回题库

                if not self.question.wait_check_page('搜索'):
                    self.question.clear_search_operation()  # 清除 搜索词

                if self.question.wait_check_page():  # 检查点
                    self.home.click_tab_hw()  # 返回 主界面
            else:
                print('未进入题库页面')
        else:
            Toast().get_toast()  # 获取toast
            print("未进入主界面")

    @teststeps
    def game_detail_operation(self):
        """游戏详情页"""
        if self.detail.wait_check_page():
            if self.detail.wait_check_list_page():  # 题单详情页
                game = self.detail.game_item()  # 题目
                for i in range(len(game[1])):
                    if self.detail.wait_check_list_page():
                        print('================================================================')
                        game_type = game[3][i]  # 类型
                        if game_type == '闪卡练习':
                            game_type = self.detail.game_mode(game[1][i])  # 获取小游戏模式
                        print(game_type)
                        value = game_type_operation(game_type)  # 小游戏编号
                        # if value == 7:  #
                        #     continue

                        if value is not None:
                            game[2][i].click()  # 进入小游戏
                            self.check_operation(value)  # 查看小游戏详情页 具体操作

    @teststeps
    def check_operation(self, value):
        """查看小游戏详情页 具体操作"""
        if self.game.wait_check_page():  # 游戏详情页
            if self.game.wait_check_list_page():
                print('---------------------游戏详情页---------------------')
                self.game.game_title()  # title
                print(self.game.game_info())
                self.game.teacher_nickname()  # 老师昵称
                count = self.game.game_num()  # 小题数/日期
                print('-----------------------')

                if value in (3, 4, 5, 16, 17, 19):  # 句子/单词 + 解释类
                    sentence = self.game.sentence()  # 句子
                    hint = self.game.hint()  # 解释
                    self.list_operation(value, sentence, hint)
                elif value in (10, 11, 12, 13, 18, 20, 21, 24):  # 单词拼写/听写  闪卡单词
                    word = self.game.word()
                    explain = self.game.explain()
                    self.list_operation(value, word, explain)
                elif value in (1, 2):  # 单选 ('单项选择', '听后选择')
                    if self.game.verify_options():  # 有选项
                        SingleChoice().swipe_operation(count[0])  # 单选题 滑屏及具体操作
                elif value == 6:  # 阅读理解
                    if self.game.verify_content_text():
                        self.game.content()
                elif value == 7:  # 完形填空
                    if ClozePage().verify_content_text():
                        article = ClozePage().article_content()
                        print(article.text)
                        print('-----------------------------------')
                elif value == 8:  # 补全文章
                    if self.game.verify_article_content_text():
                        self.game.article_content()
                elif value == 9:  # 选词填空
                    if BankedCloze().verify_content_text():
                        article = BankedCloze().content_value()
                        print(article.text)
                        print('-----------------------------------')
                elif value == 15:  # ('听音选图')
                    if self.game.verify_img():  # 有 图片选项
                        print('题数:', count[0])
                        PictureDictation().exo_play_operation()
                elif value == 22:  # 微课
                    if CreateTinyCourse().judge_video_exist():
                        TinyCourse().tiny_course_play_operation()  # 播放 视频
                elif value == 23:  # 磨耳朵
                    if self.game.verify_img() and self.game.verify_sentence():  # 有 图片选项 and 句子
                        print('磨耳朵')

            if self.game.wait_check_page():
                self.home.back_up_button()  # 返回题单详情页

    @teststeps
    def list_operation(self, value, word, explain):
        """游戏详情页"""
        content = []
        for k in range(len(explain) - 1):
            self.sentence_hint_operation(value, word, explain, content, k)  # 循环操作

        if int(len(word)) > 3:
            SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
            if self.game.wait_check_list_page():
                sentence = self.game.sentence()  # 句子
                hint = self.game.hint()  # 解释

                for z in range(1, len(hint) - 1):
                    num = hint[z].text
                    if num not in content:
                        self.sentence_hint_operation(value, sentence, hint, content, z)

    @teststeps
    def sentence_hint_operation(self, value, sentence, hint, content, k):
        """单词句子类 循环操作
        :param value: 小游戏编号
        :param sentence: 句子
        :param hint: 解释
        :param content：所有解释，用于翻页操作判断
        :param k: 循环index
        """
        if value == 11:  # '单词拼写'
            remove = self.game.remove_type()  # 去除 类型
            print(sentence[k].text, ' ', hint[k].text, '\n', remove[k].text)
        elif value in (4, 5):  # 听音连句/句型转换
            obstruct = self.game.obstruct()  # 干扰
            print(sentence[k].text, ' ', hint[k].text, '\n', obstruct[k].text)
        elif value in (20, 21) and self.game.verify_img():  # 闪卡单词  有 图片选项
            img = self.game.result_img()
            print(sentence[k].text, ' ', hint[k].text, ' ', img[k].text)
        else:
            print(sentence[k].text, ' ', hint[k].text)
        print('-----------------------------------')

        content.append(hint[k].text)
