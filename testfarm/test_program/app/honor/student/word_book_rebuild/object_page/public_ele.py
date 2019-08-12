#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 14:37
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.word_book_rebuild.object_page.data_handle import WordDataHandlePage
from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.games_keyboard import Keyboard
from testfarm.test_program.utils.get_attribute import GetAttribute


class PublicElementPage(BasePage):

    @teststep
    def wait_check_game_title_page(self):
        """游戏标题页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_title')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 提示 页面
    @teststep
    def wait_check_tips_page(self):
        """提示页面检查点"""
        locator = (By.ID, '{}md_title'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_play_voice_page(self):
        """喇叭播放按钮"""
        locator = (By.ID, '{}play_voice'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def tips_content(self):
        """提示 具体内容"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "md_content").text
        return item

    @teststep
    def commit_button(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "md_buttonDefaultPositive") \
            .click()

    @teststep
    def fab_next_btn(self):
        """下一步按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_next')
        return ele

    @teststep
    def fab_commit_btn(self):
        """下一步提交按钮"""
        time.sleep(1)
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_commit')
        return ele


    @teststep
    def game_title(self):  # 题型标题
        time.sleep(1)
        title = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    @teststep
    def bank_count(self):
        """题目个数"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return int(ele.get_attribute('contentDescription'))


    @teststep
    def sound_icon(self):
        """喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() +'sound')
        return ele

    @teststep
    def game_title(self):  # 题型标题
        title = self.driver\
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    @teststep
    def game_mode_id(self):
        """获取题目的mode_id"""
        mode_id = int(self.game_title().get_attribute('contentDescription').split('  ')[1])
        return mode_id

    @teststeps
    def tips_operate(self):
        """提示信息处理"""
        if self.wait_check_tips_page():
            print(self.tips_content(), '\n')
            self.commit_button()              #  确定按钮

    @teststep
    def next_btn_judge(self, var, fun):
        """下一步按钮状态判断"""
        value = GetAttribute().enabled(fun())
        if value != var:  # 测试 下一步 按钮 状态
            print('★★★ 下一步按钮 状态Error', value)

    @teststep
    def next_btn_operate(self, var, fun):
        """下一步按钮操作"""
        self.next_btn_judge(var, fun)
        fun().click()
        time.sleep(1.5)

    @teststep
    def game_keyboard_operate(self, word):
        """键盘输入字母操作"""
        for j in range(0, len(word)):
            if j == 4:
                Keyboard().games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                Keyboard().games_keyboard(word[j].upper())  # 点击键盘对应 大写字母
            elif j == 5:
                Keyboard().games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                Keyboard().games_keyboard(word[j].lower())  # 点击键盘对应字母
            else:
                Keyboard().games_keyboard(word[j])


    @teststep
    def check_word_order_is_right(self, study_words, word_info, sys_only=False):
        """查看单词练习顺序是否正确"""
        print('======== 开始单词校验 ===========')
        record_page_ids = list(word_info.keys())
        error_code = []
        print("数据库记录id：", study_words)
        print("页面获取id：", record_page_ids)
        if sys_only or len(study_words) >= 10:
            for x in record_page_ids:
                if int(x) not in study_words:
                    print('★★★ 此单词不在需要练习列表中！', word_info[x])
                    error_code.append(x)
        else:
            for x in study_words:
                if str(x) not in record_page_ids:
                    print('★★★ 此单词为老师布置，但是未在学习列表中！', word_info[x])
                    error_code.append(x)

        if not len(error_code):
            print('单词顺序校验成功\n')

        print('======== 单词顺序校验完毕 ============\n')

    @teststep
    def check_word_is_only_has_vocab_apply(self, explain_id, new_explain_words, stu_id):
        """查看单词是否只有词汇运用"""
        if explain_id in new_explain_words:
            print('此单词是新释义单词')
            word_level = WordDataHandlePage().get_level_by_explain_id(explain_id, stu_id)
            lager_level_count = WordDataHandlePage().check_has_other_studied_explain(explain_id, stu_id, word_level)
            if lager_level_count:
                print('★★★ 存在F值比此单词大的解释，单词复习只有词汇运用，不应在此游戏中出现')