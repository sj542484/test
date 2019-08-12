import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class CompleteText(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.homework = Homework()
        self.answer = AnswerPage()

    @teststep
    def wait_check_complete_article_page(self):
        locator = (By.ID, '{}ss_view'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def drag_btn(self):
        ele = self.driver.find_element_by_id('{}dragger'.format(self.id_type()))
        return ele

    @teststep
    def article(self):
        """文章"""
        ele = self.driver.find_element_by_id('{}ss_view'.format(self.id_type()))
        return ele


    @teststep
    def opt_char(self):
        """选项 字母 ABCD"""
        ele = self.driver.find_elements_by_id('{}tv_char'.format(self.id_type()))
        return ele

    @teststep
    def opt_text(self):
        """选项 文本"""
        ele = self.driver.find_elements_by_id('{}tv_item'.format(self.id_type()))
        return ele

    @teststep
    def next_button(self):
        ele = self.driver.find_element_by_id('{}fab_next'.format(self.id_type()))
        return ele

    @teststep
    def next_button_judge(self, var):
        next_btn = self.next_button()
        item = next_btn.get_attribute('selected')
        if item != var:  # 测试 下一步 按钮 状态
            print('★★★ 下一步按钮 状态Error', item)

    @teststep
    def next_button_operate(self, var):
        self.next_button().click()
        self.next_button_judge(var)

    @teststeps
    def play_complete_article_game(self, num, exam_json):
        """补全文章 答卷过程"""
        exam_json['补全文章'] = bank_json = {}
        if self.wait_check_complete_article_page():
            self.next_button_operate('false')  # 下一题按钮状态判断
            article = self.article()
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
        article = self.article()
        print(article.text, '\n')
        loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
        self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方

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