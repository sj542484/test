# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/9 13:38
# -------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.sentence_link_word import LinkWordToSentenceGame
from app.honor.student.library.object_pages.library_public_page import LibraryPubicPage
from app.honor.student.library.object_pages.games.restore_word import RestoreWord
from app.honor.student.library.object_pages.result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class LinkToSentence(LinkWordToSentenceGame):

    def __init__(self):
        self.public = LibraryPubicPage()

    @teststep
    def result_explain(self):
        """正确答案"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_hint')
        return ele

    @teststep
    def result_answer_by_explain(self, explain):
        """结果页句子"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/preceding-sibling::android.widget.TextView'.format(explain))
        return ele.text

    @teststep
    def mine_icon_by_sentence(self, explain):
        """对错图标"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../following-sibling::android.widget.ImageView'
                                                .format(explain))
        return ele

    @teststep
    def get_sentence_size(self, explain):
        """获取句子的大小"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../..'.format(explain))
        return ele.size


    @teststeps
    def link_sentence_operate(self, fq, sec_answer):
        """连词成句操作"""
        timer = []
        mine_answer = {}
        total_num = self.public.rest_bank_num()
        for i in range(0, total_num):
            if self.wait_check_link_sentence_page():
                self.next_btn_judge('false', self.fab_commit_btn)             # 判断下一步状态
                self.public.rate_judge(total_num, i)
                explain = self.sentence_explain().strip()
                print('解释：', explain)
                if fq == 1:
                    RestoreWord().drag_operate(self.word_alpha()[-1], self.word_alpha()[0])
                    self.next_btn_operate('true', self.fab_commit_btn)
                else:
                    right_answer = sec_answer[explain]
                    self.do_right_operate(right_answer)

                if not self.wait_check_right_answer_page():
                    print('★★★ 点击下一步后未发现正确答案')
                else:
                    right_answer = self.right_answer()
                    print(right_answer)
                mine = ' '.join([x.text for x in self.word_alpha()])
                mine_answer[explain] = mine
                print('我的答案：', mine)
                print('-' * 20, '\n')
                timer.append(self.public.bank_time())
                self.fab_next_btn().click()

        self.public.judge_timer(timer)
        done_answer = mine_answer if fq == 1 else sec_answer
        return done_answer, total_num

    @teststeps
    def link_sentence_result_operate(self, mine_answer):
        """连词成句结果页处理"""
        if ResultPage().wait_check_answer_page():
            right_answer = {}
            right, wrong = [], []
            answer_info = []
            print('===== 查看结果页 =====\n')
            while len(answer_info) < len(mine_answer):
                result_explains = self.result_explain()
                for explain in result_explains:
                    if explain.text in answer_info:
                        continue
                    else:                                           # 倒数第一道题，向上滑出一道题的距离
                        result_explain = explain.text
                        print('解释：', result_explain)
                        answer_info.append(result_explain)
                        result_answer = self.result_answer_by_explain(result_explain)
                        print('答案：', result_answer)

                        mine_icon = self.mine_icon_by_sentence(result_explain)
                        if mine_answer[result_explain] != result_answer:
                            if GetAttribute().selected(mine_icon) == 'true':       # 校验图标是否正确
                                print('★★★ 我的答案与正确答案不一致，但是图标显示正确！')
                            else:
                                print('图标验证正确')
                            wrong.append(result_explain)

                        else:
                            if GetAttribute().selected(mine_icon) == 'false':
                                print('★★★ 我的答案与正确答案一致，但是图标显示不正确！')
                            else:
                                print('图标验证正确')
                            right.append(result_explain)
                        right_answer[result_explain] = result_answer

                    print('-'*30, '\n ')
                self.screen_swipe_up(0.5, 0.9, 0.3, 1000)

            print('正确答案：', right_answer)
            self.click_back_up_button()
            return wrong, right, right_answer

    @teststep
    def do_right_operate(self, right_answer):
        """连词成绩做对操作"""
        right_word_list = right_answer.split(' ')
        index = 0
        print('初始句子：', ' '.join([x.text for x in self.word_alpha()]).strip())
        for i in range(index, len(right_word_list)):
            alpha_list = self.word_alpha()
            for j in range(len(alpha_list)):
                if alpha_list[j].text == right_word_list[i]:
                    if alpha_list[j].text != alpha_list[index].text:
                        RestoreWord().drag_operate(alpha_list[j], alpha_list[index])
                    index += 1
                    break
            if ' '.join([x.text for x in self.word_alpha()]).strip() == right_answer:
                break