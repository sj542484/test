import re
from app.honor.student.games.article_complete import CompleteArticleGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class CompleteText(CompleteArticleGame):

    def __init__(self):
        self.answer = AnswerPage()

    @teststeps
    def play_complete_article_game(self, num, exam_json):
        """补全文章 答卷过程"""
        exam_json['补全文章'] = bank_json = {}
        if self.wait_check_complete_article_page():
            self.next_btn_judge('false', self.fab_next_btn)  # 下一题按钮状态判断
            article = self.rich_text()
            print(article.text)

            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 300)  # 向上拖拽 使题目全部显现
            self.get_options()

            for i in range(num):  # 依次点击选项
                if self.wait_check_complete_article_page():
                    select_text = self.opt_text()[i].text
                    self.opt_char()[i].click()
                    print("选择选项：", select_text)
                    bank_json[i] = select_text
                    index = i
                    self.answer.skip_operator(i, num, '补全文章', self.wait_check_complete_article_page,
                                              self.judge_tip_status, index, next_page=1)

    @teststeps
    def judge_tip_status(self, i):
        if self.opt_char()[i].get_attribute("selected") == "true":
            print('跳转后选中状态未发生改变')
        else:
            print('★★★ Error-- 跳转后选中状态发生改变！')

    @teststep
    def get_options(self):
        opt_char = self.opt_char()
        opt_text = self.opt_text()

        for i in range(len(opt_text)):
            print(opt_char[i].text, ' ', opt_text[i].text)
        return opt_char, opt_text

    @teststeps
    def complete_article_detail(self, bank_info):
        """补全文章 试卷详情页"""
        article = self.rich_text()
        print(article.text, '\n')
        self.drag_operate()
        desc = article.get_attribute('contentDescription')
        answer_order = re.findall(r'\[(.*?)\]', desc)[0]
        right_answer_list = answer_order.split(', ')
        mine_answer_list = list(bank_info.values())
        right = []
        wrong = []

        print("正确答案顺序：", right_answer_list)
        print("我的答案顺序：", mine_answer_list, '\n')
        for i in range(len(right_answer_list)):
            if right_answer_list[i] == mine_answer_list[i]:
                right.append(right_answer_list[i])
            else:
                wrong.append(right_answer_list[i])

        opt_chars = self.opt_char()
        opt_text = self.opt_text()
        for j in range(len(opt_text)):
            if opt_text[j].text in right:
                if opt_chars[j].get_attribute("contentDescription") == 'right':
                    print("选项", opt_chars[j].text, "内容填入正确")
                else:
                    print("★★★选项", opt_chars[j].text, "内容填入正确但是图标显示错误")
            elif opt_text[j].text in wrong:
                if opt_chars[j].get_attribute("contentDescription") == 'error':
                    print("选项", opt_chars[j].text, "内容填入错误")
                else:
                    print("★★★选项", opt_chars[j].text, "内容填入错误但是图标显示正确")
        print('-------------------------------\n')