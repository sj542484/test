import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.word_book.object_page.data_action import WordBookDataHandle
from testfarm.test_program.app.honor.student.word_book.object_page.mysql_data import WordBookSql
from testfarm.test_program.utils.games_keyboard import Keyboard
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.utils.get_attribute import GetAttribute


class FlashCard(BasePage):
    """单词本 - 闪卡练习"""
    def __init__(self):
        self.homework = Homework()
        self.home = HomePage()
        self.mysql = WordBookSql()
        self.common = WordBookDataHandle()

    @teststeps
    def wait_check_study_page(self):
        """以“闪卡练习 -学习模式”的xpath-text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置熟词')]")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_copy_page(self):
        """以“闪卡练习 -抄写模式”的xpath-text为依据"""
        locator = (By.ID, self.id_type() + "english")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_sentence_page(self):
        """以“闪卡练习 -抄写模式”的xpath-text为依据"""
        locator =(By.ID, self.id_type() + "sentence")
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_explain_page(self):
        """判断解释是否存在"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_chinese")
            return True
        except:
            return False

    # 学习模式
    @teststep
    def pattern_switch(self):
        """点击右上角的全英/英汉，切换模式"""
        self.driver\
            .find_element_by_id(self.id_type() + "side")\
            .click()
        time.sleep(2)

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def author(self):
        """例句推荐老师"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "author").text
        return english

    @teststep
    def english_study(self):
        """全英模式 页面内展示的word"""
        english = self.driver\
            .find_element_by_id(self.id_type() + "tv_english").text
        return english

    @teststep
    def explain_study(self):
        """英汉模式 页面内展示的word解释"""
        explain = self.driver.find_element_by_id(self.id_type() + "tv_chinese")
        return explain.text

    @teststep
    def sentence_study(self):
        """全英模式 页面内展示的句子"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "sentence").text
        return english


    @teststep
    def sentence_explain_study(self):
        """英汉模式 页面内展示的句子解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "sentence_explain").text
        return explain

    @teststep
    def explain_copy(self):
        """抄写模式的单词翻译"""
        explain = self.driver.find_element_by_id(self.id_type() + "chinese")
        return explain.text

    @teststep
    def star_button(self):
        """星标按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "iv_star")
        return ele

    @teststep
    def familiar_button(self):
        """熟词按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "expert")
        return ele


    @teststep
    def click_star(self):
        """闪卡练习页面内五角星按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "iv_star") \
            .click()

    @teststep
    def click_familiar(self):
        """设置为熟词 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "expert").click()

    # 抄写模式
    @teststep
    def word_copy(self):
        """闪卡练习- 抄写模式 内展示的Word"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "tv_word").text
        return ele

    @teststep
    def english_copy(self):
        """单页面内 答题框填入的Word"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "english").text
        return word[::2]

    # 提示 页面
    @teststeps
    def wait_check_tips_page(self):
        """以“icon”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@resource-id,'{}md_title')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def tips_title(self):
        """提示title"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "md_title").text
        print(item)
        return item

    @teststep
    def tips_content(self):
        """提示 具体内容"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "md_content").text
        print(item+"\n")
        time.sleep(2)
        return item

    @teststep
    def commit_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "md_buttonDefaultPositive") \
            .click()
        time.sleep(2)

    @teststep
    def skip_button(self):
        """放弃 按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'md_buttonDefaultNeutral') \
            .click()
        time.sleep(2)

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'md_buttonDefaultNegative') \
            .click()

    @teststeps
    def tips_operate(self):
        """温馨提示 页面信息"""
        if self.wait_check_tips_page():  # 提示 页面
            self.tips_title()
            self.tips_content()
            self.commit_button()  # 确定按钮

    @teststeps
    def study_word_core(self):
        """闪卡练习学习模式 主要步骤"""
        word = self.english_study()  # 单词
        if self.wait_check_explain_page():
            explain = self.explain_study()  # 解释
            print('单词：%s\n解释：%s' %(word, explain))

            if self.wait_check_sentence_page():  # 判断句子是否存在
                sentence = self.sentence_study()  # 句子
                sen_explain = self.sentence_explain_study()  # 句子解释
                auth = self.author()  # 推荐老师
                print('句子：%s\n句子解释：%s\n推荐老师：%s' %(sentence, sen_explain, auth))

            self.pattern_switch()  # 切换到 全英模式
            self.pattern_switch()  # 切换到 英汉模式
            self.click_voice()
        else:
            print('★★★ Error- 默认不为英汉模式')
        return word


    ##学习模式
    @teststeps
    def study_new_word(self, i,star,familiar):
        """学习模式  新词操作"""
        if i == 0:
            print('\n闪卡练习-学习模式(新词)\n')

        word = self.study_word_core()
        if i in range(2, 9, 3):  # 点击star按钮
            self.click_star()
            self.tips_operate()

            if i == 5:
                self.click_star()  # 取消标星
            else:
                star.append(word)

        if i in range(0, 10, 2):  # 点击标熟按钮
            self.click_familiar()
            self.tips_operate()
            if i == 4:
                self.click_familiar()  # 取消标熟
            else:
                familiar.append(word)

        self.next_word(i)

    @teststeps
    def study_mine_word(self, i, star_list, familiar_list,star_add,familiar_add):
        """学习模式  单词详情操作"""
        if i == 0:
            print('\n闪卡练习-单词详情(我的单词)\n')

        if i in(range(0,5)):
            word = self.study_word_core()

            if word in star_list:                                   #单词是否在标星数组中
                self.judge_word_is_star(i)             #判断单词星标是否被标注
                self.judge_word_is_familiar(familiar_list, word, i,familiar_add)     #判断单词是否同时被标熟
            else:
                if i == 1 or i == 3:
                    self.click_star()
                    self.tips_operate()
                    star_add.append(word)
                self.judge_word_is_familiar(familiar_list, word, i,familiar_add)     #判断单词是否被标熟

            self.next_word(i)                                  #下一单词滑屏还是点击按钮
        else:
            print('用户下所有标星单词：', star_list + star_add)
            print('用户下所有标熟单词：', familiar_list + familiar_add )
            print('-------------------------------------')
            self.home.click_back_up_button()

    @teststeps
    def next_word(self, i):
        """进入下一单词的方式"""
        if i == 1:  # 向左滑屏
            self.screen_swipe_left(0.8, 0.5, 0.1, 1000)
            time.sleep(1)
        else:
            self.homework.next_button_operate('true')
            time.sleep(1)

        print('-------------------------------------')

    @teststep
    def judge_word_is_star(self, i):
        """判断单词是否被标星"""
        if GetAttribute().selected(self.star_button()) == 'true':  # 判断但是标星是否被标注
            print('单词已标星')
            if i ==3:
                self.click_star()  # 取消标星
        else:
            print("★★★ Error--此题未被标星")

    @teststep
    def judge_word_is_familiar(self, familiar, word,i,familiar_add):
        """判断单词是否被标熟"""
        if word in familiar:
            if GetAttribute().selected(self.familiar_button()) == 'true':
                print("★★★ Error-- 此题未被标熟")
                self.click_familiar()
                self.tips_operate()
                familiar_add.append(word)
            else:
                print('单词已标熟')
        else:
            if i == 2 or i == 4:
                self.click_familiar()
                self.tips_operate()
                familiar_add.append(word)

    # 抄写模式
    @teststeps
    def copy_new_word(self, i):
        """抄写模式  新词操作"""
        if i == 0:
            print('\n闪卡练习-抄写模式(新词)\n')
        word = self.word_copy()
        self.copy_word_core(word)

    @teststeps
    def copy_mine_word(self, stu_id, i,star_add):
        """抄写模式  我的单词操作"""
        if i == 0:
            print('\n闪卡练习-抄写模式((单词详情)\n')
        word = self.word_copy()
        if i in(range(3)):
            star_words = self.common.get_star_words(stu_id)
            self.copy_word_core(word)
            stars = star_words + star_add
            if word not in stars:
                print('★★★ Error-- 单词未被标星却出现抄写模式')
        else:
            self.home.click_back_up_button()    # 若没有点击放弃，且i>=4，则点击 确定按钮
            if self.wait_check_tips_page():
                self.tips_operate()
                time.sleep(2)

    @teststeps
    def copy_word_core(self, word):
        """闪卡练习 抄写模式 主要步骤"""
        # self.homework.click_voice()  # 听力按钮
        word_explain = self.explain_copy()
        print("单词：%s\n解释：%s" % (word, word_explain))
        copy_word = self.english_copy()
        if len(copy_word) != 0:
            print('★★★ Error-- 抄写栏不为空', copy_word)
            for i in range(len(copy_word)):
                Keyboard().games_keyboard('backspace')

        for j in range(0, len(word)):
            if j == 4:
                Keyboard().games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                Keyboard().games_keyboard(word[j].upper())  # 点击键盘对应 大写字母
            elif j == 5:
                Keyboard().games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                Keyboard().games_keyboard(word[j].lower())  # 点击键盘对应字母
            else:
                Keyboard().games_keyboard(word[j])
        time.sleep(3)
        print('--------------------------')
