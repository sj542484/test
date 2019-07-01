# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/26 15:55
# -------------------------------------------
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testfarm.test_program.app.honor.student.library.object_pages.game_page import GamePage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.basepage import BasePage
from testfarm.test_program.conf.decorator import teststep, teststeps
from testfarm.test_program.utils.get_attribute import GetAttribute
from testfarm.test_program.utils.toast_find import Toast


class LibraryPage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.game = GamePage()

    @teststep
    def wait_check_library_page(self, school_name):
        """图书馆页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"{}-图书馆")]'.format(school_name))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_book_list_page(self):
        """书单等待页面"""
        locator = (By.ID, self.id_type() + 'book_num')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_book_punch_page(self):
        """书籍打卡页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"看完书打个卡,才完整嘛")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_share_web_view_page(self):
        """分享web页面检查点"""
        locator = (By.ID, self.id_type() + 'status_content_view')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_student_read_data_page(self):
        """查看页面是否有学生阅读数据"""
        locator = (By.ID, self.id_type() + 'name')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_no_data_page(self):
        """页面没有数据"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"点击屏幕 重新加载")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_course_page(self, course_name):
        """检查页面是否存下指定课本"""
        locator = (By.XPATH, '//*[@text="{}"]'.format(course_name))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_has_books_page(self):
        """书单 图书馆 书籍列表页面检查点"""
        locator = (By.ID, '{}book_img_dilatation'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_book_list_page(self):
        """书单页面检查点"""
        locator = (By.ID, '{}book_summary'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_mine_reading_page(self):
        """我的阅读页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"我的阅读")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_end_tip_page(self):
        """到底了页面提示检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"到底啦 下拉刷新试试")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_no_bank_page(self):
        """暂无排行页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"马上开始，抢占沙发~")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_book_progress_page(self):
        """检查书单页面是否有书籍进度"""
        locator = (By.ID, self.id_type() + 'progress_num')
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_user_name_page(self, nickname):
        """检查图书页面是否存在用户名"""
        locator = (By.XPATH, '//*[@text="{}"]'.format(nickname))
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_no_rank_page(self):
        """没有排行页面检查点"""
        locator = (By.ID, self.id_type() + 'no_rank')
        try:
            WebDriverWait(self.driver, 2, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def no_data_tip(self):
        """没有数据提示"""
        ele = self.driver.find_element_by_id(self.id_type() + 'empty_view_tv')
        return ele.text

    @teststep
    def course_type(self):
        """图书种类"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'hint_text')
        return ele

    @teststep
    def course_more_btn(self, course_type):
        """每种图书下的查看更多按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/following-sibling::android.widget.TextView'.format(course_type))
        return ele

    @teststep
    def book_names(self):
        """图书名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'book_name')
        return ele

    @teststep
    def book_progress(self, book_name):
        """书籍进度"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{}")]/'
                                                '../following-sibling::android.widget.RelativeLayout'.format(book_name))
        child_ele = ele.find_elements_by_xpath('.//*')
        return child_ele[-1].text

    @teststep
    def book_tab(self):
        """图书 书单 tab"""
        ele = self.driver.find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')
        return ele

    @teststep
    def book_title(self):
        """书单标题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'book_title')
        return ele.text

    @teststep
    def book_list_num(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'book_num')
        return ele.text

    @teststep
    def book_list_summary(self):
        """书单描述"""
        ele = self.driver.find_element_by_id(self.id_type() + 'book_summary')
        return ele.text

    @teststep
    def test_book_name(self, book_name):
        """测试书籍元素"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]'.format(book_name))
        return ele

    @teststep
    def mine_book_progress(self, book_name):
        """我的阅读一栏下图书对应的阅读进度"""
        ele = self.driver.find_element_by_xpath('//*[@text="我的阅读"]/../following-sibling::android.widget.FrameLayout'
                                                '/android.widget.LinearLayout/android.widget.LinearLayout/android'
                                                '.widget.RelativeLayout/android.widget.TextView[contains(@text,'
                                                '"{}")]/../following-sibling::android.widget.RelativeLayout'
                                                '/descendant::android.widget.TextView'
                                                .format(book_name))
        return ele.text

    @teststep
    def book_student_name(self):
        """书籍打卡页面学生姓名"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'name')
        return ele

    @teststep
    def book_read_time(self, student_name):
        """书籍阅读时间"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{}")]/following-sibling::'
                                                'android.widget.LinearLayout/android.widget.LinearLayout/'
                                                'android.widget.TextView'.format(student_name))
        return ele.text

    @teststep
    def book_read_progress(self, student_name):
        """书籍阅读进度"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{}")]/following-sibling::'
                                                'android.widget.LinearLayout/android.widget.LinearLayout/'
                                                'android.widget.RelativeLayout/android.widget.TextView'
                                                .format(student_name))
        return ele.text

    @teststep
    def part_btn(self, student_name):
        """片段按钮"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,'
                                                '"{}")]/following-sibling::android.widget.TextView[1]'
                                                .format(student_name))
        return ele

    @teststep
    def like_btn(self, student_name):
        """点赞"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,'
                                                '"{}")]/following-sibling::android.widget.TextView[2] '
                                                .format(student_name))
        return ele

    @teststeps
    def read_data_operate(self, nickname, progress):
        """图书阅读数据操作"""
        user_process = 0
        if self.wait_check_book_punch_page():
            student_list = []
            while True:
                if self.wait_check_student_read_data_page():     # 图书数据页面
                    students = self.book_student_name()          # 获取学生名称
                    for x in students:
                        if x.text in student_list:
                            continue
                        else:
                            student_list.append(x.text)
                            book_time = self.book_read_time(x.text)
                            book_progress = self.book_read_progress(x.text)            # 获取和用户昵称相同的进度
                            if x.text == nickname:
                                user_process = int(book_progress.split('%')[0])
                                if user_process != 100:
                                    if book_progress != progress:
                                        print('★★★ 主页展示进度与书籍页面展示进度不一致')
                                else:
                                    if progress != '完成':
                                        print('★★★ 进度已为100，但是主页进度显示不是【完成】')

                            print(x.text, '时间：', book_time, '进度:', book_progress)    # 输出时间、进度
                            self.part_btn(x.text).click()
                            if not Toast().find_toast('暂无推荐口语片段'):                 # 查看是否有口语提示
                                print('★★★ 未发现暂无口语提示')

                            if GetAttribute().selected(self.like_btn(x.text)) == 'true':   # 若点赞已被点击过
                                print('今天已点赞过该学生')
                                self.like_btn(x.text).click()                        # 再次点击点赞图标
                                if not Toast().find_toast('一天内不可以重复点赞哦！'):       # 检测是否出现不可重复点赞提示
                                    print('★★★ 未提示不可以重复点赞')
                            else:
                                like_nums = int(self.like_btn(x.text).text)         # 获取点赞数
                                self.like_btn(x.text).click()                       # 点赞
                                time.sleep(1)
                                if GetAttribute().selected(self.like_btn(x.text)) == 'false':  # 点击后判断点击后状态
                                    print('★★★ 点赞过后图标颜色未更改！')

                                if int(self.like_btn(x.text).text) != like_nums + 1:    # 判断点赞数是否加1
                                    print('★★★ 点赞后点赞数目未增加')

                                if GetAttribute().selected(self.like_btn(x.text)) == 'true':
                                    self.like_btn(x.text).click()                      # 再次点击点赞图标
                                    if not Toast().find_toast('一天内不可以重复点赞'):     # 检测是否出现不可重复点赞提示
                                        print('★★★ 未提示不可以重复点赞')

                        print('-'*20, '\n')

                    if self.wait_check_end_tip_page():
                        break
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.4, 1000)

            btn_text = self.game.start_game_btn().text           # 根据进度判断按钮内容是否正确
            if self.wait_check_user_name_page(nickname):
                if user_process != 100:
                    if btn_text != '继续':
                        print('★★★ 读书进度不为100, 开始按钮的内容应为继续', btn_text)
                else:
                    if btn_text != '再来一遍':
                        print('★★★ 读书进度为100, 开始按钮的内容应为再来一遍', btn_text)
            else:
                if btn_text != '开始':
                    print('★★★ 当前书籍未阅读， 开始按钮内容应为开始', btn_text)

    @teststeps
    def check_book_operate(self, index):
        """查看书籍操作"""
        book_list = []
        while True:
            books = self.book_names()
            for y in books:  # 遍历点击书籍，查看书籍是否有数据
                if self.wait_check_has_books_page():
                    if y.text in book_list:
                        continue
                    else:
                        book_list.append(y.text)
                        progress = self.book_progress(y.text)
                        print("书名称和进度：", y.text, progress)
                        y.click()

                        if progress == '不可用':
                            if not self.wait_check_no_data_page():
                                print('★★★ 未发现图书下架提示页面')
                            print('该图书已下架！')
                        else:
                            if self.wait_check_book_punch_page():
                                if index == 4 and len(book_list) == 1:        # 当为第五个标签时,做对一小题，接下来立即打卡都可以分享
                                    self.game.punch_share_btn().click()
                                    if not self.wait_check_no_data_page():
                                        print('★★★ 未显示先看书再打卡界面！')
                                    else:
                                        self.home.click_back_up_button()

                                    if self.wait_check_book_punch_page():
                                        self.game.start_game_btn().click()        # 开始/继续/再来一遍
                                        if self.game.wait_check_bank_list_page(): # 大题页面
                                            self.game.testbank_type()[0].click()  # 点击第一道大题
                                            if self.game.wait_check_game_page():  # 进入游戏页面
                                                self.game.play_book_games(fq=1)   # 游戏过程
                                                self.home.click_back_up_button()        # 返回
                                                if self.game.wait_check_bank_list_page():
                                                    self.home.click_back_up_button()
                                                    if self.wait_check_book_punch_page():
                                                        pass
                                    self.PAUNCHED = 1                    # 讲打卡状态更改为1
                                else:
                                    self.game.punch_share_btn().click()
                                    if self.PAUNCHED == 0:
                                        if not self.wait_check_no_data_page():
                                            print('★★★ 未显示先看书再打卡界面！')
                                        self.home.click_back_up_button()
                                        if self.wait_check_book_punch_page():
                                            self.home.click_back_up_button()

                                    if self.PAUNCHED == 1:
                                        if not self.game.wait_check_share_page():
                                            print('★★★ 未显示分享页面')
                                        else:
                                            self.game.share_page_operate()
            if self.wait_check_end_tip_page():
                print('~' * 20, '\n')
                break
            else:
                self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)

    @teststeps
    def check_book_list_operate(self):
        """查看书单操作"""
        book_list = []
        while True:
            books = self.book_names()
            for y in books:  # 遍历点击书籍，查看书籍是否有数据
                if self.wait_check_has_books_page():
                    if y.text in book_list:
                        continue
                    else:
                        book_list.append(y.text)
                        if self.wait_check_book_progress_page():
                            print('★★★ 书单列表中存在图书进度')
                        y.click()
                        if self.wait_check_book_list_page():
                            print("\n书单名称：", self.book_title())
                            print('书籍数量:', self.book_list_num(), '\n',
                                  "书单简介：", self.book_list_summary(), '\n'
                                  )
                            books_num = int(re.findall(r'\d+', self.book_list_num())[0])
                            book_info = []
                            while True:
                                books = self.book_names()
                                for x in books:  # 遍历点击书籍，查看书籍是否有数据
                                    if self.wait_check_has_books_page():
                                        if x.text in book_info:
                                            continue
                                        else:
                                            book_info.append(x.text)
                                            progress = self.book_progress(x.text)
                                            print("\t书名:", x.text, '\t进度:', progress)
                                            x.click()
                                            if progress == '不可用':
                                                if not self.wait_check_no_data_page():
                                                    print('★★★ 未发现图书下架提示页面')
                                                print('\t该图书已下架！')
                                            else:
                                                if self.wait_check_book_punch_page():
                                                    self.game.punch_share_btn().click()
                                                    if self.PAUNCHED == 0:
                                                        if not self.wait_check_no_data_page():
                                                            print('\t★★★ 未显示先看书再打卡界面！')

                                                    if self.PAUNCHED == 1:
                                                        if not self.game.wait_check_share_page():
                                                            print('\t★★★ 未显示分享页面')

                                            self.home.click_back_up_button()
                                            if self.wait_check_book_punch_page():
                                                self.home.click_back_up_button()
                                if self.wait_check_book_list_page():
                                    if len(book_info) != books_num:
                                        self.screen_swipe_up(0.5, 0.9, 0.47, 1000)
                                    else:
                                        break
                        else:
                            print('此书单没有数据')
                            self.home.click_back_up_button()

                        if self.wait_check_book_list_page():
                            self.home.click_back_up_button()

            if self.wait_check_end_tip_page():
                break
            else:
                self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)

    @teststep
    def check_other_set_operate(self):
        """查看其他系列内书籍"""
        set_books_name = []
        book_short_name = []
        time.sleep(3)
        book_num = self.book_list_num()
        while True:
            for x in self.book_names():
                if x.text in book_short_name:
                    continue
                else:
                    book_short_name.append(x.text)
                    x.click()
                    if self.wait_check_book_punch_page():
                        book_name = self.book_title()
                        set_books_name.append(book_name)
                        self.click_back_up_button()
                        time.sleep(1)

            if len(book_short_name) < int(re.findall(r'\d+', book_num)[0]):
                self.home.screen_swipe_up(0.5, 0.8, 0.55, 1000)
            else:
                break
        return set_books_name

    @teststeps
    def from_bank_back_to_home_operate(self, school_name):
        """从书籍大题页面返回主页面"""
        if self.game.wait_check_bank_list_page():
            self.home.click_back_up_button()
            if self.wait_check_book_punch_page():
                self.home.click_back_up_button()
                if self.wait_check_book_list_page():
                    self.home.click_back_up_button()
                    if self.wait_check_course_page('其他教材'):
                        self.home.click_back_up_button()
                        if self.wait_check_library_page(school_name):
                            self.home.click_tab_hw()
                            if self.home.wait_check_home_page():
                                print('返回值主页面~~')


