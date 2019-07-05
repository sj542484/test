#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from testfarm.test_program.app.honor.teacher.home.object_page.home_page import ThomePage
from testfarm.test_program.app.honor.teacher.login.object_page.login_page import TloginPage
from testfarm.test_program.app.honor.teacher.play_games.object_page.homework_page import Homework
from testfarm.test_program.app.honor.teacher.test_bank.object_page.filter_page import FilterPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.test_bank_page import TestBankPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.question_detail_page import QuestionDetailPage
from testfarm.test_program.app.honor.teacher.test_bank.object_page.games_detail_page import GamesPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase, teststeps
from testfarm.test_program.utils.swipe_screen import SwipeFun
from testfarm.test_program.utils.toast_find import Toast


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

            if self.question.wait_check_page('题单'):  # 页面检查点
                name = self.question.question_name()  # 题单名
                for i in range(len(name[0])):
                    if self.question.wait_check_page('题单'):  # 页面检查点
                        name = self.question.question_name()  # 题单名
                        if 'autotest_' in name[1][i]:
                            print('==========================================================')
                            print(name[1][i])
                            name[0][i].click()  # 点击进入该作业

                            self.game_detail_operation() # 游戏详情页
                            if self.detail.wait_check_page():
                                self.home.back_up_button()  # 返回题库

                if not self.question.wait_check_page('搜索'):
                    self.question.clear_search_operation()  # 清除 搜索词

                if self.question.wait_check_page('题单'):  # 检查点
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
                name = self.question.question_name()  # 题目
                for i in range(len(name[0])):
                    if self.detail.wait_check_list_page():
                        mody = self.question.question_type(i)  # 类型
                        if mody == '闪卡练习':
                            mody = Homework().game_mode(i)  # 获取小游戏模式
                        self.question.question_name()[0][i].click()  # 进入小游戏

                        if self.game.wait_check_page():  # 游戏详情页
                            if self.game.wait_check_list_page():
                                print('---------------------游戏详情页---------------------')
                                # todo 传参var[0] 题数
                                self.game.game_title()  # title
                                print(self.game.game_info())
                                self.game.teacher_nickname()  # 老师昵称
                                count = self.game.game_num()  # 小题数

                                if mody in ('单词听写', '单词拼写', '词汇选择', '猜词游戏', '连连看', '还原单词', '单词学习','单词抄写'):
                                    if self.game.verify_question_index():  # 单词类  题号+单词+解释
                                        index = self.game.question_index()  # 题号
                                        word = self.game.word()  # 单词
                                        explain = self.game.explain()  # 解释
                                        if mody == '单词拼写':
                                            remove = self.game.remove()  # 去除
                                            for k in range(len(explain)):
                                                print(index[k].text, word[k].text, '\n', remove[k].text, '\n', explain[k].text)
                                                if self.game.verify_speak_button():
                                                    self.game.speak_button(k)
                                        else:
                                            for k in range(len(explain)):
                                                print(index[k].text, word[k].text, explain[k].text)
                                                if self.game.verify_speak_button():
                                                    self.game.speak_button(k)
                                        last = index[len(explain)-1].text

                                        if int(len(index)) > 6:
                                            SwipeFun().swipe_vertical(0.5, 0.85, 0.15)
                                            index = self.game.question_index()  # 题号
                                            word = self.game.word()  # 单词
                                            explain = self.game.explain()  # 解释
                                            for z in range(len(explain)):
                                                num = index[z].text
                                                if int(num[:-1]) > int(last[:-1]):
                                                    print(index[z].text, word[z].text, explain[z].text)
                                                    if self.game.verify_speak_button():
                                                        self.game.speak_button(z)

                                elif  mody in ('补全文章', '阅读理解' ,'完形填空' ,'选词填空'):  # 文章类
                                    if self.game.verify_content_text():
                                        self.game.article_content()  # 文章内容
                                elif mody in ('单项选择', '听后选择'):  # 单选/
                                    if self.game.verify_options():  # 有选项
                                        self.game.swipe_operation(int(count))  # 单选题 滑屏及具体操作
                                elif mody in ('强化炼句', '连词成句' , '句型转换','句子学习'):  # 句子类
                                    last = []
                                    sentence = self.game.sentence()  # 句子
                                    hint = self.game.hint()  # 解释
                                    for k in range(len(hint)):
                                        print(sentence[k].text, hint[k].text)
                                        last.append(hint[k].text)

                                    if int(len(sentence)) > 3:
                                        SwipeFun().swipe_vertical(0.5, 0.9, 0.1)
                                        sentence = self.game.sentence()  # 句子
                                        hint = self.game.hint()  # 解释
                                        for z in range(len(hint)):
                                            num = hint[z].text
                                            if num not in last:
                                                print(sentence[z].text, hint[z].text)
                                elif mody in ('听音选图'):
                                    if self.game.verify_img():  # 有 图片选项
                                        self.game.swipe_operation(int(count))  # 单选题 滑屏及具体操作

                            if self.game.wait_check_page():
                                self.home.back_up_button()  # 返回题单详情页
