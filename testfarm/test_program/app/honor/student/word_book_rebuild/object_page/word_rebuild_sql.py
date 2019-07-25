#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 16:41
# -----------------------------------------
from testfarm.test_program.app.honor.student.word_book.object_page.mysql_data import WordBookSql


class WordRebuildSql(WordBookSql):

    def find_sys_words_trans_id(self, stu_id):
        """获取系统的解释的id"""
        sql = "SELECT translation_id FROM word_student_fluency WHERE student_id = {} and " \
              "deleted_at is NULL and auth_type_ids=1".format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_teacher_words_trans_id(self, stu_id):
        """获取老师单词的解释的id"""
        sql = "SELECT translation_id FROM word_student_fluency WHERE student_id = {} and " \
              "deleted_at is NULL and auth_type_ids=2 order by created_at".format(stu_id)
        return self.execute_sql_return_result(sql)

    def update_student_word_fluency_data(self, stu_id):
        """更新学生单词数据"""
        sql = 'UPDATE word_student_fluency SET fluency_level=0, last_finish_at = NULL, ' \
              'deleted_at = NULL WHERE student_id = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def update_student_word_data(self, stu_id):
        """更改学生单词数据value为0"""
        sql = 'UPDATE `user_word_data` SET `value` = "0" WHERE `account_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_word_wrong_data(self, stu_id):
        """删除学生单词错题表数据"""
        sql = 'DELETE FROM `wordbook_rebuild`.`word_homework_student_record` WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def find_explain_level_by_id(self, explian_id, stu_id):
        """根据解释id 获取当前解释的F值"""
        sql = 'SELECT fluency_level FROM word_student_fluency WHERE translation_id = {} and student_id = {}'\
              .format(explian_id, stu_id)
        return self.execute_sql_return_result(sql)

    def update_has_studied_word_date(self, update_date, stu_id, fluency_level):
        """更改F值》=1的最后完成时间"""
        sql = 'UPDATE `word_student_fluency` SET `last_finish_at` = "{}" WHERE ' \
              '`student_id` = {} and fluency_level = {}'.format(str(update_date), stu_id, fluency_level)
        return self.execute_sql_only(sql)

    def update_word_record_date(self, date, stu_id):
        """更改单词记录，去重"""
        sql = "UPDATE `word_homework_student_record` SET `created_at` = '%s', `update_at` = '%s' " \
              "WHERE `student_id` = %s" % (str(date), str(date), stu_id)
        self.execute_sql_only(sql)

