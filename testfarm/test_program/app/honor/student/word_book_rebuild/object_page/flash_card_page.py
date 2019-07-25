import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.homework.object_page.homework_page import Homework
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.data_handle import DataActionPage
from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.public_ele import PublicElementPage
from testfarm.test_program.utils.games_keyboard import Keyboard
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststeps, teststep
from testfarm.test_program.utils.get_attribute import GetAttribute


class FlashCard(BasePage):
    """单词本 - 闪卡练习"""
    def __init__(self):
        self.homework = Homework()
        self.home = HomePage()
        self.public = PublicElementPage()

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

    # ================= 学习模式 ======================
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
        ele = self.driver \
            .find_element_by_id(self.id_type() + "author")
        return ele.text

    @teststep
    def english_study(self):
        """全英模式 页面内展示的word"""
        english = self.driver\
            .find_element_by_id(self.id_type() + "tv_english")
        return english.text

    @teststep
    def explain_study(self):
        """英汉模式 页面内展示的word解释"""
        explain = self.driver.find_element_by_id(self.id_type() + "tv_chinese")
        return explain

    @teststep
    def sentence_study(self):
        """全英模式 页面内展示的句子"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "sentence")
        return ele.text


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
    def copy_word(self):
        """闪卡练习- 抄写模式 内展示的Word"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "tv_word").text
        return ele

    @teststep
    def input_word(self):
        """单页面内 答题框填入的Word"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "english").text
        return word[::2]


    @teststep
    def skip_button(self):
        """放弃 按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'md_buttonDefaultNeutral') \
            .click()

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'md_buttonDefaultNegative') \
            .click()

    @teststep
    def check_alert_tip_operate(self, index, group_count):
        """看是否有弹框提示"""
        if index == 0 and group_count == 0:
            if self.public.wait_check_tips_page():
                self.public.tips_operate()
            else:
                print('★★★第一次点击标星未显示提示')
            if self.wait_check_study_page():
                pass


    # ====================== 学习模式 ===========================
    @teststeps
    def flash_study_model(self, all_words, star_words, familiar_words, word_info,
                          index, group_count, new_explain_words, repeat_words, stu_id):
        """:param all_words 记录当前闪卡的所有单词
           :param star_words 标星单词
           :param familiar_words 标熟单词
           :param word_info 记录今日所做的所有新词
           :param index 循环次数
           :param group_count 做的组数
           :param new_explain_words 新释义单词
           :param repeat_words 重复单词
           :param stu_id 学生id
        """
        """学习模式  新词操作"""
        if index == 0:
            print('\n===== 闪卡练习 学习模式 =====\n')
        word = self.english_study()

        if word in all_words:                   # 判断单词是否去重
            print('★★★ 本组已存在本单词，单词未去重！')

        if self.wait_check_explain_page():
            all_words.append(word)               # 加入单词列表
            explain = self.explain_study()       # 解释
            explain_id = explain.get_attribute('contentDescription').split(' ')[0]
            if word not in list(word_info.keys()):
                word_info[word] = []
            else:
                repeat_words.append(word)
                explain_id_list = word_info[word]
                if explain_id in explain_id_list:
                    print('★★★ 该解释已作为新词出现过')
                else:
                    if DataActionPage().get_explain_level(word_info[word], stu_id, 1):
                        new_explain_words.append(explain_id)

            if explain_id in word_info[word]:
                print('★★★  该解释已作为新词出现过！')
            else:
                word_info[word].append(explain_id)

            print('单词：', word, '\n',
                  '解释：', explain.text, '\n',
                  '句子：', self.sentence_study(), '\n',
                  '句子解释：', self.sentence_explain_study(), '\n',
                  '推荐老师：', self.author()
                  )
            self.pattern_switch()               # 切换到 全英模式
            if self.wait_check_explain_page():  # 校验是否成功切换
                print('★★★ 切换全英模式， 依然存在解释')
            self.pattern_switch()               # 切换回 英汉模式
            if index % 2 == 0:                      # 标熟
                if index == 2:
                    self.click_familiar()
                    if self.familiar_button().text != '取消熟词':
                        print('★★★ 点击熟词后内容未发生变化')
                    self.click_familiar()
                    if self.familiar_button().text != '设置熟词':
                        print('★★★ 点击熟词后内容未发生变化')

                self.click_familiar()
                self.check_alert_tip_operate(index, group_count)    # 判断首次标熟是否有提示

                familiar_words[explain.text] = word

            if index in [0, 1]:
                if index == 1:
                    self.click_star()               # 标星
                    if self.star_button().get_attribute('selected') != 'true':
                        print('★★★ 点击标星按钮后，按钮未点亮')
                    self.click_star()
                    if self.star_button().get_attribute('selected') != 'false':
                        print('★★★ 取消标星后，按钮未置灰')
                self.click_star()  # 标星
                self.check_alert_tip_operate(index, group_count)   # 判断首次标星是否有提示
                star_words.append(word)
        else:
            print('★★★ 默认不是英汉模式')

        self.next_word(index, word)
        print('-'*30, '\n')


    @teststeps
    def flash_copy_model(self, star_words):
        """闪卡抄写模式"""
        for x in range(len(star_words)):
            word = self.copy_word()
            word_explain = self.explain_copy()
            input_word = self.input_word()

            if word not in star_words:
                print('★★★ 单词未标星，但是有抄写模式', word)
            print("单词：%s\n解释：%s" % (word, word_explain))

            if len(input_word) != 0:
                print('★★★ Error-- 抄写栏不为空', input_word)
                for i in range(len(input_word)):
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

            time.sleep(5)
            print('-'*30, '\n')


    @teststeps
    def study_mine_word(self, i, star_list, familiar_list, star_add, familiar_add):
        """学习模式  单词详情操作"""
        if i == 0:
            print('\n闪卡练习-单词详情(我的单词)\n')

        if i in(range(0, 5)):
            word = self.study_word_core()

            if word in star_list:                      # 单词是否在标星数组中
                self.judge_word_is_star(i)             # 判断单词星标是否被标注
                self.judge_word_is_familiar(familiar_list, word, i, familiar_add)     # 判断单词是否同时被标熟
            else:
                if i == 1 or i == 3:
                    self.click_star()
                    self.public.tips_operate()
                    star_add.append(word)
                self.judge_word_is_familiar(familiar_list, word, i, familiar_add)     # 判断单词是否被标熟

            self.next_word(i)                                  # 下一单词滑屏还是点击按钮
        else:
            print('用户下所有标星单词：', star_list + star_add)
            print('用户下所有标熟单词：', familiar_list + familiar_add )
            print('-------------------------------------')
            self.home.click_back_up_button()

    @teststeps
    def next_word(self, i, word):
        """进入下一单词的方式"""
        if i == 1:  # 向左滑屏
            self.screen_swipe_left(0.9, 0.5, 0.1, 1000)
            if self.wait_check_study_page():
                if self.english_study() == word:
                    print('★★★ 左右滑屏未成功，仍处于已学单词页面')
        else:
            self.homework.next_button_operate('true')

    @teststep
    def judge_word_is_star(self, i):
        """判断单词是否被标星"""
        if GetAttribute().selected(self.star_button()) == 'true':  # 判断但是标星是否被标注
            print('单词已标星')
            if i == 3:
                self.click_star()  # 取消标星
        else:
            print("★★★ Error--此题未被标星")

    @teststep
    def judge_word_is_familiar(self, familiar, word, i, familiar_add):
        """判断单词是否被标熟"""
        if word in familiar:
            if GetAttribute().selected(self.familiar_button()) == 'true':
                print("★★★ Error-- 此题未被标熟")
                self.click_familiar()
                self.public.tips_operate()
                familiar_add.append(word)
            else:
                print('单词已标熟')
        else:
            if i == 2 or i == 4:
                self.click_familiar()
                self.public.tips_operate()
                familiar_add.append(word)


    @teststeps
    def scan_game_operate(self):
        """闪卡游戏过滤"""
        word_info = {}
        if self.wait_check_study_page():
            game_count = self.public.bank_count()             # 获取闪卡个数
            for x in range(game_count):
                word = self.english_study()                   # 单词
                explain = self.explain_study()                # 解释
                print('单词：', word)
                print('解释：', explain.text)
                explain_id = explain.get_attribute('contentDescription').split(' ')[0]  # 解释id
                word_info[explain_id] = explain.text          # 将解释id与解释存入字典中
                self.next_button().click()   # 点击 下一题 按钮()
                print('-' * 30, '\n')

        self.click_back_up_button()         # 退出弹框处理
        if self.public.wait_check_tips_page():
            self.public.tips_operate()
        return word_info
