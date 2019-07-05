# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/2 15:04
# -------------------------------------------
from testfarm.test_program.app.honor.student.library.object_pages.data_action import DataAction
from testfarm.test_program.app.honor.student.library.object_pages.usercenter_page import UserCenterPage
from testfarm.test_program.app.honor.student.login.object_page.home_page import HomePage
from testfarm.test_program.conf.base_page import BasePage


class DataHandlePage(BasePage):
    def __init__(self):
        self.mysql = DataAction()
        self.user = UserCenterPage()
        self.home = HomePage()

    def get_recommend_books_or_set(self, school_id):
        """获取推荐栏的数据"""
        school_books = self.mysql.find_latest_school_books(school_id)
        school_book_set = self.mysql.find_latest_school_book_set(school_id)
        sys_books = self.mysql.find_system_latest_books()
        sys_book_set = self.mysql.find_system_latest_book_set()

        recommend_book = [x[0] for x in school_books]
        if len(school_books) < 3:
            recommend_book.extend([y[0] for y in sys_books])

        recommend_book_set = [x[0] for x in school_book_set]
        if len(school_book_set) < 3:
            recommend_book_set.extend([y[0] for y in sys_book_set])

        # print('书籍：', recommend_book)
        # print('书单：', recommend_book_set)
        recommend_data = recommend_book[:3] if len(recommend_book) != 0 else recommend_book_set[:3]
        print('推荐书籍数据：', recommend_data)
        return recommend_data

    def get_mine_read_books(self, stu_id):
        """获取我的书籍前三本"""
        mine_book_ids = [x[0] for x in self.mysql.find_student_reading_books(stu_id)]
        return mine_book_ids

    def set_book_delete_value(self, book_ids):
        """设置图书delete不为NUll 即图书不生效"""
        for x in book_ids:
            self.mysql.update_book(x)

    def set_book_delete_null(self, book_ids):
        """设置图书delete 为NULL 即图书生效"""
        for x in book_ids:
            self.mysql.update_book_delete_null(x)

    def delete_student_book_data(self, stu_id):
        """删除学生图书、图书做题记录、勋章获取记录"""
        self.mysql.delete_student_books(stu_id)
        self.mysql.delete_student_read_record(stu_id)
        self.mysql.delete_student_library_medal(stu_id)

    def get_all_book_ids(self, school_id):
        """获取学校/系统 的书单和书籍id"""
        school_books = self.mysql.find_school_books_id(school_id)
        school_book_set = self.mysql.find_school_book_set_id(school_id)
        sys_books = self.mysql.find_sys_books_id(school_id)
        sys_book_set = self.mysql.find_sys_book_set_id(school_id)

        school_book_ids = [x[0] for x in school_books]
        school_set_ids = [x[0] for x in school_book_set]
        sys_book_ids = [x[0] for x in sys_books]
        sys_set_ids = [x[0] for x in sys_book_set]

        print('学校书籍id', school_book_ids)
        print('学校书单id', school_set_ids)

        print('系统书籍id', sys_book_ids)
        print('系统书单id', sys_set_ids, '\n')

        return school_book_ids, school_set_ids, sys_book_ids, sys_set_ids

    def kind_one(self, all_id):
        """系统书单>0， 其他均为0"""
        for i in range(len(all_id) - 1):
            self.set_book_delete_value(all_id[i])
        self.set_book_delete_null(all_id[3])

    def kind_two(self, all_id):
        """学校书籍为0, 学校书单<3, 系统书籍为0， 学校书单不为0"""
        school_book_set = all_id[1][:2]
        self.set_book_delete_null(school_book_set)

    def kind_three(self, all_id):
        """学校书籍为0,学校书单>=3, 系统书籍为0， 学校书单不为0"""
        self.set_book_delete_null(all_id[1])

    def kind_four(self, all_id):
        """学校书籍为0，学校书单可以不为0， 系统书籍不为0， 系统书单不为0"""
        self.set_book_delete_null(all_id[2])

    def kind_five(self, all_id):
        """学校书籍<3 书单不为0，系统书籍不为0， 书单不为0"""
        school_book = all_id[0][:2]
        self.set_book_delete_null(school_book)

    def kind_six(self, all_id):
        """所有数据均不为0"""
        self.set_book_delete_null(all_id[0])

    def get_other_set_books(self, school_id, course_name):
        """获取其他系列内书籍名称"""
        result = self.mysql.find_course_label_id(course_name)
        try:
            label_id = list(result)[0][0]
        except:
            label_id = 0
        print('标签id：', label_id)

        if label_id:
            all_books_id = self.mysql.find_label_book_ids(school_id, label_id)
            try:
                all_books_id = all_books_id[0][0].split(',')
            except:
                all_books_id = []

            all_set_books_id = self.mysql.find_label_book_set_books_id(school_id, label_id)
            try:
                all_set_books_id = all_set_books_id[0][0].split(',')
            except:
                all_set_books_id = []

            book_set_names = self.mysql.find_label_book_set_name(school_id, label_id)

            other_set_book_id_list = list(set(all_books_id).difference(set(all_set_books_id)))
            try:
                other_set_book_names = [x[0] for x in self.
                                        mysql.find_book_name_by_id_list('{}'.format(tuple(other_set_book_id_list)))]
            except:
                other_set_book_names = []

            all_set_names = [x[0] for x in book_set_names]
            return all_set_names, other_set_book_names, label_id

    def get_set_books(self,course_name, label_id):
        """获取系列下书籍名称"""
        book_item_ids = self.mysql.find_books_id_by_set_name(course_name, label_id)
        reform_book_ids = '{}'.format(tuple(book_item_ids[0][0].split(',')))
        book_names = self.mysql.find_book_name_by_id_list(reform_book_ids)
        print('{}系列数据库下书籍名称：'.format(course_name), [x[0] for x in book_names])
        print('-'*30, '\n')
        return [x[0] for x in book_names]















