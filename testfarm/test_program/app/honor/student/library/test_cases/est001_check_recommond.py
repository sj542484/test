# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/2 16:05
# -------------------------------------------
import time
import unittest
from app.honor.student.library.object_pages.library_page import LibraryPage
from app.honor.student.library.object_pages.library_data_handle import DataHandlePage
from app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.decorator import setup, teardown, testcase, teststep


class Recommend(unittest.TestCase):
    """准确率"""

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
    def test_recommend(self):
        """测试推荐一栏数据"""
        if self.home.wait_check_home_page():
            user_data = UserCenterPage().get_user_info()
            school_id = user_data[2]
            stu_id = user_data[0]
            if self.home.wait_check_home_page():
                print('进入主界面')
                self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
                mine_books = self.data.get_mine_read_books(stu_id)
                if len(mine_books) == 0:
                    if self.home.wait_check_mine_more_btn_page():
                        print('★★★ 我的书籍为0，但页面显示出查看更多按钮')
                else:
                    page_mine_books = self.home.tab_books('我的阅读')
                    print('我的阅读数据：', mine_books)
                    print('页面我的阅读，', page_mine_books)
                    if mine_books[:3] != page_mine_books:
                        print('★★★ 我的阅读数据与数据库数据不符，校验失败')
                    else:
                        print('数据校验成功')
                print('-'*20, '\n')

                all_kind_ids = self.data.get_all_book_ids(school_id)
                print('第一种情况：除系统书单外，其他数据均为0， 此时页面需展示系统书单')
                self.data.kind_one(all_kind_ids)

                if school_id != 0:
                    self.check_recommend_data(school_id)
                    print('第二种情况，学校书籍为0，书单<3, 系统书籍为0， 书单>0')
                    self.data.kind_two(all_kind_ids)
                    self.check_recommend_data(school_id)

                    if len(all_kind_ids[1]) >= 3:
                        print('第三种情况， 学校书籍为0， 书单>=3, 系统书籍为0， 书单不为0')
                        self.data.kind_three(all_kind_ids)
                        self.check_recommend_data(school_id)

                    print('第四种情况, 学校书籍为0， 书单不为0， 系统书籍不为0， 书单不为0')
                    self.data.kind_four(all_kind_ids)
                    self.check_recommend_data(school_id)

                    print('第五种情况, 学校书籍<3， 书单不为0， 系统书籍不为0， 书单不为0')
                    self.data.kind_five(all_kind_ids)
                    self.check_recommend_data(school_id)

                    if len(all_kind_ids[0]) >= 3:
                        print('第六种情况， 学校书籍>=3, 其他均不为0')
                        self.data.kind_six(all_kind_ids)
                        self.check_recommend_data(school_id)
                else:
                    print('该学生暂时没有学校')


    @teststep
    def check_recommend_data(self, school_id):
        """校验推荐数据具体操作步骤"""
        self.home.click_tab_profile()
        if UserCenterPage().wait_check_user_center_page():
            time.sleep(2)
            self.home.click_tab_hw()
            if self.home.wait_check_home_page():
                page_recommend_books = self.home.tab_books('推荐')
                db_recommend_books = self.data.get_recommend_books_or_set(school_id)
                if len(db_recommend_books) == 0:
                    if self.home.wait_check_recommend_more_btn_page():
                        print('★★★ 推荐数据为0, 却出现发现更多按钮')
                print('页面展示数据', page_recommend_books)

                page_recommend_books.sort()
                db_recommend_books.sort()
                if page_recommend_books != db_recommend_books:
                    print('★★★ 页面与实际数据不符，校验失败')
                else:
                    print('数据校验成功')
            print('-'*20, '\n')


