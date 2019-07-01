# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/2 13:40
# -------------------------------------------
import sys

import pymysql as pymysql
from testfarm.test_program.conf.base_config import GetVariable as gv


class DataAction:
    @classmethod
    def start_db(cls):
        """启动数据库"""
        cls.db = pymysql.connect(gv.HOST, gv.USER_NAME, gv.PASSWORD, gv.DB)
        cls.cursor = cls.db.cursor()
        print('启动数据库')

    def close_db(self):
        print('关闭数据库')
        self.db.close()

    def execute_sql_return_result(self, sql):
        result = 0
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.commit()
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.db.rollback()
        return result

    def execute_sql_only(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.db.rollback()

    def find_student_id(self, phone):  # 根据翻译查询指定单词
        """根据手机号查找自己的student id"""
        sql = "SELECT ua.id FROM user_account AS ua,`user` WHERE ua.user_id = `user`.id and `user`.phone = '{}' " \
              "AND ua.user_type_id =5" .format(phone)
        return self.execute_sql_return_result(sql)

    def find_school_id(self, school_name):
        """查询学校id"""
        sql = 'SELECT id FROM school WHERE `name`= "%s"' % school_name
        return self.execute_sql_return_result(sql)

    def find_latest_school_books(self, school_id):
        """获取学校最新发布的三本书（不是书单）"""
        sql = 'SELECT name FROM library_books WHERE school_id = {} AND type = "book"' \
              'AND school_visible = 1 AND deleted_at is NULL GROUP BY name ORDER BY updated_at DESC'.format(school_id)
        return self.execute_sql_return_result(sql)

    def find_latest_school_book_set(self, school_id):
        """查找学校最新布置的"""
        sql = 'SELECT name FROM library_books WHERE school_id = {} AND type = "book_set"' \
              'AND school_visible = 1 AND deleted_at is NULL GROUP BY name ORDER BY updated_at DESC'.format(school_id)
        return self.execute_sql_return_result(sql)

    def find_system_latest_books(self):
        """查找系统最新书籍"""
        sql = 'SELECT name FROM library_books WHERE school_id = 0 AND type = "book"' \
              'AND school_visible = 1 AND deleted_at is NULL GROUP BY name ORDER BY updated_at DESC'
        return self.execute_sql_return_result(sql)

    def find_system_latest_book_set(self):
        """查找系统最新书单"""
        sql = 'SELECT name FROM library_books WHERE school_id = 0 AND type = "book_set"' \
              'AND school_visible = 1 and deleted_at is NULL GROUP BY name ORDER BY updated_at DESC'
        return self.execute_sql_return_result(sql)

    def find_school_books_id(self, school_id):
        """获取学校图书id"""
        sql = 'SELECT id FROM library_books WHERE school_id = "{}" AND type = "book"'.format(school_id)
        return self.execute_sql_return_result(sql)

    def find_school_book_set_id(self, school_id):
        """获取学校图书id"""
        sql = 'SELECT id FROM library_books WHERE school_id = "{}" AND type = "book_set"'.format(school_id)
        return self.execute_sql_return_result(sql)

    def find_sys_books_id(self, school_id):
        """获取学校图书id"""
        sql = 'SELECT id FROM library_books WHERE school_id = 0 AND type = "book"'.format(school_id)
        return self.execute_sql_return_result(sql)

    def find_sys_book_set_id(self, school_id):
        """获取学校图书id"""
        sql = 'SELECT id FROM library_books WHERE school_id = 0 AND type = "book_set"'.format(school_id)
        return self.execute_sql_return_result(sql)

    def update_book(self, book_id):
        """更改书籍"""
        sql = 'UPDATE library_books SET deleted_at = "2019-04-12 17:26:30" WHERE id = {}'.format(book_id)
        return self.execute_sql_only(sql)

    def find_student_reading_books(self, stu_id):
        """查询学生阅读过的书籍"""
        sql = 'SELECT lb.`name` FROM library_student_books AS sb, library_books as lb WHERE ' \
              'sb.book_id=lb.id AND sb.student_id="%s" GROUP BY sb.book_id ORDER BY sb.last_read_at DESC' % stu_id
        return self.execute_sql_return_result(sql)

    def update_book_delete_null(self, book_id):
        """更改书籍"""
        sql = 'UPDATE library_books SET deleted_at=NULL WHERE id = {}'.format(book_id)
        return self.execute_sql_only(sql)

    def delete_student_read_record(self, stu_id):
        """删除学生阅读记录"""
        sql = "DELETE FROM library_student_book_record WHERE student_id = %s" % stu_id
        return self.execute_sql_only(sql)

    def delete_student_books(self, stu_id):
        """删除学生书籍"""
        sql = 'DELETE FROM library_student_books  WHERE `student_id` = %s' % stu_id
        return self.execute_sql_only(sql)

    def delete_student_library_medal(self, stu_id):
        """删除学生勋章记录"""
        sql = 'DELETE FROM medal_account_record  WHERE `account_id` = %s' % stu_id
        return self.execute_sql_only(sql)

    def find_student_books(self, stu_id):
        """查询学生所有书籍"""
        sql = 'SELECT * FROM `library_student_books` WHERE `student_id` = %s' % stu_id
        return self.execute_sql_return_result(sql)

    def update_one_book_spend_time(self, book_id, timer):
        """更改书籍"""
        sql = 'UPDATE library_student_books SET `spend_time` = %s WHERE `id` = %s' %(timer, book_id)
        return self.execute_sql_only(sql)

    def find_course_label_id(self, course_name):
        """根据标签名称获取标签id"""
        sql = 'SELECT id FROM label WHERE `name` = "{}"'.format(course_name)
        return self.execute_sql_return_result(sql)

    def find_label_book_set_books_id(self, school_id, label_id):
        """查询标签所有校系列下的书籍"""
        sql = "SELECT GROUP_CONCAT(item_ids) from library_books WHERE school_id in (0,{}) and FIND_IN_SET('{}',label_ids)" \
              "and type='book_set' and deleted_at is NULL and school_visible = 1".format(school_id, label_id)
        return self.execute_sql_return_result(sql)

    def find_label_book_set_name(self, school_id, label_id):
        """查询标签下所有系列名称"""
        sql = "SELECT name from library_books WHERE school_id in (0,{}) and FIND_IN_SET('{}',label_ids) " \
              "and type='book_set' and deleted_at is NULL and school_visible = 1".format(school_id, label_id)
        return self.execute_sql_return_result(sql)

    def find_label_book_ids(self, school_id, label_id):
        """查询标签下所有书籍id"""
        sql = "SELECT GROUP_CONCAT(id) from library_books WHERE school_id in (0,{}) and FIND_IN_SET('{}',label_ids) " \
              "and type='book' and deleted_at is NULL and school_visible = 1".format(school_id, label_id)
        return self.execute_sql_return_result(sql)

    def find_book_name_by_id_list(self, book_id):
        """根据书籍id列表获取书籍名称"""
        sql = "SELECT name FROM library_books WHERE id in {} and deleted_at is NULL" .format(book_id)
        return self.execute_sql_return_result(sql)

    def find_books_id_by_set_name(self, set_name, label_id):
        """根据系列名称获取书籍id"""
        sql = "SELECT item_ids from library_books WHERE name like '{}%' and FIND_IN_SET('{}',label_ids) " \
              "and type='book_set' and deleted_at is NULL and school_visible=1".format(set_name, label_id)
        return self.execute_sql_return_result(sql)

