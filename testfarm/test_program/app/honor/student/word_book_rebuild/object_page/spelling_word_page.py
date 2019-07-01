import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from app.student.homework.object_page.homework_page import Homework
from app.student.word_book_rebuild.object_page.data_action import DataActionPage
from app.student.word_book_rebuild.object_page.flash_card_page import FlashCard
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class SpellingWord(BasePage):
    """单词拼写"""
    def __init__(self):
        self.get = GetAttribute()
        self.homework = Homework()
        self.common = DataActionPage()
        self.key = Keyboard()

    @teststeps
    def wait_check_spell_page(self):
        """以“词汇选择 -句子选单词模式”的 提示按钮 为依据"""
        locator = (By.ID, "{}hint".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_explain_page(self):
        """以“结束”的 为依据"""
        locator = (By.ID, self.id_type() + 'tv_explain')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_word_random_page(self):
        """以随机拼写的 提示按钮 为依据"""
        locator = (By.ID, self.id_type() + 'tv_word')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def explain(self):
        """展示的翻译"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return explain

    @teststep
    def word(self):
        """展示的Word"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        word = ele[1::2]
        return word

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def mine_answer(self):
        """展示的Word  前后含额外字符:aa"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        return word[::2]

    @teststep
    def finish_word(self):
        """完成答题 之后 展示的Word 每个字母之间有空格"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        return word[::2]

    @teststep
    def correct_judge(self):
        """判断 答案是否展示"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_answer")
            return True
        except:
            return False

    @teststep
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_answer")
        return word.text

    # 默写模式
    @teststep
    def hint_button(self):
        """提示按钮"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "hint")
        return ele

    @teststeps
    def dictation_word_judge(self):
        """判断是否展示Word"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "tv_word")
            return True
        except:
            return False

    @teststeps
    def dictation_word(self):
        """展示的Word"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        value = ele[::2]
        return value

    @teststeps
    def dictation_pattern_new(self, i, spell_word, familiar_word):
        """单词默写 新词"""
        if i == 0:
            print('\n单词拼写 - 默写模式\n')
        self.dictation_pattern_core(spell_word, familiar_word)

    @teststeps
    def dictation_pattern_core(self, spell_word, familiar_word):
        """单词拼写 - 《默写模式》游戏过程"""
        explain = self.explain()  # 题目
        if explain in spell_word:
            print('★★★ 该单词在拼写单词中已经出现过！')
        else:
            spell_word.append(explain)
        value = familiar_word[explain]
        self.hint_ele_operate(value)
        print('解释：', explain)
        self.key.games_keyboard('backspace')
        print('单词:', value)
        for j in range(0, len(value)):
            self.keyboard_operate(j, value[j])  # 点击键盘 具体操作
        self.answer_judge()


    @teststeps
    def dictation_pattern_recite(self, i, first_game, spell_word):
        """单词默写 复习"""
        if i == 0:
            level1_count = self.common.get_different_level_words(1)  # 获取需要B轮复习的单词
            new_word = self.common.get_different_level_words(0)   # 获取新词个数
            if new_word != 0:
                if level1_count != 0:
                    if first_game[0] != '词汇选择(复习)':
                        print('★★★ Error-第一个游戏不是B1的词汇选择游戏')
                    else:
                        print("B轮单词存在,首个游戏为 '词汇选择(复习)' 名称正确！")
                else:
                    if first_game[0] != '词汇运用(复习)':
                        print("★★★ Error-第一个游戏不是B2/C1/D1/E1的词汇运用游戏'")
                    else:
                        print("B轮单词已结束，首个游戏为 '词汇运用(复习)' 名称正确！\n")
                print('----------------------------------')
                print('\n单词拼写 - 默写模式(新词)\n')
        self.dictation_pattern_core(spell_word, word_type=2)

    @teststeps
    def dictation_pattern_mine(self, i, familiar_add, spell_word):
        """单词默写 我的单词"""
        if i == 0:
            print("\n单词拼写 - 默写模式(单词详情)\n")
        explain = self.explain()  # 题目
        value = self.common.get_word_by_explain(explain)
        familiars = self.common.get_familiar_words() + familiar_add
        intersect_list = list(set(value).intersection(set(familiars)))  # 取获取单词数组与标星单词数组的交集
        if i in range(0, 5):
            self.dictation_pattern_core(spell_word, word_type=1)
            if len(intersect_list) == 0:
                print('★★★ Error-- 单词未被标熟却出现默写模式')
        else:
            FlashCard().tips_operate()
            for i in familiar_add:
                level = self.common.get_word_level(i)
                if level < 3:
                    print("★★★ Error--提交未成功，单词熟练度未更改")




    @teststeps
    def hint_ele_operate(self, value):
        self.homework.next_button_operate('false')  # 下一题 按钮 判断加 点击操作
        if self.dictation_word_judge():  # 默写模式 - 字母未全部消除
            print('★★★ Error - 单词拼写 默写模式 - 字母未全部消除')

        hint = self.hint_button()  # 提示按钮

        if self.get.enabled(hint) == 'true':
            hint.click()  # 点击 提示按钮
            if self.get.enabled(self.hint_button()) != 'false':
                print('★★★ Error - 点击后提示按钮enabled属性错误')

            if self.dictation_word_judge():  # 出现首字母提示
                first_word = self.dictation_word()
                if len(first_word) == 1:
                    if first_word == value[0]:
                        print('点击提示出现首字母提示', first_word)
                    else:
                        print('点击提示出现首字母提示', first_word)
                        print("★★★ Error - 首字母提示错误")
                else:
                    print('★★★ Error - 提示字母不为一个')
            else:
                print("★★★ Error - 首字母提示未出现")
        else:
            print('★★★ Error - 提示按钮enabled属性错误')

    @teststeps
    def answer_judge(self):
        answer = self.finish_word()  # 我的答案
        self.homework.next_button_operate('true')  # 下一题 按钮 状态判断 加点击
        self.result_operate(answer, self.mine_answer())  # 下一步按钮后的答案页面 测试
        self.click_voice()
        self.homework.next_button_operate('true')  # 下一题 按钮 状态判断 加点击

    @teststeps
    def result_operate(self, answer, mine):
        """下一步按钮后的答案页面"""
        print('我的答案:', answer)
        print('去除大小写结果:', mine)
        if self.correct_judge():
            correct = self.correct()  # 正确答案
            print('填写错误，正确答案:', correct)
            if len(mine) <= len(correct):  # 输入少于或等于单词字母数的字符
                if mine.lower() != answer.lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('★★★ Error - 字符数少于或等于时:', mine.lower(), answer.lower())
            else:  # 输入过多的字符
                if correct + mine[len(correct):].lower() != correct + answer[len(correct):].lower():
                    # 展示的 我的答题结果 是否与我填入的一致
                    print('★★★ Error - 字符输入过多时:', correct + mine[len(correct):].lower(), correct + answer[len(
                        correct):].lower())
        else:  # 回答正确
            if mine.lower() != answer.lower():  # 展示的 我的答题结果 是否与我填入的一致
                print('★★★ Error - 展示的答题结果 与我填入的不一致:', mine.lower(), answer.lower())
            else:
                print('回答正确!')
        print('----------------------------------')

    @teststeps
    def keyboard_operate(self, j, value):
        """点击键盘 具体操作"""
        if j == 4:
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.key.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.key.games_keyboard(value)  # 点击键盘对应字母

    @teststeps
    def dictation_random_pattern_recite(self, i):
        """错题再练 单词拼写 随机模式"""
        if i == 0:
            print('\n错题再练--单词拼写 随机模式\n')

        self.homework.next_button_operate('false')
        explain = self.explain()
        print('解释：', explain)
        word = self.common.get_word_by_explain(explain)
        print("正确单词：", word)
        tip_word = self.word()
        print('提示词：', tip_word)

        right_word = [x for x in word if len(x) == len(tip_word)]
        alphas = [right_word[0][x] for x in range(len(right_word[0])) if tip_word[x] == '_']
        print(alphas)
        for k in range(len(alphas)):
            self.keyboard_operate(k, alphas[k])  # 点击键盘 具体操作
        print('填充后单词为：', self.word())
        print('----------------------------------')
        self.homework.next_button_operate('true')  # 提交
        self.click_voice()
        self.homework.next_button_operate('true')  # 下一题 按钮 判断加 点击操作
        time.sleep(2)





