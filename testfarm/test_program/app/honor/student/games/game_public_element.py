#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:35
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.conf.base_page import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute


class PublicPage(BasePage):
    @teststep
    def wait_check_game_title_page(self):
        """游戏标题页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_title')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

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
    def wait_check_dragger_btn(self):
        """检查页面是否存在拖拽按钮"""
        locator = (By.ID, self.id_type() + "dragger")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_rich_text_page(self):
        """文章类游戏富文本元素页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_keyboard_page(self):
        """键盘页面检查"""
        locator = (By.ID, '{}keyboard_abc_view'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def game_title(self):  # 题型标题
        title = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    @teststep
    def game_mode_id(self):
        """获取题目的mode_id"""
        mode_id = int(self.game_title().get_attribute('contentDescription').split('  ')[1])
        return mode_id


    @teststep
    def hide_keyboard_btn(self):
        """键盘隐藏按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'keyboard_hide')
        return ele

    @teststep
    def rich_text(self):
        """文章类游戏文章文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rich_text')
        return ele

    @teststep
    def question(self):
        """游戏问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'question')
        return ele

    @teststep
    def clear_btn(self):
        """清除按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'bt_clear')
        return ele

    @teststep
    def tips_content(self):
        """提示 具体内容"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "md_content")
        return item.text

    @teststep
    def click_confirm_btn(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "md_buttonDefaultPositive") \
            .click()

    @teststeps
    def tips_operate(self):
        """提示信息处理"""
        if self.wait_check_tips_page():
            print(self.tips_content(), '\n')
            self.click_confirm_btn()  # 确定按钮

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def fab_next_btn(self):
        """下一步按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_next')
        return ele

    @teststep
    def fab_commit_btn(self):
        """下一步提交按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_commit')
        return ele

    @teststep
    def opt_text(self):
        """选项 文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_item')
        return ele

    @teststep
    def opt_char(self):
        """选项 字母 ABCD"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_char')
        return ele

    @teststep
    def sound_icon(self):
        """喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sound')
        return ele

    @teststep
    def drag_btn(self):
        """拖拽按钮"""
        ele = self.driver.find_element_by_id('{}dragger'.format(self.id_type()))
        return ele

    @teststep
    def font_middle(self):
        """第一个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_middle")
        return ele

    @teststep
    def font_large(self):
        """第二个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_large")
        return ele

    @teststep
    def font_great(self):
        """第三个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_great")
        return ele

    @teststeps
    def get_rich_text_input_count(self):
        """获取需要输入的个数"""
        sentence_desc = self.rich_text().get_attribute('contentDescription')
        input_num = len([x for x in sentence_desc.split('##')[1].split('  ') if x != ''])
        return input_num


    @teststeps
    def check_position_change(self):
        if self.wait_check_keyboard_page():
            self.hide_keyboard_btn().click()
        """校验字体变化"""
        if GetAttribute().checked(self.font_large()) == 'false':  # 查看页面是否默认选择第二个Aa
            print('★★★ 页面未默认选择中等字体')

        # 依次点击Aa，并获取第一个填空的X轴位置，比较大小
        large_size = self.rich_text().size
        print("中等字体", large_size)

        self.font_middle().click()
        time.sleep(1)
        middle_size = self.rich_text().size
        print("小字体", middle_size)

        self.font_great().click()
        time.sleep(1)
        great_size = self.rich_text().size
        print("大字体", great_size)

        if large_size['height'] < middle_size['height']:
            print('★★★ 大字体变中等字体未发生变化')
        if great_size['height'] < large_size['height']:
            print('★★★ 超大字变大字体未发生变化')

    @teststeps
    def drag_operate(self, drag_type=0):
        """拖拽操作"""
        loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
        if drag_type:
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, self.get_window_size()[1] - 20)  # 拖拽至最上方
        else:
            self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方

    @teststeps
    def next_btn_judge(self, var, fun):
        """下一步按钮状态判断"""
        value = GetAttribute().enabled(fun())
        if value != var:  # 测试 下一步 按钮 状态
            print('★★★ 按钮 状态Error', value)

    @teststeps
    def next_btn_operate(self, var, fun):
        """下一步按钮操作"""
        self.next_btn_judge(var, fun)
        fun().click()
        time.sleep(1.5)

    @teststep
    def get_last_text_id(self):
        """获取最后一个文本的属性"""
        last_text = self.driver.find_elements_by_class_name('android.widget.TextView')
        last_text_id = last_text[-1].get_attribute('resourceId')
        if 'question' in last_text_id:
            return 'ques'
        elif 'item' in last_text_id:
            return 'opt'

    @teststep
    def get_ques_opt_scale(self):
        """获取包含题目或只有选项的屏幕占比"""
        ques_text = self.question()[0].text
        ques_bank = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(ques_text))
        ques_options = self.driver.find_element_by_xpath('//*[@text="{}"]/following-sibling::android.'
                                                         'widget.LinearLayout'.format(ques_text))
        screen_height = self.get_window_size()[1]
        ques_scale = float('%.2f' % (ques_bank.size['height'] / screen_height))
        opt_scale = float('%.2f' % (ques_options.size['height'] / screen_height))
        return ques_scale, opt_scale
