#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/31 9:32
# -----------------------------------------
import random
import unittest

from testfarm.test_program.app.honor.student.library.object_pages.library_page import LibraryPage
from testfarm.test_program.app.honor.student.library.object_pages.sql_data_page import DataHandlePage
from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.app.honor.student.login.object_page.login_page import LoginPage
from testfarm.test_program.conf.decorator import setup, teardown, testcase


class Medal(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.data = DataHandlePage()
        cls.library = LibraryPage()
        cls.login.app_status()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_compare_page_data(self):
        """对比页面数据，查看是否与数据库一致"""
        if self.home.wait_check_home_page():
            user_info = UserCenterPage().get_user_info()                        # 获取个人信息 id/名称
            school_id = user_info[2]
            school_name = user_info[1]
            if self.home.wait_check_home_page():
                self.home.check_more()[0].click()                              # 第一个查看更多
                for i in range(2):                                             # 共查询两个标签
                    if self.library.wait_check_library_page(school_name):
                        course_type = self.library.course_type()
                        course_name = random.choice([x.text for x in course_type])     # 随机获取当前页面的课程标签
                        print('选择标签：', course_name)
                        page_set_names = []
                        result = self.data.get_other_set_books(school_id, course_name)  # 获取所有书籍，其他系列书籍
                        all_set_name = result[0]
                        other_set_name = result[1]
                        course_label_id = result[2]
                        self.library.course_more_btn(course_name).click()
                        if self.library.wait_check_course_page(course_name):          # 点击系列，验证书籍数据
                            if self.library.wait_check_no_data_page():
                                print(self.library.no_data_tip())
                                self.library.click_back_up_button()
                            else:
                                while True:                                          # 遍历书籍，获取名称，与数据库数据比较
                                    book_set_names = self.library.book_names()
                                    for x in book_set_names:
                                        if x.text in page_set_names:
                                            continue
                                        else:
                                            set_name = x.text
                                            page_set_names.append(set_name)
                                            x.click()
                                            set_books = self.library.check_other_set_operate()
                                            print("{}系列页面下书籍列表：".format(set_name), set_books)
                                            if set_name != '其他':
                                                db_book_name = self.data.get_set_books(set_name, course_label_id)
                                                if len(list(set(db_book_name).difference(set(set_books)))) != 0:
                                                    print('★★★ {}系列内书籍与数据库不一致！'.format(set_name))
                                                else:
                                                    print('{}书籍数据验证通过~~'.format(set_name))
                                            else:
                                                print('其他系列书籍名称：', other_set_name)
                                                if len(list(set(other_set_name).difference(set(set_books)))) != 0:
                                                    print('★★★ 其他系列内书籍与数据库不一致！')
                                                else:
                                                    print('其他书籍数据验证通过~~')

                                            self.library.click_back_up_button()
                                            if self.library.wait_check_course_page(course_name):
                                                pass
                                    if self.library.wait_check_end_tip_page():
                                        self.library.click_back_up_button()
                                        break
                                    else:
                                        self.home.screen_swipe_up(0.5, 0.9, 0.35, 1000)

                        print("\n页面书籍系列名称：", page_set_names)
                        print('所有系列名称：', all_set_name)
                        if len(list(set(all_set_name).difference(set(page_set_names[:-1])))) != 0:
                            print('★★★ 页面系列标签与数据库不一致')
                        else:
                            print('系列书籍核实正确')

                        if self.library.wait_check_library_page(school_name):
                            self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)







