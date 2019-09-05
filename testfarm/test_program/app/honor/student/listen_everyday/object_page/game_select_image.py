#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/5 20:03
# -----------------------------------------
import random
import time

from app.honor.student.library.object_pages.games.listen_select_img import ListenSelectImg
from app.honor.student.library.object_pages.result_page import ResultPage
from conf.decorator import teststep
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class ListenSelectImagePage(ListenSelectImg):
    @teststep
    def play_listen_select_image_game(self):
        """听音选图游戏过程"""
        print('----- < 听音选图 > -----\n')
        mine_answer = {}
        total_num = self.public.rest_bank_num()
        for i in range(total_num):
            if self.wait_check_listen_image_page():
                ques_index = self.ques_index()
                question = ques_index + '.' + self.listen_question()
                print('问题：', question)
                self.public.rate_judge(total_num, i)
                random_index = random.randint(0, len(self.image_options()) - 1)
                random_choice = self.image_options()[random_index]
                choice_desc = random_choice.get_attribute('contentDescription')
                print('选择答案：', choice_desc)
                mine_answer[question] = choice_desc
                random_choice.click()
                time.sleep(1)
                print('-'*30, '\n')
        while True:
            self.fab_commit_btn().click()
            if Toast().find_toast('请听完音频，再提交答案'):
                time.sleep(3)
            else:
                break
        return mine_answer

    @teststep
    def listen_select_image_game_result_operate(self, mine_answer):
        """听音选图结果页操作"""
        if ResultPage().wait_check_answer_page():
            self.voice_play_btn().click()
            banks = []
            while True:
                questions = self.result_question()
                for i, ques in enumerate(questions):
                    if ques.text in banks:
                        continue
                    else:
                        if i == len(questions) - 1:
                            self.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        banks.append(ques.text)
                        print('问题：', ques.text)
                        mine = mine_answer[ques.text]
                        print('我的选择：', mine)
                        result_images = self.result_ques_images(ques.text)
                        # print([x.get_attribute('contentDescription') for x in result_images])
                        for x in result_images:
                            desc = x.get_attribute('contentDescription')
                            if mine in desc:
                                if GetAttribute().selected(x) == 'false':
                                    print('★★★ 所选与页面展示的不一致')
                                if 'true' in desc:
                                    print('选择正确', mine)
                                elif 'false' in desc:
                                    print('选择错误', end=' ')
                            else:
                                if 'true' in desc:
                                    print('正确选项：', desc.split('##')[0].strip())

                    print('-' * 20, '\n')

                if len(banks) != len(mine_answer):
                    self.screen_swipe_up(0.5, 0.9, 0.5, 1000)
                else:
                    break
        self.click_back_up_button()
