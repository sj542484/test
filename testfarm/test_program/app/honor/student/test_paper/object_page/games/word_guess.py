import random
from app.honor.student.games.word_guess import GuessWordGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps


class GuessingWord(GuessWordGame):

    def __init__(self):
        self.home = HomePage()
        self.answer = AnswerPage()

    @teststeps
    def play_guessing_word_game(self, num, exam_json):
        """猜词游戏 """
        exam_json['猜词游戏'] = bank_json = {}
        for i in range(num):
            explain = self.word_explain()
            print('解释：', explain)

            word = self.guess_word()
            print('填充前单词：', word)

            key_put = []
            while '_' in word:
                word = self.guess_word()
                enable_key = [x for x in self.keyboard_key() if x.get_attribute('enabled') == 'true']
                random_index = random.randint(0, len(enable_key)-1)
                enable_key[random_index].click()
                key_put.append(enable_key[random_index].text)

            print('我输入的单词：', ''.join(key_put))
            bank_json[explain] = ''.join(key_put)
            finish_word = self.guess_word()
            print('最终提示单词：', finish_word)
            self.answer.skip_operator(i, num, '猜词游戏', self.wait_check_guess_word_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        if '_' in self.guess_word():
            print('★★★ Error-- 跳转回来题目处于未完成状态')
        else:
            print('滑屏后题目处于完成状态')