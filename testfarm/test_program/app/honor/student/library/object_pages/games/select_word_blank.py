# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/9 15:01
# -------------------------------------------
import random
import re
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.games.common_page import CommonPage
from testfarm.test_program.app.honor.student.library.object_pages.result_page import ResultPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.click_bounds import ClickBounds
from testfarm.test_program.utils.games_keyboard import Keyboard
from testfarm.test_program.utils.get_attribute import GetAttribute


class SelectWordBlank(BasePage):
    """选词填空"""

    def __init__(self):
        self.common = CommonPage()

    @teststep
    def wait_check_select_blank_page(self):
        """选词填空页面检查点"""
        locator = (By.ID, '{}tb_content'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    def wait_check_hint_btn_page(self):
        """检测是否存在提示按钮"""
        locator = (By.ID, '{}prompt'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_hint_content_page(self):
        """提示词页面检查点"""
        locator = (By.ID, '{}md_titleFrame'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def hint_answer(self):
        """提示答案"""
        ele = self.driver.find_element_by_xpath('//*[@resource-id="{}md_customViewFrame"]/'
                                                'android.widget.ScrollView/android.widget.TextView'
                                                .format(self.id_type()))

        return ele.text


    @teststep
    def hint_btn(self):
        """提示词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'prompt')
        return ele

    @teststep
    def content(self):
        """文章内容"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tb_content')
        return ele

    @teststep
    def get_first_blank_position(self, content):
        """获取第一个填空的位置"""
        desc = content.get_attribute('contentDescription')
        position_info = re.findall(r'\[(.*?)\]', desc)  # 从属性中获取每个填空的位置
        x_position = position_info[1].split(',')        # 获取第一个填空的x值
        y_position = position_info[2].split(',')        # 获取第一个填空的y值
        return int(float(x_position[0])), int(float(y_position[0]))

    @teststeps
    def select_word_blank_operate(self, fq, sec_answer, half_exit):
        timer = []
        mine_answer = {}
        if self.wait_check_select_blank_page():
            total_num = self.common.rest_bank_num()
            if self.wait_check_hint_btn_page():
                self.hint_btn().click()              # 点击提示词，检验提示页面是否出现
                if not self.wait_check_hint_content_page():
                    print('★★★ 点击提示词按钮未出现提示词')
                else:
                    print('提示词：', self.hint_answer())
                HomePage().click_blank()
            if self.wait_check_select_blank_page():
                content = self.content()
                self.check_position_change(content)
                first_blank_position = self.get_first_blank_position(content)
                print(first_blank_position)
                ClickBounds().click_bounds(float(first_blank_position[0]) + 115,
                                           float(first_blank_position[1]) + 499)  # 点击第一个填空

                for i in range(0, total_num):
                    if self.wait_check_select_blank_page():
                        self.common.judge_next_is_true_false('false')              # 判断下一步状态
                        self.common.rate_judge(total_num, i)

                        if fq == 1:
                            random_str = ''.join(random.sample(string.ascii_letters, 2))
                            for x in random_str:
                                Keyboard().games_keyboard(x)
                            mine_answer[i] = random_str

                        else:
                            right_answer = sec_answer[i]
                            for x in right_answer:
                                Keyboard().games_keyboard(x)

                    timer.append(self.common.bank_time())
                    if i != total_num - 1:
                        Keyboard().games_keyboard('enter')
                    timer.append(self.common.bank_time())

                    if i == 2:
                        if half_exit:
                            self.click_back_up_button()
                            break
                print('我的答案：', mine_answer)
            self.common.judge_next_is_true_false('true')
            self.common.judge_timer(timer)
            self.common.next_btn().click()
            answer = mine_answer if fq == 1 else sec_answer
            return answer, total_num

    @teststep
    def check_position_change(self, content):
        """校验字体变化"""
        if GetAttribute().checked(self.common.font_large()) == 'false':      # 查看页面是否默认选择第二个Aa
            print('★★★ 页面未默认选择中等字体')

        # 依次点击Aa，并获取第一个填空的X轴位置，比较大小
        large_pt = self.get_first_blank_position(content)
        large_pt_y = large_pt[1]

        self.common.font_middle().click()
        time.sleep(1)
        middle_pt = self.get_first_blank_position(content)
        middle_pt_y = middle_pt[1]

        self.common.font_great().click()
        time.sleep(1)
        great_pt = self.get_first_blank_position(content)
        great_pt_y = great_pt[1]

        if not large_pt_y > middle_pt_y:
            print('★★★ 大字体变中等字体未发生变化')

        if not great_pt_y > large_pt_y:
            print('★★★ 超大字变大字体未发生变化')

        self.common.font_large().click()
        time.sleep(2)

    @teststep
    def select_word_blank_result_operate(self, mine_answer):
        """选词填空结果页操作"""
        right_answer = {}
        right, wrong = [], []
        index = 0
        if ResultPage().wait_check_answer_page():
            self.hint_btn().click()                   # 点击提示词，校验是否出现提示答案页面
            if not self.wait_check_hint_content_page():
                print('★★★ 点击提示词按钮未出现提示词')
            else:
                print('提示词：', self.hint_answer())
            HomePage().click_blank()
            cont_desc = self.content().get_attribute('contentDescription')             # 从desc中获取正确答案
            answers = re.findall(r'\[(.*?)\]', cont_desc)[0].split(', ')
            for i in range(len(answers)):                  # 将正确答案与输入的答案依次对比，并根据对错存入数组中
                if answers[i] != mine_answer[i]:
                    wrong.append(answers[i])
                    right_answer[index] = answers[i]
                    index += 1
                else:
                    right.append(answers[i])
        self.click_back_up_button()
        return wrong, right, right_answer


