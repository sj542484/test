
from app.honor.student.games.sentence_link_word import LinkWordToSentenceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.word_book_rebuild.object_page.restore_word_page import WordRestore
from conf.decorator import teststep, teststeps


class Conjunctions(LinkWordToSentenceGame):
    """连词成句"""

    def __init__(self):
        self.home = HomePage()
        self.restore = WordRestore()
        self.answer = AnswerPage()

    @teststep
    def detail_answers(self):
        """详情页 句子"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_answer')
        return ele

    @teststep
    def detail_explain(self, var):
        """详情页 解释"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/'
                                                'following-sibling::android.widget.TextView' % var)
        return ele.text

    @teststep
    def detail_icon(self, var):
        """详情页 图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"%s")]/../'
                                                'following-sibling::android.widget.ImageView' % var)
        return ele

    @teststeps
    def play_conjunctions_game(self, num, exam_json):
        """连词成句 游戏过程"""
        exam_json['连词成句'] = bank_json = {}
        for i in range(num):
            explain = self.sentence_explain()
            print(explain)

            word_alpha = self.word_alpha()
            word = [x.text for x in word_alpha]
            print('连句前句子：', ' '.join(word))

            for j in range(len(word_alpha)-1, -1, -1):
                self.restore.drag_operate(self.word_alpha()[j], self.word_alpha()[0])

            finish_word = [x.text for x in self.word_alpha()]
            print('连句后句子：', ' '.join(finish_word))
            bank_json[explain] = ' '.join(finish_word)
            self.answer.skip_operator(i, num, "连词成句", self.wait_check_link_sentence_page,
                                      self.judge_tip_status, finish_word)

    @teststep
    def judge_tip_status(self, finish_word):
        sentence = ''.join([x.text for x in self.word_alpha()])
        if finish_word == sentence:
            print('题目跳转后句子顺序未发生变化')
        else:
            print("★★★题目跳转后句子顺序发生变化!")

    @teststeps
    def conjunctions_detail(self, bank_info):
        tips = []
        while True:
            answers = self.detail_answers()
            for i in range(len(answers)):
                ans = answers[i].text
                if ans in tips:
                    continue
                else:
                    tips.append(ans)
                    if i != len(answers) - 1:
                        self.result_check(ans, bank_info)
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.6, 1000)
                        self.result_check(ans, bank_info)
                        self.home.screen_swipe_down(0.5, 0.6, 0.75, 1000)
            if len(tips) < len(bank_info):
                self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
            else:
                break

    @teststeps
    def result_check(self, answer, bank_info):
        explain = self.detail_explain(answer)
        mine_icon = self.detail_icon(answer)

        mine_answer = bank_info[explain]
        print('解释：', explain)
        print('答案：', answer)
        print('我的答案：', mine_answer)

        if answer == mine_answer:
            if mine_icon.get_attribute('selected') == 'true':
                print('结果核实正确')
            else:
                print('★★★ 答案正确图标显示错误！')
        else:
            if mine_icon.get_attribute('selected') == 'false':
                print('结果核实正确')
            else:
                print('★★★ 答案不正确图标显示正确！')
        print('-'*20, '\n')