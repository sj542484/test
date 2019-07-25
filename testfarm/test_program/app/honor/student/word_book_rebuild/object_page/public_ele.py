#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 14:37
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps


class PublicElementPage(BasePage):

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
    def game_title(self):  # 题型标题
        title = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return title.text

    @teststep
    def bank_count(self):
        """题目个数"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return int(ele.get_attribute('contentDescription'))


    @teststep
    def fab_sound_icon(self):
        """喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() +'fab_sound')
        return ele

    @teststeps
    def tips_operate(self):
        """提示信息处理"""
        if self.wait_check_tips_page():
            print(self.tips_content(), '\n')
            self.commit_button()              #  确定按钮

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
